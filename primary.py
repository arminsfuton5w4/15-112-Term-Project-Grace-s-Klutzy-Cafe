from cmu_graphics import *
import random
from PIL import Image
# from layout import * 

################################################################################
        # CLASSES
################################################################################

class Waitress:
    def __init__(self, x, y):
        self.x, self.y = x,y
        self.image=None
        self.whichOrder=None
        self.isWaitressAtNode=False
        self.isBackAtCounter=False
    
    def draw(self, app):
        drawImage('images/gothicWaitress.PNG',self.x, self.y,width=125,height=145, align='center')
    
    def waitressPath(self, start, target):
        visited=set()
        state=(False, [target], [])
        path=DFS(board, state, visited, start)
        path=state[-1]
        pathCoord=nodeToCoord(path)
        return pathCoord

waitressG=Waitress(200,200)

class Layout:
    def __init__(self,tables):
        self.tables=tables
        self.filledSeats=[]
    
    def isAtTable(self, other):
        x,y=coordToNode(other.x, other.y)
        if (y, x) in self.tables:
            other.isAtTable=True
    
    def isWaitressAtNode(self, other, target):
        print('target:', target)
        x,y=coordToNode(other.x, other.y)
        print('what am i even checking', (y,x))
        if y == target[1] and x==target[0]:
            print('target is equal to x,y')
            other.isWaitressAtNode=True
    
    def isBackAtCounter(self, other, target):
        x,y=coordToNode(other.x, other.y)
        if (y, x) == target:
            other.isBackAtCounter=True
    
    def isAtExit(self, other, target):
        x,y=coordToNode(other.x, other.y)
        if (y, x) == target:
            other.isAtExit=True

layout2=Layout([(0,4),(0,5),(1,4),(1,5), (2,1),(2,2),(3,1),(3,2), (2,7),(2,8),(3,7),(3,8)])
layout=Layout([(1,4),(3,2),(3,8)])

class Customer:
    def __init__(self, x, y):
        self.x, self.y = x,y
        self.orderBase, self.orderT1, self.orderT2=generateOrder()
        self.isAtTable=False
        self.time=10
        self.giveTip=self.orderBase.price*0.10
        self.leave=False
        self.isAtExit=False
    
    def __repr__(self):
        return f'{self.orderT1} {self.orderT2} {self.orderBase}'
    
    def customerPath(self, start, target):
        visited=set()
        state=(False, target, [])
        path=DFS(board, state, visited, start)
        path=state[-1]
        pathCoord=nodeToCoord(path)
        return pathCoord
    
    def howMuchTip(self):
        if 6<=self.time<=10:
            return self.giveTip
        elif 2<=self.time<=5:
            return self.giveTip-self.giveTip*0.5
        elif 0<=self.time<=1:
            return self.giveTip-self.giveTip*0.8
        else:
            return 0
    
#     def timeToLeave(self):
#         if self.time==0 or ateMyOrder(app):
#             return True
#         return False

# def ateMyOrder(app):
#     return app.orderDelivered

def nodeToCoord(path):
    pathCoord=[]
    if isinstance(path, list):
        for i in range(len(path)):
            x=200+50*path[i][1]
            y=200+50*path[i][0]
            pathCoord.append((x,y))
        return pathCoord
    elif isinstance(path, tuple):
        x=200+50*(path[1])
        y=200+50*(path[0])
        return (x,y)

def coordToNode(coordX, coordY):
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
    def __init__(self, name, link, x,y, price, ogXY):
        self.name=name
        self.image=CMUImage(Image.open(link))
        self.x, self.y=x,y
        self.r=25
        self.price=price
        self.ogXY=ogXY
    
    def __repr__(self):
        return f'{self.name}'
    
    def __hash__(self):
        return hash(str(self)) 

class Toppings:
    def __init__(self, name, link, x,y, ogXY):
        self.name=name
        self.image=CMUImage(Image.open(link))
        self.x, self.y=x,y
        self.r=25
        self.ogXY=ogXY
    
    def __repr__(self):
        return f'{self.name}'  

    def __hash__(self):
        return hash(str(self)) 

def distance(x0,y0,x1,y1):
    return (((x1-x0)**2+(y1-y0)**2)**0.5)

cakeRoll=Base('cake-roll', 'images/cakeRoll.PNG',50, 120, 7.50, (50, 120))
crepeCake=Base('crepe-cake', 'images/crepeCake.PNG',92, 100, 8.00, (92,105))
sunday=Base('sunday', 'images/sunday.PNG', 50, 190, 6.75, (50, 190))
milkTea=Base('milk-tea', 'images/boba2.PNG', 92, 165, 5.50, (92, 165))

baseSet={cakeRoll, crepeCake, sunday, milkTea}

matcha=Toppings('matcha', 'images/matcha.PNG',175, 60, (175,60))
strawberry=Toppings('strawberry', 'images/strawberry.PNG',215,45, (215,45))
chocolate=Toppings('chocolate', 'images/chocolate.PNG',252,28, (252,28))
ube=Toppings('ube', 'images/ube.PNG',175,128, (175,128))
redBean=Toppings('red-bean', 'images/redBean.PNG',215,115, (215,115))
mango=Toppings('mango', 'images/mango.PNG',252, 90, (252,90))

toppingSet={strawberry, mango, chocolate, ube, redBean, matcha}

ingredientList=[cakeRoll, crepeCake, sunday, milkTea, strawberry, mango, chocolate, ube, redBean, matcha]

menuPrice ={'cake-roll':7.50, 'milk-tea':5.50, 'sunday':6.75, 'crepe-cake':8.00}

class Orders:
    def __init__(self):
        self.orders=[]
        self.finished=[]
        self.delivered=[]

orderList=Orders()

class finalOrders:
    def __init__(self, base, t1, t2, link):
        self.link=link

################################################################################
        # DFS
        # Initial write-up assissted + taught by TA Lukas (lkebulad)
        # Later modified to fix some bugs + adjust to needs of my game
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
    b,target,L=state
    if not b:
        L.append(v)
    if v in target:
        b=True
    return (b, target, L)

################################################################################
        # OTHER
################################################################################

def generateOrder():
    toppings=list(toppingSet)
    topping1=toppings[random.randint(0,len(toppings)-1)]
    remaining_toppings=[topping for topping in toppings if topping!=topping1]
    topping2=remaining_toppings[random.randint(0,len(remaining_toppings)-1)]
    
    base=(list(baseSet))[random.randint(0,len(baseSet)-1)]
    order=(base, topping1, topping2)
    orderList.orders.append(order)
    print(orderList.orders)
    
    return order

class Revenue:
    def __init__(self):
        self.tip=0
        self.earning=0
        self.total=self.tip+self.earning

income=Revenue()

def calculateRevenue(menu,tip):
    for order in orderList.delivered:
        base=order.base
        income.earning+=base.price

    #revenue system for tipping
    pass

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
    app.wIndex=0

    app.isDragging=False
    app.currItem=None
    app.orderComplete=False
    app.clickedPerson=None
    app.goServe=False
    app.orderDelivered=False
    app.showMenu=False

#VIEW
def drawTable(app):
    tableW, tableH, color=125,100,'red'         
    for i in range(3):
        if i%2==1:
            drawImage('images/table.PNG', 450, 250, width=tableW, height=tableH, align='center')
        else:
            drawImage('images/table.PNG',350+i*100,350,width=tableW, height=tableH, align='center')
    
def drawOrderList(app):
    drawRect(375, 25, 150, 160, fill='blue', opacity=30)
    drawLabel('ORDERS:', 450, 45, bold=True)
    for i in range(len(app.customers)):
        customer=app.customers[i]
        drawLabel(f'{customer.orderT1} {customer.orderT2} {customer.orderBase}', 450, 65+i*15, size=10)

################################################################################
    #Draw board functions referenced my code from Tetris
################################################################################
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
    drawImage('images/display.PNG', 0,0, width=app.width, height=app.height)
    #display revenue
    #drawLabel({})
    #display currOrder
    if len(orderList.orders)>0:
        currOrder=orderList.orders[0]
        base, t1, t2=currOrder[0], currOrder[1], currOrder[2]
        w,h=75,75
        start, gap=50, 10
        drawImage(base.image, start, app.height-90, width=w, height=h)
        drawImage(t1.image, start+w+gap, app.height-90, width=w-10, height=h-10)
        drawImage(t2.image, start+2*(w+gap), app.height-90, width=w-10, height=h-10)


def redrawAll(app):
   
    drawImage('images/backdrop.PNG', 0,0, width=app.width, height=app.height+10)
    # drawPolygon(70,250, 120,280, 210,220, 160,190, fill='lavender')

    # drawTable(app)
    drawOrderList(app)
    drawBoard(app)

    drawDisplay(app)
    waitressG.draw(app)
    
    for customer in app.customers:
        drawImage('images/blueBunny.PNG', customer.x, customer.y, width=50,height=100, align='center')
        drawLabel(customer.time, customer.x, customer.y)

    for base in baseSet:
        size=base.r*2
        drawImage(base.image, base.x, base.y, align='center', width=size, height=size)
    
    for topping in toppingSet:
        size=topping.r*2
        drawImage(topping.image, topping.x, topping.y, align='center', width=size, height=size)
    drawTable(app)

    if app.showMenu:
        drawImage('images/menu.PNG', 0, 0, width=app.width,height=app.height, opacity=95)


#CONTROLLER

def generateCustomer(app):
    newCustomer=Customer(700,200)
    app.customers.append(newCustomer)

def removeSeat(coordX,coordY, tables):
    x,y=coordToNode(coordX, coordY)
    if (y,x) in tables:
        tables.remove((y,x))
    layout.filledSeats.append((y, x))

def moveCustomer(i, app):
    for customer in app.customers:
        layout.isAtTable(customer)
        if not customer.isAtTable:
            tables=layout.tables
            pathCoord=customer.customerPath((0,9), tables)
            i%=len(pathCoord)
            customer.x, customer.y=pathCoord[i][0], pathCoord[i][1]
        else:
            removeSeat(customer.x, customer.y, layout.tables)

def leaveCustomer(i, app):
    for customer in app.customers:
        if customer.leave:
            if not customer.isAtExit:
                pathCoord=customer.customerLeave()
                i%=len(pathCoord)
                customer.x, customer.y=pathCoord[i][0], pathCoord[i][1]

def whenOrderReady(app):
    if app.orderComplete:
        #ingredients move back to original position (track original position)
        orderBase, orderT1, orderT2 =counter.base, counter.topping1, counter.topping2
        #finalRender=finalOrders(orderBase, orderT1, orderT2)
        orderBase.x, orderBase.y=orderBase.ogXY
        orderT1.x, orderT1.y=orderT1.ogXY
        orderT2.x, orderT2.y=orderT2.ogXY
  
        #all counter attributes are reset back to none
        counter.base, counter.topping1, counter.topping2=None, None, None

        #replace all images on counter to image of final product
        
        #have waitress hold the final product image
        #wait for player to click on a customer to send the order to
        #if they walk to the wrong person...if they click on a new person(right or wrong)...
        #...the waitress should redirect path to the new person
        #if they walk to the right person, the order is DONE
        pass
    pass

def whenOrderDone(app):
    if app.orderDelivered:
        app.goServe=False
        wx, wy=coordToNode((waitressG.x, waitressG.y))
        waitressGoesBack=waitressG.waitressPath((wx, wy),(0,0))

        #app.orderComplete=False
        app.orderDelivered=False

    #when order is DONE, waitress makes her way BACK to the counter
    #and waits (for the next order to be finished) or picks up the next order
    #SIMULTANEOUSLY, customer with this order LEAVES
    pass

def countDown(app):
    for customer in app.customers:
        if customer.time<=0 and orderList.orders!=[]:
            orderList.orders.pop(0)
        else:
            customer.time-=0.5

def onStep(app):
    app.counter+=1
    if app.counter%100==0 and len(app.customers)<3:
        print(app.customers)
        generateCustomer(app)
        app.isCooking=True
    if app.counter%100==0 and len(orderList.orders)>0:
        countDown(app)
    if orderList.orders==[]:
        app.isCooking=False
    #Customer Movement
    if app.counter%10==0 and len(orderList.orders)>0:
        moveCustomer(app.currIndex, app)
        leaveCustomer(app.currIndex, app)
        app.currIndex+=1
    #Waitress Movement
    if app.goServe:
        moveWaitress(app.wIndex, app, waitressG)
        app.wIndex+=1
    if app.orderDelivered:
        app.wIndex=0
        goBackCounter(app.wIndex, waitressG)
        app.wIndex+=1
        

################################################################################
        # POINT in POLYGON    
        # general concept + math explained by TA, wrote code myself 
################################################################################

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

def isCurrOrderComplete(base, t1, t2, app):
    print('base:', base, 't1:', t1, 't2:', t2)
    currOrder=orderList.orders[0]
    #check if the order is complete
    if base==currOrder[0] and (t1==currOrder[1] or t1==currOrder[2]) and (t2==currOrder[2] or t2==currOrder[1]):
        app.orderComplete=True
        waitressG.whichOrder=currOrder
        orderList.finished.append(currOrder)
        orderList.orders.pop(0)
        print('order is complete!')
        whenOrderReady(app)
        return True

def isInCurrOrder(currItem):
    currOrder=orderList.orders[0]
    print('current order is:', currOrder)
    if currItem in currOrder:
        return True
    return False
    #check if item is part of the current order

def clickedPerson(mouseX, mouseY, app):
    for node in layout.filledSeats: #(x,y)
        print('node:', node)
        coordinates=nodeToCoord(node) #(200,300, left/top)
        print(coordinates)
        if coordinates!=None:
            coordX, coordY=(coordinates[0]+app.cellWidth/2), (coordinates[1]+app.cellHeight/2) #xchange to center
            d=distance(mouseX, mouseY, coordX, coordY)
            if d<app.cellWidth:
                print(node, True)
                return (node, True)
        return (None, False)

def moveWaitress(i, app, waitress):
    for node in layout.filledSeats:
        if node==app.clickedPerson:
            target=node
    layout.isWaitressAtNode(waitress, target)
    if not layout.isWaitressAtNode(waitress, target):
        pathCoord=waitress.waitressPath((0,0), target)
        i%=len(pathCoord)
        waitress.x, waitress.y=pathCoord[i][0], pathCoord[i][1]
        wx,wy=coordToNode(waitress.x, waitress.y)
        print('at node:', (wy,wx))
        print('not at node yet!')
    else:
        #check if waitress order matches customer order
        print('reached node!')
        if waitress.whichOrder==orderList.finisihed[-1]:
            app.orderDelivered=True
            orderList.delivered.append(orderList.finished[-1])
        app.goServe=False

def goBackCounter(i, waitress):
    if not layout.isBackAtCounter(waitress, (0,0)):
        wx, wy=coordToNode(waitress.x, waitress.y)
        pathCoord=waitress.waitressPath((wx,wy),(0,0))
        i%=len(pathCoord)
        waitress.x, waitress.y=pathCoord[i][0], pathCoord[i][1]

def onMousePress(app, mouseX, mouseY):
    if app.isCooking:
        check=clickedIngredient(mouseX, mouseY)
        if check[1]:
            app.currItem=check[0]
            app.isDragging=True
    if app.orderComplete:
        checkPerson=clickedPerson(mouseX, mouseY, app)
        if checkPerson!=None:
            if checkPerson[1]:
                app.goServe=True
                app.clickedPerson=checkPerson[0]
    if insideMenuButton(mouseX, mouseY, app):
        app.showMenu=True

def insideMenuButton(mouseX, mouseY, app):
    buttonLeft, buttonTop, buttonSize=(app.width-75), 60,50
    right=buttonLeft+buttonSize
    bottom=buttonTop+buttonSize
    if (buttonLeft<=mouseX<=right) and (buttonTop<=mouseY<=bottom):
        return True

def onMouseDrag(app, mouseX, mouseY):
    if app.isCooking:
        ingredient=app.currItem
        if ingredient!=None:
            ingredient.x, ingredient.y=mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.isCooking:
        if inCounter(mouseX, mouseY):
            #Checks for property of currItem - base or topping - & updates counter
            if app.currItem in baseSet:
                counter.base=app.currItem
                print('base:', counter.base)
            elif app.currItem in toppingSet and counter.topping1==None:
                counter.topping1=app.currItem
                print('t1:', counter.topping1)
            elif app.currItem in toppingSet and counter.topping2==None:
                counter.topping2=app.currItem
                print('t2:', counter.topping2)
            # elif app.currItem in toppingSet and counter.topping1!=None and counter.topping2!=None:
            #     counter.topping1=app.currItem

            #Checks if the currItem is in the currOrder
            if isInCurrOrder(app.currItem):
                print('it belongs to the order!')
                app.currItem.x, app.currItem.y=mouseX, mouseY
            else:
                print('not part of the order!')
                if app.currItem==counter.topping1:
                    counter.topping1=None
                if app.currItem==counter.topping2:
                    counter.topping2=None
                if app.currItem==counter.base:
                    counter.base=None
                app.currItem.x, app.currItem.y=app.currItem.ogXY
            isCurrOrderComplete(counter.base, counter.topping1, counter.topping2, app)
        else:
            if app.currItem!=None: 
                app.currItem.x, app.currItem.y=app.currItem.ogXY
    if app.showMenu:
        app.showMenu=False

def main():
    runApp()

main()
cmu_graphics.run()