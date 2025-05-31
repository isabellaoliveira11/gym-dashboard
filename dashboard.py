import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Força Local – Dashboard",  
    page_icon="🏋️",                            
    layout="wide"                              
)



df_raw = pd.read_csv("academia_cancelamento_com_previsoes.csv")
df_raw['Data de Matrícula'] = pd.to_datetime(df_raw['Data de Matrícula'], errors='coerce')
df = df_raw.copy()

meses_pagamento = [c for c in df.columns if c.startswith("2024-")]
meses_display = {mes: mes.replace("2024-", "").zfill(2) + "/2024" for mes in meses_pagamento}

# --- Funções de dashboard

def visao_geral():
    st.subheader("Distribuição dos Alunos")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(df, x="Idade", title="Distribuição por Idade"))
        st.plotly_chart(px.pie(df, names="Gênero", title="Distribuição por Gênero"))
    with c2:
        st.plotly_chart(px.pie(df, names="Plano", title="Distribuição por Plano"))
        st.plotly_chart(px.pie(df, names="Meio de Pagamento", title="Distribuição por Meio de Pagamento"))

    st.subheader("Estatísticas por Mês")
    mes = st.selectbox("Selecione o mês", meses_pagamento, format_func=lambda x: meses_display[x])
    total_mat = df[df["Data de Matrícula"].dt.strftime("%Y-%m") == mes].shape[0]
    total_ativos = df[df[mes] > 0].shape[0]
    st.markdown(f"📚 Matrículas em **{meses_display[mes]}**: **{total_mat}**")
    st.markdown(f"✅ Alunos ativos com pagamento no mês: **{total_ativos}**")


def alunos_alto_risco():
    st.subheader("🚨 Alunos com Risco de Cancelamento")

    filtro_plano = st.selectbox("📦 Filtrar por plano", ["Todos"] + sorted(df["Plano"].unique()))
    filtro_risco = st.selectbox("🚦 Filtrar por risco", ["Todos", "Crítico (≥80%)", "Alerta (60–79.9%)", "Atenção (40–59.9%)", "Baixo (<40%)"])

    risco_df = df[df["Status de Cancelamento"] == 0].copy()

    # Adiciona a coluna de cor da bolinha
    def classifica_risco(prob):
        if prob >= 0.80:
            return "🔴 Crítico"
        elif prob >= 0.60:
            return "🟠 Alerta"
        elif prob >= 0.40:
            return "🟡 Atenção"
        else:
            return "🟢 Baixo"

    risco_df["Classificação de Risco"] = risco_df["Probabilidade de Cancelamento"].apply(classifica_risco)

    # Aplica filtros
    if filtro_plano != "Todos":
        risco_df = risco_df[risco_df["Plano"] == filtro_plano]

    if filtro_risco != "Todos":
        risco_df = risco_df[risco_df["Classificação de Risco"].str.contains(filtro_risco.split()[0])]

    if risco_df.empty:
        st.info("Nenhum aluno encontrado com os critérios selecionados.")
    else:
        st.dataframe(
            risco_df[[
                "Nome", "Idade", "Gênero", "Plano", "Tempo de Permanência (meses)",
                "Total de Pagamentos", "Probabilidade (%)", "Classificação de Risco"
            ]].sort_values("Probabilidade (%)", ascending=False),
            use_container_width=True,
            hide_index=True
        )



def lista_alunos():
    st.subheader("👥 Lista de Alunos")
    df["Status"] = df["Status de Cancelamento"].map({0: "Ativo", 1: "Cancelado"})

    # --- Filtros
    filtro_nome = st.text_input("🔍 Buscar por nome:")
    filtro_plano = st.selectbox("📦 Filtrar por plano", ["Todos"] + sorted(df["Plano"].unique()))
    filtro_status = st.selectbox("📌 Filtrar por status", ["Todos", "Ativo", "Cancelado"])
    filtro_risco = st.selectbox("🚦 Filtrar por risco", ["Todos", "Crítico (≥80%)", "Alerta (60–79.9%)", "Atenção (40–59.9%)", "Sem risco (<40%)"])

    # --- Aplicar filtros
    res = df.copy()
    if filtro_nome:
        res = res[res["Nome"].str.contains(filtro_nome, case=False)]
    if filtro_plano != "Todos":
        res = res[res["Plano"] == filtro_plano]
    if filtro_status != "Todos":
        res = res[res["Status"] == filtro_status]
    if filtro_risco != "Todos":
        if "Crítico" in filtro_risco:
            res = res[res["Probabilidade de Cancelamento"] >= 0.80]
        elif "Alerta" in filtro_risco:
            res = res[(res["Probabilidade de Cancelamento"] >= 0.60) & (res["Probabilidade de Cancelamento"] < 0.80)]
        elif "Atenção" in filtro_risco:
            res = res[(res["Probabilidade de Cancelamento"] >= 0.40) & (res["Probabilidade de Cancelamento"] < 0.60)]
        elif "Sem risco" in filtro_risco:
            res = res[res["Probabilidade de Cancelamento"] < 0.40]

    # --- Cards
    if filtro_nome:
        if not res.empty:
            for _, aluno in res.iterrows():
                risco = aluno['Probabilidade de Cancelamento']
                # Cor por faixa de risco
                if risco >= 0.80:
                    cor_risco = "#d9534f"
                    bolinha = "🔴"
                elif risco >= 0.60:
                    cor_risco = "#f0ad4e"
                    bolinha = "🟠"
                elif risco >= 0.40:
                    cor_risco = "#ffc107"
                    bolinha = "🟡"
                else:
                    cor_risco = "#5cb85c"
                    bolinha = "🟢"

                emoji_status = "✅" if aluno["Status"] == "Ativo" else "❌"
                st.markdown(f"""
                <div style="background-color:#f5f5f5; padding:20px; border-radius:15px; 
                            margin: 0 auto 20px auto; max-width: 500px; box-shadow: 0 2px 20px rgba(0,0,0,0.08); 
                            font-size:15px; color:#222;">
                    <h4 style="margin-bottom:12px;"> {aluno['Nome']}</h4>
                    <p><strong>🆔 ID:</strong> {aluno['ID Aluno']} | 🎂 <strong>Idade:</strong> {aluno['Idade']} anos | 🧬 <strong>Gênero:</strong> {aluno['Gênero']}</p>
                    <p>📞 <strong>Telefone:</strong> {aluno['Telefone']}</p>
                    <p>📦 <strong>Plano:</strong> {aluno['Plano']} | 💳 <strong>Pagamento:</strong> {aluno['Meio de Pagamento']}</p>
                    <p>📊 <strong>Tempo de Permanência:</strong> {aluno['Tempo de Permanência (meses)']} meses | 💰 <strong>Total de Pagamentos:</strong> {aluno['Total de Pagamentos']}</p>
                    <p>📈 <strong>Probabilidade de Cancelamento:</strong> {bolinha} 
                        <span style="color:{cor_risco}; font-weight:bold;">{(risco * 100):.2f}%</span></p>
                    <p>📌 <strong>Status:</strong> {emoji_status} {aluno['Status']}</p>
                </div>
                """, unsafe_allow_html=True)



        else:
            st.warning("Nenhum aluno encontrado com esse nome.")
    else:
        st.markdown("""
            <style>
                [data-testid="stDataFrame"] {
                    width: 100% !important;
                }
            </style>
        """, unsafe_allow_html=True)

        st.dataframe(
            res[[
                "ID Aluno", "Nome", "Idade", "Gênero", "Telefone", "Plano", "Meio de Pagamento",
                "Tempo de Permanência (meses)", "Total de Pagamentos", "Probabilidade (%)", "Status"
            ]],
            use_container_width=True,
            height=400
        )


# --- 4) Layout principal
st.title("🏋️ Força Local – Dashboard de Gestão")
menu = ["🏠 Home", "📊 Visão Geral",  "🚨 Alto Risco", "👥 Lista de Alunos"]
op = st.sidebar.selectbox("Navegar", menu)

if op == "🏠 Home":
    st.write("Bem-vindo(a)! Use o menu à esquerda para explorar o dashboard.")
elif op == "📊 Visão Geral":
    visao_geral()
elif op == "🚨 Alto Risco":
    alunos_alto_risco()
else:
    lista_alunos()
