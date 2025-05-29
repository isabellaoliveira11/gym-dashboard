
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Carregar os dados
df_raw = pd.read_csv("teste3.csv")
df_raw['Data de Matrícula'] = pd.to_datetime(df_raw['Data de Matrícula'], errors='coerce')
df_raw = df_raw.fillna(-1)

# 2. Remover colunas que vazam informação
colunas_vazar = ['Data de Cancelamento', 'Mês do Cancelamento', 'Estação do Cancelamento', 'Motivo do Cancelamento']
df_raw.drop(columns=[c for c in colunas_vazar if c in df_raw.columns], inplace=True)

# 3. One-hot encoding
df = pd.get_dummies(df_raw.copy(), columns=['Gênero', 'Plano', 'Meio de Pagamento'], dummy_na=False)

# 4. Features derivadas
# ❄️ Manter só os meses de inverno e dezembro
meses = ['2023-06', '2023-07', '2023-08', '2023-12']

# Se houver outras colunas de mês, remove do DataFrame
todos_os_meses = [c for c in df.columns if c.startswith('2023-')]
meses_remover = [c for c in todos_os_meses if c not in meses]
df.drop(columns=meses_remover, inplace=True)

# Total de Pagamentos e % de meses pagos com base apenas nos meses escolhidos
df['Total de Pagamentos'] = df[meses].sum(axis=1)
df['Pct_Meses_Pagos'] = df.apply(
    lambda row: row['Total de Pagamentos'] / row['Tempo de Permanência (meses)']
    if row['Tempo de Permanência (meses)'] > 0 else 0, axis=1
)

# 5. Separar features e target
target = 'Status de Cancelamento'
features = [c for c in df.columns if c not in ['ID Aluno', 'Nome', target, 'Data de Matrícula']]

# 6. Rebalancear treino — amostragem equilibrada
df['cancelou'] = df[target]
positivos = df[df['cancelou'] == 1]
negativos = df[df['cancelou'] == 0].sample(n=len(positivos), random_state=42)
df_balanceado = pd.concat([positivos, negativos])

X_train = df_balanceado[features]
y_train = df_balanceado[target]

# 7. Treinamento
modelo_rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
modelo_rf.fit(X_train, y_train)

# 8. Avaliação
y_pred = modelo_rf.predict(X_train)
print(f"Acurácia (no treino balanceado): {accuracy_score(y_train, y_pred):.2f}")
print(classification_report(y_train, y_pred))
print(confusion_matrix(y_train, y_pred))

# 9. Importância das features
feat_imp = pd.Series(modelo_rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
print("\nImportância das Features:\n", feat_imp)

# 10. Salvar modelo
joblib.dump(modelo_rf, 'modelo_rf.pkl')
print("✅ Modelo salvo em 'modelo_rf.pkl'")

# 11. Prever para todos os alunos
X_all = df[features]
df_raw["Previsão de Cancelamento"] = modelo_rf.predict(X_all)
df_raw["Probabilidade de Cancelamento"] = modelo_rf.predict_proba(X_all)[:, 1]
df_raw["Probabilidade (%)"] = (df_raw["Probabilidade de Cancelamento"] * 100).round(2).astype(str) + " %"

# 12. Exportar
df_raw.to_csv("academia_cancelamento_com_previsoes.csv", index=False, encoding="utf-8-sig")
print("✅ Planilha com previsões salva em 'academia_cancelamento_com_previsoes.csv'")

# 13. Top 10 alunos ativos com maior risco
print("\n🚨 Top 10 Alunos Ativos com Maior Risco de Cancelamento:")
top10_ativos = df_raw[df_raw["Status de Cancelamento"] == 0].copy()
top10_ativos = top10_ativos.sort_values("Probabilidade de Cancelamento", ascending=False).head(10)
print(top10_ativos[[
    "ID Aluno", "Nome", "Plano", "Meio de Pagamento",
    "Total de Pagamentos", "Tempo de Permanência (meses)", "Probabilidade (%)"
]])
