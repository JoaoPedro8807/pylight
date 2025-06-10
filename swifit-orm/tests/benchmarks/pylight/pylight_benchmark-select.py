import matplotlib.pyplot as plt
import numpy as np
import time

engine = create_engine("sqlite:///benchmark.db")
session = Session(engine)
NUM_RECORDS = 10000
NUM_TESTS = 10

def create_table(session: Session):
    create_sql = text('CREATE TABLE IF NOT EXISTS benchmark (id INTEGER PRIMARY KEY, name VARCHAR);')
    session.execute(create_sql)
    session.commit()    

def get_data(session: Session, num_records: int):    
    select_sql = text('SELECT * FROM benchmark LIMIT :num_records')
    result = session.execute(select_sql, {"num_records": num_records})
    return result.fetchall()

def run_multiple_tests(num_tests: int, session: Session, num_records: int):
    # Dicionário para armazenar os tempos de cada teste
    all_results = {num: [] for num in range(num_records)}


def main():
    create_table(session=session)
    insert_data(session=session, num_records=NUM_RECORDS)
    start_time = time.time()
    data = get_data(session=session, num_records=NUM_RECORDS)
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000
    if data:
        print("dados encontrados com sucesso")
    pass

if __name__ == "__main__":
    main()


