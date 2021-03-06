import numpy as np

class MapStack:
    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny
        self.nb_layers = None
        self.maps = []

    def add_layer(self, map):
        if len(map.shape) == 2 and map.shape[0] == self.ny and map.shape[1] == self.nx:
            self.maps.append(map)
            self.nb_layers = len(self.maps)
            return "Map sucessfully added."
        else:
            return "Could not add map. Incompatible dimensions."


def compute(map_stack, map):
    status = map_stack.add_layer(map)
    return status, map_stack


if __name__ == "__main__":
    nx = 200
    ny = 200
    ms = MapStack(nx, ny)
    for i in range(10):
        ms.add_layer(np.random.rand(nx, ny))
    
    status, ms = compute(ms, np.random.rand(nx, ny))

    print(status, ms.nb_layers)

    assert ms.nb_layers == 11

