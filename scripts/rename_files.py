import os
import concurrent.futures

def renomear_subpasta(caminho_pasta_mae, nome_base, zoom_rate):
    caminho_subpasta = os.path.join(caminho_pasta_mae, zoom_rate)
    novo_nome_subpasta = os.path.join(caminho_pasta_mae, nome_base)
    
    # Verifica se a subpasta "10" existe e se o novo nome já não existe
    if os.path.exists(caminho_subpasta) and not os.path.exists(novo_nome_subpasta):
        try:
            # Renomeia a subpasta
            os.rename(caminho_subpasta, novo_nome_subpasta)
            print(f"Renomeado: {caminho_subpasta} -> {novo_nome_subpasta}")
        except Exception as e:
            print(f"Erro ao renomear {caminho_subpasta}: {e}")
    else:
        print(f"Subpasta {caminho_subpasta} já renomeada ou destino {novo_nome_subpasta} já existe.")

def renomear_subpastas(root_dir, zoom_rate):
    # Lista para armazenar as tarefas
    tarefas = []
    
    # Percorre todas as pastas no diretório raiz
    for pasta_mae in os.listdir(root_dir):
        caminho_pasta_mae = os.path.join(root_dir, pasta_mae)
        
        # Verifica se é uma pasta e se termina com "_files"
        if os.path.isdir(caminho_pasta_mae) and pasta_mae.endswith("_files"):
            nome_base = pasta_mae.replace("_files", "")
            tarefas.append((caminho_pasta_mae, nome_base, zoom_rate))
    
    # Usa ThreadPoolExecutor para paralelizar as tarefas
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mapeia as tarefas para o executor
        executor.map(lambda args: renomear_subpasta(*args), tarefas)
