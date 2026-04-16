import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Portal de Vendas Atos", layout="centered")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📊 Lançamento de Previsão - Equipe")

# Formulário de entrada
with st.form("form_vendas", clear_on_submit=True):
    vendedor = st.selectbox("Quem está lançando?", ["Atos", "Cainã", "Guilherme", "Jefferson", "Eurenice"])
    venda = st.number_input("Valor da Previsão (R$)", min_value=0.0, step=50.0)
    positivados = st.number_input("Qtd Positivados", min_value=0, step=1)
    obs = st.text_area("Notas / Observações")
    
    enviar = st.form_submit_button("Enviar para o Gestor")

if enviar:
    try:
        # Lê os dados que já existem na planilha
        df_atual = conn.read()
        
        # Cria a nova linha
        novo_registro = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Vendedor": vendedor,
            "Venda": venda,
            "Positivados": positivados,
            "Obs": obs
        }])
        
        # Junta os dados novos com os antigos
        df_final = pd.concat([df_atual, novo_registro], ignore_index=True)
        
        # Atualiza a planilha no Google Drive
        conn.update(data=df_final)
        
        st.success(f"Sucesso! Os dados de {vendedor} foram salvos.")
        st.balloons()
    except Exception as e:
        st.error("Erro ao conectar com a planilha. Verifique se ela está como 'Editor' para todos.")

# Área do Gestor (Protegida)
st.sidebar.markdown("---")
if st.sidebar.checkbox("Visualizar Relatório"):
    senha = st.sidebar.text_input("Senha de Acesso", type="password")
    if senha == "atos2026":
        st.subheader("📋 Dados Consolidados (Direto da Planilha)")
        # Lê a planilha novamente para mostrar os dados atualizados
        df_view = conn.read()
        st.dataframe(df_view, use_container_width=True)
        
        total_vendas = df_view["Venda"].sum()
        st.metric("Total Previsto no Dia", f"R$ {total_vendas:,.2f}")
