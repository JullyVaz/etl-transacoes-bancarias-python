# Santander 2025 - Ciência de Dados com Python | ETL com Gemini + API

Pipeline **ETL (Extract → Transform → Load)** desenvolvido em **Python** no **Google Colab**, utilizando **Gemini** para gerar mensagens personalizadas e envio via **API REST**.

## Principais Tecnologias
- **Python**
- **Google Colab**
- **Pandas**
- **Requests**
- **Gemini API (google-genai)**
- **Ngrok**

## Notebook (Google Colab)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16DYTeur-w3VmQ3pomeu7jtNKI4hdXxYq?usp=sharing)

Link direto:  
https://colab.research.google.com/drive/16DYTeur-w3VmQ3pomeu7jtNKI4hdXxYq?usp=sharing

## Instalação (Google Colab)
```bash
pip install -U google-genai pandas requests

Configuração da Gemini API (Secret no Colab)

Criar o Secret:

GEMINI_API_KEY

IMPORTANTE: Para usar a Gemini API é necessário que o projeto esteja com Billing vinculado no Google Cloud.

Arquivos Gerados

mensagens_IA_gemini.csv: saída da Fase 2 (Transform) com mensagens geradas pela IA

load_envio_news.csv: saída da Fase 3 (Load) com log do envio (Status/HTTP por usuário)

check_envio_news.csv: saída da Fase 3.1 (Check) com validação final (quantidade de news por usuário)

sdw2025.db: banco local (SQLite) versionado para facilitar testes

Etapas do ETL
Fase 1: Extract

Lê o arquivo SDW2025_clean.csv

Busca os usuários na API:

GET /users/{id}

Fase 2: Transform (Gemini)

Gera mensagens personalizadas com o modelo:

models/gemini-2.0-flash


Regras:

máximo 100 caracteres

português BR

até 1 emoji

sem prometer ganhos garantidos

personalização com nome, cidade, saldo e limite do cartão

Saída:

mensagens_IA_gemini.csv

Fase 3: Load (API)

Envia as mensagens para a API:

POST /users/{id}/news


Payload:

{ "description": "mensagem..." }


Saída:

load_envio_news.csv

Fase 3.1: Check (Validação)

Verifica se todos os usuários receberam news consultando:

GET /users/{id}


Saída:

check_envio_news.csv

Como executar

Execute as células no Colab na ordem:

Fase 1: Extract

Fase 2: Transform (Gemini)

Fase 3: Load

Fase 3.1: Check (opcional, recomendado)

Como rodar a API localmente (opcional)

Abra a pasta sdw2025-api

Instale as dependências:

pip install -r requirements.txt


Inicie a API:

python main.py


(Opcional) Exponha com ngrok:

ngrok http 8000

Dados

Os dados utilizados neste projeto são fictícios e usados apenas para fins educacionais.

Autora

Juliane Vaz
