import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# --- Geração de Dados (Simulado) ---
random.seed(42)
total_alunos = 500
alunos_iniciais = 200
alunos_novos = total_alunos - alunos_iniciais
cancelamentos = 200

meses_geracao = pd.date_range(start="2023-01-01", end="2023-12-01", freq="MS")

estacoes_geracao = {
    "Verão": [1, 2, 12],
    "Outono": [3, 4, 5],
    "Inverno": [6, 7, 8],
    "Primavera": [9, 10, 11]
}

proporcao_estacoes_geracao = {
    "Verão": 0.35,
    "Outono": 0.25,
    "Inverno": 0.15,
    "Primavera": 0.25
}

motivos_cancelamento_geracao = ["Mudança de Endereço", "Problemas Financeiros", "Outros"]
proporcao_motivos_geracao = {"Mudança de Endereço": 0.2, "Problemas Financeiros": 0.5, "Outros": 0.3}

def gerar_data_estacao_geracao(estacao):
    meses_estacao = estacoes_geracao[estacao]
    mes_escolhido = random.choice(meses_estacao)
    ano = 2023
    dia = random.randint(1, 28)
    return datetime(ano, mes_escolhido, dia)

def estacao_do_ano_geracao(data):
    mes = data.month
    for estacao, meses in estacoes_geracao.items():
        if mes in meses:
            return estacao

def calcular_tempo_permanencia_geracao(inicio, fim):
    return (fim.year - inicio.year) * 12 + (fim.month - inicio.month)

def gerar_data_aleatoria_geracao(data_inicio, data_fim):
    dias_diferenca = (data_fim - data_inicio).days
    if dias_diferenca > 0:
        dias_aleatorios = random.randint(0, dias_diferenca)
        return data_inicio + timedelta(days=dias_aleatorios)
    elif dias_diferenca == 0:
        return data_inicio
    else:
        return data_inicio

def escolher_motivo_cancelamento_geracao():
    motivos = list(proporcao_motivos_geracao.keys())
    pesos = list(proporcao_motivos_geracao.values())
    return random.choices(motivos, weights=pesos, k=1)[0]

nomes_geracao = [f"Aluno {i}" for i in range(1, total_alunos + 1)]
generos_geracao = ["Masculino", "Feminino"]
planos_geracao = ["Mensal", "Trimestral", "Anual"]
meios_pagamento_geracao = ["Cartão", "Dinheiro", "Pix"]

dados_geracao = []

for i in range(alunos_iniciais):
    nome = nomes_geracao[i]
    idade = random.randint(18, 60)
    genero = random.choice(generos_geracao)
    plano = random.choice(planos_geracao)
    meio_pagamento = random.choice(meios_pagamento_geracao)
    data_matricula = datetime(2023, 1, 8)

    linha = {
        "ID Aluno": i + 1,
        "Nome": nome,
        "Idade": idade,
        "Gênero": genero,
        "Plano": plano,
        "Data de Matrícula": data_matricula.strftime("%Y-%m-%d"),
        "Mês da Matrícula": data_matricula.month,
        "Meio de Pagamento": meio_pagamento,
        "Status de Cancelamento": 0,
        "Data de Cancelamento": "",
        "Mês do Cancelamento": "",
        "Estação do Cancelamento": "",
        "Motivo do Cancelamento": "",
        "Tempo de Permanência (meses)": calcular_tempo_permanencia_geracao(data_matricula, datetime(2023, 12, 31))
    }
    for mes in meses_geracao:
        linha[mes.strftime("%Y-%m")] = 1 if mes >= data_matricula else 0
    dados_geracao.append(linha)

idx_novos = alunos_iniciais
for estacao, proporcao in proporcao_estacoes_geracao.items():
    qtd = int(proporcao * alunos_novos)
    for _ in range(qtd):
        nome = nomes_geracao[idx_novos]
        idade = random.randint(18, 60)
        genero = random.choice(generos_geracao)
        plano = random.choice(planos_geracao)
        meio_pagamento = random.choice(meios_pagamento_geracao)
        data_matricula = gerar_data_estacao_geracao(estacao)

        linha = {
            "ID Aluno": idx_novos + 1,
            "Nome": nome,
            "Idade": idade,
            "Gênero": genero,
            "Plano": plano,
            "Data de Matrícula": data_matricula.strftime("%Y-%m-%d"),
            "Mês da Matrícula": data_matricula.month,
            "Meio de Pagamento": meio_pagamento,
            "Status de Cancelamento": 0,
            "Data de Cancelamento": "",
            "Mês do Cancelamento": "",
            "Estação do Cancelamento": "",
            "Motivo do Cancelamento": "",
            "Tempo de Permanência (meses)": calcular_tempo_permanencia_geracao(data_matricula, datetime(2023, 12, 31))
        }
        for mes in meses_geracao:
            linha[mes.strftime("%Y-%m")] = 1 if mes >= data_matricula else 0
        dados_geracao.append(linha)
        idx_novos += 1

cancelar_indices_geracao = random.sample(range(total_alunos), cancelamentos)

for idx_cancelar in cancelar_indices_geracao:
    aluno = dados_geracao[idx_cancelar]
    data_matricula = datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d")
    data_cancelamento = None
    mes_matricula = data_matricula.month
    probabilidade_pico = 0.7 if mes_matricula < 6 or (mes_matricula > 8 and mes_matricula < 10) else 0.3
    if random.random() < probabilidade_pico:
        if mes_matricula < 6:
            data_cancelamento = gerar_data_aleatoria_geracao(datetime(2023, 6, 1), datetime(2023, 8, 31))
        elif mes_matricula > 8 and mes_matricula < 10:
            data_cancelamento = gerar_data_aleatoria_geracao(datetime(2023, 10, 1), datetime(2023, 12, 31))
        else:
            data_cancelamento_inicio = data_matricula + timedelta(days=30)
            data_cancelamento_fim = datetime(2023, 12, 31)
            if data_cancelamento_inicio <= data_cancelamento_fim:
                data_cancelamento = gerar_data_aleatoria_geracao(data_cancelamento_inicio, data_cancelamento_fim)
    else:
        data_cancelamento_inicio = data_matricula + timedelta(days=30)
        data_cancelamento_fim = datetime(2023, 12, 31)
        if data_cancelamento_inicio <= data_cancelamento_fim:
            data_cancelamento = gerar_data_aleatoria_geracao(data_cancelamento_inicio, data_cancelamento_fim)

    if data_cancelamento and data_cancelamento > data_matricula:
        aluno["Status de Cancelamento"] = 1
        aluno["Data de Cancelamento"] = data_cancelamento.strftime("%Y-%m-%d")
        aluno["Mês do Cancelamento"] = data_cancelamento.month
        aluno["Estação do Cancelamento"] = estacao_do_ano_geracao(data_cancelamento)
        aluno["Tempo de Permanência (meses)"] = calcular_tempo_permanencia_geracao(data_matricula, data_cancelamento)
        aluno["Motivo do Cancelamento"] = escolher_motivo_cancelamento_geracao()
        for mes in meses_geracao:
            if mes > data_cancelamento:
                aluno[mes.strftime("%Y-%m")] = 0

dados_cancelados_geracao = [aluno for aluno in dados_geracao if aluno["Status de Cancelamento"] == 1]
dados_nao_cancelados_geracao = [aluno for aluno in dados_geracao if aluno["Status de Cancelamento"] == 0]

if len(dados_cancelados_geracao) > cancelamentos:
    dados_cancelados_geracao = random.sample(dados_cancelados_geracao, cancelamentos)
elif len(dados_cancelados_geracao) < cancelamentos:
    num_faltantes = cancelamentos - len(dados_cancelados_geracao)
    alunos_para_forcar_cancelamento = random.sample(dados_nao_cancelados_geracao, min(num_faltantes, len(dados_nao_cancelados_geracao)))
    for aluno in alunos_para_forcar_cancelamento:
        data_matricula = datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d")
        if random.random() < 0.5:
            data_cancelamento = gerar_data_aleatoria_geracao(datetime(2023, 6, 1), datetime(2023, 8, 31))
        else:
            data_cancelamento = gerar_data_aleatoria_geracao(datetime(2023, 10, 1), datetime(2023, 12, 31))
        if data_cancelamento > data_matricula:
            aluno["Status de Cancelamento"] = 1
            aluno["Data de Cancelamento"] = data_cancelamento.strftime("%Y-%m-%d")
            aluno["Mês do Cancelamento"] = data_cancelamento.month
            aluno["Estação do Cancelamento"] = estacao_do_ano_geracao(data_cancelamento)
            aluno["Tempo de Permanência (meses)"] = calcular_tempo_permanencia_geracao(data_matricula, data_cancelamento)
            aluno["Motivo do Cancelamento"] = escolher_motivo_cancelamento_geracao()
            dados_cancelados_geracao.append(aluno)

dados_final_geracao = dados_cancelados_geracao + dados_nao_cancelados_geracao
df_gerado = pd.DataFrame(dados_final_geracao)
df_gerado.to_csv("academia_dados_e_pagamentos_simulado_picos_cancelamento.csv", index=False, encoding='utf-8-sig')

print("✅ Arquivo de dados simulado gerado com sucesso!")

# --- Dashboard Streamlit ---
# Carregar os dados
df = pd.read_csv("academia_dados_e_pagamentos_simulado_picos_cancelamento.csv")

# Mapeamento de meses para exibição
meses_display = {
    "2023-01": "Janeiro", "2023-02": "Fevereiro", "2023-03": "Março", "2023-04": "Abril",
    "2023-05": "Maio", "2023-06": "Junho", "2023-07": "Julho", "2023-08": "Agosto",
    "2023-09": "Setembro", "2023-10": "Outubro", "2023-11": "Novembro", "2023-12": "Dezembro"
}

meses_pagamento = list(meses_display.keys())

# Função para exibir a lista de alunos com pagamento no mês selecionado
def lista_de_alunos_com_pagamento(mes_key):
    alunos_lista = df[["ID Aluno", "Nome", "Idade", "Plano", mes_key]]
    alunos_lista = alunos_lista.rename(columns={mes_key: "Pagamento no mês"})
    alunos_lista = alunos_lista.sort_values(by="Nome")
    return alunos_lista

# Função para mostrar o histórico de pagamentos de um aluno
def exibir_historico_pagamentos(aluno_id):
    aluno = df[df["ID Aluno"] == aluno_id].iloc[0]
    historico_pagamentos = aluno[meses_pagamento]

    fig = go.Figure(data=[go.Bar(x=[meses_display[m] for m in historico_pagamentos.index], y=historico_pagamentos.values)])
    fig.update_layout(title="Histórico de Pagamentos")
    st.plotly_chart(fig)

    return aluno

# Função para criar os gráficos da visão geral
def visao_geral():
    st.subheader("Distribuição dos Alunos")
    col1, col2 = st.columns(2)
    with col1:
        fig_idade = px.histogram(df, x="Idade", title="Por Idade")
        st.plotly_chart(fig_idade)
        fig_genero = px.pie(df, names="Gênero", title="Por Gênero")
        st.plotly_chart(fig_genero)
    with col2:
        fig_plano = px.pie(df, names="Plano", title="Por Plano")
        st.plotly_chart(fig_plano)
        fig_meio_pagamento = px.pie(df, names="Meio de Pagamento", title="Por Meio de Pagamento")
        st.plotly_chart(fig_meio_pagamento)

    st.subheader("Estatísticas por Mês")
    mes_escolhido_key = st.selectbox("Selecione o mês", meses_pagamento, format_func=lambda x: meses_display[x])

    total_matriculas = df[df["Data de Matrícula"].str[:7] == mes_escolhido_key].shape[0]
    total_cancelamentos = df[(df["Status de Cancelamento"] == 1) &
                                (df["Data de Cancelamento"].str[:7] == mes_escolhido_key)].shape[0]
    total_ativos = df[df[mes_escolhido_key] > 0].shape[0]

    st.write(f"📊 Quantidade de matrículas em **{meses_display[mes_escolhido_key]}**: **{total_matriculas}**")
    st.write(f"❌ Quantidade de cancelamentos em **{meses_display[mes_escolhido_key]}**: **{total_cancelamentos}**")
    st.write(f"✅ Quantidade de alunos ativos (pagaram em **{meses_display[mes_escolhido_key]}**): **{total_ativos}**")

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
        mes_aluno_key = st.selectbox("Selecione o mês para visualizar pagamentos", meses_pagamento, format_func=lambda x: meses_display[x])
        alunos = lista_de_alunos_com_pagamento(mes_aluno_key)
        st.dataframe(alunos)

        aluno_id = st.selectbox("Selecione um aluno para detalhes", alunos["ID Aluno"])

        if aluno_id:
            aluno = exibir_historico_pagamentos(aluno_id)
            st.subheader(f"Detalhes do Aluno: {aluno['Nome']}")
            st.write(f"**Idade:** {aluno['Idade']}")
            st.write(f"**Gênero:** {aluno['Gênero']}")
            st.write(f"**Plano:** {aluno['Plano']}")
            st.write(f"**Data de Matrícula:** {pd.to_datetime(aluno['Data de Matrícula']).strftime('%d/%m/%Y')}")
            st.write(f"**Meio de Pagamento:** {aluno['Meio de Pagamento']}")
            st.write(f"**Status de Cancelamento:** {'Cancelado' if aluno['Status de Cancelamento'] == 1 else 'Ativo'}")
            st.write(f"**Tempo de Permanência:** {aluno['Tempo de Permanência (meses)']} meses")
            if aluno['Status de Cancelamento'] == 1 and aluno['Data de Cancelamento']:
                st.write(f"**Data de Cancelamento:** {pd.to_datetime(aluno['Data de Cancelamento']).strftime('%d/%m/%Y')}")
                st.write(f"**Motivo do Cancelamento:** {aluno['Motivo do Cancelamento']}")

    elif escolha == "Visão Geral":
        st.header("Visão Geral da Academia")
        visao_geral()

    elif escolha == "Cancelamentos":
        st.header("Cancelamentos na Academia")
        grafico_cancelamentos()

# Executar o aplicativo
if __name__ == "__main__":
    main()