from flask import Flask, render_template, request, jsonify
from mqtt.database.ocorrencias import salvar_ocorrencia, buscar_ocorrencias
import os


app = Flask(
    __name__,
    template_folder="..",      
    static_folder="../src",    
    static_url_path="/src"     
)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/api/movimento", methods=["POST"])
def receber_movimento():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({
                "erro": "Nenhum dado foi enviado."
            }), 400
        
        tipo = dados.get("tipo", "movimento")

        ocorrencia = salvar_ocorrencia(tipo)

        return jsonify({
            "mensagem": "Movimento recebido com sucesso.",
            "ocorrencia": ocorrencia
        }), 201

    except Exception as erro:
        return jsonify({
            "erro": str(erro)
        }), 500

@app.route("/api/ocorrencias", methods=["GET"])
def listar_ocorrencias():
    try:
        ocorrencias = buscar_ocorrencias()

        return jsonify(ocorrencias)

    except Exception as erro:
        return jsonify({
            "erro": str(erro)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)