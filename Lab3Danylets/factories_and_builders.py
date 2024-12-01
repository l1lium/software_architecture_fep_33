from models import SmallItem, HeavyItem, RefrigeratedItem, LiquidItem, LightWeightShip, MediumShip, HeavyShip

class ItemFactory:
    @staticmethod
    def create_item(item_type, id, weight, count, container_id):
        if item_type == 'small':
            return SmallItem(id, weight, count, container_id)
        elif item_type == 'heavy':
            return HeavyItem(id, weight, count, container_id)
        elif item_type == 'refrigerated':
            return RefrigeratedItem(id, weight, count, container_id)
        elif item_type == 'liquid':
            return LiquidItem(id, weight, count, container_id)
        else:
            raise ValueError(f"Unknown item type: {item_type}")

class ShipBuilder:
    def __init__(self):
        self._id = None
        self._fuel_capacity = 0
        self._container_capacity = 0

    def set_id(self, id):
        self._id = id
        return self

    def set_fuel_capacity(self, fuel_capacity):
        self._fuel_capacity = fuel_capacity
        return self

    def set_container_capacity(self, container_capacity):
        self._container_capacity = container_capacity
        return self

    def build_lightweight_ship(self):
        return LightWeightShip(self._id, self._fuel_capacity, self._container_capacity)

    def build_medium_ship(self):
        return MediumShip(self._id, self._fuel_capacity, self._container_capacity)

    def build_heavy_ship(self):
        return HeavyShip(self._id, self._fuel_capacity, self._container_capacity)