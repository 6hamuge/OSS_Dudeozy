import math
import collections
import time
from queue import PriorityQueue
from main.models import *

Point = collections.namedtuple("Point", ["x", "y"])

Hmap = {}
TileValue_Map = {}

# 시간 측정 데코레이터 함수
def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("Elapsed time [{}]: {:.6f} sec".format(original_fn.__name__, end_time - start_time))
        return result

    return wrapper_fn

# 현재 위치에서 목적지까지의 거리 - manheten distance
def Heuristic(a, b):
    return abs(a.q - b.q) + abs(a.r - b.r)

# Heuristic function for hexagonal grid (Diagonal distance)
def HexHeuristic(a, b):
    return (abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2

class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __hash__(self):
        return hash((self.q, self.r))

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current node to end
        self.f = 0  # Total cost: g + h
        self.cost = 0  # Cost of traversing this tile
        self.TileValue = 0  # Value associated with this tile
        self.TileValue_sum = 0  # Accumulated value to reach this tile

# Function to calculate costs from various geographic data
@logging_time
def giveCost(startx, starty, endx, endy):
    # Fetch data from database models
    loadpoint = Loadpoint.objects.filter(lon__range=(endx, startx), lat__range=(endy, starty)).order_by('lat')
    lamp = Lamp.objects.filter(lon__range=(endx, startx), lat__range=(endy, starty)).order_by('lat')
    cctv = Cctv.objects.filter(lon__range=(endx, startx), lat__range=(endy, starty)).order_by('lat')
    securitycenter = Securitycenter.objects.filter(lon__range=(endx, startx), lat__range=(endy, starty)).order_by('lat')
    alltimeshop = Alltimeshop.objects.filter(lon__range=(endx, startx), lat__range=(endy, starty)).order_by('lat')

    # Process each type of data and update Hmap
    for coor in alltimeshop:
        hex_point = Hex(int(coor.lon), int(coor.lat))
        if hex_point in Hmap:
            Hmap[hex_point] = Hmap[hex_point] + 1

    for coor in securitycenter:
        hex_point = Hex(int(coor.lon), int(coor.lat))
        if hex_point in Hmap:
            Hmap[hex_point] = Hmap[hex_point] + 1

    for coor in cctv:
        hex_point = Hex(int(coor.lon), int(coor.lat))
        if hex_point in Hmap:
            Hmap[hex_point] = Hmap[hex_point] + 1

    for coor in loadpoint:
        hex_point = Hex(int(coor.lon), int(coor.lat))
        if hex_point in Hmap:
            Hmap[hex_point] = Hmap[hex_point] + 1

    for coor in lamp:
        hex_point = Hex(int(coor.lon), int(coor.lat))
        if hex_point in Hmap:
            Hmap[hex_point] = Hmap[hex_point] + 1

# A* algorithm to find the shortest path on hexagonal grid
@logging_time
def astar(starthex, endhex, mapsize):
    startNode = Node(None, starthex)
    endNode = Node(None, endhex)
    openList = []
    closeList = []

    openList.append(startNode)

    max_h = Heuristic(starthex, endhex)

    while openList:
        currentNode = openList[0]
        currentIdx = 0

        for index, item in enumerate(openList):
            if item.TileValue < currentNode.TileValue:
                currentNode = item
                currentIdx = index

        openList.pop(currentIdx)
        closeList.append(currentNode)

        if currentNode.position == endNode.position:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []

        neighbor = get_hex_neighbors(currentNode.position)

        for newPosition in neighbor:
            if Hmap.get(newPosition) is not None:
                TileCost = Hmap[newPosition]
            else:
                continue

            new_node = Node(currentNode, newPosition)

            if new_node in closeList:
                continue

            new_node.cost = int(TileCost)
            new_node.g = int(currentNode.g) + 1
            new_node.h = int(HexHeuristic(new_node.position, endhex))
            new_node.f = new_node.g + new_node.h

            new_node.TileValue = 1 / (1 + new_node.cost) + (new_node.f / max_h)
            new_node.TileValue_sum = currentNode.TileValue_sum + new_node.TileValue

            TileValue_Map[new_node.position] = new_node.TileValue

            if new_node in openList:
                idx = openList.index(new_node)
                if new_node.TileValue < openList[idx].TileValue:
                    openList.pop(idx)
                else:
                    continue

            children.append(new_node)

        children = sorted(children, key=lambda Node: Node.TileValue, reverse=True)
        openList = openList + children

    path = []
    for ch in closeList:
        path.append(ch.position)
    return path[::-1]


# Function to get neighbors of a hex in the grid
def get_hex_neighbors(hex_position):
    q, r = hex_position.q, hex_position.r
    neighbors = [
        Hex(q + 1, r - 1), Hex(q + 1, r), Hex(q, r + 1),
        Hex(q - 1, r + 1), Hex(q - 1, r), Hex(q, r - 1)
    ]
    return neighbors

# Function to initialize and start the pathfinding process
@logging_time
def startSetting(start_coordinate, end_coordinate):
    startX = float(start_coordinate[1])
    startY = float(start_coordinate[0])
    endX = float(end_coordinate[1])
    endY = float(end_coordinate[0])

    # Calculate center and grid parameters (similar to hexgrid.Grid initialization)
    center_q = (startX + endX) / 2
    center_r = (startY + endY) / 2
    rate = 110.574 / (111.320 * math.cos(37.55582994870823 * math.pi / 180))
    grid_size = Point(rate * 0.00004, 0.00004)

    # Start and end points in hex coordinates
    sPoint = Hex(startX, startY)
    ePoint = Hex(endX, endY)

    # Determine the map size based on the maximum absolute value of q or r
    map_size = max(abs(sPoint.q), abs(sPoint.r))

    # Expand the map size to include potential neighbors
    real_hexMap_size = int(map_size + 15)

    # Create left and right corner points
    LeftCorner = (center_q - grid_size.x * real_hexMap_size, center_r - grid_size.y * real_hexMap_size)
    RightCorner = (center_q + grid_size.x * real_hexMap_size, center_r + grid_size.y * real_hexMap_size)

    startx, starty = LeftCorner[0], LeftCorner[1]
    endx, endy = RightCorner[0], RightCorner[1]

    # Adjust the range for fetching database data
    if endx > startx:
        temp = endx
        endx = startx
        startx = temp
    if endy > starty:
        temp = endy
        endy = starty
        starty = temp

    neighbor = get_hex_neighbors(Hex(center_q, center_r))

    for hex in neighbor:
        Hmap[hex] = 0

    giveCost(startx, starty, endx, endy)

    path = astar(sPoint, ePoint, map_size)
    
    grid_object = {
       'grid_size': (grid_size.x, grid_size.y),
        'map_size': map_size,
        'real_hexMap_size': real_hexMap_size,
        'start_corner': (startx, starty),
        'end_corner': (endx, endy),
        'neighbor': neighbor,  # Optional: Include if needed
        'path': path,  # Optional: Include if needed
    }

    return Hmap, path, TileValue_Map, grid_object
