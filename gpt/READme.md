# 🧠 MiniGPT - Um Modelo Transformer Causal em PyTorch

Este repositório implementa, passo a passo, a arquitetura de um modelo de linguagem (LLM) baseado no **GPT (Generative Pretrained Transformer)**, utilizando **PyTorch puro** e com foco em **clareza educacional**.

Nosso objetivo é construir, a partir do zero, todos os componentes fundamentais de um LLM autoregressivo:

- Embeddings de tokens e posições
- Mecanismo de atenção causal (self-attention com máscara)
- Empilhamento de blocos Transformer
- MLP (Feedforward)
- Normalizações e conexões residuais
- Cabeça de linguagem para predição de próximos tokens
- Inferência e (futuramente) treinamento supervisionado

---

## 🔧 Arquitetura Base

A arquitetura segue o padrão do GPT original com as seguintes etapas:

```text
Tokens de entrada (B, T)
   │
   ├─► Embedding de tokens ──┐
   ├─► Embedding de posições ┘ → soma → x ∈ ℝ^{B × T × d}
   │
   ├─► [ Transformer Block ] × N
   │     ├─ LayerNorm
   │     ├─ Self-Attention (multi-head, causal)
   │     ├─ Residual
   │     ├─ LayerNorm
   │     ├─ MLP (GELU)
   │     └─ Residual
   │
   ├─► LayerNorm final
   └─► Projeção Linear para vocabulário (ℝ^{B × T × vocab_size})
