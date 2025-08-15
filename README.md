# Projeto: DataBot – Agente Inteligente para Análise e Resumo de Dados Públicos

## Objetivo
Criar um agente inteligente capaz de:
1. Buscar dados de uma API pública (ex.: dados climáticos, financeiros ou de saúde).
2. Fazer limpeza e análise estatística básica.
3. Gerar insights e previsões usando modelos de Machine Learning.
4. Resumir os resultados em linguagem natural (NLP).
5. Responder a perguntas do usuário sobre os dados, no estilo chatbot.

## Arquitetura
**Fluxo Geral:**
1. **Extração de Dados** – API pública (ex.: OpenWeather, IBGE, CoinGecko).
2. **Processamento** – Pandas + Python.
3. **Machine Learning** – Scikit-learn (previsões, regressão ou classificação).
4. **NLP** – OpenAI API, spaCy ou Transformers para gerar resumo automático.
5. **Agente Inteligente** – Frameworks como LangChain ou LlamaIndex para integrar busca, análise e respostas.
6. **Interface** – Streamlit ou Flask para interação web.

## Exemplo de Uso
- O usuário pergunta:  
  *"Qual foi a temperatura média dos últimos 7 dias e qual a previsão para amanhã?"*  
- O agente:
  - Busca os dados climáticos históricos e de previsão.
  - Calcula a média.
  - Usa modelo de previsão de séries temporais (ex.: Prophet).
  - Responde em texto claro:  
    *"A temperatura média foi de 27,3°C e a previsão para amanhã é 28°C com 20% de chance de chuva."*

## Tecnologias
- **Linguagem:** Python
- **Coleta de Dados:** `requests`, `pandas`
- **Análise & ML:** `scikit-learn`, `prophet`, `numpy`
- **NLP & Agentes:** `langchain`, `transformers`, `openai` (opcional)
- **Visualização:** `matplotlib`, `plotly`, `streamlit`
- **Armazenamento:** SQLite ou PostgreSQL

---

## Instalação e Execução

### Requisitos
- Python 3.10+
- Windows, macOS ou Linux

### Passos
1. Crie e ative um ambiente virtual:
   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Executar o App Web (Streamlit)
```bash
streamlit run app.py
```

### Executar o Script de Demonstração
```bash
python scripts/demo_pipeline.py
```

## Estrutura de Pastas
```
.
├─ databot/
│  ├─ agent/
│  │  └─ orchestrator.py
│  ├─ data/
│  │  ├─ extract.py
│  │  └─ transform.py
│  ├─ ml/
│  │  └─ model.py
│  ├─ nlp/
│  │  └─ summarize.py
│  ├─ utils/
│  │  └─ logging.py
│  ├─ __init__.py
│  └─ config.py
├─ scripts/
│  └─ demo_pipeline.py
├─ app.py
├─ requirements.txt
├─ README.md
└─ prompt_databot.md
```

## Roadmap (Passo a Passo)
- [x] Criar estrutura modular do projeto
- [x] Implementar extração via Open-Meteo
- [x] Processar e enriquecer dados (features básicas)
- [x] Treinar modelo simples de regressão (RandomForest)
- [x] Sumarizador simples em PT-BR
- [x] App Streamlit com perguntas ao agente
- [ ] Adicionar cache/DB (SQLite) para histórico local
- [ ] Permitir múltiplas fontes (ex.: IBGE, CoinGecko)
- [ ] Substituir/alternar para modelos de séries temporais dedicados (Prophet/ARIMA)
- [ ] Integrar LLM opcional (OpenAI) para respostas mais ricas

## Observações
- O projeto usa Open-Meteo por não exigir chave de API.
- O modelo é educativo e leve para rodar localmente. Para produção, avalie tuning, validação por séries temporais e robustez.
