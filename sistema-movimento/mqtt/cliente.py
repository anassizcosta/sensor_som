import os
import json
from pathlib import Path
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from database.ocorrencias import salvar_ocorrencia

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORTA = int(os.getenv("MQTT_PORT", "1883"))
TOPICO = os.getenv("MQTT_TOPIC", "sensor/movimento")


def quando_conectar(client, rc):
    if rc == 0:
        print(" MQTT conectado com sucesso ao broker:", BROKER)
        client.subscribe(TOPICO)
        print("Inscrito no tópico:", TOPICO)
    else:
        print(" Erro ao conectar no MQTT. Código de erro:", rc)

def quando_receber(msg):
    try:
        mensagem = msg.payload.decode('utf-8')
        print("cd Mensagem recebida:", mensagem)

        dados = json.loads(mensagem)
        tipo = dados.get("tipo", "movimento")

        salvar_ocorrencia(tipo)
        print("Ocorrência salva no banco de dados com sucesso!")

    except json.JSONDecodeError:
        print("Erro: A mensagem recebida não é um JSON válido.")
    except Exception as erro:
        print("Erro ao processar mensagem MQTT:", type(erro).__name__, "-", erro)


def iniciar_mqtt():
    if hasattr(mqtt, "CallbackAPIVersion"):
        cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    else:
        cliente = mqtt.Client()

    cliente.on_connect = quando_conectar
    cliente.on_message = quando_receber

    print("Tentando conectar ao broker MQTT em:", BROKER)
    cliente.connect(BROKER, PORTA, 60)
    cliente.loop_forever()


if __name__ == "__main__":
    iniciar_mqtt()