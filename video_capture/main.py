import cv2 as cv
import requests

# Realizo uma requisição para a rota que criará a pasta responsável por armazenará as imagens capturadas
requests.get('http://localhost:3001/video/create_video')

# Inicializo a captura de vídeo através da webcam standard do computador
cap = cv.VideoCapture(0)

# Loop para ficar capturando o vídeo até que o usuário aperte a tecla 'q'
while True:
    ret, frame = cap.read()  # Captura um único quadro do vídeo
    if not ret:
        break  # Se não conseguimos capturar um quadro, terminamos o loop

    # Convertemos o quadro em um formato que pode ser enviado via POST.
    ret, jpeg = cv.imencode('.jpg', frame)
    if not ret:
        break
    jpeg_bytes = jpeg.tobytes()

    # Realizo uma requisição para a rota que armazenará as imagens capturadas pelo usuário
    requests.post('http://localhost:3001/video/video_upload',
                  files={'image': ('image.jpg', jpeg_bytes, 'image/jpeg')})

    # Exibimos o quadro capturado para o usuário
    cv.imshow('frame', frame)
    # Se o usuário apertar a tecla 'q', terminamos o loop e encerramos a captura de vídeo
    if cv.waitKey(1) == ord('q'):
        break

# Encerramos a captura de vídeo e fechamos todas as janelas abertas que estavam exibindo o vídeo e realizamos a requisição para a rota que finalizará o processo de upload do vídeo
cap.release()
cv.destroyAllWindows()
requests.get('http://localhost:3001/video/finish_video')

