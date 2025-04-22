from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main.model.base.model_base import Model


class BaseFilter:
    model: "Model" = None

    def __init__(self, filters: dict):
        self.filters = filters

    def validate_fields(self) -> None:
        """
        Valida se os campos fornecidos no filtro existem no modelo.
        """
        for field in self.filters.keys():
            if field not in self.model._fields:
                raise ValueError(f"O campo '{field}' não existe no modelo '{self.model.__class__.__name__}'.")

    def to_sql(self, model: "Model") -> str:
        self.model = model
        """
        Converte os filtros em uma cláusula WHERE SQL.
        """
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")