from cmu_graphics import *
import random
from PIL import Image
from urllib.request import urlopen
import os, pathlib
# from layout import * 

################################################################################
        # Fixing speed of the program, credit to Professor Kosbie
################################################################################

imagePathToCmuImageMap = dict()

def fixImage(imagePath):
    if imagePath in imagePathToCmuImageMap:
        return imagePathToCmuImageMap[imagePath]
    else:
        absPath = '/Users/gh/Documents/GitHub/oneTwelveTP/' + imagePath
        pilImage=Image.open(absPath)
        cmuImage = CMUImage(pilImage)
        imagePathToCmuImageMap[imagePath] = cmuImage
        return cmuImage

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
    
    def draw(self):
        drawImage(fixImage('images/gothicWaitress.PNG'),self.x, self.y,width=125,height=145, align='bottom-left')
    
    def waitressPath(self, start, target):
        visited=set()
        state=(False, [target], [])
        path=DFS(board, state, visited, start)
        path=state[-1]
        pathCoord=nodeToCoord(path)
        return pathCoord

waitressG=Waitress(200,350)

class Layout:
    def __init__(self,tables):
        self.tables=tables
        self.filledSeats=set()
    
    def isAtTable(self, other):
        x,y=coordToNode(other.x, other.y)
        if (y, x) in self.tables:
            other.isAtTable=True
    
    def isWaitressAtNode(self, other, target):
        x,y=coordToNode(other.x, other.y)
        if (y,x)==target:
            print('waitress STOPP y,x')
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
    def __init__(self, x, y, skin):
        self.x, self.y = x,y
        self.skin=skin
        self.orderBase, self.orderT1, self.orderT2=generateOrder()
        self.order=(self.orderBase, self.orderT1, self.orderT2)
        self.seat=None
        self.isAtTable=False
        self.time=10
        self.giveTip=self.orderBase.price*0.10
        self.leave=False
        self.isAtExit=False
        self.pathIndex=0
    
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
            return pythonRound(rounded(self.giveTip), 2)
        elif 2<=self.time<=5:
            self.giveTip=self.giveTip-self.giveTip*0.5
            return pythonRound(rounded(self.giveTip), 2)
        elif 0<=self.time<=1:
            self.giveTip=self.giveTip-self.giveTip*0.8
            return pythonRound(rounded(self.giveTip), 2)
        else:
            return 0.00
    
    def timeToLeave(self):
        if self.time==0 or self.leave==True:
            return True
        return False

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

counter=Counter()

class Base:
    def __init__(self, name, link, x,y, price, ogXY):
        self.name=name
        self.image=link
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
        self.image=link
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

class Orders:
    def __init__(self):
        self.orders=[]
        self.finished=[]
        self.delivered=[]

orderList=Orders()

class finalOrders:
    def __init__(self, base, link):
        self.base=base
        self.link=link
        self.x, self.y=None, None

finalCrepeCake=finalOrders(crepeCake, 'images/finalCrepeCake.PNG')
finalSunday=finalOrders(sunday, 'images/finalSunday.PNG')
finalCakeRoll=finalOrders(cakeRoll, 'images/finalCakeRoll.PNG')
finalMilkTea=finalOrders(milkTea, 'images/finalMilkTea.PNG')

finalSet={finalCrepeCake, finalSunday, finalCakeRoll, finalMilkTea}

################################################################################
        # DFS
        # Initial write-up assissted + taught by TA Lukas (lkebulad)
        # Later modified to fix some bugs + adjust to needs of my game
        # makeAdjacencyList() function wrote by self
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
        self.tip=0.00
        self.earning=0.00
        self.total=0.00

income=Revenue()

def calculateRevenue(app):
    finishedOrder=orderList.delivered[-1]
    base=finishedOrder[0]
    income.earning+=base.price

    finishedCustomer=app.customers[0]
    
    tip=finishedCustomer.howMuchTip()
    income.tip+=tip
    income.total=income.tip+income.earning
    print(income.earning, income.tip, income.total)

################################################################################

#MODEL
def onAppStart(app):
    app.width, app.height = 800,500
    app.rows, app.cols=4,12
    app.cellWidth, app.cellHeight = 50,50
    app.StepsPerSecond=1

    app.customers=[]
    app.customerSkin=['images/blueBunny.PNG', 'images/yellowBunny.PNG', 'images/greenBunny.PNG']
    app.customerJustServed=[]
    app.isCooking=False
    app.revenue=0.00
    
    app.currIndex=0
    app.counter=0
    app.wIndex=0
    app.gwIndex=0

    app.isDragging=False
    app.currItem=None
    app.orderComplete=False
    app.clickedPerson=None
    app.goServe=False
    app.orderDelivered=False
    app.beginNextOrder=False
    
    app.showMenu=False
    app.showFinal=False

#VIEW
def drawTable():
    tableW, tableH =125,100         
    for i in range(3):
        if i%2==1:
            drawImage(fixImage('images/table.PNG'), 450, 250, width=tableW, height=tableH, align='center')
        else:
            drawImage(fixImage('images/table.PNG'),350+i*100,350,width=tableW, height=tableH, align='center')
    
def drawOrderList(app):
    lightPink=rgb(251,227,227)
    menuWidth, menuHeight=150, 140
    drawRect(app.width-425, app.height-475, menuWidth, menuHeight, fill=lightPink, opacity=80, border='black')
    drawLabel('Orders:', 450, 45, font='grenze', bold=True, size=14)
    for i in range(len(app.customers)):
        customer=app.customers[i]
        drawLabel(f'{customer.orderT1} {customer.orderT2} {customer.orderBase}', 450, 70+i*15, size=11)

####        FONT ISN'T WORKING          ####

################################################################################
    # Draw board functions referenced my code from Tetris
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
    drawImage(fixImage('images/display.PNG'), 0,0, width=app.width, height=app.height)
    drawLabel('instructions:', 81, 415, size=16)
    #display revenue
    drawLabel(f'earning      tip         total', app.width-200, app.height-70, size=16, align='center', font='grenze')
    drawLabel(f'${income.earning} + ${income.tip} = ${income.total}', app.width-200, app.height-40, size=22, align='center')
    #display currOrder
    if len(orderList.orders)>0:
        currOrder=orderList.orders[0]
        base, t1, t2=currOrder[0], currOrder[1], currOrder[2]
        w,h=75,75
        start, gap=60, 10
        drawImage(fixImage(base.image), start, app.height-90, width=w, height=h)
        drawImage(fixImage(t1.image), start+w+gap, app.height-90, width=w-10, height=h-10)
        drawImage(fixImage(t2.image), start+2*(w+gap), app.height-90, width=w-10, height=h-10)
        for i in range(2):
            drawLabel('+', start+(w+gap)*2*i, app.height-50, size=24)


def redrawAll(app):
   
    drawImage(fixImage('images/backdrop.PNG'), 0,0, width=app.width, height=app.height+10)

    drawOrderList(app)
    drawBoard(app)

    drawDisplay(app)
    waitressG.draw()
    
    for customer in app.customers:
        drawImage(fixImage(customer.skin), customer.x, customer.y, width=50,height=100, align='center')
        drawLabel(customer.time, customer.x, customer.y)

    for base in baseSet:
        size=base.r*2
        drawImage(fixImage(base.image), base.x, base.y, align='center', width=size, height=size)
    
    for topping in toppingSet:
        size=topping.r*2
        drawImage(fixImage(topping.image), topping.x, topping.y, align='center', width=size, height=size)
    
    drawTable()

    if app.showMenu:
        drawImage(fixImage('images/menu.PNG'), 0, 0, width=app.width,height=app.height, opacity=95)
    
    drawFinal(app, waitressG)

def drawFinal(app, waitress):
    if app.showFinal:
        for final in finalSet:
            currOrderBase=orderList.finished[-1][0]
            if final.base==currOrderBase:
                drawImage(fixImage(final.link), waitress.x+10, waitress.y-100, width=45, height=45)

#CONTROLLER

def generateCustomer(app):
    skin=app.customerSkin[random.randint(0,(len(app.customerSkin)-1))]
    newCustomer=Customer(700,200, skin)
    app.customers.append(newCustomer)

def removeSeat(coordX,coordY, tables):
    x,y=coordToNode(coordX, coordY)
    if (y,x) in tables:
        tables.remove((y,x))
        layout.filledSeats.add((y, x))

def moveCustomer(app):
    for customer in app.customers:
        if not customer.timeToLeave():
            layout.isAtTable(customer)
            if not customer.isAtTable:
                customer.pathIndex+=1
                tables=layout.tables
                pathCoord=customer.customerPath((0,9), tables)
                customer.pathIndex%=len(pathCoord)
                customer.x, customer.y=pathCoord[customer.pathIndex][0], pathCoord[customer.pathIndex][1]
            else:
                removeSeat(customer.x, customer.y, layout.tables)
                seatx,seaty=coordToNode(customer.x, customer.y)
                customer.seat=(seaty, seatx)
                customer.pathIndex=0
                print('customer seated at:', customer.seat)

def leaveCustomer(app):
    for customer in app.customers:
        exit=(0,9)
        if customer.timeToLeave():
            layout.isAtExit(customer, exit)
            if not customer.isAtExit:
                pathCoord=customer.customerPath(customer.seat, (0,9))
                customer.pathIndex%=len(pathCoord)
                customer.x, customer.y=pathCoord[customer.pathIndex][0], pathCoord[customer.pathIndex][1]
                x,y=coordToNode(customer.x, customer.y)
                customer.pathIndex+=1
                print('customer leaving!!', (y, x), 'leaving from:',customer.seat)
            else:
                print('customer has left')
                customer.leave=False
                app.customers.pop(0)
                layout.filledSeats.remove(customer.seat)
                layout.tables.append(customer.seat)

def moveBackImage(): 
    orderBase, orderT1, orderT2 =counter.base, counter.topping1, counter.topping2
    orderBase.x, orderBase.y=orderBase.ogXY
    orderT1.x, orderT1.y=orderT1.ogXY
    orderT2.x, orderT2.y=orderT2.ogXY

def whenOrderReady(app):
    if app.orderComplete:
        #ingredients move back to original position (track original position)
        moveBackImage()

        #replace all images on counter to image of final product
        app.showFinal=True
        
        #all counter attributes are reset back to none
        counter.base, counter.topping1, counter. topping2=None, None, None

        #wait for player to click on a customer to send the order to
        #if they walk to the wrong person...if they click on a new person(right or wrong)...
        #...the waitress should redirect path to the new person
        #if they walk to the right person, the order is DONE

def whenOrderDone(app):
    if app.orderDelivered and len(app.customers)>0:
        #when order is DONE, waitress makes her way BACK to the counter
        #and waits (for the next order to be finished) or picks up the next order
        #SIMULTANEOUSLY, customer with this order LEAVES
        currCustomer=app.customers[0]
        currCustomer.leave=True
        app.orderComplete=False

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
    
    if len(app.customers)>1 and app.beginNextOrder:
        app.isCooking=True
    elif len(app.customers)==1:
        app.isCooking=True
    
    if orderList.orders==[]:
        app.isCooking=False
    if app.counter%50==0 and len(orderList.orders)>0:
        countDown(app)
    
    #Customer Movement
    if app.counter%2==0 and len(app.customers)>0:
        moveCustomer(app)
        leaveCustomer(app)
    #Waitress Movement
    if app.goServe:
        moveWaitress(app.wIndex, app, waitressG)
        app.wIndex+=1
    if app.orderDelivered:
        goBackCounter(app.gwIndex, app, waitressG)
        app.gwIndex+=1
    whenOrderDone(app)
        
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
    if base==currOrder[0] and (t1==currOrder[1] or t1==currOrder[2]) and (t2==currOrder[2] or t2==currOrder[1]):
        app.orderComplete=True
        waitressG.whichOrder=currOrder
        orderList.finished.append(currOrder)
        orderList.orders.pop(0)
        app.isCooking=False
        print('order is complete!')
        whenOrderReady(app)
        return True

def isInCurrOrder(currItem):
    currOrder=orderList.orders[0]
    print('current order is:', currOrder)
    if currItem in currOrder:
        return True
    return False

def clickedPerson(mouseX, mouseY, app):
    print('filledSeats:', layout.filledSeats)
    for node in layout.filledSeats:
        coordinates=nodeToCoord(node)
        print('node:', node, coordinates)
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
    print('waitress is serving...', target)
    layout.isWaitressAtNode(waitress, target)
    if not waitress.isWaitressAtNode:
        pathCoord=waitress.waitressPath((2,0), target)
        i%=len(pathCoord)
        waitress.x, waitress.y=pathCoord[i][0], pathCoord[i][1]
        wx,wy=coordToNode(waitress.x, waitress.y)
        print('at node:', (wy,wx), 'not there yet')
    else:
        #check if waitress order matches customer order
        #if not, waitress will stop walking. player has to reclick to trigger new path
        #player cannot move to next order until current order is delivered
        print('reached node!')
        app.goServe=False
        rightPerson=servedRightPerson(waitress.whichOrder, target, app)
        if rightPerson[1]:
            app.orderDelivered=True
            print('successfully delivered :)')
            orderList.delivered.append(orderList.finished[-1])
            app.showFinal=False
            app.wIndex=0
            calculateRevenue(app)
            app.customerJustServed=rightPerson[0]
        else:
            print('unsucessful delivery :(')
            print('waitress delivering', waitress.whichOrder, 'should deliver to', orderList.finished[-1])
        waitress.isWaitressAtNode=False

def servedRightPerson(waitressOrder, target, app):
    currCustomer=None
    for customer in app.customers:
        if customer.seat==target:
            currCustomer=customer
    if waitressOrder==currCustomer.order:
        return (currCustomer, True)
    return (currCustomer, False)

def goBackCounter(i, app, waitress):
    start=app.customerJustServed.seat
    layout.isBackAtCounter(waitress, (2,0))
    if not waitress.isBackAtCounter:
        pathCoord=waitress.waitressPath(start,(2,0))
        i%=len(pathCoord)
        waitress.x, waitress.y=pathCoord[i][0], pathCoord[i][1]
    else:
        app.beginNextOrder=True
        app.orderDelivered=False
        app.gwIndex=0
        waitress.isBackAtCounter=False

def onMousePress(app, mouseX, mouseY):
    if app.isCooking:
        check=clickedIngredient(mouseX, mouseY)
        if check[1]:
            app.currItem=check[0]
            app.isDragging=True
    if app.orderComplete:
        checkPerson=clickedPerson(mouseX, mouseY, app)
        print('checkPerson:', checkPerson)
        if checkPerson!=None:
            if checkPerson[1]:
                app.goServe=True
                app.clickedPerson=checkPerson[0]
                print('app.clickedPerson:', app.clickedPerson)
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

def wrongIngredientReset(app):
    if app.currItem==counter.topping1:
        counter.topping1=None
    if app.currItem==counter.topping2:
        counter.topping2=None
    if app.currItem==counter.base:
        counter.base=None

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

            #Checks if the currItem is in the currOrder
            if isInCurrOrder(app.currItem):
                print('it belongs to the order!')
                app.currItem.x, app.currItem.y=mouseX, mouseY
            else:
                print('not part of the order!')
                wrongIngredientReset(app)
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