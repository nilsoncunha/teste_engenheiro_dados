import os
import requests
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / 'data/raw'

user = 'wandersondsm'
repo = 'teste_engenheiro'
branch = 'main'

def check_path_exists(paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'Pasta "{path}" criada com sucesso!')
        else:
            print(f'A pasta "{path}" já existe.')

def init_process():
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(url)

    # Analisa se conseguimos acesso a API, se não retorna erro
    if response.status_code == 200:
        # Pega o caminho dos arquivos e adiciona em uma lista
        tree = response.json().get("tree", [])
        files = [item for item in tree if item["path"].startswith('data') and item["type"] == "blob"]

        qtd_files = len(files)
        count = 1

        print('Realizando download dos arquivos...')
        # Itera sobre a lista de arquivos para realizar o download
        for file in files:
            file_path = file["path"].split("/")[-1]  # Nome do arquivo
            download_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file['path']}"
            file_response = requests.get(download_url)

            # Caso obtermos resposta positiva o arquivo será baixado e salvo com seu respectivo nome na pasta "data"
            if file_response.status_code == 200:
                with open(f'{data_path}/{file_path}', "w") as f:
                    f.write(file_response.text)
                print(f"{file_path} - {count} of {qtd_files} - baixado com sucesso!")
                count += 1
            else:
                print(f"Erro no arquivo {file_path}: {file_response.status_code}")
    else:
        print("Erro na lista:", response.status_code)

if __name__=="__main__":
    paths_to_check = [f'{data_path}']
    check_path_exists(paths_to_check)
    init_process()