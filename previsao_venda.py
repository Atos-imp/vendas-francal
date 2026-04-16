import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração simples
st.set_page_config(page_title="Portal Atos", layout="centered")

# Isso cria um "banco de dados" temporário na nuvem do Streamlit
if 'banco_dados' not in st.session_state:
    st.session_state['banco_dados'] = []

st.title("📊 Previsão de Vendas - Equipe Atos")

# --- ÁREA DO VENDEDOR ---
with st.form("form_vendas", clear_on_submit=True):
    vendedor = st.selectbox("Selecione seu nome", ["Atos", "Cainã", "Guilherme", "Jefferson", "Eurenice"])
    venda = st.number_input("Previsão de Venda (R$)", min_value=0.0, step=50.0)
    positivados = st.number_input("Clientes Positivados", min_value=0, step=1)
    obs = st.text_area("Observações")

    enviar = st.form_submit_button("Enviar para o Gestor")

if enviar:
    novo_item = {
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Vendedor": vendedor,
        "Venda": venda,
        "Posit.": positivados,
        "Obs": obs
    }
    st.session_state['banco_dados'].append(novo_item)
    st.success(f"Valeu, {vendedor}! Dados enviados.")

# --- ÁREA DO GESTOR ---
st.sidebar.markdown("---")
if st.sidebar.checkbox("Acesso Gestor"):
    senha = st.sidebar.text_input("Senha", type="password")
    if senha == "atos2026":
        st.subheader("📋 Relatório em Tempo Real")
        if st.session_state['banco_dados']:
            df = pd.DataFrame(st.session_state['banco_dados'])
            st.table(df)  # Exibe uma tabela simples e limpa

            total = df["Venda"].sum()
            st.metric("Total da Equipe", f"R$ {total:,.2f}")
        else:
            st.info("Nenhum dado lançado ainda.")