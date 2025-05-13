import os

import os
from tqdm import tqdm

def count_imgs(diretorio):
    extensoes_imagens = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
    total_imagens = 0
    arquivos = []

    # Coletar todos os arquivos no diretório
    for root, _, files in os.walk(diretorio):
        arquivos.extend(os.path.join(root, file) for file in files)

    # Contar imagens com barra de progresso
    with tqdm(total=len(arquivos), desc="Contando imagens", unit="file") as pbar:
        for file in arquivos:
            if os.path.splitext(file)[1].lower() in extensoes_imagens:
                total_imagens += 1
            pbar.update(1)
    
    return total_imagens
