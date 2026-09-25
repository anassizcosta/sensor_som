#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include "conexao.h"

const int sensor = 4;
const int ledVermelho = 25;
const int ledVerde = 26;
const int buzzer = 27;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long ultimaTentativaMQTT = 0;
const unsigned long intervaloTentativaMQTT = 5000;


unsigned long fimDoAlerta = 0;
const unsigned long tempoBloqueio = 5000;

void conectarWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Conectando ao Wi-Fi");

  unsigned long inicio = millis();

  while (WiFi.status() != WL_CONNECTED && millis() - inicio < 20000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi Conectado!");
  } else {
    Serial.println("\nWi-Fi falhou!");
  }
}

void conectarMQTT() {
  if (client.connected()) {
    return;
  }

  if (millis() - ultimaTentativaMQTT < intervaloTentativaMQTT &&
      ultimaTentativaMQTT != 0) {
    return;
  }

  ultimaTentativaMQTT = millis();

  String clientId = "ESP32-Fisico-" + String(random(0xffff), HEX);

  Serial.print("Conectando ao MQTT...");

  if (client.connect(clientId.c_str())) {
    Serial.println("\nConectado ao MQTT com sucesso!");
  } else {
    Serial.print("Falha no MQTT, codigo de erro: ");
    Serial.println(client.state());
  }
}

bool enviarMovimentoViaHTTP() {
  WiFiClient clientHttp;
  HTTPClient http;

  String url = "http://" + String(API_HOST) + ":" + String(API_PORT) + "/api/movimento";

  String payload = "{\"tipo\": \"movimento\"}";

  Serial.print("Tentando envio HTTP para: ");
  Serial.println(url);

  if (!http.begin(clientHttp, url)) {
    Serial.println("Falha ao iniciar conexao HTTP.");
    return false;
  }

  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(payload);
  String resposta = http.getString();

  http.end();

  Serial.print("HTTP code: ");
  Serial.println(httpCode);

  Serial.print("Resposta: ");
  Serial.println(resposta);

  return httpCode >= 200 && httpCode < 300;
}

void setup() {
  Serial.begin(115200);

  pinMode(sensor, INPUT);
  pinMode(ledVermelho, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(buzzer, OUTPUT);

  digitalWrite(ledVerde, HIGH);
  digitalWrite(ledVermelho, LOW);
  digitalWrite(buzzer, LOW);

  noTone(buzzer);

  conectarWiFi();

  client.setServer(MQTT_BROKER, MQTT_PORT);
  client.setSocketTimeout(10);
  client.setKeepAlive(30);
}

void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi caiu. Reconectando...");
    conectarWiFi();
  }

  if (client.connected()) {
    client.loop();
  } else {
    conectarMQTT();
  }

  int movimento = digitalRead(sensor);

  
  if (millis() < fimDoAlerta) {
    delay(50);
    return;
  }

  if (movimento == HIGH) {

    Serial.println("MOVIMENTO DETECTADO!");

    bool enviado = false;

    if (client.connected()) {

      enviado = client.publish(
        MQTT_TOPIC,
        "{\"tipo\": \"movimento\"}"
      );

      if (enviado) {
        Serial.println("Mensagem enviada via MQTT!");
      } else {
        Serial.println("Falha no MQTT. Tentando HTTP...");
      }
    }

    if (!enviado) {

      enviado = enviarMovimentoViaHTTP();

      if (enviado) {
        Serial.println("Mensagem enviada via HTTP!");
      } else {
        Serial.println("MQTT e HTTP falharam.");
      }
    }

    
    digitalWrite(ledVerde, LOW);

    
    for (int i = 0; i < 8; i++) {

      digitalWrite(ledVermelho, HIGH);
      tone(buzzer, 1000);

      delay(250);

      digitalWrite(ledVermelho, LOW);
      noTone(buzzer);

      delay(250);

      if (client.connected()) {
        client.loop();
      }
    }

    
    noTone(buzzer);
    digitalWrite(buzzer, LOW);
    digitalWrite(ledVermelho, LOW);

    digitalWrite(ledVerde, HIGH);

    Serial.println("Alerta finalizado.");
    Serial.println("Sistema voltou ao normal.");

    fimDoAlerta = millis() + tempoBloqueio;

    Serial.println("Sensor temporariamente bloqueado.");
  }

  delay(50);
}