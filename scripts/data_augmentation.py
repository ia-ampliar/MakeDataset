import os
import random
import imgaug.augmenters as iaa
import cv2
import numpy as np
from tqdm import tqdm

def augment_dataset(input_dir, output_dir, operations, factor=2):
    """
    Aplica data augmentation a um conjunto de imagens e mantém a estrutura de diretórios.
    
    :param input_dir: Caminho do dataset original.
    :param output_dir: Caminho para salvar o novo dataset aumentado.
    :param operations: Lista de operações a serem aplicadas.
    :param factor: Multiplicidade de aumento do dataset.
    """
    augmenters = {
        "flip": iaa.Fliplr(0.5),
        "flip_v": iaa.Flipud(0.5),
        "rotate_90": iaa.Rot90((1, 3)),
        "crop": iaa.Crop(percent=(0, 0.2)),
        "rotation": iaa.Affine(rotate=(-15, 15)),
        "shear": iaa.Affine(shear=(-10, 10))
    }
    
    selected_augmenters = [augmenters[op] for op in operations if op in augmenters]
    augmenter_seq = iaa.Sequential(selected_augmenters)

    # Percorre todas as subpastas (CIN e MSI)
    for subfolder in os.listdir(input_dir):
        subfolder_path = os.path.join(input_dir, subfolder)
        
        if not os.path.isdir(subfolder_path):
            continue  # Ignora arquivos que não sejam diretórios
        
        images = [f for f in os.listdir(subfolder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        output_subfolder = os.path.join(output_dir, subfolder)
        os.makedirs(output_subfolder, exist_ok=True)  # Mantém a estrutura de diretórios

        for img_name in tqdm(images, desc=f"Augmenting {subfolder}"):
            img_path = os.path.join(subfolder_path, img_name)
            image = cv2.imread(img_path)
            if image is None:
                continue  # Ignora imagens corrompidas ou inválidas
            
            for i in range(factor):
                augmented_img = augmenter_seq(image=image)
                new_name = f"aug_{i}_{img_name}"
                cv2.imwrite(os.path.join(output_subfolder, new_name), augmented_img)
