import time
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

class SqlalchemyBenchmark:
    def __init__(self, session: Session, inserts_range: int = 10000, step: int = 1000, num_tests: int = 10):
        self.session = session
        self.inserts_range = inserts_range
        self.step = step
        self.num_tests = num_tests

        if step > inserts_range:
            raise ValueError("step deve ser menor ou igual a inserts_range.")
        if inserts_range % step != 0:
            raise ValueError("inserts_range deve ser divisível por step.")
        if num_tests < 1 or num_tests > 20:
            raise ValueError("num_tests deve estar entre 1 e 20.")

    def create_table(self):
        create_sql = text('CREATE TABLE IF NOT EXISTS benchmark (id INTEGER PRIMARY KEY, name VARCHAR);')
        self.session.execute(create_sql)
        self.session.commit()

    def insert_data(self, num_records: int):

        data_to_insert = [{"name": f"Name {i}"} for i in range(num_records)]
        
        # Executa a inserção em lote
        insert_sql = text('INSERT INTO benchmark (name) VALUES (:name)')
        self.session.execute(insert_sql, data_to_insert)
        self.session.commit()

    def select_data(self, num_records):
        select_sql = text('SELECT * FROM benchmark WHERE id <= :max_id')
        self.session.execute(select_sql, {"max_id": num_records}).fetchall()

    def update_data(self, num_records):
        update_sql = text('UPDATE benchmark SET name = :new_name WHERE id <= :max_id')
        self.session.execute(update_sql, {"new_name": "Updated Name", "max_id": num_records})
        self.session.commit()

    def delete_data(self, num_records):
        delete_sql = text('DELETE FROM benchmark WHERE id <= :max_id')
        self.session.execute(delete_sql, {"max_id": num_records})
        self.session.commit()

    def clear_table(self):
        
        self.session.execute(text('DELETE FROM benchmark;'))
        self.session.commit()

    def benchmark_operation(self, operation: str, num_records: int):
        start_time = time.time()
        operation(num_records)
        end_time = time.time()
        return (end_time - start_time) * 1000  # em ms

    def benchmark_inserts(self):
        results = []
        for num_records in range(self.step, self.inserts_range + 1, self.step):
            execution_time_ms = self.benchmark_operation(self.insert_data, num_records)
            results.append((num_records, execution_time_ms))
            self.clear_table()  
        return results

    def benchmark_selects(self):
        results = []
        for num_records in range(self.step, self.inserts_range + 1, self.step):
            self.insert_data(num_records)  # Preenche a tabela com dados
            execution_time_ms = self.benchmark_operation(self.select_data, num_records)
            results.append((num_records, execution_time_ms))
            self.clear_table()  
        return results

    def benchmark_updates(self):
        results = []
        for num_records in range(self.step, self.inserts_range + 1, self.step):
            self.insert_data(num_records)  # Preenche a tabela com dados
            execution_time_ms = self.benchmark_operation(self.update_data, num_records)
            results.append((num_records, execution_time_ms))
            self.clear_table() 
        return results

    def benchmark_deletes(self):
        results = []
        for num_records in range(self.step, self.inserts_range + 1, self.step):
            self.insert_data(num_records)  # Preenche a tabela com dados
            execution_time_ms = self.benchmark_operation(self.delete_data, num_records)
            results.append((num_records, execution_time_ms)) 
            self.clear_table()  # Limpa a tabela para o próximo teste
        return results

    def run_multiple_tests(self, operation: str):
        all_results = {num: [] for num in range(self.step, self.inserts_range + 1, self.step)}

        for test in range(self.num_tests):
            print(f"Executando teste {test + 1}/{self.num_tests} para operação {operation}...")
            if operation == "insert":
                results = self.benchmark_inserts()
            elif operation == "select":
                results = self.benchmark_selects()
            elif operation == "update":
                results = self.benchmark_updates()
            elif operation == "delete":
                results = self.benchmark_deletes()
            else:
                raise ValueError("Operação inválida. Use 'insert', 'select', 'update' ou 'delete'.")

            for num_records, execution_time_ms in results:
                all_results[num_records].append(execution_time_ms)

        averages_total = []
        averages_per_operation = []
        for num_records in sorted(all_results.keys()):
            times_ms = all_results[num_records]
            avg_time_ms = np.mean(times_ms)  # Média do tempo total
            avg_time_per_operation_ms = (avg_time_ms / num_records)  # Média do tempo por operação

            averages_total.append((num_records, avg_time_ms))
            averages_per_operation.append((num_records, avg_time_per_operation_ms))

            print(f"Média para {num_records} registros: {avg_time_ms:.2f} ms")
            print(f"Média por operação: {avg_time_per_operation_ms:.5f} ms")

        return averages_total, averages_per_operation

    def plot_results(self, averages_total: list, averages_per_operation: list, operation: str):
        num_records_total = [result[0] for result in averages_total]
        avg_times_total_ms = [result[1] for result in averages_total]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(num_records_total, avg_times_total_ms, marker='o', linestyle='-', color='b')
        plt.title(f"Tempo Total de Execução ({operation.capitalize()})")
        plt.xlabel("Número de Registros")
        plt.ylabel("Tempo Médio de Execução (ms)")
        plt.grid(True)

        num_records_per_operation = [result[0] for result in averages_per_operation]
        avg_times_per_operation_ms = [result[1] for result in averages_per_operation]
        


        print("Resultados para o gráfico:", num_records_per_operation,  avg_times_per_operation_ms)

        plt.subplot(1, 2, 2)
        plt.plot(num_records_per_operation, avg_times_per_operation_ms, marker='o', linestyle='-', color='r')
        plt.title(f"Tempo Médio por {operation.capitalize()}")
        plt.xlabel("Número de Registros")
        plt.ylabel("Tempo Médio por Operação (ms)")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

def main():
    engine = create_engine("sqlite:///benchmark.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    benchmark = SqlalchemyBenchmark(session=session, inserts_range=10000, step=1000, num_tests=10)
    benchmark.create_table()

    print("Testando INSERT...")
    averages_total_insert, averages_per_insert = benchmark.run_multiple_tests("insert")
    benchmark.plot_results(averages_total_insert, averages_per_insert, "insert")

    print("Testando SELECT...")
    averages_total_select, averages_per_select = benchmark.run_multiple_tests("select")
    benchmark.plot_results(averages_total_select, averages_per_select, "select")

    print("Testando UPDATE...")
    averages_total_update, averages_per_update = benchmark.run_multiple_tests("update")
    benchmark.plot_results(averages_total_update, averages_per_update, "update")

    print("Testando DELETE...")
    averages_total_delete, averages_per_delete = benchmark.run_multiple_tests("delete")
    benchmark.plot_results(averages_total_delete, averages_per_delete, "delete")

if __name__ == "__main__":
    main()