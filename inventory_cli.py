from inventory import Inventory, Product
import db


def load_inventory_from_db(inv: Inventory) -> None:
    for p in db.list_products():
        inv.products[p.id] = p


def prompt_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Entrada inválida, ingrese un número entero.")


def prompt_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Entrada inválida, ingrese un número válido.")


def main():
    db.init_db()
    inv = Inventory()
    load_inventory_from_db(inv)

    menu = """
    --- Sistema de Inventario ---
    1) Añadir producto
    2) Eliminar producto
    3) Actualizar cantidad
    4) Actualizar precio
    5) Buscar por nombre
    6) Mostrar todos
    0) Salir
    """

    while True:
        print(menu)
        choice = input("Opción: ").strip()
        if choice == "1":
            pid = prompt_int("ID (entero): ")
            if inv.get(pid):
                print("ID ya existe en el inventario.")
                continue
            name = input("Nombre: ").strip()
            qty = prompt_int("Cantidad: ")
            price = prompt_float("Precio: ")
            desc = input("Descripción (opcional): ").strip()
            p = Product(pid, name, qty, price, desc)
            try:
                inv.add_product(p)
                db.insert_product(p)
                print("Producto añadido.")
            except Exception as e:
                print("Error añadiendo producto:", e)

        elif choice == "2":
            pid = prompt_int("ID a eliminar: ")
            removed = inv.remove_product(pid)
            if removed:
                db.delete_product(pid)
                print("Producto eliminado.")
            else:
                print("No se encontró producto con ese ID.")

        elif choice == "3":
            pid = prompt_int("ID a actualizar cantidad: ")
            if not inv.get(pid):
                print("No existe ese producto.")
                continue
            qty = prompt_int("Nueva cantidad: ")
            inv.update_quantity(pid, qty)
            db.update_product(inv.get(pid))
            print("Cantidad actualizada.")

        elif choice == "4":
            pid = prompt_int("ID a actualizar precio: ")
            if not inv.get(pid):
                print("No existe ese producto.")
                continue
            price = prompt_float("Nuevo precio: ")
            inv.update_price(pid, price)
            db.update_product(inv.get(pid))
            print("Precio actualizado.")

        elif choice == "5":
            term = input("Buscar nombre: ").strip()
            results = inv.find_by_name(term)
            if not results:
                print("No se encontraron productos.")
            else:
                for p in results:
                    print(p)

        elif choice == "6":
            allp = inv.list_all()
            if not allp:
                print("Inventario vacío.")
            else:
                for p in allp:
                    print(p)

        elif choice == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
