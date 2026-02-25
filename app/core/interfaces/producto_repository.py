from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.producto import Producto


class ProductoRepository(ABC):

    @abstractmethod
    def guardar(self, producto: Producto):
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def obtener_por_sku(self, sku: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def actualizar(self, producto: Producto):
        pass

    @abstractmethod
    def eliminar_logico(self, sku: str):
        pass