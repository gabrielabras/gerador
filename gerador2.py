
import os
import streamlit as st
from datetime import datetime, timedelta

def ultimo_dia_do_mes(data):
    proximo_mes = data.replace(day=28) + timedelta(days=4)
    return (proximo_mes - timedelta(days=proximo_mes.day)).day

def gerar_arquivos_sped(ano, cnpj, razao_social, endereco, cep, cod_mun, uf, contato_nome, telefone, email):
    estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
               'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

    modelo = """|0000|09|4|{estado}|{cnpj}|{razao_social}|{data_ini}|{data_fim}|1|{competencia}|
|0001|1|
|0005|{razao_social}|{endereco}|{cep}|{cod_mun}|{uf}|{contato_nome}|{telefone}|{email}|
|0990|4|
|1001|0|
|1990|2|
|9001|1|
|9900|0000|1|
|9900|0001|1|
|9900|0005|1|
|9900|0006|0|
|9900|0990|1|
|9900|1001|1|
|9900|1990|1|
|9900|9001|1|
|9900|9900|11|
|9900|9990|1|
|9900|9999|1|
|9990|14|
|9999|20|"""

    pasta_raiz = f"arquivos_{ano}"
    os.makedirs(pasta_raiz, exist_ok=True)

    for mes in range(1, 13):
        pasta_mes = os.path.join(pasta_raiz, f"{mes:02d}")
        os.makedirs(pasta_mes, exist_ok=True)

        data_ini = datetime(ano, mes, 1)
        data_fim = datetime(ano, mes, ultimo_dia_do_mes(data_ini))

        ini_str = data_ini.strftime("%Y%m%d")
        fim_str = data_fim.strftime("%Y%m%d")
        competencia = (data_ini + timedelta(days=31)).strftime("%Y%m")

        for estado in estados:
            conteudo = modelo.format(
                estado=estado,
                cnpj=cnpj,
                razao_social=razao_social,
                data_ini=ini_str,
                data_fim=fim_str,
                competencia=competencia,
                endereco=endereco,
                cep=cep,
                cod_mun=cod_mun,
                uf=uf,
                contato_nome=contato_nome,
                telefone=telefone,
                email=email
            )

            nome_arquivo = os.path.join(pasta_mes, f"sped_{estado}_{ano}_{mes:02d}.txt")

            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)

    # Retorna o caminho absoluto da pasta raiz
    return os.path.abspath(pasta_raiz)

# Interface Streamlit
st.title("Gerador de Arquivos por Ano")

# Campos de entrada para o usuário (sem valores padrão)
ano = st.number_input("Informe o ano", min_value=2000, max_value=2100, step=1)
cnpj = st.text_input("CNPJ")
razao_social = st.text_input("Razão Social")
endereco = st.text_input("Endereço")
cep = st.text_input("CEP")
cod_mun = st.text_input("Código do Município")
uf = st.selectbox("UF", ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                         'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                         'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])
contato_nome = st.text_input("Nome do Contato")
telefone = st.text_input("Telefone")
email = st.text_input("E-mail")

if st.button("Gerar Arquivos"):
    if cnpj and razao_social and endereco and cep and cod_mun and uf and contato_nome and telefone and email:
        caminho_pasta = gerar_arquivos_sped(ano, cnpj, razao_social, endereco, cep, cod_mun, uf, contato_nome, telefone, email)
        st.success(f"Arquivos para {ano} gerados com sucesso!")
        st.info(f"Os arquivos foram salvos em: {caminho_pasta}")
    else:
        st.error("Por favor, preencha todos os campos antes de gerar os arquivos.")