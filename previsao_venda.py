import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestão Atos", layout="centered")

# Conecta à planilha (usando o link que você colocou nos Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📊 Portal de Vendas Atos")

with st.form("form_vendas", clear_on_submit=True):
    vendedor = st.selectbox("Vendedor", ["Atos", "Cainã", "Guilherme", "Jefferson", "Eurenice"])
    venda = st.number_input("Previsão (R$)", min_value=0.0)
    positivados = st.number_input("Positivados", min_value=0)
    obs = st.text_area("Observações")
    enviar = st.form_submit_button("Enviar Dados")

if enviar:
    # 1. Lê o que já tem na planilha
    df_existente = conn.read()
    
    # 2. Cria a nova linha
    nova_linha = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Vendedor": vendedor,
        "Venda": venda,
        "Positivados": positivados,
        "Obs": obs
    }])
    
    # 3. Junta e salva
    df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
    conn.update(data=df_atualizado)
    
    st.success("✅ Enviado! Os dados já estão na planilha do gestor.")

# Área do Gestor
if st.sidebar.checkbox("Acesso Gestor"):
    senha = st.sidebar.text_input("Senha", type="password")
    if senha == "atos2026":
        # Lê a planilha atualizada para você ver
        df_adm = conn.read()
        st.subheader("Relatório Geral")
        st.dataframe(df_adm)
