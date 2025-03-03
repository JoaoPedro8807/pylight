import time
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///benchmark.db")
session = Session(engine)
insert_sql = text('INSERT INTO benchmark (name) VALUES (:name)')
for i in range(10000):
    session.execute(insert_sql, {"name": f"Name {i}"})
session.commit()


INSERTS_RANGE = 10000  
STEP = 1000  # intervalo de inserções
NUM_TESTS = 10  

def create_table(session):
    create_sql = text('CREATE TABLE IF NOT EXISTS benchmark (id INTEGER PRIMARY KEY, name VARCHAR);')
    session.execute(create_sql)
    session.commit()

def insert_data(session, num_records):
    insert_sql = text('INSERT INTO benchmark (name) VALUES (:name)')
    for i in range(num_records):
        session.execute(insert_sql, {"name": f"Name {i}"})
    session.commit()

def clear_table(session):
    session.execute(text('DELETE FROM benchmark;'))
    session.commit()

def benchmark_inserts(session, max_records, step):
    results = []
    for num_records in range(step, max_records + 1, step):
        start_time = time.time()
        insert_data(session, num_records)
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000  # Convertendo para ms
        results.append((num_records, execution_time_ms))
        clear_table(session)  # Limpa a tabela para o próximo teste
    return results

def run_multiple_tests(num_tests, session, max_records, step):
    """Executa o benchmark várias vezes e retorna as médias."""
    # Dicionário para armazenar os tempos de cada teste
    all_results = {num: [] for num in range(step, max_records + 1, step)}

    for test in range(num_tests):
        print(f"Executando teste {test + 1}/{num_tests}...")
        results = benchmark_inserts(session, max_records, step)
        for num_records, execution_time_ms in results:
            all_results[num_records].append(execution_time_ms)

    averages_total = []
    averages_per_insert = []
    for num_records in sorted(all_results.keys()):
        times_ms = all_results[num_records]
        avg_time_ms = np.mean(times_ms)  # Média do tempo total
        avg_time_per_insert_ms = (avg_time_ms / num_records) * 1000  # Média do tempo por insert

        averages_total.append((num_records, avg_time_ms))
        averages_per_insert.append((num_records, avg_time_per_insert_ms))

        print(f"Média para {num_records} registros: {avg_time_ms:.2f} ms")
        print(f"Média por insert: {avg_time_per_insert_ms:.5f} ms")

    return averages_total, averages_per_insert

def plot_results(averages_total, averages_per_insert):
    # Gráfico 1: Tempo total de execução
    num_records_total = [result[0] for result in averages_total]
    avg_times_total_ms = [result[1] for result in averages_total]

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(num_records_total, avg_times_total_ms, marker='o', linestyle='-', color='b')
    plt.title("Tempo Total de Execução")
    plt.xlabel("Número de Registros Inseridos")
    plt.ylabel("Tempo Médio de Execução (ms)")
    plt.grid(True)

    # Gráfico 2: Tempo por insert
    num_records_per_insert = [result[0] for result in averages_per_insert]
    avg_times_per_insert_ms = [result[1] for result in averages_per_insert]

    plt.subplot(1, 2, 2)
    plt.plot(num_records_per_insert, avg_times_per_insert_ms, marker='o', linestyle='-', color='r')
    plt.title(f"Tempo Médio a cada {STEP} Insert")
    plt.xlabel("Número de Registros Inseridos")
    plt.ylabel("Tempo Médio por Insert (ms)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    with Session(engine) as session:
        create_table(session)
        averages_total, averages_per_insert = run_multiple_tests(NUM_TESTS, session, INSERTS_RANGE, STEP)
        plot_results(averages_total, averages_per_insert)

if __name__ == "__main__":
    main()