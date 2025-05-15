import sys
from tqdm import tqdm
from rename_files import renomear_subpastas
from rename_imgs import organize_and_move_images
from split_dataset import split_dataset
from count_imgs import count_imgs
from data_augmentation_v2 import augment_dataset
from remove_imgs_backgroud import  clean_dataset



def menu():
    print("--------------------------------------------------------------------------")
    print("OPTIONS:")
    print("Rename Files path                       ---> 1")
    print("Rename Images for the same name of path ---> 2")
    print("Remove Blue images                      ---> 3")
    print("Split Data                              ---> 4")
    print("count images dataset                    ---> 5")
    print("Data Augmentation                       ---> 6")
    print("Exit                                    ---> 7")
    option = input("choice your option: ")

    try:
        if isinstance(option, str):
            option = int(option)
    except:
        print("try again")

    if option == 1:
        print()
        # Define o diretório raiz
        root_dir = str(input(r"type your directory for to rename files: "))
        zoom_rate = str(input("type the zoom rate aply in build process of the dataset (ex.: 10x): "))
        renomear_subpastas(root_dir, zoom_rate)

    elif option == 2:
        print()
        input_file = input("type the path for your file.txt: ")
        organize_and_move_images(input_file)
    
    elif option == 3:
        input_file_in = input("type the path for your dataset file (ex: CIN/MSI): ")
        input_file_out = input("type the path for your output file (ex: CIN/MSI): ")
        # Executa a limpeza
        clean_dataset(input_file_in, input_file_out)

    elif option == 4:
        print()
        dataset_path = input("type the path for your dataset: ")
        output_path = input("type the path for your output: ")
        config_path = input("type the path for your config file: ")
        print()
        print("Spliting dataset...")
        split_dataset(dataset_path, output_path, config_path)
    
    elif option == 5:
        dataset_path = input("type the path for your dataset: ")
        print()
        print(f"Quantidade total de imagens no diretório: {count_imgs(dataset_path)}")

    
    elif option == 6:
        print()

        input_directory = input("Digite o caminho do diretório de entrada (ex: ./matrix): ").strip()
        operations_to_apply = input("Digite as operações desejadas separadas por vírgula (flip, rotate_90, crop, rotation, shear): ").split(",")
        if operations_to_apply is None or operations_to_apply == "":
            operations_to_apply = ["flip", "flip_v", "rotate_90", "crop", "rotation", "shear"]

        augmentation_factor = int(input("Digite o fator de multiplicidade: "))

        augment_dataset(
            input_dir=input_directory,
            operations=operations_to_apply,
            factor=augmentation_factor
        )

    elif option == 7:
        print()
        print("Goodbye!")
        sys.exit(0)


    else:
        print("Invalid option")
        menu()
    print("--------------------------------------------------------------------------")



if __name__ == "__main__":
    menu()