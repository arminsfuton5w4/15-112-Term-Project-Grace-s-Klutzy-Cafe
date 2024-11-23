from cmu_graphics import *
import random
import copy

################################################################################
        # CLASSES
################################################################################

class Waitress:
    def __init__(self, x, y):
        self.x, self.y = x,y
    
    def draw(self, app):
        drawRect(self.x, self.y,50,100, fill='purple')
    
    def waitressPath(self, app):
        tables=layout.filledSeats
        visited=set()
        state=(False, tables, [])
        path=DFS(board, state, visited,())
        pathCoord=graphToCoord(app, path)
        return pathCoord

class Layout:
    def __init__(self,tables):
        self.tables=tables
        self.filledSeats=[]
    
    def isAtTable(self, other, app):
        x,y=coordToGraph(other.x, other.y)
        if (y, x) in self.tables:
            other.isAtTable=True

layout2=Layout([(0,4),(0,5),(1,4),(1,5), (2,1),(2,2),(3,1),(3,2), (2,7),(2,8),(3,7),(3,8)])
layout=Layout([(1,4),(3,2),(3,8)])

class Customer:
    def __init__(self, x, y):
            self.x, self.y = x,y
            self.orderBase, self.orderT1, self.orderT2=generateOrder(menu, allToppings)
            self.isAtTable=False
            self.mood=3 #3=happy, 2=impatient, 1=angry
    
    def __repr__(self):
        return f'{self.orderT1} {self.orderT2} {self.orderBase}'
    
    def customerPath(self,app):
        tables=layout.tables
        visited=set()
        state=(False, tables, [])
        path=DFS(board, state, visited, (0,9))
        path=state[-1]
        pathCoord=graphToCoord(app, path)
        return pathCoord

def graphToCoord(app, path):
    pathCoord=[]
    for i in range(len(path)):
        x=200+app.cellWidth*path[i][1]
        y=200+app.cellHeight*path[i][0]
        pathCoord.append((x,y))
    return pathCoord

def coordToGraph(coordX, coordY):
    x=(coordX-200)//50
    y=(coordY-200)//50
    return x,y

class Counter:
    def __init__(self):
        self.base=None
        self.topping1=None
        self.topping2=None
        self.coordinates=[(70,250), (120,280), (210,220), (160,190)]
# after drag into counter --> they become the items
# check 3 fields are field, display image

counter=Counter()

class Base:
    def __init__(self, name, link, x,y, price):
        self.name=name
        self.image=link
        self.x, self.y=x,y
        self.r=25
        self.price=price
    
    def __repr__(self):
        return f'{self.name}'
    
    def __hash__(self):
        return hash(str(self)) 

class Toppings:
    def __init__(self, name, link, x,y):
        self.name=name
        self.image=link
        self.x, self.y=x,y
        self.r=25
    
    def __repr__(self):
        return f'{self.name}'  

    def __hash__(self):
        return hash(str(self)) 

def distance(x0,y0,x1,y1):
    return (((x1-x0)**2+(y1-y0)**2)**0.5)

cakeRoll=Base('cake-roll', 'cmu://903290/33748782/0c726d7f441baf1ab17eb76c5f755f13.png',40, 140, 7.50)
crepeCake=Base('crepe-cake', 'cmu://903290/35264027/_+(5).jpeg',90, 110, 8.00)
sunday=Base('sunday', 'cmu://903290/35264045/_+(4).jpeg', 40, 210, 6.75)
milkTea=Base('milk-tea', 'cmu://903290/35227983/tokihyo_.jpeg', 90, 180, 5.50)
baseSet={cakeRoll, crepeCake, sunday, milkTea}

matcha=Toppings('matcha', 'cmu://903290/35266745/Trà+xanh+Matcha+Sencha+Gyokuro,+trà+xanh,+trà+Trung+Quốc,+món+ăn+png.jpeg',)
strawberry=Toppings('strawberry', 'cmu://903290/35266755/⊹+⋆ﾟ꒰ఎ+♡+໒꒱+⋆ﾟ⊹.jpeg',)
chocolate=Toppings('chocolate', 'cmu://903290/35266743/chocolate+png+#png.jpeg', )
ube=Toppings('ube', 'cmu://903290/35266738/Okinawa+Sweet+Potato.jpeg',)
redBean=Toppings('red-bean', 'cmu://903290/35266740/kidney+bean+organic+crops+red+kidney+beans.jpeg', )
mango=Toppings('mango', 'cmu://903290/35266750/(xiaohongshu+ID_+DAZHI_BUKUN)+digital+art+cute+pfp+icon+kawaii+mango+fruit+dog.jpeg', )
toppingSet={strawberry, mango, chocolate, ube, redBean, matcha}

ingredientList=[cakeRoll, crepeCake, sunday, milkTea, strawberry, mango, chocolate, ube, redBean]


menu=['cake-roll', 'milk-tea','sunday','crepe-cake']
menuPrice ={'cake-roll':7.50, 'milk-tea':5.50, 'sunday':6.75, 'crepe-cake':8.00}
allToppings=['strawberry', 'mango', 'matcha', 'chocolate', 'ube', 'red-bean']

class Orders:
    def __init__(self):
        self.orders=[]

orderList=Orders()

################################################################################
        # DFS
################################################################################

def makeAdjacencyList():
    adjList=dict()
    for row in range(4):
        for col in range(12):
            #four edge case: corners: 2 edges
            if row==0 and col==0:
                adjList[(row,col)]={(row+1, col), (row, col+1)}
            elif row==0 and col==11:
                adjList[(row,col)]={(row+1, col), (row, col-1)}
            elif row==3 and col==0:
                adjList[(row,col)]={(row-1, col), (row, col+1)}
            elif row==3 and col==11:
                adjList[(row,col)]={(row-1, col), (row, col-1)}
            #sides of the board: 3 edges
            elif row==0:
                adjList[(row,col)]={(row+1, col), (row, col-1), (row, col+1)}
            elif col==0:
                adjList[(row,col)]={(row-1, col), (row+1, col), (row, col+1)}
            elif row==3:
                adjList[(row,col)]={(row-1, col), (row, col-1), (row, col+1)}
            elif col==11:
                adjList[(row,col)]={(row-1, col), (row+1, col), (row, col-1)}
            #everything else: 4 edges
            else:
                adjList[(row, col)]={(row-1, col), (row+1, col), (row, col-1), (row, col+1)}
    return adjList

board=makeAdjacencyList()

def DFS(adjacencyList, state, s, v):
    b,target,L=state
    if v in s:
        return revisit(state, v)
    else:
        state=visit(state, v)
        s.add(v)
        for neighbor in adjacencyList.get(v,[]):
            state=DFS(adjacencyList, state, s, neighbor)
        state=finish(state, v)
    return state

def visit(state, v): 
    b,target,L=state
    if not b:
        L.append(v)
    if v in target:
        b=True
    return (b, target, L)
    
def revisit(state, v):
    return state

def finish(state, v):
    return state

################################################################################
        # OTHER
################################################################################

def generateOrder(menu, allToppings):
    toppings=copy.copy(allToppings)
    topping1=allToppings[random.randint(0,len(allToppings)-1)]
    toppings.remove(topping1)
    topping2=toppings[random.randint(0,len(toppings)-1)]
    base=menu[random.randint(0,len(menu)-1)]
    order=(base, topping1, topping2)
    orderList.orders.append(order)
    return order

def getRevenue(menu,tip):
    pass

#table locations & boundaries    

################################################################################
#MODEL
def onAppStart(app):
    app.width, app.height = 800,500
    app.rows, app.cols=4,12
    app.cellWidth, app.cellHeight = 50,50

    app.customers=[]
    app.isCooking=False
    app.revenue=0.00
    app.StepsPerSecond=1
    app.currIndex=0
    app.counter=0
    app.translucence=0 #0: opacity=0, 1: opacity=50, 2: opacity=100

    app.ingredientSize=45
    app.isDragging=False
    app.currItem

#VIEW
def drawTable(app):
    tableW, tableH, color=100,75,'red'         
    for i in range(3):
        if i%2==1:
            drawOval(450, 250, tableW, tableH, fill=color)
        else:
            drawOval(350+i*100,350,tableW, tableH, fill=color)
    
def drawOrderList(app):
    drawRect(375, 25, 150, 160, fill='blue', opacity=30)
    drawLabel('orders', 450, 45, bold=True)
    for i in range(len(app.customers)):
        customer=app.customers[i]
        drawLabel(f'{customer.orderT1} {customer.orderT2} {customer.orderBase}', 450, 65+i*15, size=10)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def getCellLeftTop(app, row, col):
    cellLeft = 200 + col * app.cellWidth
    cellTop = 200 + row * app.cellHeight
    return (cellLeft, cellTop)

def drawCell(app, rows, col):
    cellLeft, cellTop=getCellLeftTop(app, rows, col)
    cellWidth,cellHeight=50,50
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black', borderWidth=0.15)   

def drawDisplay(app):
    displayHeight=200
    drawRect(0, app.height-100, app.width, displayHeight, fill='blue', opacity=30)

def redrawAll(app):
    drawPolygon(70,250, 120,280, 210,220, 160,190)
    drawTable(app)
    drawOrderList(app)
    drawBoard(app)

    drawDisplay(app)
    w=Waitress(200,200)
    w.draw(app)
    
    for customer in app.customers:
        drawRect(customer.x, customer.y, 50,100, fill='red', align='center')

    for base in baseSet:
        size=base.r*2
        drawImage(base.link, base.x, base.y)
    
#CONTROLLER

def generateCustomer(app):
    newCustomer=Customer(700,200)
    app.customers.append(newCustomer)

def removeSeat(coordX,coordY, tables):
    x,y=coordToGraph(coordX, coordY)
    if (y,x) in tables:
        tables.remove((y,x))
    layout.filledSeats.append((y, x))

def moveCustomer(i, app):
    for customer in app.customers:
        layout.isAtTable(customer, app)
        if not customer.isAtTable:
            pathCoord=customer.customerPath(app)
            print('not at table:', customer)
            i%=len(pathCoord)
            customer.x, customer.y=pathCoord[i][0], pathCoord[i][1]
        else:
            removeSeat(customer.x, customer.y, layout.tables)

def onStep(app):
    app.counter+=1
    if app.counter%100==0 and len(app.customers)<3:
        print(app.customers)
        generateCustomer(app)
    if app.counter%10==0 and len(app.customers)>0:
        moveCustomer(app.currIndex, app)
        app.currIndex+=1

###################################
        # POINT in POLYGON
###################################

def pointInPolygon(coordinates, mouseX, mouseY):
    intersections=0
    for i in range(len(coordinates)-1):
        p1, p2=coordinates[i], coordinates[i+1]
        x1,y1=p1[0], p1[1]
        x2,y2=p2[0], p2[1]
        slope=((y2-y1)/(x2-x1))
        x=(mouseY-y1+slope*x1)/slope
        if x1<=x<=x2:
            intersections+=1
    return intersections%2==1

def inCounter(mouseX, mouseY):
    coordinates=counter.coordinates
    return pointInPolygon(coordinates, mouseX, mouseY)

#ingredients will just be circle pictures
def clickedIngredient(mouseX, mouseY):
    for item in ingredientList:
        d=distance(mouseX, mouseY, item.x, item.y)
        if d<=item.r:
            return (item, True)
    return (None, False)

def isCurrOrder(base, t1, t2):
    #check if item is part of the current order
    for order in orderList.orders:
        if ((base in order) or (t1 in order) or (t2 in order)):
            return True
    #check if the order is complete
    pass

def onMousePress(app, mouseX, mouseY):
    check=clickedIngredient(mouseX, mouseY)
    if check[1]:
        app.translucence=1
        app.currItem=check[0]
        app.isDragging=True
    # if (mouseX, mouseY) in #table coordinates

def onMouseDrag(app, mouseX, mouseY):
    ingredient=app.currItem[0]
    ingredient.x, ingredient.y=mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    if inCounter(mouseX, mouseY):
        if app.currItem in baseSet:
            counter.orderBase=app.currItem
        elif app.currItem in toppingSet:
            counter.orderT1=app.currItem
        #update Counter class with either...(1) Base, (2) Topping 1, (3) Topping 2
        if isCurrOrder(counter.orderBase, counter.orderT1, counter.orderT2):
            app.isDragging=False

def main():
    runApp()

main()
cmu_graphics.run()