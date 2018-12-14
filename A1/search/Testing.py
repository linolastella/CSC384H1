if state[1:].count(False) == 1:  # missing one corner
    return ClosestCornerDistance(x1, y1)[0]

if state[1:].count(False) == 2:  # missing two corners
    FirstCorner = ClosestCornerDistance(x1, y1)

    x2, y2 = FirstCorner[1]
    Dist = FirstCorner[0]

    return Dist + ClosestCornerDistance(x2, y2)[0]

if state[1:].count(False) == 3:  # missing three corners
    FirstCorner = ClosestCornerDistance(x1, y1)

    x2, y2 = FirstCorner[1]
    Dist1 = FirstCorner[0]

    SecondCorner = ClosestCornerDistance(x2, y2)

    x3, y3 = SecondCorner[1]
    Dist2 = SecondCorner[0]

    return Dist1 + Dist2 + ClosestCornerDistance(x3, y3)[0]

# missing all corners
FirstCorner = ClosestCornerDistance(x1, y1)

x2, y2 = FirstCorner[1]
Dist1 = FirstCorner[0]

SecondCorner = ClosestCornerDistance(x2, y2)

x3, y3 = SecondCorner[1]
Dist2 = SecondCorner[0]

ThirdCorner = ClosestCornerDistance(x3, y3)

x4, y4 = ThirdCorner[1]
Dist3 = ThirdCorner[0]

return Dist1 + Dist2 + Dist3 + ClosestCornerDistance(x4, y4)[0]