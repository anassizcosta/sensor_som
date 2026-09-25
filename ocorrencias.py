from .conexao import conectar_banco

def salvar_ocorrencia (tipo="movimento"):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        comando = """
            INSERT INTO ocorrencias
            (tipo, status)
            VALUES (%s, %s)
            RETURNING id, tipo, data_hora, status
        """

        cursor.execute(
            comando,
            (tipo, "DETECTADA")
        )

        resultado = cursor.fetchone()

        conexao.commit()

        return {
            "id": resultado[0],
            "tipo": resultado[1],
            "data_hora": resultado[2].isoformat(),
            "status": resultado[3]
        }

    finally:
        cursor.close()
        conexao.close()


def buscar_ocorrencias():
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        comando = """
            SELECT
                id,
                tipo,
                data_hora,
                status
            FROM ocorrencias
            ORDER BY data_hora ASC
        """

        cursor.execute(comando)

        resultados = cursor.fetchall()

        ocorrencias = []

        for linha in resultados:
            ocorrencias.append({
                "id": linha[0],
                "tipo": linha[1],
                "data_hora": linha[2].isoformat(),
                "status": linha[3]
            })

        return ocorrencias

    finally:
        cursor.close()
        conexao.close()
