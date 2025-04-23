import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados
df = pd.read_csv("academia_dados_e_pagamentos_oficial.csv")

meses_pagamento = ["2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", 
                   "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"]

# Função para exibir a lista de alunos com pagamento no mês selecionado
def lista_de_alunos_com_pagamento(mes):
    alunos_lista = df[["ID Aluno", "Nome", "Idade", "Plano", mes]]
    alunos_lista = alunos_lista.rename(columns={mes: "Pagamento no mês"})
    alunos_lista = alunos_lista.sort_values(by="Nome")
    return alunos_lista

# Função para mostrar o histórico de pagamentos de um aluno
def exibir_historico_pagamentos(aluno_id):
    aluno = df[df["ID Aluno"] == aluno_id].iloc[0]
    historico_pagamentos = aluno[meses_pagamento]
    
    fig = go.Figure(data=[go.Bar(x=historico_pagamentos.index, y=historico_pagamentos.values)])
    fig.update_layout(title="Histórico de Pagamentos")
    st.plotly_chart(fig)

    return aluno

# Função para criar os gráficos da visão geral
def visao_geral():
    fig_idade = px.histogram(df, x="Idade", title="Distribuição de Idades dos Alunos")
    fig_genero = px.pie(df, names="Gênero", title="Distribuição por Gênero")
    fig_plano = px.pie(df, names="Plano", title="Distribuição de Planos")
    fig_meio_pagamento = px.pie(df, names="Meio de Pagamento", title="Distribuição por Meio de Pagamento")

    st.plotly_chart(fig_idade)
    st.plotly_chart(fig_genero)
    st.plotly_chart(fig_plano)
    st.plotly_chart(fig_meio_pagamento)

    st.subheader("Estatísticas por Mês")
    mes_escolhido = st.selectbox("Selecione o mês", meses_pagamento)

    total_matriculas = df[df["Data de Matrícula"].str[:7] == mes_escolhido].shape[0]
    total_cancelamentos = df[(df["Status de Cancelamento"] == 1) & 
                             (df["Data de Cancelamento"].str[:7] == mes_escolhido)].shape[0]
    total_ativos = df[df[mes_escolhido] > 0].shape[0]

    st.write(f"📌 Quantidade de matrículas no mês: **{total_matriculas}**")
    st.write(f"❌ Quantidade de cancelamentos no mês: **{total_cancelamentos}**")
    st.write(f"✅ Quantidade de alunos ativos (pagaram no mês): **{total_ativos}**")

# Função para gráficos de cancelamentos
def grafico_cancelamentos():
    df_cancelamentos = df[df["Status de Cancelamento"] == 1]
    cancelamentos_por_estacao = df_cancelamentos.groupby("Estação do Cancelamento").size().reset_index(name="Quantidade")
    
    fig = px.bar(cancelamentos_por_estacao, x="Estação do Cancelamento", y="Quantidade", title="Cancelamentos por Estação")
    st.plotly_chart(fig)

# Layout do Streamlit
def main():
    st.title("Dashboard da Academia")

    menu = ["Home", "Alunos", "Visão Geral", "Cancelamentos"]
    escolha = st.sidebar.selectbox("Escolha uma opção", menu)

    if escolha == "Home":
        st.header("Bem-vindo ao Dashboard da Academia!")
    
    elif escolha == "Alunos":
        st.header("Lista de Alunos")
        mes_aluno = st.selectbox("Selecione o mês para visualizar pagamentos", meses_pagamento)
        alunos = lista_de_alunos_com_pagamento(mes_aluno)
        st.dataframe(alunos)

        aluno_id = st.selectbox("Selecione um aluno para detalhes", alunos["ID Aluno"])

        if aluno_id:
            aluno = exibir_historico_pagamentos(aluno_id)
            st.subheader(f"Detalhes do Aluno: {aluno['Nome']}")
            st.write(f"Idade: {aluno['Idade']}")
            st.write(f"Gênero: {aluno['Gênero']}")
            st.write(f"Plano: {aluno['Plano']}")
            st.write(f"Data de Matrícula: {aluno['Data de Matrícula']}")
            st.write(f"Meio de Pagamento: {aluno['Meio de Pagamento']}")
            st.write(f"Status de Cancelamento: {'Cancelado' if aluno['Status de Cancelamento'] == 1 else 'Ativo'}")
            st.write(f"Tempo de Permanência: {aluno['Tempo de Permanência (meses)']} meses")

    elif escolha == "Visão Geral":
        st.header("Visão Geral da Academia")
        visao_geral()

    elif escolha == "Cancelamentos":
        st.header("Cancelamentos na Academia")
        grafico_cancelamentos()

# Executar o aplicativo
if __name__ == "__main__":
    main()
