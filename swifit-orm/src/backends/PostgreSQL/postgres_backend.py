from ..database_backend import DatabaseBackend

class PostgreSQLBackend(DatabaseBackend):
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, **kwargs):
        print("executando connect no postgres")
        import psycopg2
        self.connection = psycopg2.connect(**kwargs)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params=None):
        self.cursor.execute(query, params or ())

    def fetch_all(self):
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_default_conection_params() -> dict:
        return {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "user": "postgres",
            "password": "postgres",
        }

    def __exit__(self):
        self.close()