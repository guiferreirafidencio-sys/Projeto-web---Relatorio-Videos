import os
import time
import threading
from dotenv import load_dotenv

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

import yt_dlp
import google.generativeai as genai

load_dotenv()

status = ""
resultado_final = None

# 🔑 APIs
api_keys = [
    os.getenv("api_1"),
    os.getenv("api_2"),
    os.getenv("api_3"),
    os.getenv("api_4")
]

prompt = """
Pegue o texto abaixo e:

1. Corrija português
2. Mantenha contexto
3. Organize como relatório
4. Destaque pontos importantes
5. Use tópicos

Texto:
"""

# =========================
# 📥 BAIXAR ÁUDIO
# =========================
def baixar_audio(url):
    global status
    status = "🔄 Baixando áudio..."

    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.mp3',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])


# =========================
# 🎧 TRANSCRIÇÃO (WHISPER SAFE)
# =========================
def transcrever():
    global status
    status = "🎧 Transcrevendo..."

    try:
        import whisper
    except ImportError:
        raise Exception("Whisper não instalado. Rode: pip install openai-whisper")

    model = whisper.load_model("tiny")
    result = model.transcribe("audio.mp3")

    return result["text"]


# =========================
# 🧠 RESUMO IA
# =========================
def gerar_resumo(texto):
    global status
    status = "🧠 Gerando resumo..."

    for i, key in enumerate(api_keys):
        try:
            if not key:
                continue

            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt + texto)

            return response.text

        except Exception as e:
            erro = str(e)
            print(f"API {i+1} falhou: {erro}")

            time.sleep(1)
            continue

    raise Exception("Todas as APIs falharam")


# =========================
# 📄 GERAR DOC
# =========================
def gerar_doc(url, resumo):
    global status
    status = "📄 Gerando documento..."

    nome_docx = "relatorio.docx"

    doc = Document()

    titulo = doc.add_heading("Relatório do Vídeo", 0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(url)

    doc.add_heading("Resumo", 1)

    for linha in resumo.split("\n"):
        if linha.strip():
            p = doc.add_paragraph(linha)

            if linha.startswith("#"):
                run = p.runs[0]
                run.bold = True
                run.font.size = Pt(14)

    doc.save(nome_docx)

    return nome_docx


# =========================
# 🔥 PROCESSO PRINCIPAL
# =========================
def processar(url):
    global status, resultado_final

    try:
        status = "🚀 Iniciando..."

        baixar_audio(url)
        texto = transcrever()
        resumo = gerar_resumo(texto)
        arquivo = gerar_doc(url, resumo)

        resultado_final = resumo
        status = "✅ Finalizado"

        return arquivo

    except Exception as e:
        print("ERRO:", e)
        status = "❌ Erro no processamento"
        return None


# =========================
# 🚀 THREAD
# =========================
def iniciar_processamento(url):
    if not url:
        return "URL inválida"

    thread = threading.Thread(target=processar, args=(url,))
    thread.daemon = True
    thread.start()

    return "Processo iniciado"


# =========================
# 📡 STATUS
# =========================
def get_status():
    return status