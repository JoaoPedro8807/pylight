from src.main import Pylight, Session
from pylight_example import create_table as create_table_example
from pylight_example import Book
class PylightBenchmark:
    def __init__(self, db_url: str, inserts_range: int = 10000, step: int = 1000, num_tests: int = 10):
        self.db = db_url or "sqlite:///benchmark.db"
        self.inserts_range = inserts_range
        self.step = step
        self.num_tests = num_tests

        if step > inserts_range:
            raise ValueError("step must be less than or equal to inserts_range.")
        if inserts_range % step != 0:
            raise ValueError("inserts_range must be divisible by step.")
        if num_tests < 1 or num_tests > 20:
            raise ValueError("num_tests must be between 1 and 20.")

    def create_table(self):
        create_table_example(self.db)
        
        #self.db.execute('CREATE TABLE IF NOT EXISTS benchmark (id INTEGER PRIMARY KEY, name TEXT);')

    def insert_data(self, num_records: int):
        data_to_insert = [{"name": f"Name {i}"} for i in range(num_records)]
        self.db.insert('benchmark', data_to_insert)


    def insert_book(self, loop_value: int, session: Session):
        pessoa = Book.create(
            nome=f"Name {loop_value}",
            data="2021-10-10",
            ativo=True,
            numero=10
        )   
        session.add(pessoa, commit=True)

    def select_data(self, num_records):
        return self.db.select('SELECT * FROM benchmark WHERE id <= ?', (num_records,))

    def update_data(self, num_records):
        self.db.execute('UPDATE benchmark SET name = ? WHERE id <= ?', ("Updated Name", num_records))

    def delete_data(self, num_records):
        self.db.execute('DELETE FROM benchmark WHERE id <= ?', (num_records,))

    def clear_table(self):
        self.db.execute('DELETE FROM benchmark;')

    def benchmark_operation(self, operation, num_records: int):
        import time
        start_time = time.time()
        operation(num_records)
        end_time = time.time()
        return (end_time - start_time) * 1000  # in ms

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
            self.insert_data(num_records)
            execution_time_ms = self.benchmark_operation(self.select_data, num_records)
            results.append((num_records, execution_time_ms))
            self.clear_table()  
        return results

    def benchmark_updates(self):
        results = []
        for num_records in range(self.step, self.inserts_range + 1, self.step):
            self.insert_data(num_records)
            execution_time_ms = self.benchmark_operation(self.update_data, num_records)
            results.append((num_records, execution_time_ms))
            self.clear_table() 
        return results

    def benchmark_deletes(self):
        results = []
        for num_records in range(self.step, self.inserts_range + 1, self.step):
            self.insert_data(num_records)
            execution_time_ms = self.benchmark_operation(self.delete_data, num_records)
            results.append((num_records, execution_time_ms)) 
            self.clear_table()  
        return results

    def run_multiple_tests(self, operation: str):
        all_results = {num: [] for num in range(self.step, self.inserts_range + 1, self.step)}

        for test in range(self.num_tests):
            print(f"Running test {test + 1}/{self.num_tests} for operation {operation}...")
            if operation == "insert":
                results = self.benchmark_inserts()
            elif operation == "select":
                results = self.benchmark_selects()
            elif operation == "update":
                results = self.benchmark_updates()
            elif operation == "delete":
                results = self.benchmark_deletes()
            else:
                raise ValueError("Invalid operation. Use 'insert', 'select', 'update', or 'delete'.")

            for num_records, execution_time_ms in results:
                all_results[num_records].append(execution_time_ms)

        averages_total = []
        averages_per_operation = []
        for num_records in sorted(all_results.keys()):
            times_ms = all_results[num_records]
            avg_time_ms = sum(times_ms) / len(times_ms)
            avg_time_per_operation_ms = (avg_time_ms / num_records)

            averages_total.append((num_records, avg_time_ms))
            averages_per_operation.append((num_records, avg_time_per_operation_ms))

            print(f"Average for {num_records} records: {avg_time_ms:.2f} ms")
            print(f"Average per operation: {avg_time_per_operation_ms:.5f} ms")

        return averages_total, averages_per_operation

    def plot_results(self, averages_total: list, averages_per_operation: list, operation: str):
        import matplotlib.pyplot as plt
        import numpy as np

        num_records_total = [result[0] for result in averages_total]
        avg_times_total_ms = [result[1] for result in averages_total]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(num_records_total, avg_times_total_ms, marker='o', linestyle='-', color='b')
        plt.title(f"Total Execution Time ({operation.capitalize()})")
        plt.xlabel("Number of Records")
        plt.ylabel("Average Execution Time (ms)")
        plt.grid(True)

        num_records_per_operation = [result[0] for result in averages_per_operation]
        avg_times_per_operation_ms = [result[1] for result in averages_per_operation]

        plt.subplot(1, 2, 2)
        plt.plot(num_records_per_operation, avg_times_per_operation_ms, marker='o', linestyle='-', color='r')
        plt.title(f"Average Time per {operation.capitalize()}")
        plt.xlabel("Number of Records")
        plt.ylabel("Average Time per Operation (ms)")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

def main():
    benchmark = PylightBenchmark(db_url="sqlite:///benchmark.db", inserts_range=10000, step=1000, num_tests=10)
    benchmark.create_table()

    print("Testing INSERT...")
    averages_total_insert, averages_per_insert = benchmark.run_multiple_tests("insert")
    benchmark.plot_results(averages_total_insert, averages_per_insert, "insert")

    print("Testing SELECT...")
    averages_total_select, averages_per_select = benchmark.run_multiple_tests("select")
    benchmark.plot_results(averages_total_select, averages_per_select, "select")

    print("Testing UPDATE...")
    averages_total_update, averages_per_update = benchmark.run_multiple_tests("update")
    benchmark.plot_results(averages_total_update, averages_per_update, "update")

    print("Testing DELETE...")
    averages_total_delete, averages_per_delete = benchmark.run_multiple_tests("delete")
    benchmark.plot_results(averages_total_delete, averages_per_delete, "delete")

if __name__ == "__main__":
    main()