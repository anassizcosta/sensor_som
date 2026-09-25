-- Execute no Neon se ainda não tiver criado as tabelas.

CREATE TABLE IF NOT EXISTS locais (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS dispositivos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    local_id INTEGER NOT NULL,
    topico_mqtt VARCHAR(150) NOT NULL,

    FOREIGN KEY (local_id) REFERENCES locais(id)
);

CREATE TABLE IF NOT EXISTS ocorrencias (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) NOT NULL DEFAULT 'DETECTADA',

    FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
);

-- Dados iniciais para o projeto.

INSERT INTO locais (nome, descricao)
SELECT 'Sala 01', 'Local monitorado pelo sensor PIR'
WHERE NOT EXISTS (
    SELECT 1 FROM locais WHERE nome = 'Sala 01'
);

INSERT INTO dispositivos (nome, local_id, topico_mqtt)
SELECT
    'ESP32-01',
    id,
    'sensor/movimento'
FROM locais
WHERE nome = 'Sala 01'
AND NOT EXISTS (
    SELECT 1 FROM dispositivos WHERE nome = 'ESP32-01'
);
