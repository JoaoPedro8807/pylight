from typing import TYPE_CHECKING, Tuple, List, Optional
from main.filters import BaseFilter
from querys import QueryBuilder

if TYPE_CHECKING:
    from querys import InsertQuery, UpdateQuery
    from backend import DatabaseBackend, SqliteBackend
    from main.model import Model



class SQLCompiler:
 
    def create_table_sql(self, backend: "DatabaseBackend", model: "Model", **kwargs) -> str:
        fields = model._fields.items()
        print("fields", fields) 

        sql = f"CREATE TABLE IF NOT EXISTS {model._meta.get('db_table')} ({', '.join(
            [f'{field_name} {field_object.get_sql_type(backend, length=field_object._LENGTH)} {field_object.get_create_params(backend=backend)}' for field_name, field_object in fields ])});"
        print("SQL CREATE TABLE: ", sql)
        return sql
    
    def insert_sql(self, backend: "DatabaseBackend", model: "Model", **kwargs) -> Tuple[str, list]:
        aux_params = []
        returning_id = kwargs.get("returning_id", False)
        if returning_id:
            aux_params.append("RETURNING id")

        params = model.get_field_values()
        placeholder_values = ', '.join(['%s'] * len(params))
        if backend.__name__() == "SqliteBackend":
            placeholder_values = ', '.join(['?'] * len(params))
            
        sql = f"INSERT INTO {model._meta.get('db_table')} ({', '.join(params.keys())}) VALUES ({placeholder_values}) {', '.join(aux_params)};"
        params = list(params.values())
        return sql, params
    def update_sql(self, backend: "DatabaseBackend", model: "Model", **kwargs):
        params = model.get_field_values()
        placeholder_values = ', '.join([f"{field} = %s" for field in params.keys()])
        sql = f"UPDATE {model._meta.get('db_table')} SET {placeholder_values} WHERE id = %s;"
        params = list(params.values()) + [model.id] #verificar o id
        return sql, params

    def delete_sql(self, backend: "DatabaseBackend", model: "Model", **kwargs) -> Tuple[str, list]:
        sql = f"DELETE FROM {model._meta.get('db_table')} WHERE id = %s;"
        params = [model.id] 
        return sql, params
    
    def select_sql(self, backend: "DatabaseBackend", model: "Model", filters: Optional[List[BaseFilter]], **kwargs) -> Tuple[str, list]:
        builder = QueryBuilder(table_name=model._meta.get("db_table"))

        columns = kwargs.get("columns", ["*"])
        builder.select(columns)

        if filters:
            for filter in filters:
                condition, params = filter.to_sql(model=model)
                print("ADICIONANDO AOS PARAMS: ",  condition, params)
                builder.where(condition=condition, params=params)

        order_by = kwargs.get("order_by", None)
        if order_by:
            builder.order(order_by)

        limit = kwargs.get("limit", None)
        if limit:
            offset = kwargs.get("offset", None)
            builder.limit_offset(limit, offset)

        sql, params = builder.build()
        print("BUILDER RETORNANDO SQL: ", sql, "PARAMS: ", params)
        return sql, params


    def select_all_sql(self, backend: "DatabaseBackend", model: "Model", **kwargs) -> Tuple[str, list]:
        sql = f"SELECT * FROM {model._meta.get('db_table')};"
        return sql, []

    def as_sql(self):
        if isinstance(self.query, InsertQuery):
            return self._as_insert_sql()
        elif isinstance(self.query, UpdateQuery):
            return self._as_update_sql()

    def _as_insert_sql(self):
        fields = self.query.fields
        values = self.query.objs
        sql = f"INSERT INTO {self.query.model._meta.db_table} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))});"
        params = [obj[field] for field in fields for obj in values]
        return sql, params

    def _as_update_sql(self):
        fields = self.query.values.keys()
        values = self.query.values.values()
        filters = self.query.filters
        sql = f"UPDATE {self.query.model._meta.db_table} SET {', '.join([f'{field} = %s' for field in fields])} WHERE {', '.join([f'{field} = %s' for field in filters.keys()])};"
        params = list(values) + list(filters.values())
        return sql, params
    

    def get_field_params(self, model: "Model") -> str:
        fields = model._fields

        
