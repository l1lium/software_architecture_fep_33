from factories_and_builders import ItemFactory, ShipBuilder
from models import Port

def main():
    # Створення предметів через фабрику
    small_item = ItemFactory.create_item("small", 1, 10, 2, 3)
    heavy_item = ItemFactory.create_item("heavy", 2, 50, 1, 4)

    # Створення корабля через будівельник
    builder = ShipBuilder()
    lightweight_ship = builder.set_id(1).set_fuel_capacity(100).set_container_capacity(5).build_lightweight_ship()

    # Створення порту і взаємодія з кораблем
    port = Port(id=1, latitude=40.7128, longitude=-74.0060)  # Координати порту
    port.add_ship(lightweight_ship)
    print(f"Корабель додано в порт: {port}")

if __name__ == "__main__":
    main()