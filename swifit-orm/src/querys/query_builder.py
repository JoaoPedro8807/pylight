from typing import List, Optional, Tuple, Union


class QueryBuilder:

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns: List[str] = ["*"]  # Por padrão, seleciona todas as colunas
        self.filters = []
        self.order_by = []
        self.limit = None
        self.offset = None

    def select(self, columns: Optional[List[str]] = None) -> "QueryBuilder":
        """
        Define as colunas a serem selecionadas.
        """
        if columns:
            self.columns = columns
        return self

    def where(self, condition: str, params: Union[list, str]) -> "QueryBuilder":
        """
        Adiciona uma cláusula WHERE.
        """
        self.filters.append((condition, params))
        print("ESTADO DO FILTER: ", self.filters)
        return self

    def order(self, column: str, direction: str = "ASC") -> "QueryBuilder":
        """
        Adiciona uma cláusula ORDER BY.
        """
        self.order_by.append(f"{column} {direction}")
        return self

    def limit_offset(self, limit: int, offset: int = 0) -> "QueryBuilder":
        """
        Define LIMIT e OFFSET.
        """
        self.limit = limit
        self.offset = offset
        return self

    def build(self) -> Tuple[str, list]:
        """
        Constrói a consulta SQL final.
        """
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table_name}"
        params = []

        if self.filters:
            where_clauses = [f[0] for f in self.filters]
            print("CLAUSULE DO BUILDER: ", where_clauses)
            sql += f" WHERE {' AND '.join(where_clauses)}"
            for _, p in self.filters:

                params.extend(p)
            

            print("SQL DO FINAL BUILDER: ", sql, "PARAMS: ", params)    

        if self.order_by:
            sql += f" ORDER BY {', '.join(self.order_by)}"

        if self.limit is not None:
            sql += f" LIMIT {self.limit}"
            if self.offset:
                sql += f" OFFSET {self.offset}"

        return sql, params
