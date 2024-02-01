import random

PLAYER_SIZE = 50
WALL_SIZE = 50


class Map:
    @staticmethod
    def load_map(filename):
        with open(filename, 'r') as f:
            map_info = f.readlines()
        return [line.strip() for line in map_info]

    @staticmethod
    def generate_objects(map_info):
        object_counts = map_info[0].strip().split(',')
        object_counts = {obj.split(':')[0]: int(obj.split(':')[1]) for obj in object_counts}

        map_width = len(map_info[1])
        map_height = len(map_info) - 1

        valid_positions = [(x * PLAYER_SIZE, y * PLAYER_SIZE) for y in range(map_height) for x in range(map_width)
                           if map_info[y + 1][x] == ' ']

        diamonds = []
        bombs = []
        aqua_suits = []

        for obj_type, count in object_counts.items():
            for _ in range(count):
                pos = random.choice(valid_positions)
                valid_positions.remove(pos)
                if obj_type == 'D':
                    diamonds.append(pos)
                elif obj_type == 'B':
                    bombs.append(pos)
                elif obj_type == 'T':
                    aqua_suits.append(pos)

        return diamonds, bombs, [], [], aqua_suits
