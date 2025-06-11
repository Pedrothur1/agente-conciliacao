import streamlit as st
import pandas as pd
from conciliacao import padroniza_base_cliente, padroniza_extrato_caixa, padroniza_extrato_itau, conciliacao_1_1

st.title("Agente de Conciliação Bancária FP&A")

base_file = st.file_uploader("Base do cliente (.xls/.xlsx)", type=['xls', 'xlsx'])
caixa_file = st.file_uploader("Extrato Caixa (.xlsx)", type=['xlsx'])
itau_file = st.file_uploader("Extrato Itaú (.xlsx)", type=['xlsx'])

if base_file and caixa_file and itau_file:
    base = padroniza_base_cliente(base_file)
    caixa = padroniza_extrato_caixa(caixa_file)
    itau = padroniza_extrato_itau(itau_file)
    extratos = pd.concat([caixa, itau], ignore_index=True)
    resultado = conciliacao_1_1(base, extratos)
    st.write("Resumo da Conciliação:")
    st.write(resultado['Conciliado'].value_counts())
    st.write("Baixe o arquivo de resultado:")
    resultado_xlsx = resultado.to_excel(index=False)
    st.download_button(
        label="Baixar resultado (.xlsx)",
        data=resultado_xlsx,
        file_name="resultado_conciliacao.xlsx"
    )
