Configuração da API Key (Colab Secret)

Crie o Secret no Colab:

GEMINI_API_KEY

⚠️ Para usar Gemini API é necessário Billing vinculado no Google Cloud.

📂 Arquivos

SDW2025_clean.csv → base com UserID

mensagens_IA_gemini.csv → mensagens geradas (Fase 2)

check_envio_news.csv → validação do envio (Fase 3.1)

sdw2025.db → banco local (SQLite) versionado para facilitar testes

🧠 Etapas do ETL
✅ Fase 1 — Extract

Busca os usuários na API:

GET /users/{id}

✅ Fase 2 — Transform (Gemini)

Modelo utilizado:

models/gemini-2.0-flash


Regras:

até 100 caracteres

pt-BR

até 1 emoji

sem prometer ganhos

✅ Fase 3 — Load

Envia as mensagens:

POST /users/{id}/news


Payload:

{ "description": "mensagem..." }

✅ Fase 3.1 — Check (Validação)

Confirma que todos os usuários receberam news.

Resultado esperado:

OK: 100 | SEM_NEWS: 0 | ERROS: 0

▶️ Execução

Execute as células no Colab na ordem:

Fase 1 — Extract

Fase 2 — Transform

Fase 3 — Load

Fase 3.1 — Check (opcional)

🖥️ Como rodar a API localmente (opcional)

Abra a pasta do projeto sdw2025-api

Instale as dependências:

pip install -r requirements.txt


Inicie a API:

python main.py


(Opcional) Exponha com ngrok para usar no Colab:

ngrok http 8000

🔒 Dados

Os dados utilizados neste projeto são fictícios e usados apenas para fins educacionais.

O arquivo sdw2025.db está versionado apenas para facilitar testes locais e também contém dados fictícios.

👩‍💻 Autora

Juliane Vaz
