# 🏋️‍♀️ FitIA – Previsão de Cancelamentos na Academia

Este projeto tem como objetivo prever o risco de cancelamento de alunos de uma academia, utilizando dados reais e técnicas de Inteligência Artificial.

## 🎯 Objetivo
Desenvolver uma solução inteligente para auxiliar a gestão da academia na identificação precoce de alunos com risco de cancelamento. A partir disso, ações preventivas podem ser tomadas, reduzindo a evasão.

## 📊 Como Funciona
- Utilizamos uma base com **500 alunos** contendo dados sobre idade, plano, forma de pagamento e histórico de pagamentos mês a mês.
- Criamos variáveis estratégicas:
- O modelo de IA utilizado foi o **Random Forest**, treinado com alunos ativos e cancelados.
- O modelo alcançou uma **acurácia de até 96%** na base balanceada.

## ⚙️ Tecnologias Utilizadas
- `Python`
- `pandas`, `scikit-learn`, `joblib`
- `Streamlit` para dashboard
- `Figma` para prototipação do app
- `Plotly` para gráficos interativos

## 💻 Acesso ao Projeto

- 🔗 [Acessar o Dashboard](https://gym-dashboard-gyyufifvmbkddrxhv6pjfd.streamlit.app/)
- 📱 [Visualizar o App no Figma](https://www.figma.com/design/1HyXdFnBQrRdHKzydqqX0h/FitIA?node-id=0-1&t=EfjHyR3E5HM3ntLX-1)
- 👩‍💻 [Código Fonte no GitHub](https://github.com/isabellaoliveira11/gym-dashboard)

## 🧠 Diferenciais
- Dashboard completo com filtros por risco, status, plano e nome do aluno.
- Relatórios por mês e estação do ano.
- Prototipação de app com sistema de **registro de frequência**, que futuramente será integrado à IA para **refinar as previsões**.

## 📌 Resultado
A solução entrega:
- Análise individual do risco de cancelamento de cada aluno;
- Lista dos alunos com risco crítico (≥70%);
- Visualização gerencial por mês, plano, idade, gênero e estação do ano;
- Um app complementar para manter o hábito dos alunos e enriquecer os dados.

---

> Este projeto foi desenvolvido como entrega final do hackathon/desafio proposto, com foco em impacto real e usabilidade para a gestão da academia.
