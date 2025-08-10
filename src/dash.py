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

@st.cache_resource(show_spinner=True)
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
        yesterday_chart = px.line(data_c[data_c.loc[:,'Data'].apply(lambda x: pd.to_datetime(x).date()) == pd.Timestamp.now().date() - pd.Timedelta(days=1)],
                                    x='Data',
                                    y='Visitantes',
                                    title='Visitantes ontem')
        st.plotly_chart(yesterday_chart, use_container_width=True)

    with col2:
        today_chart = px.line(data_c[data_c.loc[:,'Data'].apply(lambda x: pd.to_datetime(x).date()) == pd.Timestamp.now().date()],
                                x='Data',
                                y='Visitantes',
                                title='Visitantes hoje')
        st.plotly_chart(today_chart, use_container_width=True)     
        
    
    
    return None    

weekdays = weekdays_dict()

def projection_show(df_projecao:pd.DataFrame):

    df_proj_c = df_projecao.copy()
    df_proj_c['weekday'] = df_proj_c.index.weekday
    df_proj_c['hour'] = df_proj_c.index.hour
    
    df_projecao_agg = df_proj_c.groupby(['weekday', 'hour']).agg(['mean', 'max', 'min', 'std']).reset_index()
    
    weekday_selection = st.selectbox("Selecione o dia da semana para projeção",
                            options=list(weekdays.keys()), index = pd.Timestamp.now().date().weekday())
            
    if weekday_selection in weekdays:
        #try: 
            df_projecao_selected = df_projecao_agg[df_projecao_agg['weekday'] == weekdays[weekday_selection]]
            df_projecao_selected.columns = ['weekday', 'Horário', 'Média de Visitantes', 'Máximo observado', 'Mínimo observado', 'visitors_std']
            st.subheader(f"Projeção de visitantes para {weekday_selection}")
            
            # Create the plotly figure
            fig = go.Figure()            

            fig.add_trace(go.Scatter(x=df_projecao_selected['Horário'],
                                    y=df_projecao_selected['Máximo observado'],
                                    mode='lines',
                                    name='Máximo observado',
                                    line=dict(color='#74a5dd', width=1)))

            fig.add_trace(go.Scatter(x=df_projecao_selected['Horário'],
                                    y=df_projecao_selected['Mínimo observado'],
                                    mode='lines',
                                    name='Mínimo observado',
                                    line=dict(color='#74a5dd', width=1)))

            fig.add_trace(go.Scatter(x=df_projecao_selected['Horário'].tolist() + df_projecao_selected['Horário'][::-1].tolist(),
                                    y=df_projecao_selected['Máximo observado'].tolist() + df_projecao_selected['Mínimo observado'][::-1].tolist(),
                                    fill='toself',
                                    fillcolor='rgba(116, 165, 221, 0.5)',  # Light gray fill
                                    line=dict(color='rgba(255,255,255,0)'),
                                    name='Área entre Máximo e Mínimo',
                                    showlegend=False))
            
            fig.add_trace(go.Scatter(x=df_projecao_selected['Horário'],
                                    y=df_projecao_selected['Média de Visitantes'],
                                    mode='lines',
                                    name='Média de Visitantes',
                                    line=dict(color='#74a5dd', width=2)))
            
            if weekdays[weekday_selection] == pd.Timestamp.now().date().weekday():
                today_visitors = df_proj_c[df_proj_c.index.date == pd.Timestamp.now().date()]
                today_visitors.reset_index(inplace=True)
                today_visitors_agg = today_visitors.loc[:, ['hour', 'visitors']].groupby('hour').agg('mean').reset_index()
                today_visitors_agg.columns = ['hour', 'Visitantes']


                fig.add_trace(go.Scatter(x=today_visitors_agg['hour'],
                                        y=today_visitors_agg['Visitantes'],
                                        mode='lines',
                                        name='Visitantes de Hoje',
                                        line=dict(color='#ff7f0e', width=2, dash='dash')))

            # Update layout
            fig.update_layout(title=f'Projeção de visitantes para {weekday_selection}',
                            xaxis_title='Horário',
                            yaxis_title='Número de Visitantes',
                            template='plotly_white')

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

        #except:
           # st.error("Erro ao filtrar os dados para o dia selecionado. Verifique se os dados estão disponíveis.")

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



