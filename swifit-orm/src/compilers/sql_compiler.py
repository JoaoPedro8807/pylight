from typing import TYPE_CHECKING
from main.model import Model

if TYPE_CHECKING:
    from querys import InsertQuery, UpdateQuery
    from backend import DatabaseBackend, SqliteBackend


class SQLCompiler:
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
    
    def create_table_sql(self, backend: "DatabaseBackend", model: Model, **kwargs) -> str:
        fields = model._fields.items()


        print("fields", fields) 

        sql = f"CREATE TABLE IF NOT EXISTS {model._meta.get('db_table')} ({', '.join(
            [f'{field_name} {field_object.get_sql_type(backend, length=field_object._LENGTH)} {field_object.get_create_params(backend=backend)}' for field_name, field_object in fields ])});"
        print("SQL CREATE TABLE: ", sql)
        return sql

    def get_field_params(self, model: Model) -> str:
        fields = model._fields

        
