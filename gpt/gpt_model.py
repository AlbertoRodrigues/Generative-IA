import math
import torch
import torch.nn as nn
from vocab import tokens

class GPT(nn.Module):
    """
    GPT minimalista – 5 camadas, 4 cabeças, cada camada tem
    suas próprias projeções Q, K, V, Wo e seu próprio MLP.

    • forward(idx)         → logits (T, vocab_size)
    • predict_next_token() → string do próximo token
    • predict_all_sentence() → imprime passo-a-passo até max_tokens
    • init_tokens(prompt)  → guarda prompt inicial + vocabulário
    """

    def __init__(self, context_length, n_layers, n_heads, n_embd, max_tokens):
        super().__init__()

        # Hiper-parâmetros
        self.vocab_size   = len(tokens)
        self.context_length = context_length 
        self.n_layers       = n_layers
        self.n_heads        = n_heads
        self.n_embd         = n_embd
        self.max_tokens     = max_tokens
        self.head_dim       = self.n_embd // self.n_heads
        assert self.n_embd % self.n_heads == 0, "n_embd deve ser divisível por n_heads"

        # --- Embeddings -----------------------------------------------------
        self.wte = nn.Embedding(self.vocab_size, self.n_embd)
        self.wpe = nn.Embedding(self.context_length, self.n_embd)

        # --- Projeções Atenção & MLP independentes por camada ---------------
        self.qkv_proj = nn.ModuleList([
            nn.Linear(self.n_embd, 3 * self.n_embd) for _ in range(self.n_layers)
        ])
        self.out_proj = nn.ModuleList([
            nn.Linear(self.n_embd, self.n_embd) for _ in range(self.n_layers)
        ])
        self.mlp = nn.ModuleList([
            nn.Sequential(
                nn.Linear(self.n_embd, 2 * self.n_embd),
                nn.GELU(approximate='tanh'),
                nn.Linear(2 * self.n_embd, self.n_embd)
            ) for _ in range(self.n_layers)
        ])
        #self.ln1 = nn.ModuleList([nn.LayerNorm(self.n_embd) for _ in range(self.n_layers)])
        self.ln = nn.LayerNorm(self.n_embd)
        self.ln.weight.requires_grad = False   # desliga gradiente de γ
        self.ln.bias.requires_grad   = False   # desliga gradiente de β

        # --- Máscara causal (bool) ------------------------------------------
        self.register_buffer(
            "mask",
            torch.tril(torch.ones(self.context_length, self.context_length, dtype=torch.bool))
        )

        # --- Saída final -----------------------------------------------------
        #self.final_ln = nn.LayerNorm(self.n_embd)
        self.lm_head  = nn.Linear(self.n_embd, self.vocab_size)

        # --- Place-holders de prompt / vocabulário --------------------------

        self.token_to_idx = {tok: idx for idx, tok in enumerate(tokens)}
        self.idx_to_token = {idx: tok for tok, idx in self.token_to_idx.items()}

        # congelar parâmetros de todas as LayerNorm
        #for ln in list(self.ln1) + list(self.ln2) + [self.final_ln]:
        #    ln.weight.requires_grad = False   # desliga gradiente de γ
        #    ln.bias.requires_grad   = False   # desliga gradiente de β

    # --------------------------------------------------------------------- #
    #  Utilitários de vocabulário / prompt
    # --------------------------------------------------------------------- #
    def init_tokens(self, tokens_list):
        """Define prompt inicial e dicionários token↔id."""
        self.tokens_list  = list(tokens_list)


    def _update_indices_tensor(self, seq):
        """Converte `seq` (lista de tokens) para tensor de índices,
           limitando ao último `context_length`."""
        idxs = [self.token_to_idx[tok] for tok in seq]
        return torch.tensor(idxs, dtype=torch.long, device=self.wte.weight.device)

    # --------------------------------------------------------------------- #
    #  Bloco de atenção (usa pesos da camada `l`)
    # --------------------------------------------------------------------- #
    def _self_attention(self, x, l):
        # x: (T, C)
        T, C = x.size()
        qkv = self.qkv_proj[l](x)                 # (T, 3C)
        q, k, v = qkv.chunk(3, dim=1)

        q = q.view(T, self.n_heads, self.head_dim).transpose(0, 1)  # (nh,T,hd)
        k = k.view(T, self.n_heads, self.head_dim).transpose(0, 1)
        v = v.view(T, self.n_heads, self.head_dim).transpose(0, 1)

        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att.masked_fill(~self.mask[:T, :T], float('-inf'))
        att = torch.softmax(att, dim=-1)
        y   = att @ v                                           # (nh,T,hd)
        y   = y.transpose(0, 1).contiguous().view(T, C)         # (T,C)
        return self.out_proj[l](y)                              # (T,C)

    # --------------------------------------------------------------------- #
    #  Forward: devolve logits para todos os tokens
    # --------------------------------------------------------------------- #
    def forward(self, idx):
        """
        idx : LongTensor (T,) – sequência de índices de tokens.
        Retorna logits (T, vocab_size).
        """
        T = idx.size(0)
        pos = torch.arange(T, device=idx.device)
        #print(idx)
        #print(pos)
        x   = self.wte(idx) + self.wpe(pos)

        for l in range(self.n_layers):
            x = x + self._self_attention(self.ln(x), l)
            x = x + self.mlp[l](self.ln(x))

        x = self.ln(x)                      # (T, C)
        return self.lm_head(x)[-1]                  # (T, vocab_size)

    # --------------------------------------------------------------------- #
    #  Geração
    # --------------------------------------------------------------------- #
    def predict_next_token(self):
        """
        seq : lista de tokens (prompt + já gerados)
        Retorna o próximo token (string).
        """
        idx = self._update_indices_tensor(self.tokens_list)
        logits = self.forward(idx)
        probs  = torch.softmax(logits, dim=-1)       # último passo
        next_id = torch.multinomial(probs, 1).item()
        return self.idx_to_token[next_id]

    def predict_all_sentence(self):
        """
        Gera até `max_tokens` novos tokens SEM alterar o prompt original.
        Imprime a frase a cada passo e devolve a lista completa.
        """
        prompt = list(self.tokens_list)          # cópia imutável
        generated = []

        for step in range(self.max_tokens):
            self.tokens_list = prompt + generated
            next_tok = self.predict_next_token()
            generated.append(next_tok)
            print(f"Passo {step+1}: {' '.join(self.tokens_list)}")
        self.tokens_list = prompt

        return prompt + generated

