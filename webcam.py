import cv2 as cv

#Cria um objeto denominado VideoCapture. 0 corresponde ao índice do dispositivo, geralmente a
#webcam interna, ou primeira webcam
cap = cv.VideoCapture(0) 

while True:
#cap.read() retorna dois valores um booleano (ret) que checa se a leitura teve sucesso
#frame a imagem capturada
    ret, frame = cap.read()
#Interrompe o loop, caso a captura tenha falhado, isto é ret = False
    if not ret:
        break

#Abre uma janela denominada WebCam e mostra o frame cpaturado em cada iteração do loop
    cv.imshow("Webcam", frame)
#Se preciosar q, o loop se encerra

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()