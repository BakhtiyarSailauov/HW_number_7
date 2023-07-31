from models import Flower


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []

    def get_all(self) -> Flower:
        return self.flowers

    def save(self, flower: Flower):
        flower.id = len(self.flowers) + 1
        self.flowers.append(flower)

    def get_by_id(self, id: int) -> Flower:
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None