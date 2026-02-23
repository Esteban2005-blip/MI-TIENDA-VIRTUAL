from db import init_db


def main():
    init_db()
    print("Base de datos inicializada en ./data/inventory.db")


if __name__ == "__main__":
    main()
