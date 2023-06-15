import os
import shutil
import time

import cv2 as cv
import numpy as np
from dotenv import load_dotenv
from sanic import Blueprint, Request
from sanic.response import json
from supabase import create_client

# Carregando as variáveis de ambiente
load_dotenv()

# Definindo o blueprint das rotas de vídeo
video = Blueprint('video', __name__)

# Carregando as credenciais do Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


# Rota que criará uma pasta responsável por armazenará as imagens capturadas pelo usuário
@video.get("/create_video")
async def create_video(request: Request) -> json:
    # Lista o nome de todos os diretórios e arquivos que existem na pasta
    names = os.listdir("./assets/videos")
    # Remove os arquivos da lista que não seguem o padrão de pastas de vídeo
    for name in names:
        if name[0] != "v":
            names.remove(name)
    # Realizo uma sequência de verificações para saber qual será o número da pasta que será criada para evitar conflitos
    last_number = 0
    if len(names) > 0:
        last_name = names[-1]
        if last_name[5] == " ":
            last_number = last_name[-2] + last_name[-1]
            last_number = int(last_number)
            new_number = last_number + 1
        else:
            last_number = last_name[-1]
            last_number = int(last_number)
            new_number = last_number + 1
    else:
        new_number = last_number + 1

    # Criação da pasta com o nome apropriado
    sequence_dir = os.path.join("./assets/videos", f"video {new_number}")
    os.makedirs(sequence_dir, exist_ok=True)

    return json({"status": "success"})


# Rota que armazenará as imagens capturadas pelo usuário
@video.post("/video_upload")
async def video_upload(request: Request) -> json:
    # Pego a imagem enviada pelo usuário e a transformo em um array de bytes
    image_bytes = request.files.get('image')[1]
    nparr = np.fromstring(image_bytes, np.uint8)
    # Transformo o array de bytes em uma imagem com o OpenCV
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    # Armazeno as imagens sempre na pasta de vídeo mais recente, então pego o nome da pasta mais recente e removo qualquer arquivo que não siga o padrão de imagens
    names = sorted(os.listdir("./assets/videos"))

    for name in names:
        if name[0] != "v":
            names.remove(name)

    last_folder = names[-1]
    sequence_dir = os.path.join("./assets/videos", last_folder)

    # Salvo a imagem com o timestamp atual para evitar conflitos de nomes
    timestamp = int(time.time() * 1000)
    image_file_path = os.path.join(sequence_dir, f"{timestamp}.jpg")

    cv.imwrite(image_file_path, img)

    return json({"status": "success"})


# Rotas que criará o vídeo e o armazenará no Supabase
@video.get("/finish_video")
async def finish_video(request: Request) -> json:
    # Como estou estou armazenando os frames na pasta mais recente, pego o nome da pasta mais recente
    names = sorted(os.listdir("./assets/videos"))
    last_folder = names[-1]
    sequence_dir = os.path.join("./assets/videos", last_folder)

    # Crio um objeto de vídeo com o OpenCV e já informo o codec, o fps, o resolução do vídeo e o caminho onde o vídeo será salvo
    video_path = os.path.join(sequence_dir, 'video.mp4')
    out = cv.VideoWriter(video_path, cv.VideoWriter_fourcc(*'mp4v'), 27, (1280, 720))

    # Pego cada frame da pasta e escrevo no vídeo
    for frame_name in sorted(os.listdir(sequence_dir)):
        frame_path = os.path.join(sequence_dir, frame_name)
        if frame_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            frame = cv.imread(frame_path)
            out.write(frame)

    # Fechando o objeto de vídeo
    out.release()

    # Apago todos os frames pois eles já foram salvos no vídeo
    for frame_name in sorted(os.listdir(sequence_dir)):
        frame_path = os.path.join(sequence_dir, frame_name)
        if frame_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            os.remove(frame_path)

    # Crio um cliente do Supabase e faço o upload do vídeo
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    timestamp = int(time.time() * 1000)
    res = supabase.storage.from_(BUCKET_NAME).upload(f"video-{timestamp}.mp4", video_path)

    # Verifico se o upload foi bem sucedido
    if res.url is None:
        return json({"status": "error"}, 500)

    # Apago a pasta dos frames
    shutil.rmtree(sequence_dir)

    return json({"status": "success", "video url": res.url})
