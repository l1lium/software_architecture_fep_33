import unittest
from factories_and_builders import ItemFactory, ShipBuilder
from models import LightWeightShip, Port

class TestFactoryAndBuilder(unittest.TestCase):
    def test_item_factory(self):
        item = ItemFactory.create_item("small", 1, 10, 2, 3)
        self.assertEqual(item.get_total_weight(), 20)

    def test_ship_builder(self):
        builder = ShipBuilder()
        ship = builder.set_id(1).set_fuel_capacity(100).set_container_capacity(5).build_lightweight_ship()
        self.assertIsInstance(ship, LightWeightShip)
        self.assertEqual(ship._fuel_capacity, 100)

    def test_port_operations(self):
        port = Port(id=1, latitude=40.7128, longitude=-74.0060)
        ship = LightWeightShip(id=1, fuel_capacity=100, container_capacity=5)
        port.add_ship(ship)
        self.assertIn(ship, port._ships)

if __name__ == "__main__":
    unittest.main()