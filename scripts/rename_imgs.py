import os
import shutil
import sys
import concurrent.futures

def organize_and_move_images(input_file):
    """
    Organiza e renomeia imagens com base no nome da pasta anterior,
    movendo as imagens para as pastas 'CIN' ou 'MSI' com base no rótulo.

    :param input_file: Caminho para o arquivo contendo a lista de pastas e seus rótulos.
    """
    current_dir = os.getcwd()

    # Criar as pastas principais CIN e MSI, se não existirem
    cin_folder = os.path.join(current_dir, 'CIN')
    msi_folder = os.path.join(current_dir, 'MSI')
    os.makedirs(cin_folder, exist_ok=True)
    os.makedirs(msi_folder, exist_ok=True)

    try:
        with open(input_file, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o arquivo {input_file}: {e}")
        return

    def process_line(line):
        try:
            # Dividir linha no formato 'caminho_da_pasta, rótulo'
            folder_path, label = line.split(',')
            folder_path = folder_path.strip()
            label = label.strip()

            # Verificar se o rótulo é válido
            if label not in ['CIN', 'MSI']:
                print(f"[ERRO] Rótulo inválido para a pasta {folder_path}: {label}")
                return

            # Verificar se a pasta existe
            if not os.path.isdir(folder_path):
                print(f"[ERRO] Pasta não encontrada: {folder_path}")
                return

            # Determinar a pasta de destino com base no rótulo
            destination_folder = cin_folder if label == 'CIN' else msi_folder

            # Iterar sobre as subpastas e arquivos dentro da pasta principal
            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)

                    # Verificar se é um arquivo
                    if not os.path.isfile(file_path):
                        continue

                    # Determinar o nome da pasta anterior (pasta principal)
                    parent_folder_name = os.path.basename(folder_path)

                    # Renomear o arquivo com o nome da pasta anterior
                    file_name_without_ext, file_ext = os.path.splitext(file_name)
                    new_file_name = f"{parent_folder_name}_{file_name_without_ext}{file_ext}"

                    # Novo caminho para a imagem dentro da pasta de destino
                    new_file_path = os.path.join(destination_folder, new_file_name)

                    # Verificar se a imagem já foi gerada
                    if os.path.exists(new_file_path):
                        print(f"[INFO] Imagem já existe: {new_file_path}")
                        continue

                    # Mover e renomear a imagem
                    shutil.move(file_path, new_file_path)
                    print(f"[INFO] Movido e renomeado: {file_path} -> {new_file_path}")

        except Exception as e:
            print(f"[ERRO] Falha ao processar a linha: '{line}': {e}")

    # Usar ThreadPoolExecutor para processar as linhas em paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_line, lines)

