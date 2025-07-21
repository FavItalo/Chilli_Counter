import os
import sys

import streamlit as st
import pandas as pd
import requests as rq

import plotly.express as px
import plotly.graph_objects as go

def weekdays_dict():
    return {
        'Segunda-feira' : 0,
        'Terça-feira'   : 1,
        'Quarta-feira'  : 2,
        'Quinta-feira'  : 3,
        'Sexta-feira'   : 4,
        'Sábado'        : 5,
        'Domingo'       : 6
    }


@st.cache_data(show_spinner=True)
def load_data():
    r = rq.get("https://47k4ctcb5h.execute-api.sa-east-1.amazonaws.com/dev/chilli-visitors")
    df = pd.DataFrame.from_records(r.json()['data'])
    df.loc[:,'date'] = pd.to_datetime(df['date'], unit='s')-pd.DateOffset(hours=3)
    df.set_index('date', inplace=True)
    
    return df.sort_index(ascending=True)

@st.cache_resource(show_spinner=True)
def historical_show(data:pd.DataFrame):
    data_c = data.copy()
    data_min = data_c.index.min()
    data_max = data_c.index.max()
    
    data_c.reset_index(inplace=True)
    data_c.columns = ['Data', 'Visitantes']
    
    
    st.subheader(f"Dados disponíveis de {data_min.strftime('%d/%m/%Y')} até {data_max.strftime('%d/%m/%Y')}")

    
    historical_chart = px.line(data_c, x='Data', y='Visitantes', title='Visitantes ao longo do tempo')
    st.plotly_chart(historical_chart, use_container_width=True)
    
            
    col1, col2 = st.columns(2)
    with col1:
        today_chart = px.line(data_c[data_c.loc[:,'Data'].apply(lambda x: pd.to_datetime(x).date()) == pd.Timestamp.now().date()],
                                x='Data',
                                y='Visitantes',
                                title='Visitantes hoje')
        st.plotly_chart(today_chart, use_container_width=True)     
        
    with col2:
        yesterday_chart = px.line(data_c[data_c.loc[:,'Data'].apply(lambda x: pd.to_datetime(x).date()) == pd.Timestamp.now().date() - pd.Timedelta(days=1)],
                                    x='Data',
                                    y='Visitantes',
                                    title='Visitantes ontem')
        st.plotly_chart(yesterday_chart, use_container_width=True)
    
    return None    

weekdays = weekdays_dict()

def projection_show(df_projecao:pd.DataFrame):
    df_projecao['weekday'] = df_projecao.index.weekday
    df_projecao['hour'] = df_projecao.index.hour
    
    df_projecao_agg = df_projecao.groupby(['weekday', 'hour']).agg(['mean', 'max', 'min', 'std']).reset_index()
    
    weekday_selection = st.selectbox("Selecione o dia da semana para projeção",
                            options=list(weekdays.keys()))
            
    if weekday_selection in weekdays:
        try:

            
            df_projecao_selected = df_projecao_agg[df_projecao_agg['weekday'] == weekdays[weekday_selection]]
            df_projecao_selected.columns = ['weekday', 'Horário', 'Média de Visitantes', 'Máximo observado', 'Mínimo observado', 'visitors_std']
            st.subheader(f"Projeção de visitantes para {weekday_selection}")
            
            weekday_graf = px.line(df_projecao_selected, x='Horário',
                                    y='Média de Visitantes',
                                    title=f'Projeção de visitantes para {weekday_selection}')
            st.plotly_chart(weekday_graf, use_container_width=True)
        except:
            st.error("Erro ao filtrar os dados para o dia selecionado. Verifique se os dados estão disponíveis.")

    else:
        st.error("Escolha um dia da semana válido.")

st.title("Dashboad Chilli Hotel")

# get_data = st.button("Obter dados")
# if get_data:
#     try:
data = load_data()
historical_show(data)
    
st.subheader("Projeção de visitantes")
projection_show(data)
        
        
    # except Exception as e:
    #     st.error(f"Erro ao obter dados: {e}")



