from flask import Flask, render_template, request, jsonify, send_file
import threading
import os
import resumidor

app = Flask(__name__)

# =========================
# CONTROLE DE PROCESSO
# =========================
processando = False


@app.route('/')
def home():
    return render_template('index.html')


# =========================
# INICIAR PROCESSAMENTO
# =========================
@app.route('/iniciar', methods=['POST'])
def iniciar():
    global processando

    url = request.form.get('video')

    if not url:
        return jsonify({"erro": "URL inválida"}), 400

    if processando:
        return jsonify({"erro": "Já existe um processo rodando"}), 429

    processando = True

    def worker():
        global processando
        try:
            resumidor.processar(url)
        finally:
            processando = False

    threading.Thread(target=worker).start()

    return jsonify({"status": "Processo iniciado"})


# =========================
# STATUS
# =========================
@app.route('/status')
def status():
    return jsonify({
        "processando": processando,
        "status": getattr(resumidor, "status", ""),
        "resultado": getattr(resumidor, "resultado_final", None)
    })


# =========================
# DOWNLOAD PAGE
# =========================
@app.route('/download_page')
def download_page():
    return render_template('pegar.html')


# =========================
# DOWNLOAD PDF
# =========================
@app.route('/download')
def download():
    caminho = "relatorio_video.pdf"

    if not os.path.exists(caminho):
        return jsonify({"erro": "Arquivo ainda não foi gerado"}), 404

    return send_file(caminho, as_attachment=True)


# =========================
# PREVIEW PDF
# =========================
@app.route('/preview')
def preview():
    caminho = "relatorio_video.pdf"

    if not os.path.exists(caminho):
        return jsonify({"erro": "Arquivo ainda não foi gerado"}), 404

    return send_file(caminho, mimetype='application/pdf')


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)