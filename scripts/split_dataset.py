import os
import shutil
import yaml
import sys
from tqdm import tqdm

def load_split_config(config_path):
    """
    Carrega a configuração de divisão de dados a partir de um arquivo YAML ou TXT.
    """
    if config_path.endswith(".yaml") or config_path.endswith(".yml"):
        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    elif config_path.endswith(".txt"):
        split_config = {"train": [], "val": [], "test": []}
        current_section = None
        with open(config_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line.lower() in ("train:", "val:", "test:"):
                    current_section = line.lower().replace(":", "")
                elif current_section and line:
                    split_config[current_section].append(line)
        return split_config
    else:
        raise ValueError("Formato de arquivo não suportado. Use .yaml ou .txt")

def split_dataset(dataset_path, output_path, config_path):
    """
    Divide um dataset em conjuntos de treino, validação e teste com base em substrings definidas em um arquivo de configuração.
    """
    # Carregar configuração
    split_config = load_split_config(config_path)
    
    # Criar diretórios de saída
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_path, subset), exist_ok=True)
    
    # Obter todas as classes e arquivos
    all_files = []
    for class_name in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_path):
            for file in os.listdir(class_path):
                if os.path.isfile(os.path.join(class_path, file)):
                    all_files.append((class_name, file))
    
    total_files = len(all_files)
    
    # Processar arquivos com barra de progresso
    with tqdm(total=total_files, desc="Processando arquivos", unit="file") as pbar:
        for class_name, file in all_files:
            class_path = os.path.join(dataset_path, class_name)
            file_path = os.path.join(class_path, file)
            destination = None
            
            for subset, substrings in split_config.items():
                if any(substring in file for substring in substrings):
                    destination = os.path.join(output_path, subset, class_name, file)
                    os.makedirs(os.path.join(output_path, subset, class_name), exist_ok=True)
                    break
            
            # Se encontrou um destino, copiar o arquivo
            if destination:
                shutil.copy(file_path, destination)
            
            pbar.update(1)
    
    print(f"Dataset dividido e salvo em: {output_path}")
