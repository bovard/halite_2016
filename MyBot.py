from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("bovard")

countCache = {}
maxedCols = []
maxedRows = []

def findCountToEndOfAllies(location, d):
    max = gameMap.height
    if d == EAST or d == WEST:
        max = gameMap.width

    # if we've already gone the max in this rowl/column before, return
    if (d == NORTH or d == SOUTH) and location.y in maxedCols:
        return max
    if (d == EAST or d == WEST) and location.x in maxedRows:
        return max

    i = 0
    while i < max and gameMap.getSite(location, d).owner == myID:
        i += 1
        location = gameMap.getLocation(location, d)
        if countCache.get(str(location)):
            return i + countCache[str(location)]

    # if we've gone the max, update
    if i == max:
        if d == NORTH or d == SOUTH:
            maxedCols.append(location.y)
        else:
            maxedRows.append(location.x)

    return i


def move(location):
    site = gameMap.getSite(location)
    allies = 0
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID and neighbour_site.strength < site.strength:
            return Move(location, d)
        if neighbour_site.owner == myID:
            allies += 1
    if allies < 4:
        countCache[str(location)] = 0
    if site.strength < site.production * 5:
        return Move(location, STILL)
    if allies == 4:
        counts = [findCountToEndOfAllies(location, d) for d in CARDINALS]
        d = counts.index(min(counts)) + 1
        countCache[str(location)] = min(counts)
        return Move(location, d)

    return Move(location, STILL)

while True:
    moves = []
    countCache = {}
    maxedCols = []
    maxedRows = []
    gameMap = getFrame()

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)
