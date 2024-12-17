import pandas as pd
import unidecode
import os
from pathlib import Path
from tqdm import tqdm
import math
import re

def get_total_lines(filename, encoding='latin1'):
    """
    Conta o número total de linhas no arquivo de forma eficiente.
    """
    with open(filename, 'r', encoding=encoding) as f:
        return sum(1 for _ in f)

def get_optimal_chunk_size(file_size_gb):
    """
    Determina o tamanho ideal do chunk baseado no tamanho do arquivo.
    """
    if file_size_gb < 0.25:      # Menos de 250MB
        return 25000
    elif file_size_gb < 0.5:     # Menos de 500MB
        return 50000
    elif file_size_gb < 1:       # Menos de 1GB
        return 100000
    elif file_size_gb < 1.5:     # Menos de 1.5GB
        return 150000
    elif file_size_gb < 2:       # Menos de 2GB
        return 200000
    elif file_size_gb < 2.5:     # Menos de 2.5GB
        return 250000
    elif file_size_gb < 3:       # Menos de 3GB
        return 300000
    elif file_size_gb < 3.5:     # Menos de 3.5GB
        return 350000
    else:                        # 3.5GB ou mais
        return 400000

def format_text(text):
    """
    Aplica todas as transformações de texto necessárias:
    1. Remove acentos
    2. Converte para maiúsculas
    3. Remove espaços múltiplos
    """
    # Converte para string caso não seja
    text = str(text)
    # Remove acentos
    text = unidecode.unidecode(text)
    # Converte para maiúsculas
    text = text.upper()
    # Remove espaços múltiplos (mantendo um espaço único entre palavras)
    text = ' '.join(text.split())
    return text

def process_large_csv(input_file, output_file, chunk_size):
    """
    Processa um arquivo CSV grande aplicando as transformações de texto.
    """
    encoding = 'latin1'

    try:
        print("Contando linhas do arquivo...")
        total_lines = get_total_lines(input_file)
        total_chunks = math.ceil(total_lines / chunk_size)

        print(f"Total de linhas: {total_lines:,}")
        print(f"Tamanho do chunk: {chunk_size:,}")
        print(f"Total de chunks: {total_chunks:,}")

        if os.path.exists(output_file):
            os.remove(output_file)

        chunks = pd.read_csv(
            input_file,
            chunksize=chunk_size,
            encoding=encoding,
            sep=';',
            quotechar='"',
            na_filter=False,
            dtype=str,
            keep_default_na=False
        )

        first_chunk = True

        with tqdm(total=total_chunks, desc="Processando chunks") as pbar:
            for chunk in chunks:
                # Aplica todas as transformações em todas as colunas
                for column in chunk.columns:
                    chunk[column] = chunk[column].apply(format_text)

                chunk.to_csv(
                    output_file,
                    mode='w' if first_chunk else 'a',
                    index=False,
                    header=False,
                    encoding=encoding,
                    sep=';',
                    quotechar='"',
                    quoting=1,
                    na_rep=''
                )

                first_chunk = False
                pbar.update(1)

        return True
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return False

def process_directory(input_dir, output_dir):
    """
    Processa todos os arquivos CSV em um diretório.
    """
    os.makedirs(output_dir, exist_ok=True)

    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    total_files = len(csv_files)

    print(f"\nEncontrados {total_files} arquivos CSV para processar")

    for idx, csv_file in enumerate(csv_files, 1):
        input_path = os.path.join(input_dir, csv_file)
        output_path = os.path.join(output_dir, f"processed_{csv_file}")

        print(f"\nProcessando arquivo {idx}/{total_files}: {csv_file}")
        file_size_gb = os.path.getsize(input_path) / (1024 * 1024 * 1024)
        print(f"Tamanho do arquivo: {file_size_gb:.2f} GB")

        chunk_size = get_optimal_chunk_size(file_size_gb)

        if process_large_csv(input_path, output_path, chunk_size):
            print(f"✓ Arquivo {csv_file} processado com sucesso!")
        else:
            print(f"✗ Falha ao processar {csv_file}")

def process_all_directories(base_dir):
    """
    Processa todas as pastas que contêm arquivos CSV.
    """
    # Lista de pastas para processar
    directories = [
        'Cnaes', 'Empresas', 'Estabelecimentos', 'Motivos',
        'Municipios', 'Naturezas', 'Paises', 'Qualificacoes',
        'Simples', 'Socios'
    ]

    total_dirs = len(directories)
    print(f"Iniciando processamento de {total_dirs} diretórios")

    for idx, dir_name in enumerate(directories, 1):
        input_dir = os.path.join(base_dir, dir_name)
        output_dir = os.path.join(base_dir, f"{dir_name}_Processados")

        print(f"\n[{idx}/{total_dirs}] Processando diretório: {dir_name}")

        if os.path.exists(input_dir):
            process_directory(input_dir, output_dir)
        else:
            print(f"Diretório {dir_name} não encontrado.")

    print("\nProcessamento de todos os diretórios concluído!")

if __name__ == "__main__":
    base_dir = r"C:\Users\NOT-20190718\Documents\cnpjs"
    process_all_directories(base_dir)