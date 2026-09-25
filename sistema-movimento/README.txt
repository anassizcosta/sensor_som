SISTEMA IoT DE DETECÇÃO DE MOVIMENTO

ESTRUTURA

app.py
database/
mqtt/
static/
templates/
tests/

PRIMEIRO PASSO

1. Crie um ambiente virtual:
   python -m venv venv

2. Ative:
   Windows:
   venv\Scripts\activate

3. Instale:
   pip install -r requirements.txt

4. Abra o arquivo .env.

5. Coloque a NOVA string de conexão do Neon em DATABASE_URL.

6. Confirme que as tabelas locais, dispositivos e ocorrencias existem no Neon.

7. Execute:
   python app.py

8. Abra:
   http://127.0.0.1:5000

MQTT

Para iniciar o receptor MQTT:
   python -m mqtt.cliente

O ESP32 deve publicar no tópico:
   sensor/movimento

Exemplo de mensagem:
   {"dispositivo_id": 1, "tipo": "movimento"}

TESTES

Execute:
   pytest

ROTAS

GET /
Página principal.

POST /api/movimento
Recebe dados de movimento.

GET /api/ocorrencias
Retorna as ocorrências do banco em JSON.

IMPORTANTE

O arquivo .env não deve ser enviado para o GitHub.
