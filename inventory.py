from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float
    description: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', qty={self.quantity}, price={self.price})"


class Inventory:
    """Gestión en memoria de productos usando un diccionario {id: Product}.

    Se diseñó para búsquedas rápidas por ID y filtrado por nombre.
    """

    def __init__(self):
        self.products: Dict[int, Product] = {}

    def add_product(self, product: Product) -> None:
        if product.id in self.products:
            raise ValueError(f"Producto con ID {product.id} ya existe")
        self.products[product.id] = product

    def remove_product(self, product_id: int) -> Optional[Product]:
        return self.products.pop(product_id, None)

    def update_quantity(self, product_id: int, quantity: int) -> None:
        p = self.products.get(product_id)
        if not p:
            raise KeyError(f"Producto con ID {product_id} no encontrado")
        p.quantity = quantity

    def update_price(self, product_id: int, price: float) -> None:
        p = self.products.get(product_id)
        if not p:
            raise KeyError(f"Producto con ID {product_id} no encontrado")
        p.price = price

    def find_by_name(self, name: str) -> List[Product]:
        name_lower = name.lower()
        return [p for p in self.products.values() if name_lower in p.name.lower()]

    def list_all(self) -> List[Product]:
        return list(self.products.values())

    def get(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)
