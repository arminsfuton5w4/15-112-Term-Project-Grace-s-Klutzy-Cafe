
def pointInPolygon(coordinates, mouseX, mouseY):
    intersections=0
    n=len(coordinates)
    for i in range(n):
        p1, p2=coordinates[i], coordinates[(i+1)%n]
        x1,y1=p1
        x2,y2=p2
        slope=((y2-y1)/(x2-x1))
        x=(mouseY-y1+slope*x1)/slope
        if x1<=x<=x2:
            intersections+=1
    return intersections%2==1

coordinates=[(70,250), (120,280), (210,220), (160,190)]
print(pointInPolygon(coordinates, 100, 250))