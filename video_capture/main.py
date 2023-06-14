import cv2 as cv
import requests

requests.get('http://localhost:3001/video/create_video')

cap = cv.VideoCapture(0)  # 0 geralmente se refere à webcam principal

while True:
    ret, frame = cap.read()  # Captura um único quadro de vídeo
    if not ret:
        break  # Se não conseguimos capturar um quadro, terminamos o loop

    # Aqui, você pode converter o quadro em um formato que pode ser enviado via POST.
    ret, jpeg = cv.imencode('.jpg', frame)
    if not ret:
        break
    jpeg_bytes = jpeg.tobytes()

    requests.post('http://localhost:3001/video/video_upload',
                  files={'image': ('image.jpg', jpeg_bytes, 'image/jpeg')})

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
requests.get('http://localhost:3001/video/finish_video')

