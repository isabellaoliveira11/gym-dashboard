import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- Configurações ---
random.seed(42)
total_alunos = 500
alunos_iniciais = 200
alunos_novos = total_alunos - alunos_iniciais
cancelamentos_maximo = 180

# Datas e Estações
meses = pd.date_range(start="2023-01-01", end="2023-12-01", freq="MS")
meses_numeros = list(range(1, 13))

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

motivos_cancelamento = ["Problemas Financeiros", "Outros"]
proporcao_motivos = {"Problemas Financeiros": 0.7, "Outros": 0.3}

# --- Funções auxiliares ---
def gerar_data_estacao(estacao):
    meses_estacao = estacoes[estacao]
    mes_escolhido = random.choice(meses_estacao)
    return datetime(2023, mes_escolhido, random.randint(1, 28))

def estacao_do_ano(data):
    mes = data.month
    for estacao, meses_lista in estacoes.items():
        if mes in meses_lista:
            return estacao

def calcular_tempo_permanencia(inicio, fim):
    return (fim.year - inicio.year) * 12 + (fim.month - inicio.month)

def gerar_data_aleatoria(data_inicio, data_fim):
    dias_diferenca = (data_fim - data_inicio).days
    if dias_diferenca > 0:
        return data_inicio + timedelta(days=random.randint(1, dias_diferenca))
    return data_inicio

def escolher_motivo_cancelamento():
    motivos = list(proporcao_motivos.keys())
    pesos = list(proporcao_motivos.values())
    return random.choices(motivos, weights=pesos, k=1)[0]

def escolher_meio_pagamento(plano):
    if plano == "Anual":
        return random.choices(["Cartão", "Dinheiro", "Pix"], weights=[0.6, 0.2, 0.2])[0]
    return random.choice(["Pix", "Dinheiro", "Cartão"])

# --- Gerar Dados ---
nomes = [f"Aluno {i}" for i in range(1, total_alunos + 1)]
generos = ["Masculino", "Feminino"]
planos = ["Mensal",  "Anual"]

dados = []

# Alunos Iniciais (Janeiro)
for i in range(alunos_iniciais):
    nome = nomes[i]
    genero = random.choices(["Feminino", "Masculino"], weights=[0.7, 0.3])[0]
    idade = random.choices(range(18, 61), weights=[2 if 25 <= a <= 45 else 1 for a in range(18, 61)])[0] if genero == "Feminino" else random.randint(18, 60)
    plano = random.choice(planos)
    meio_pagamento = escolher_meio_pagamento(plano)
    data_matricula = datetime(2023, 1, random.randint(1, 28))

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

# Novos Alunos durante o ano
idx = alunos_iniciais
for estacao, proporcao in proporcao_estacoes.items():
    qtd = int(proporcao * alunos_novos)
    for _ in range(qtd):
        nome = nomes[idx]
        genero = random.choices(["Feminino", "Masculino"], weights=[0.7, 0.3])[0]
        idade = random.choices(range(18, 61), weights=[2 if 25 <= a <= 45 else 1 for a in range(18, 61)])[0] if genero == "Feminino" else random.randint(18, 60)
        plano = random.choice(planos)
        meio_pagamento = escolher_meio_pagamento(plano)
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

# --- Inadimplência (simulação de alguns alunos com atraso de pagamento) ---
alunos_mensais = [a for a in dados if a["Plano"] == "Mensal"]
alunos_inadimplentes = random.sample(alunos_mensais, int(0.10 * len(alunos_mensais)))

for aluno in alunos_inadimplentes:
    mes_inicio = random.randint(1, 10)
    duracao = random.choice([1, 2])
    for i in range(duracao):
        if mes_inicio + i <= 12:
            aluno[meses[mes_inicio + i - 1].strftime("%Y-%m")] = 0

# --- Cancelamentos programados (picos no inverno + outros meses) ---
cancelamentos_alvo = {
    2: 5, 3: 6, 4: 8, 5: 5,
    6: 25, 7: 22, 8: 21,
    9: 12, 10: 16, 11: 18, 12: 23
}

cancelamentos_por_mes = {mes: 0 for mes in meses_numeros}
total_cancelados = 0
random.shuffle(dados)

for mes, alvo in cancelamentos_alvo.items():
    candidatos = [aluno for aluno in dados if aluno["Status de Cancelamento"] == 0 and datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d").month <= mes]
    random.shuffle(candidatos)
    for aluno in candidatos[:alvo]:
        data_cancelamento = gerar_data_aleatoria(datetime(2023, mes, 1), datetime(2023, mes, 28))
        if datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d") < data_cancelamento:
            aluno["Status de Cancelamento"] = 1
            aluno["Data de Cancelamento"] = data_cancelamento.strftime("%Y-%m-%d")
            aluno["Mês do Cancelamento"] = data_cancelamento.month
            aluno["Estação do Cancelamento"] = estacao_do_ano(data_cancelamento)
            aluno["Motivo do Cancelamento"] = escolher_motivo_cancelamento()
            aluno["Tempo de Permanência (meses)"] = calcular_tempo_permanencia(datetime.strptime(aluno["Data de Matrícula"], "%Y-%m-%d"), data_cancelamento)
            for mes_ in meses:
                if mes_ > data_cancelamento:
                    aluno[mes_.strftime("%Y-%m")] = 0
            cancelamentos_por_mes[mes] += 1
            total_cancelados += 1
            if total_cancelados >= cancelamentos_maximo:
                break
    if total_cancelados >= cancelamentos_maximo:
        break

# --- Salvar o CSV Final ---
df_final = pd.DataFrame(dados)
df_final.to_csv("academia_dados_previsao_cancelamento.csv", index=False, encoding='utf-8-sig')

print(f"✅ Arquivo gerado com sucesso com {total_cancelados} cancelamentos (máximo {cancelamentos_maximo})!")
print("Cancelamentos por mês:", cancelamentos_por_mes)
