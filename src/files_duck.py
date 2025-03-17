import os
import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / 'data'
database_path = BASE_DIR / 'database'

def check_path_exists(paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'Pasta "{path}" criada com sucesso!')
        else:
            print(f'A pasta "{path}" já existe.')

def init_process():
    print('Processing data to staging...')
    duckdb.sql(f"""
        WITH unnest_entry AS (
            SELECT resourceType
                  ,type
                  ,unnest(entry) as entry
            FROM read_json(
                '{data_path}/raw/*.json'
                ,maximum_object_size=43554428
                ,union_by_name=true
            )
        )
        SELECT *
        FROM unnest_entry""").to_parquet(file_name=f'{data_path}/staging/processed.parquet', overwrite=True)

    print('Creating table on DuckDB...')
    con = duckdb.connect(f'{database_path}/clinic.db')
    con.sql(f"""
        CREATE OR REPLACE TABLE clinic_history AS (
            SELECT *
            FROM read_parquet('{data_path}/staging/processed.parquet')
        )
    """)
    con.close()

if __name__=="__main__":
    paths_to_check = [f'{data_path}/raw', f'{data_path}/staging', database_path]
    check_path_exists(paths_to_check)
    init_process()