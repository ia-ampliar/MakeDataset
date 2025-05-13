import staintools
from pathlib import Path
import re
import os
import cv2 as cv
import multiprocessing
import numpy as np

def create_new_folder(_patient_path, ori_str, replace_str):
    _new_patient_path = re.sub(ori_str, replace_str, _patient_path)
    Path(_new_patient_path).mkdir(parents=True, exist_ok=True)
    return _new_patient_path

def variance_of_laplacian(image):
    # Converte a imagem para escala de cinza na CPU
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Aplica o Laplacian na CPU
    laplacian = cv.Laplacian(gray, cv.CV_64F)
    # Calcula a variância
    return laplacian.var()

def find_blur(imagePath):
    imagePath = Path(imagePath).resolve()
    # Carrega a imagem na CPU
    image = cv.imread(str(imagePath))

    if image is None:
        print(f"Failed to read image at: {imagePath}")
        return None, 0

    # Calcula o desfoque na CPU
    fm = variance_of_laplacian(image)
    return image, fm

def calculate_background_color_percentage(image):
    # Define os intervalos de cores para branco, azul, cinza, vermelho, verde e preto
    colors = {
        'white': ([200, 200, 200], [255, 255, 255]),
        'blue': ([100, 0, 0], [255, 100, 100]),
        'gray': ([100, 100, 100], [200, 200, 200]),
        'red': ([0, 0, 100], [100, 100, 255]),
        'green': ([0, 100, 0], [100, 255, 100]),
        'black': ([0, 0, 0], [50, 50, 50])
    }

    # Calcula a porcentagem de cada cor no fundo da imagem
    total_pixels = image.shape[0] * image.shape[1]
    color_percentages = {}

    for color, (lower, upper) in colors.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv.inRange(image, lower, upper)
        color_percentages[color] = np.sum(mask == 255) / total_pixels

    return color_percentages

def blur_color_processing(_root, _img_path, _img, _img_path_template, _blur_threshold=1000):
    image, fm = find_blur(_img_path)
    if image is None:
        return fm  # Se a imagem não pôde ser lida, retorna diretamente

    print(f"Processing: {_img_path}, Blur score: {fm}")

    if fm <= _blur_threshold:
        # Não armazenar imagens desfocadas
        print(f"Image is blurred and will not be saved: {_img_path}")
    else:
        # Calcula a porcentagem de cada cor no fundo da imagem
        color_percentages = calculate_background_color_percentage(image)

        # Verifica se a imagem tem mais de 80% de uma das cores no fundo
        for color, percentage in color_percentages.items():
            if percentage > 0.8:
                print(f"Image has more than 80% {color} background and will not be saved: {_img_path}")
                return fm

        # Se a imagem passar no teste de cor, salva a imagem
        _new_img_folder = create_new_folder(_root, "tiling", "tiling_filtered")
        _new_img_path = os.path.join(_new_img_folder, _img)

        # Verifica se a imagem já existe no diretório de destino
        if os.path.exists(_new_img_path):
            print(f"Image already exists, skipping: {_new_img_path}")
            return fm

        try:
            # Salvar a imagem no diretório de destino
            success = cv.imwrite(_new_img_path, image)
            if success:
                print(f"Image saved to: {_new_img_path}")
            else:
                raise IOError(f"Failed to save image at: {_new_img_path}")

        except Exception as e:
            print(f"Error during image processing: {e}")

    return fm

# Caminho relativo ao diretório do projeto
relative_path = r"C:\Users\Fernando Alves\Desktop\ComputerVision\Datasets\Dataset-224x224-tiling\CIN"
project_base = os.getcwd()
# Construir o caminho absoluto
absolute_path = os.path.join(project_base, relative_path)

def pre_processing(extra_prefix="", _img_path_template=absolute_path):
    print("[INFO] Starting blur detection ...")
    cpu_num = multiprocessing.cpu_count()
    print(f"The CPU number of this machine is {cpu_num}")
    pool = multiprocessing.Pool(cpu_num)

    _image_path = "HEAL_Workspace/tiling" + str(extra_prefix)
    for _root, _dir, _imgs in os.walk(_image_path):
        _imgs = [f for f in _imgs if not f[0] == '.']
        _dir[:] = [d for d in _dir if not d[0] == '.']

        for idx in range(len(_imgs)):
            _img = _imgs[idx]
            _img_path = os.path.join(_root, _img)

            # Processamento paralelo com multiprocessing
            pool.apply_async(blur_color_processing, (_root, _img_path, _img, _img_path_template))

    pool.close()
    pool.join()