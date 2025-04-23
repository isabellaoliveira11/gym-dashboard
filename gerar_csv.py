import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações
random.seed(42)
total_alunos = 500
alunos_iniciais = 200
alunos_novos = total_alunos - alunos_iniciais
cancelamentos = 200

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

# Motivos de cancelamento
motivos_cancelamento = ["Mudança de Endereço", "Problemas Financeiros", "Outros"]
proporcao_motivos = {"Mudança de Endereço": 0.2, "Problemas Financeiros": 0.5, "Outros": 0.3}

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
    if dias_diferenca > 0:
        dias_aleatorios = random.randint(0, dias_diferenca)
        return data_inicio + timedelta(days=dias_aleatorios)
    elif dias_diferenca == 0:
        return data_inicio
    else:
        return data_inicio

def escolher_motivo_cancelamento():
    motivos = list(proporcao_motivos.keys())
    pesos = list(proporcao_motivos.values())
    return random.choices(motivos, weights=pesos, k=1)[0]

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
        "Motivo do Cancelamento": "",
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
            "Motivo do Cancelamento": "",
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
    data_cancelamento = None

    mes_matricula = data_matricula.month

    # Probabilidade maior de cancelar se matriculado antes dos picos
    probabilidade_pico = 0.7 if mes_matricula < 6 or (mes_matricula > 8 and mes_matricula < 10) else 0.3
    if random.random() < probabilidade_pico:
        # Cancelamento no pico de junho-agosto
        if mes_matricula < 6:
            data_cancelamento = gerar_data_aleatoria(datetime(2023, 6, 1), datetime(2023, 8, 31))
        # Cancelamento no pico de outubro-dezembro
        elif mes_matricula > 8 and mes_matricula < 10:
            data_cancelamento = gerar_data_aleatoria(datetime(2023, 10, 1), datetime(2023, 12, 31))
        # Cancelamento em outros meses com menor probabilidade, mas ainda possível
        else:
            data_cancelamento_inicio = data_matricula + timedelta(days=30) # Cancela pelo menos um mês depois
            data_cancelamento_fim = datetime(2023, 12, 31)
            if data_cancelamento_inicio <= data_cancelamento_fim:
                data_cancelamento = gerar_data_aleatoria(data_cancelamento_inicio, data_cancelamento_fim)
    else:
        # Cancelamentos com menor probabilidade nos outros meses
        data_cancelamento_inicio = data_matricula + timedelta(days=30) # Cancela pelo menos um mês depois
        data_cancelamento_fim = datetime(2023, 12, 31)
        if data_cancelamento_inicio <= data_cancelamento_fim:
            data_cancelamento = gerar_data_aleatoria(data_cancelamento_inicio, data_cancelamento_fim)

    if data_cancelamento and data_cancelamento > data_matricula:
        aluno["Status de Cancelamento"] = 1
        aluno["Data de Cancelamento"] = data_cancelamento.strftime("%Y-%m-%d")
        aluno["Mês do Cancelamento"] = data_cancelamento.month
        aluno["Estação do Cancelamento"] = estacao_do_ano(data_cancelamento)
        aluno["Tempo de Permanência (meses)"] = calcular_tempo_permanencia(data_matricula, data_cancelamento)
        aluno["Motivo do Cancelamento"] = escolher_motivo_cancelamento()

        for mes in meses:
            if mes > data_cancelamento:
                aluno[mes.strftime("%Y-%m")] = 0

# Remover alunos que não foram cancelados (para manter o número exato de cancelamentos)
dados_cancelados = [aluno for aluno in dados if aluno["Status de Cancelamento"] == 1]
dados_nao_cancelados = [aluno for aluno in dados if aluno["Status de Cancelamento"] == 0]

if len(dados_cancelados) > cancelamentos:
    dados_cancelados = random.sample(dados_cancelados, cancelamentos)
elif len(dados_cancelados) < cancelamentos:
    # Se por acaso houver menos cancelamentos do que o desejado, podemos ajustar (opcional)
    num_faltantes = cancelamentos - len(dados_cancelados)
    alunos_para_forcar_cancelamento = random.sample(dados_nao_cancelados, min(num_faltantes, len(dados_nao_cancelados)))
    for aluno in alunos_para_forcar_cancelamento:
        data_matricula = datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d")
        # Força o cancelamento em um dos picos ou em outro mês
        if random.random() < 0.5:
            data_cancelamento = gerar_data_aleatoria(datetime(2023, 6, 1), datetime(2023, 8, 31))
        else:
            data_cancelamento = gerar_data_aleatoria(datetime(2023, 10, 1), datetime(2023, 12, 31))

        if data_cancelamento > data_matricula:
            aluno["Status de Cancelamento"] = 1
            aluno["Data de Cancelamento"] = data_cancelamento.strftime("%Y-%m-%d")
            aluno["Mês do Cancelamento"] = data_cancelamento.month
            aluno["Estação do Cancelamento"] = estacao_do_ano(data_cancelamento)
            aluno["Tempo de Permanência (meses)"] = calcular_tempo_permanencia(data_matricula, data_cancelamento)
            aluno["Motivo do Cancelamento"] = escolher_motivo_cancelamento()
            dados_cancelados.append(aluno)

dados_final = dados_cancelados + dados_nao_cancelados
df_final = pd.DataFrame(dados_final)
df_final.to_csv("academia_dados_e_pagamentos_simulado_picos_cancelamento.csv", index=False, encoding='utf-8-sig')

print("✅ Arquivo gerado com sucesso com picos de cancelamento!")