import requests
import json
import streamlit as st
import pandas as pd
import unicodedata

@st.cache_data
def load_data():
    response = requests.get("http://modal-flex.cpcon.net:8080/aluno")
    return json.loads(response.text)

resp = load_data()


def remove_acentos(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text.replace('ç', 'C')


diasDics = {
    "Dia 1": "14",
    "Dia 2": "15",
    "Dia 3": "16",
    "Dia 4": "17",
    "Dia 5": "18",
    "Dia 6": "19"
}


ofApi = pd.DataFrame(resp)


ofApi["date"] = pd.to_datetime(ofApi["date"], format='ISO8601')

dfin = pd.read_csv("RespeitaSeuPai.csv", delimiter=";", index_col=False, encoding='utf-8')
dfin["Nome"] = dfin["Nome"].apply(remove_acentos)


st.title('Listagem de presença Semana da Tecnologia')

dias = diasDics.keys()
selected_dia = st.selectbox("Selecione um dia:", dias)


resultado_dia_selected = ofApi[ofApi["date"].dt.day == int(diasDics[selected_dia])]
pesquisa = st.text_input("Pesquise o nome")

if pesquisa:
    dfin = dfin[dfin["Nome"].str.contains(pesquisa, case=False, na=False)]
    
dfin["Tag"] = dfin["Tag"].astype(str)
dffinal = dfin[dfin["Tag"].isin(resultado_dia_selected["tag"])]

# Exibir a tabela filtrada
st.table(dffinal)
