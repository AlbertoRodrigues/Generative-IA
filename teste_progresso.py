import streamlit as st
import time
import threading

# Cria placeholders para a barra de progresso, para o texto e para a resposta
progress_bar = st.progress(0)
progress_text = st.empty()  # Placeholder para o texto da porcentagem
result_placeholder = st.empty()

# Variáveis de controle
answer_generated = False
answer = None

def generate_answer():
    # Simula um processamento longo (por exemplo, 20 segundos)
    time.sleep(20)
    return "Resposta gerada!"

def run_generation():
    global answer, answer_generated
    answer = generate_answer()
    answer_generated = True

# Inicia a thread que gera a resposta
threading.Thread(target=run_generation, daemon=True).start()

# Atualiza a barra de progresso a cada 5 segundos até 90%
current_progress = 0
while not answer_generated and current_progress < 90:
    time.sleep(5)
    current_progress += 10
    progress_bar.progress(current_progress)
    progress_text.text(f"Progresso: {current_progress}%")

# Se a resposta ainda não foi gerada, espera até que seja, então atualiza a barra para 100%
while not answer_generated:
    time.sleep(0.5)  # aguarda um pouco antes de checar novamente

progress_bar.progress(100)
progress_text.text("Progresso: 100%")
result_placeholder.write(answer)
