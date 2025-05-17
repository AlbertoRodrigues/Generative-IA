import math
import torch
import torch.nn as nn
from vocab import tokens

import math
import torch
import torch.nn as nn
from vocab import tokens

class GPT(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.max_tokens     = 12
        self.context_length = 16
        self.vocab_size     = 209
        self.n_layers       = 5     # agora duas camadas
        self.n_heads        = 4      # agora quatro cabeças
        self.n_embd         = 256

        # Embeddings
        self.wte = nn.Embedding(self.vocab_size, self.n_embd)
        self.wpe = nn.Embedding(self.context_length, self.n_embd)

        # MLP
        self.fc1 = nn.Linear(self.n_embd, 2 * self.n_embd)
        self.gelu = nn.GELU(approximate='tanh')
        self.fc2 = nn.Linear(2 * self.n_embd, self.n_embd)

        # Normalização
        self.ln = nn.LayerNorm(self.n_embd)
        self.ln.weight.requires_grad = False
        self.ln.bias.requires_grad = False

        # Atenção
        self.qkv_proj = nn.Linear(self.n_embd, 3 * self.n_embd)
        self.out_proj = nn.Linear(self.n_embd, self.n_embd)
        self.head_dim = self.n_embd // self.n_heads

        # Máscara causal
        self.mask = torch.tril(torch.ones(self.context_length,
                                          self.context_length)
                               ).view(self.context_length,
                                      self.context_length)

        # Final head
        self.final_ln = nn.LayerNorm(self.n_embd)
        self.lm_head   = nn.Linear(self.n_embd, self.vocab_size)

        assert self.n_embd % self.n_heads == 0, "n_embd deve ser divisível por n_heads"

    def init_tokens(self, tokens_list):
        self.tokens_list = tokens_list
        self.tokens_vocab = {token: idx for idx, token in enumerate(tokens)}
        self.idx_to_token = {idx: token for token, idx in self.tokens_vocab.items()}

    def mlp(self, x):
        x = self.fc1(x)
        x = self.gelu(x)
        x = self.fc2(x)
        return x

    def layer_norm(self, x):
        return self.ln(x)

    def self_attention(self, x):
        # x: (T, C)
        T, C = x.size()
        qkv = self.qkv_proj(x)               # (T, 3*C)
        q, k, v = qkv.chunk(3, dim=1)        # cada um (T, C)

        # projeção multi-head
        q = q.view(T, self.n_heads, self.head_dim).transpose(0,1)  # (nh, T, hd)
        k = k.view(T, self.n_heads, self.head_dim).transpose(0,1)
        v = v.view(T, self.n_heads, self.head_dim).transpose(0,1)

        # produto escalar e escala
        att = (q @ k.transpose(-2,-1)) / math.sqrt(self.head_dim)   # (nh, T, T)

        # máscara causal
        att = att.masked_fill(self.mask[:T, :T] == 0, float('-inf'))

        # softmax
        att = torch.softmax(att, dim=-1)

        # aplicação sobre v
        y = att @ v  # (nh, T, hd)

        # concatena heads
        y = y.transpose(0,1).contiguous().view(T, C)  # (T, C)

        # projeção final
        return self.out_proj(y)

    def tokens_idx(self, tokens_chosen):
        # Pegar os índices correspondentes
        indices = [self.tokens_vocab[token] for token in tokens_chosen]

        # Converter para tensor, se quiser passar ao modelo
        self.indices_tensor = torch.tensor(indices, dtype=torch.long)

    def forward(self):
        # 1) lookup embeddings
        idx = self.indices_tensor         # (T,)
        T   = idx.size(0)
        tok_emb = self.wte(idx)           # (T, n_embd)
        pos_emb = self.wpe(torch.arange(T, device=idx.device))  # (T, n_embd)
        x = tok_emb + pos_emb             # (T, n_embd)

        # 2) aplica N camadas de (LN → Atenção → Residual → LN → MLP → Residual)
        for _ in range(self.n_layers):
            # pré-atenção
            x_norm = self.layer_norm(x)
            attn_out = self.self_attention(x_norm)
            x = x + attn_out

            # pré-MLP
            x_norm = self.layer_norm(x)
            mlp_out = self.mlp(x_norm)
            x = x + mlp_out

        return x[-1]  # vetor do último token (n_embd,)

    def predict_logits(self, x):
        x = self.final_ln(x)  # (n_embd,)
        return self.lm_head(x)  # (vocab_size,)

    def predict_next_token(self):
        self.tokens_idx(self.tokens_list)
        vec = self.forward()               # (n_embd,)
        logits = self.predict_logits(vec)  # (vocab_size,)
        probs = torch.softmax(logits, dim=-1)
        idx  = torch.multinomial(probs, num_samples=1).item()
        return self.idx_to_token[idx]

    def predict_all_sentence(self):
        # guarda cópia do estado original
        original = list(self.tokens_list)

        for step in range(self.max_tokens):
            nt = self.predict_next_token()
            self.tokens_list.append(nt)
            print(f"Passo {step+1}: {' '.join(self.tokens_list)}")

        # recupera o estado original
        self.tokens_list = original
        return list(original)