import os
import shutil
import random
def split_dataset(dataset_path, output_path, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1, seed=42):
    """
    Divide um dataset em conjuntos de treino, validação e teste.
    """
    # Checar proporções com tolerância
    if not abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6:
        raise ValueError("As proporções de treino, validação e teste devem somar 1.0.")

    # Garantir reprodutibilidade
    random.seed(seed)

    # Criar diretórios de saída
    train_path = os.path.join(output_path, "train")
    val_path = os.path.join(output_path, "val")
    test_path = os.path.join(output_path, "test")

    for path in [train_path, val_path, test_path]:
        os.makedirs(path, exist_ok=True)

    # Iterar sobre as classes no dataset original
    for class_name in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_name)
        if not os.path.isdir(class_path):
            continue

        # Obter todos os arquivos da classe
        files = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
        random.shuffle(files)

        # Dividir os arquivos
        train_split = int(len(files) * train_ratio)
        val_split = train_split + int(len(files) * val_ratio)

        train_files = files[:train_split]
        val_files = files[train_split:val_split]
        test_files = files[val_split:]

        # Copiar os arquivos para os diretórios correspondentes
        for file_set, target_path in zip([train_files, val_files, test_files], [train_path, val_path, test_path]):
            class_target_path = os.path.join(target_path, class_name)
            os.makedirs(class_target_path, exist_ok=True)

            for file in file_set:
                src = os.path.join(class_path, file)
                dst = os.path.join(class_target_path, file)
                shutil.copy(src, dst)

    print(f"Dataset dividido e salvo em: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Uso: python split_dataset.py <caminho_dataset_original> <caminho_dataset_novo>")
        sys.exit(1)

    # Caminho para o dataset original
    dataset_path = sys.argv[1]

    # Caminho para o novo dataset organizado
    output_path = sys.argv[2]

    # Chamar a função para dividir o dataset
    split_dataset(dataset_path, output_path)
