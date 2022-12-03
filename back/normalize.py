def getLimits(bodyPoints):
    topLeft = [1, 1]
    bottomRight = [0, 0]
    for i in range(len(bodyPoints)):
        topLeft[0] = bodyPoints[i][0] if bodyPoints[i][0] < topLeft[0] else topLeft[0]
        topLeft[1] = bodyPoints[i][1] if bodyPoints[i][1] < topLeft[1] else topLeft[1]
        bottomRight[0] = bodyPoints[i][0] if bodyPoints[i][0] > bottomRight[0] else bottomRight[0]
        bottomRight[1] = bodyPoints[i][1] if bodyPoints[i][1] > bottomRight[1] else bottomRight[1]

    return (topLeft, bottomRight)


def normalizeXY(bodyPoints):
    normPoints = []
    
    limits = getLimits(bodyPoints)
    
    topLeft = limits[0]
    bottomRight = limits[1]
        
    for i in range(len(bodyPoints)):
        normPoint = []
        normPoint.append((bodyPoints[i][0] - topLeft[0]) / (bottomRight[0]-topLeft[0]))
        normPoint.append((bodyPoints[i][1] - topLeft[1]) / (bottomRight[1]-topLeft[1]))
        normPoint.append(bodyPoints[i][2])
        normPoints.append(normPoint)
        
    return normPoints