import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações
random.seed(42)
total_alunos = 500
alunos_iniciais = 200
alunos_novos = total_alunos - alunos_iniciais
cancelamentos = 150

# Datas e estações
meses = pd.date_range(start="2023-01-01", end="2023-12-01", freq="MS")

# Estações para sazonalidade
estacoes = {
    "Verão": [1, 2, 12],
    "Outono": [3, 4, 5],
    "Inverno": [6, 7, 8],
    "Primavera": [9, 10, 11]
}

proporcao_estacoes = {
    "Verão": 0.35,
    "Outono": 0.25,
    "Inverno": 0.15,
    "Primavera": 0.25
}

# Funções auxiliares

def gerar_data_estacao(estacao):
    meses_estacao = estacoes[estacao]
    mes_escolhido = random.choice(meses_estacao)
    ano = 2023
    dia = random.randint(1, 28)
    return datetime(ano, mes_escolhido, dia)

def estacao_do_ano(data):
    mes = data.month
    for estacao, meses in estacoes.items():
        if mes in meses:
            return estacao

def calcular_tempo_permanencia(inicio, fim):
    return (fim.year - inicio.year) * 12 + (fim.month - inicio.month)

def gerar_data_aleatoria(data_inicio, data_fim):
    dias_diferenca = (data_fim - data_inicio).days
    return data_inicio + timedelta(days=random.randint(30, dias_diferenca))

# Dados base
nomes = [f"Aluno {i}" for i in range(1, total_alunos + 1)]
generos = ["Masculino", "Feminino"]
planos = ["Mensal", "Trimestral", "Anual"]
meios_pagamento = ["Cartão", "Dinheiro", "Pix"]

# Lista principal de dados
dados = []

# ------------------- Alunos Iniciais -------------------
for i in range(alunos_iniciais):
    nome = nomes[i]
    idade = random.randint(18, 60)
    genero = random.choice(generos)
    plano = random.choice(planos)
    meio_pagamento = random.choice(meios_pagamento)
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
        "Tempo de Permanência (meses)": calcular_tempo_permanencia(data_matricula, datetime(2023, 12, 31))
    }

    for mes in meses:
        linha[mes.strftime("%Y-%m")] = 1 if mes >= data_matricula else 0

    dados.append(linha)

# ------------------- Novos Alunos -------------------
idx = alunos_iniciais
for estacao, proporcao in proporcao_estacoes.items():
    qtd = int(proporcao * alunos_novos)
    for _ in range(qtd):
        nome = nomes[idx]
        idade = random.randint(18, 60)
        genero = random.choice(generos)
        plano = random.choice(planos)
        meio_pagamento = random.choice(meios_pagamento)
        data_matricula = gerar_data_estacao(estacao)

        linha = {
            "ID Aluno": idx + 1,
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
            "Tempo de Permanência (meses)": calcular_tempo_permanencia(data_matricula, datetime(2023, 12, 31))
        }

        for mes in meses:
            linha[mes.strftime("%Y-%m")] = 1 if mes >= data_matricula else 0

        dados.append(linha)
        idx += 1

# ------------------- Cancelamentos -------------------
cancelar_indices = random.sample(range(total_alunos), cancelamentos)
for idx in cancelar_indices:
    aluno = dados[idx]
    data_matricula = datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d")
    data_cancelamento = gerar_data_aleatoria(data_matricula, datetime(2023, 12, 31))

    aluno["Status de Cancelamento"] = 1
    aluno["Data de Cancelamento"] = data_cancelamento.strftime("%Y-%m-%d")
    aluno["Mês do Cancelamento"] = data_cancelamento.month
    aluno["Estação do Cancelamento"] = estacao_do_ano(data_cancelamento)
    aluno["Tempo de Permanência (meses)"] = calcular_tempo_permanencia(data_matricula, data_cancelamento)

    for mes in meses:
        if mes > data_cancelamento:
            aluno[mes.strftime("%Y-%m")] = 0

# ------------------- Salvar CSV -------------------
df_final = pd.DataFrame(dados)
df_final.to_csv("academia_dados_e_pagamentos_simulado.csv", index=False, encoding='utf-8-sig')

print("✅ Arquivo gerado com sucesso!")
