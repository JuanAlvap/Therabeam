import cv2
import numpy as np
from clientuploader import Client

#client.upload('nombre del archivo y extension'), despues de tomar la imagen, la subes por medio de este
client = Client()

def tomarFoto():
    camera = cv2.VideoCapture(0)

    state, frame = camera.read()

    print(state)

    cv2.imwrite('captured_image.png', frame)
    camera.release()

    # Convertir la imagen al espacio de color HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # O convertir al espacio de color YCrCb
    ycrcb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Definir el rango de tonos de piel en HSV
    lower_hsv = np.array([0, 30, 60], dtype=np.uint8)
    upper_hsv = np.array([20, 150, 255], dtype=np.uint8)

    # Definir el rango de tonos de piel en YCrCb
    lower_ycrcb = np.array([0, 133, 40], dtype=np.uint8)    ###
    upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)    ###

    # Para HSV
    skin_mask_hsv = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

    # Para YCrCb
    skin_mask_ycrcb = cv2.inRange(ycrcb_image, lower_ycrcb, upper_ycrcb)

    # Aplicar una operación de erosión y luego de dilatación (opening) para reducir el ruido
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask_hsv = cv2.morphologyEx(skin_mask_hsv, cv2.MORPH_OPEN, kernel)
    skin_mask_ycrcb = cv2.morphologyEx(skin_mask_ycrcb, cv2.MORPH_OPEN, kernel)   ###

    # Aplicar la máscara a la imagen original
    skin_hsv = cv2.bitwise_and(frame, frame, mask=skin_mask_hsv)
    skin_ycrcb = cv2.bitwise_and(frame, frame, mask=skin_mask_ycrcb)

    # Convertir la imagen filtrada a escala de grises
    gray_skin_hsv = cv2.cvtColor(skin_hsv, cv2.COLOR_BGR2GRAY)
    gray_skin_ycrcb = cv2.cvtColor(skin_ycrcb, cv2.COLOR_BGR2GRAY)

    # Umbral para binarizar la imagen
    _, thresh_skin_hsv = cv2.threshold(gray_skin_hsv, 0, 255, cv2.THRESH_BINARY)
    _, thresh_skin_ycrcb = cv2.threshold(gray_skin_ycrcb, 0, 255, cv2.THRESH_BINARY)

    # Detectar contornos
    contours_hsv, _ = cv2.findContours(thresh_skin_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_ycrcb, _ = cv2.findContours(thresh_skin_ycrcb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en la imagen original
    # cv2.drawContours(frame, contours_hsv, -1, (0, 255, 0), 3)
    cv2.drawContours(frame, contours_ycrcb, -1, (0, 255, 0), 3)

    # Mostrar la imagen con los contornos
    cv2.imwrite('Skin Contours.png', frame)
    cv2.imshow("Skin Contours", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Generación de coordenadas
    return contours_ycrcb


def generarCoordenadas(contours_ycrcb):
    coordinates = []
    with open("contornos.txt", "w") as File:
        for contour in contours_ycrcb:
            for point in contour:
                x, y = point[0]
                coordinates.append((x, y))
                File.write(f"{x}, {y}" + "\n")

    for coord in coordinates:
        print(coord)
    return coordinates


def pintarCoordenadasEnMatriz(coordinates, shape):
    # Crear una imagen negra (matriz de ceros) del tamaño deseado
    canva = np.zeros(shape[:2], dtype=np.uint8)  # Solo necesitamos 1 canal para la imagen en blanco y negro

    # Convertir la lista de coordenadas a un formato aceptable para fillPoly (numpy array)
    points_array = np.array(coordinates, dtype=np.int32)  # Convertir a numpy y dar la forma correcta

    # Iterar sobre las coordenadas y pintar los puntos en el canva
    cv2.fillPoly(canva, pts=[points_array], color=1)  # Rellenar el contorno con 1 (blanco)

    return canva


contornos = tomarFoto()
shape = (1080, 1920)

# hull = [cv2.convexHull(c) for c in contornos]

matrizBinaria = pintarCoordenadasEnMatriz(generarCoordenadas(contornos), shape)

cv2.imwrite('matriz_puntos.png', matrizBinaria * 255)  # Multiplicar por 255 para que sea visible

cv2.imshow("Matriz Puntos", matrizBinaria * 255)
cv2.waitKey(0)
cv2.destroyAllWindows()



