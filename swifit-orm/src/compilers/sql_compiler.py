from querys import InsertQuery, UpdateQuery

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
    
    def create_table_sql(self, model) -> str:
        fields = model.fields
        sql = f"CREATE TABLE IF NOT EXISTS {model._meta.db_table} ({', '.join([f'{field} {field_type}' for field, field_type in fields.items()])});"
        return sql