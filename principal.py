import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. Configuração da IA (Coloque sua chave nas Actions/Secrets do Streamlit)
CHAVE_API = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('gemini-pro')

st.title("🗺️ Planejador de Viagens Inteligente")
st.write("Crie seu roteiro personalizado em segundos!")

# 2. Formulário de Entrada
with st.form("form_viagem"):
    destino = st.text_input("Para onde você vai?", placeholder="Ex: Paris, Gramado, Tóquio...")
    dias = st.slider("Quantos dias vai ficar?", min_value=1, max_value=15, value=4)
    estilo = st.selectbox("Qual o estilo da viagem?", ["Econômico", "Cultural", "Aventura/Natureza", "Luxo", "Família com crianças"])
    botao_gerar = st.form_submit_button("Gerar Roteiro")

# 3. Lógica de Geração
if botao_gerar and destino:
    with st.spinner("Desenhando seu roteiro perfeito... 🏃‍♂️💨"):
        # Criando o comando para a IA
        prompt = f"Crie um roteiro de viagem detalhado dia após dia para {destino}, com duração de {dias} dias. O estilo da viagem é {estilo}. Seja específico com nomes de lugares, dicas de restaurantes e horários recomendados."
        
        resposta = model.generate_content(prompt)
        roteiro_texto = resposta.text
        
        # Mostra na tela do site
        st.success("Roteiro gerado com sucesso!")
        st.markdown(roteiro_texto)
        
        # 4. Função para criar o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, roteiro_texto.encode('latin-1', 'replace').decode('latin-1'))
        pdf_data = pdf.output(dest='S')
        
        # Botão de Download
        st.download_button(
            label="📥 Baixar Roteiro em PDF",
            data=pdf_data,
            file_name=f"roteiro_{destino}.pdf",
            mime="application/pdf"
        )
