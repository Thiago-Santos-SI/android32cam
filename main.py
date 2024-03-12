import cv2
import socket
import struct

# Configuração do endereço IP e porta do servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Inicializa a captura da webcam (0 geralmente se refere à webcam padrão)
cap = cv2.VideoCapture(0)

# Configura a resolução da webcam (opcional, dependendo da sua webcam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível capturar o frame.")
        break

    # Codificação do frame para JPEG
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])

    # Prepara e envia o frame
    header = struct.pack('I', frame_id)
    message = header + buffer.tobytes()

    try:
        sock.sendto(message, (SERVER_IP, SERVER_PORT))
    except OSError as e:
        print(f"Erro ao enviar frame: {e}")
        # Você pode adicionar aqui um controle de fluxo ou uma pausa se necessário

    frame_id += 1

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
sock.close()
