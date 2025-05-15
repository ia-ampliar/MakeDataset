import os
import random
import imgaug.augmenters as iaa
import cv2
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# Configurações globais
AVAILABLE_AUGMENTERS = {
    "flip": iaa.Fliplr(0.5),
    "flip_v": iaa.Flipud(0.5),
    "rotate_90": iaa.Rot90((1, 3)),
    "crop": iaa.Crop(percent=(0, 0.2)),
    "rotation": iaa.Affine(rotate=(-15, 15)),
    "shear": iaa.Affine(shear=(-10, 10))
}

def apply_augmentations(args):
    img_path, output_folder, operations, factor = args
    
    try:
        image = cv2.imread(img_path)
        if image is None:
            print(f"Erro ao carregar imagem: {img_path}")
            return

        img_name = os.path.basename(img_path)

        for i in range(factor):
            selected_ops = random.sample(operations, 2)
            augmenter_seq = iaa.Sequential([AVAILABLE_AUGMENTERS[op] for op in selected_ops])
            augmented_img = augmenter_seq(image=image)

            ops_str = '_'.join(selected_ops)
            base_name, ext = os.path.splitext(img_name)
            new_name = f"aug_{i}_{ops_str}_{base_name}{ext}"
            output_path = os.path.join(output_folder, new_name)

            if not os.path.exists(output_path):
                success = cv2.imwrite(output_path, augmented_img)
                if not success:
                    print(f"Falha ao salvar: {output_path}")
    except Exception as e:
        print(f"Erro ao processar {img_path}: {str(e)}")

def augment_dataset(input_dir, operations, factor=2, num_processes=None):
    input_dir = os.path.abspath(input_dir)
    valid_operations = [op for op in operations if op in AVAILABLE_AUGMENTERS]
    
    if len(valid_operations) < 2:
        raise ValueError("É necessário pelo menos 2 operações válidas")

    if num_processes is None:
        num_processes = max(1, cpu_count() - 1)

    tasks = []

    # Lista imagens diretamente na pasta input_dir
    images = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    for img_name in images:
        img_path = os.path.join(input_dir, img_name)
        tasks.append((img_path, input_dir, valid_operations, factor))

    if num_processes > 1:
        with Pool(processes=num_processes) as pool:
            list(tqdm(pool.imap_unordered(apply_augmentations, tasks), total=len(tasks), desc="Processando imagens"))
    else:
        for task in tqdm(tasks, desc="Processando imagens"):
            apply_augmentations(task)
    print("Aumento de dados concluído.")