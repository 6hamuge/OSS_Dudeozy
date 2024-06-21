import math
import collections
import time
from main.models import *

Point = collections.namedtuple("Point", ["x", "y"])

# Assuming Hmap and TileValue_Map are global variables
Hmap = {}
TileValue_Map = {}

class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __hash__(self):
        return hash((self.q, self.r))
    
# 시간 측정 데코레이터 함수
def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("소요시간 [{}]: {:.6f} sec".format(original_fn.__name__, end_time - start_time))
        return result

    return wrapper_fn

# 현재 위치에서 목적지까지의 거리 - Manhattan distance
def Heuristic(a, b) :   
    # type : (Hex(q,r), Hex(q,r))
    dx = a.q - b.q
    dy = a.r - b.r

    if dx == dy :
        return abs(dx + dy)
    else :
        return max(abs(dx), abs(dy))

# Heuristic function for hexagonal grid (Diagonal distance)
def HexHeuristic(a, b):
    return (abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2

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

# Function to get neighbors of a hex in the grid
def get_hex_neighbors(hex_position):
    q, r = hex_position.q, hex_position.r
    neighbors = [
        Hex(q + 1, r - 1), Hex(q + 1, r), Hex(q, r + 1),
        Hex(q - 1, r + 1), Hex(q - 1, r), Hex(q, r - 1)
    ]
    return neighbors

@logging_time
def giveCost(startx, starty, endx, endy):
    global Hmap
    
    # Clear Hmap before updating
    Hmap.clear()

    # x: lon, y: lat 순으로 데이터베이스 쿼리 수정
    loadpoints = Loadpoint.objects.filter(lon__range=(endy, starty), lat__range=(endx, startx)).order_by('lat')
    lamps = Lamp.objects.filter(lon__range=(endy, starty), lat__range=(endx, startx)).order_by('lat')
    cctvs = Cctv.objects.filter(lon__range=(endy, starty), lat__range=(endx, startx)).order_by('lat')
    securitycenters = Securitycenter.objects.filter(lon__range=(endy, starty), lat__range=(endx, startx)).order_by('lat')
    alltimeshops = Alltimeshop.objects.filter(lon__range=(endy, starty), lat__range=(endx, startx)).order_by('lat')
    
    
    # Log the number of loaded data points
    print(f"Loaded data points:")
    print(f"Loadpoints: {loadpoints.count()}")
    print(f"CCTVs: {cctvs.count()}")
    print(f"Alltimeshops: {alltimeshops.count()}")
    print(f"Lamps: {lamps.count()}")
    print(f"Securitycenters: {securitycenters.count()}")

    # Process each type of data and update Hmap
    for coor in loadpoints:
        lon = float(coor.lon)
        lat = float(coor.lat)
        hex_point = Hex(lat, lon)
        if hex_point in Hmap:
            Hmap[hex_point] += 1
        else:
            Hmap[hex_point] = 1

    for coor in cctvs:
        lon = float(coor.lon)
        lat = float(coor.lat)
        hex_point = Hex(lat, lon)
        if hex_point in Hmap:
            Hmap[hex_point] += 1
        else:
            Hmap[hex_point] = 1

    for coor in alltimeshops:
        lon = float(coor.lon)
        lat = float(coor.lat)
        hex_point = Hex(lat, lon)
        if hex_point in Hmap:
            Hmap[hex_point] += 1
        else:
            Hmap[hex_point] = 1

    for coor in lamps:
        lon = float(coor.lon)
        lat = float(coor.lat)
        hex_point = Hex(lat, lon)
        if hex_point in Hmap:
            Hmap[hex_point] += 1
        else:
            Hmap[hex_point] = 1

    for coor in securitycenters:
        lon = float(coor.lon)
        lat = float(coor.lat)
        hex_point = Hex(lat, lon)
        if hex_point in Hmap:
            Hmap[hex_point] += 1
        else:
            Hmap[hex_point] = 1


@logging_time
def astar(starthex, endhex):
    global Hmap, TileValue_Map

    startNode = Node(None, starthex)
    endNode = Node(None, endhex)
    openList = []
    closeList = []

    openList.append(startNode)

    max_h = Heuristic(starthex, endhex)

    step = 0

    while openList:
        step += 1
        print(f"Step {step}: Number of nodes in openList = {len(openList)}")

        currentNode = min(openList, key=lambda node: node.f)
        openList.remove(currentNode)
        closeList.append(currentNode)

        print(f"Expanding node: {currentNode.position}")

        if currentNode.position == endNode.position:
            print("Found the end node. Constructing the path...")
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        neighbor = get_hex_neighbors(currentNode.position)
        for newPosition in neighbor:
            if newPosition not in Hmap:
                continue

            TileCost = Hmap[newPosition]

            new_g = currentNode.g + 1
            new_h = HexHeuristic(newPosition, endhex)
            new_f = new_g + new_h

            in_close = False
            for node in closeList:
                if node.position == newPosition:
                    in_close = True
                    break
            if in_close:
                continue

            new_node = Node(currentNode, newPosition)
            new_node.g = new_g
            new_node.h = new_h
            new_node.f = new_f
            new_node.TileValue = 1 / (1 + TileCost) + (new_f / max_h)
            new_node.TileValue_sum = currentNode.TileValue_sum + new_node.TileValue

            in_open = False
            for node in openList:
                if node.position == newPosition:
                    in_open = True
                    if node.f > new_f:
                        node.parent = currentNode
                        node.g = new_g
                        node.h = new_h
                        node.f = new_f
                        node.TileValue = 1 / (1 + TileCost) + (new_f / max_h)
                        node.TileValue_sum = currentNode.TileValue_sum + node.TileValue
                    break
            if not in_open:
                openList.append(new_node)
                print(f"Added new node to openList: {new_node.position}")

    # No path found
    print("No path found.")
    return None

@logging_time
def startSetting(start_coordinate, end_coordinate):
    global Hmap, TileValue_Map
    
    startX = float(start_coordinate[1])
    startY = float(start_coordinate[0])
    endX = float(end_coordinate[1])
    endY = float(end_coordinate[0])

    sPoint = Hex(startX, startY)
    ePoint = Hex(endX, endY)

    # Calculate map boundaries based on start and end coordinates
    center_q = (startX + endX) / 2
    center_r = (startY + endY) / 2
    rate = 110.574 / (111.320 * math.cos(37.55582994870823 * math.pi / 180))
    grid_size = Point(rate * 0.00004, 0.00004)

    map_size = max(abs(sPoint.q), abs(sPoint.r))
    real_hexMap_size = int(map_size + 15)

    LeftCorner = (center_q - grid_size.x * real_hexMap_size, center_r - grid_size.y * real_hexMap_size)
    RightCorner = (center_q + grid_size.x * real_hexMap_size, center_r + grid_size.y * real_hexMap_size)

    startx, starty = LeftCorner[0], LeftCorner[1]
    endx, endy = RightCorner[0], RightCorner[1]

    # Ensure startx is less than endx and starty is less than endy
    if endx > startx:
        temp = endx
        endx = startx
        startx = temp
    if endy > starty:
        temp = endy
        endy = starty
        starty = temp

    # Log the range of coordinates being queried
    print(f"Querying data for range: ({startx}, {starty}) to ({endx}, {endy})")

    # Initialize neighbors for the center point
    neighbor = get_hex_neighbors(Hex(center_q, center_r))
    for hex in neighbor:
        Hmap[hex] = 0

    # Update Hmap with data from various sources
    giveCost(startx, starty, endx, endy)

    print("Before calling astar")
    path = astar(sPoint, ePoint)
    print("After calling astar")

    grid_object = {
        'grid_size': (grid_size.x, grid_size.y),
        'map_size': map_size,
        'real_hexMap_size': real_hexMap_size,
        'start_corner': (startx, starty),
        'end_corner': (endx, endy),
        'neighbor': neighbor,
        'path': path,
    }

    return Hmap, path, TileValue_Map, grid_object