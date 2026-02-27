from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def guardar(self, producto: Product):
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Product]:
        pass

    @abstractmethod
    def obtener_por_sku(self, sku: str) -> Optional[Product]:
        pass

    @abstractmethod
    def actualizar(self, producto: Product):
        pass

    @abstractmethod
    def eliminar_logico(self, sku: str):
        pass