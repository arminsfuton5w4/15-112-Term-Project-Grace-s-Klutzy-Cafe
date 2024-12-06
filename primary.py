from cmu_graphics import *
import random
from PIL import Image
from urllib.request import urlopen
import os, pathlib

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
    # start screen
################################################################################

def start_redrawAll(app):
    drawImage(fixImage('images/start.PNG'), 0,0, width=app.width,
              height=app.height)

def start_onMousePress(app, x, y):
    setActiveScreen('game')

################################################################################
        # CLASSES
################################################################################

class Waitress:
    def __init__(self, x, y, link):
        self.x, self.y = x,y
        self.image=link
        self.whichOrder=None
        self.isWaitressAtNode=False
        self.isBackAtCounter=False
    
    def draw(self):
        drawImage(fixImage(self.image),self.x, self.y,width=125,height=145,
                  align='bottom-left')
    
    def waitressPath(self, start, target):
        visited=set()
        state=(False, [target], [])
        path=DFS(board, state, visited, start)
        path=state[-1]
        pathCoord=nodeToCoord(path)
        return pathCoord

waitressG=Waitress(200,350,'images/gothicWaitress.PNG')

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
            other.isWaitressAtNode=True
    
    def isBackAtCounter(self, other, target):
        x,y=coordToNode(other.x, other.y)
        if (y, x) == target:
            other.isBackAtCounter=True
    
    def isAtExit(self, other, target):
        x,y=coordToNode(other.x, other.y)
        if (y, x) == target:
            other.isAtExit=True

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
        self.down=True
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
            self.down=False
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
        self.coordinates=[(60,250), (100,280), (210,220), (160,190)]

counter=Counter()

class Base:
    def __init__(self, name, link, x,y, price, ogXY, final):
        self.name=name
        self.image=link
        self.final=final
        self.x, self.y=x,y
        self.r=25
        self.price=price
        self.ogXY=ogXY
    
    def __repr__(self):
        return f'{self.name}'
    
    def __hash__(self):
        return hash(str(self)) 

class Toppings:
    def __init__(self, name, link, x,y, ogXY, property, prepped):
        self.name=name
        self.image=link
        self.x, self.y=x,y
        self.r=25
        self.ogXY=ogXY
        self.property=property
        self.prepped=prepped
        self.finishedPrep=False
    
    def __repr__(self):
        return f'{self.name}'  

    def __hash__(self):
        return hash(str(self)) 

def distance(x0,y0,x1,y1):
    return (((x1-x0)**2+(y1-y0)**2)**0.5)

cakeRoll=Base('cake-roll', 'images/cakeRoll.PNG',50, 120, 7.50, (50, 120), 
              'images/finalCakeRoll.PNG')
crepeCake=Base('crepe-cake','images/crepeCake.PNG',92,100,8.00,(92,105),
               'images/finalCrepeCake.PNG')
sunday=Base('sunday', 'images/sunday.PNG', 50, 190, 6.75, (50, 190),
            'images/finalSunday.PNG')
milkTea=Base('milk-tea', 'images/boba2.PNG', 92, 165, 5.50, (92, 165),
             'images/finalMilkTea.PNG')

baseSet={cakeRoll, crepeCake, sunday, milkTea}

matcha=Toppings('matcha', 'images/matcha.PNG',175, 60, (175,60), 'grind',
                'images/groundMatcha.PNG')
strawberry=Toppings('strawberry', 'images/strawberry.PNG',215,45, (215,45),'cut',
                    'images/cutStrawberry.PNG')
chocolate=Toppings('chocolate', 'images/chocolate.PNG',252,28, (252,28),'cut',
                   'images/cutChoco.PNG')
ube=Toppings('ube', 'images/ube.PNG',175,128, (175,128),'grind', 'images/groundUbe.PNG')
redBean=Toppings('red-bean', 'images/redBean.PNG',215,115, (215,115),'grind',
                 'images/groundRedBean.PNG')
mango=Toppings('mango', 'images/mango.PNG',252, 90, (252,90),'cut',
               'images/cutMango.PNG')

toppingSet={strawberry, mango, chocolate, ube, redBean, matcha}

ingredientList=[cakeRoll, crepeCake, sunday, milkTea, strawberry,
                mango, chocolate, ube, redBean, matcha]

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
                adjList[(row, col)]={(row-1, col), (row+1, col), (row, col-1),
                                     (row, col+1)}
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

################################################################################

#MODEL
def onAppStart(app):
    app.width, app.height = 800,500
    app.rows, app.cols=4,12
    app.cellWidth, app.cellHeight = 50,50
    app.StepsPerSecond=1
    app.counter=0

    app.customers=[]
    app.customerSkin=['images/blueBunny.PNG', 'images/yellowBunny.PNG',
                      'images/greenBunny.PNG']
    app.customerJustServed=[]
    app.isCooking=False
    app.revenue=0.00
    
    app.wIndex=0
    app.gwIndex=0

    app.currItem=None
    app.deliverySucess=0
    app.orderComplete=False
    app.clickedPerson=None
    app.goServe=False
    app.orderDelivered=False
    app.beginNextOrder=False
    
    app.showMenu=False
    app.showFinal=False

    ### For cutting screen ###
    app.grindingMode, app.cuttingMode=False, False

    app.holdKnife, app.holdMortar=False, False

    app.dragLine=False

    app.lineStartLocation, app.lineEndLocation=None, None

    app.circleTrail=[]
    app.maxCircles=7
    app.mousePress=False
    app.startGrinding=0
    app.showCutCounter=0
    app.doneCut=False
    app.showPrepped=0

    app.prepList=[]
    app.donePrepList=[]

#VIEW
def drawTable():
    tableW, tableH =125,100         
    for i in range(3):
        if i%2==1:
            drawImage(fixImage('images/table.PNG'), 450, 250, width=tableW,
                      height=tableH, align='center')
        else:
            drawImage(fixImage('images/table.PNG'),350+i*100,350,width=tableW,
                      height=tableH, align='center')

lightPink=rgb(251,227,227)

def drawOrderList(app):
    menuWidth, menuHeight=200, 140
    drawRect(app.width-450, app.height-475, menuWidth, menuHeight, 
             fill=lightPink, opacity=80, border='black')
    drawLabel('Orders:', 450, 45, font='grenze', bold=True, size=14)
    for i in range(len(app.customers)):
        customer=app.customers[i]
        finalImage=None
        for base in baseSet:
            if base==customer.orderBase:
                finalImage=base.final
        drawImage(fixImage(finalImage), 360, 55+i*25, width=30, height=30)
        drawLabel(f'{customer.orderT1} {customer.orderT2} {customer.orderBase}',
                  395, 70+i*25, size=11, align='left')

def drawDisplay(app):
    drawImage(fixImage('images/display.PNG'),0,0, width=app.width, 
              height=app.height)
    drawLabel('instructions:', 81, 415, size=16)
    #display revenue
    drawLabel(f'earning      tip         total', app.width-200, app.height-70,
              size=16, align='center', font='grenze')
    drawLabel(f'${income.earning} + ${income.tip} = ${income.total}',
              app.width-200, app.height-40, size=22, align='center')
    #display currOrder
    if len(orderList.orders)>0:
        currOrder=orderList.orders[0]
        base, t1, t2=currOrder[0], currOrder[1], currOrder[2]
        w,h=75,75
        start, gap=60, 10
        drawImage(fixImage(base.image), start, app.height-90, width=w, height=h)
        drawImage(fixImage(t1.image), start+w+gap, app.height-90, width=w-10,
                  height=h-10)
        drawImage(fixImage(t2.image), start+2*(w+gap), app.height-90,
                  width=w-10, height=h-10)
        for i in range(1,3):
            drawLabel('+', start+(w+gap/2)*i, app.height-50, size=24)

def game_redrawAll(app):
    drawImage(fixImage('images/backdrop.PNG'), 0,0, width=app.width,
              height=app.height+10)

    drawOrderList(app)

    drawDisplay(app)
    waitressG.draw()
    
    for customer in app.customers:
        drawImage(fixImage(customer.skin), customer.x, customer.y, width=50,
                  height=100, align='center')
        drawLabel(customer.time, customer.x, customer.y)

    for base in baseSet:
        size=base.r*2
        drawImage(fixImage(base.image), base.x, base.y, align='center',
                  width=size, height=size)
    
    for topping in toppingSet:
        size=topping.r*2
        drawImage(fixImage(topping.image), topping.x, topping.y, align='center',
                  width=size, height=size)
    
    drawFinal(app, waitressG)
    drawSucess(app, waitressG)
    drawPopUp(app)
    
    drawTable()

    if app.showMenu:
        drawImage(fixImage('images/menu.PNG'), 0, 0, width=app.width,
                  height=app.height, opacity=95)

def drawSucess(app, waitress):
    if app.deliverySucess==1:
        drawRect(waitress.x+30, waitress.y-160, 70, 15, fill=lightPink)
        drawLabel('SUCCESS!!', waitress.x+30, waitress.y-150, align='left')
    elif app.deliverySucess==2:
        drawRect(waitress.x+30, waitress.y-160, 100, 15, fill=lightPink)
        drawLabel('WRONG PERSON', waitress.x+30, waitress.y-150, align='left')

def drawPopUp(app):
    img=None
    for customer in app.customers:
        if customer.down:
            for base in baseSet:
                if base==customer.orderBase:
                    img=base.final
            if customer.time%3==0:    
                drawImage(fixImage(img), customer.x, customer.y-50, width=30,
                          height=30)

def drawFinal(app, waitress):
    if app.showFinal:
        for base in baseSet:
            currOrderBase=orderList.finished[-1][0]
            if base==currOrderBase:
                drawImage(fixImage(base.final), waitress.x+10, waitress.y-100,
                          width=45, height=45)

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
                customer.x=pathCoord[customer.pathIndex][0]
                customer.y=pathCoord[customer.pathIndex][1]
            else:
                removeSeat(customer.x, customer.y, layout.tables)
                seatx,seaty=coordToNode(customer.x, customer.y)
                customer.seat=(seaty, seatx)
                customer.pathIndex=0

def leaveCustomer(app):
    for customer in app.customers:
        exit=(0,9)
        if customer.timeToLeave():
            layout.isAtExit(customer, exit)
            if not customer.isAtExit:
                pathCoord=customer.customerPath(customer.seat, (0,9))
                customer.pathIndex%=len(pathCoord)
                customer.x=pathCoord[customer.pathIndex][0]
                customer.y=pathCoord[customer.pathIndex][1]
                x,y=coordToNode(customer.x, customer.y)
                customer.pathIndex+=1
            else:
                customer.leave=False
                layout.filledSeats.remove(customer.seat)
                app.customers.pop(0)
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

def whenOrderDone(app):
    if app.orderDelivered and len(app.customers)>0:
        currCustomer=app.customers[0]
        currCustomer.leave=True
        app.orderComplete=False

def countDown(app):
    for customer in app.customers:
        if customer.time<=0 and (customer.order in orderList.orders):
            orderList.orders.remove(customer.order)
        elif customer.time>0 and customer.down:
            customer.time-=0.5

def game_onStep(app):
    app.counter+=1
    if app.counter%100==0 and len(app.customers)<3:
        generateCustomer(app)
    
    if len(app.customers)>1 and app.beginNextOrder:
        app.isCooking=True
        app.beginNextOrder=False
    elif len(app.customers)==1:
        app.isCooking=True
    
    if orderList.orders==[]:
        app.isCooking=False
    if app.counter%50==0 and len(orderList.orders)>0:
        countDown(app)
    
    #Customer Movement
    if app.counter%5==0 and len(app.customers)>0:
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

    # cutting screen stuff
    prepList=getPrepList()
    app.prepList=prepList

        
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
    if (base==currOrder[0] and (t1==currOrder[1] or t1==currOrder[2])
        and (t2==currOrder[2] or t2==currOrder[1])):
        setActiveScreen('cutting')
        print('done prep')
        return True

def isInCurrOrder(currItem):
    currOrder=orderList.orders[0]
    print('current order is:', currOrder)
    if currItem in currOrder:
        return True
    return False

def clickedPerson(mouseX, mouseY, app):
    for node in layout.filledSeats:
        coordinates=nodeToCoord(node)
        if coordinates!=None:
            coordX=(coordinates[0]+app.cellWidth/2)
            coordY=(coordinates[1]+app.cellHeight/2)
            d=distance(mouseX, mouseY, coordX, coordY)
            if d<app.cellWidth:
                return (node, True)
    return (None, False)

def moveWaitress(i, app, waitress):
    for node in layout.filledSeats:
        if node==app.clickedPerson:
            target=node
    layout.isWaitressAtNode(waitress, target)
    if not waitress.isWaitressAtNode:
        pathCoord=waitress.waitressPath((2,0), target)
        i%=len(pathCoord)
        waitress.x, waitress.y=pathCoord[i][0], pathCoord[i][1]
    else:
        app.goServe=False
        rightPerson=servedRightPerson(waitress.whichOrder, target, app)
        if rightPerson[1]:
            resetRightPerson(app)
            app.customerJustServed=rightPerson[0]
        else:
            app.deliverySucess=2
        waitress.isWaitressAtNode=False

def resetRightPerson(app):
    app.deliverySucess=1
    app.orderDelivered=True
    orderList.delivered.append(orderList.finished[-1])
    app.showFinal=False
    app.wIndex=0
    calculateRevenue(app)
    app.count=False

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
        app.deliverySucess=0
        app.beginNextOrder=True
        app.orderDelivered=False
        app.gwIndex=0
        waitress.isBackAtCounter=False

def game_onMousePress(app, mouseX, mouseY):
    if app.isCooking:
        check=clickedIngredient(mouseX, mouseY)
        if check[1]:
            app.currItem=check[0]
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

def game_onMouseDrag(app, mouseX, mouseY):
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

def game_onMouseRelease(app, mouseX, mouseY):
    if app.isCooking:
        if inCounter(mouseX, mouseY):
            #Checks for property of currItem - base/topping - & updates counter
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
                app.currItem.x, app.currItem.y=mouseX, mouseY
            else:
                wrongIngredientReset(app)
                app.currItem.x, app.currItem.y=app.currItem.ogXY
            isCurrOrderComplete(counter.base,counter.topping1,counter.topping2,app)
        else:
            if app.currItem!=None: 
                app.currItem.x, app.currItem.y=app.currItem.ogXY
    if app.showMenu:
        app.showMenu=False

################################################################################
    # cutting station
################################################################################

def getPrepList():
    currOrder=None
    if orderList.orders!=[]:
        currOrder=orderList.orders[0]
    if currOrder!=None:
        topping1, topping2=currOrder[1], currOrder[2]
        prepList=[topping1, topping2]
        return prepList

def cutting_onScreenActivate(app):

    app.grindingMode, app.cuttingMode=False, False

    app.holdKnife, app.holdMortar=False, False

    app.dragLine=False

    app.lineStartLocation, app.lineEndLocation=None, None

    app.circleTrail=[]
    app.maxCircles=7
    app.mousePress=False
    app.startGrinding=0
    app.doneCut=False
    app.showCutCounter=0
    app.showPrepped=0

    app.donePrepList=[]

    knife.x, knife.y=knife.ogXY
    mortar.x, mortar.y=mortar.ogXY

def getCurrTopping(prepList):
    currTopping=None
    if prepList!=[]:
        currTopping=prepList[0]
    return currTopping

def cutting_onStep(app):
    updateProgress(app)
    if checkPrepProgress(app) and app.showPrepped>=200:
        app.orderComplete=True
        waitressG.whichOrder=orderList.orders[0]
        print('orderList.orders:', orderList.orders)
        orderList.finished.append(orderList.orders[0])
        app.isCooking=False
        orderList.orders.pop(0)
        print('order is complete!')
        whenOrderReady(app)
        
        setActiveScreen('game')
    
    if app.grindingMode and app.mousePress:
        app.startGrinding+=1
    
    if app.showPrepped>0:
        app.showPrepped+=1

class Tool:
    def __init__(self, name, link, x,y, ogXY):
        self.name=name
        self.image=link
        self.x, self.y=x,y
        self.size=25
        self.ogXY=ogXY
        self.w, self.h=64, 80

    def draw(self):
        drawImage(fixImage(self.image), self.x, self.y, width=150, height=150,
                  align='center')

cBoardCoordinates=(350, 150)
cBoardWidth, cBoardHeight=375, 240
cBoardCenter=(500, 270)

knife=Tool('knife','images/knife.PNG', 150,200, (150,200))
mortar=Tool('mortar', 'images/mortar.PNG',170,325, (170,325))

def drawCurrTopping(app):
    if app.prepList!=[]:
        currTopping=getCurrTopping(app.prepList)
        drawImage(fixImage(currTopping.image),cBoardCenter[0],cBoardCenter[1],
                width=300, height=300, align='center')
        drawLabel(currTopping.property, 350, 370, size=24)
    if len(app.donePrepList)==2:
        currTopping=app.donePrepList[1]
        drawImage(fixImage(currTopping.prepped),cBoardCenter[0],cBoardCenter[1],
                width=300, height=300, align='center')

def cutting_redrawAll(app):
    drawImage(fixImage('images/cuttingStation.PNG'), 0,0, width=app.width, height=app.height)

    drawCurrTopping(app)
    drawQueue(app)
    knife.draw()
    mortar.draw()

    if app.cuttingMode and app.holdKnife:
        if ((app.lineStartLocation !=None) and (app.lineEndLocation !=None)):
            drawCut(app)
    if app.grindingMode and app.holdMortar and app.circleTrail!=[]:
        drawGrind(app)

################################################################################
    # Cut animation inspired by checkpoint in 4.4.2 Mouse Moves and Drags
    # Grinding animation/UI taught by Austin!!
################################################################################

def drawCut(app):
    x0, y0=app.lineStartLocation
    x1, y1=app.lineEndLocation
    drawLine(x0, y0, x1, y1, dashes=app.dragLine)

def drawGrind(app):
    for i in range(len(app.circleTrail)):
        cx, cy=app.circleTrail[i]
        #opacity=(len(app.circleTrail)-i)//len(app.circleTrail)*100
        drawCircle(cx, cy, 20, fill=lightPink, opacity=50)
    
def drawQueue(app):
    drawLabel('Next:', app.width-150, 75, size=16)
    drawLabel('Done:', app.width-230, 75, size=16)

    if len(app.prepList)==2:
        otherTopping=app.prepList[1]
        drawImage(fixImage(otherTopping.image), app.width-150, 110, width=75, height=75,
                  align='center')
    elif len(app.donePrepList)>0:
        otherTopping=app.donePrepList[0]
        drawImage(fixImage(otherTopping.prepped), app.width-230, 110, width=75, height=75,
                  align='center')
        
def inBounds(mouseX, mouseY, coordinates, width, height):
    left, top=coordinates[0], coordinates[1]
    right=left+width
    bottom=top+height
    if (left <=mouseX<=right) and (top<=mouseY<=bottom):
        return True
    return False

def cutting_onMousePress(app, mouseX, mouseY):
    currTopping=getCurrTopping(app.prepList)
    #pick up tool
    if inBounds(mouseX, mouseY, knife.ogXY, knife.w, knife.h) and not app.holdMortar:
        app.holdKnife=True
        knife.x, knife.y=mouseX, mouseY
    elif inBounds(mouseX, mouseY, mortar.ogXY, mortar.w, mortar.h) and not app.holdKnife:
        app.holdMortar=True
        mortar.x, mortar.y=mouseX, mouseY
    #on cutting board
    if (inBounds(mouseX, mouseY, cBoardCoordinates, cBoardWidth, cBoardHeight) and
        currTopping!=None):
        if app.holdKnife and not app.cuttingMode and currTopping.property=='cut':
            app.cuttingMode=True
            app.lineStartLocation=(mouseX, mouseY)
            app.lineEndLocation=None
            app.dragLine=True
        if app.holdMortar and not app.grindingMode and currTopping.property=='grind':
            app.grindingMode=True
            app.mousePress=True

def cutting_onMouseDrag(app, mouseX, mouseY):
    if app.holdKnife:
        knife.x, knife.y=mouseX, mouseY
    if app.holdMortar:
        mortar.x, mortar.y=mouseX, mouseY
    
    if inBounds(mouseX, mouseY, cBoardCoordinates, cBoardWidth, cBoardHeight):
        if app.grindingMode:
            app.circleTrail.append((mouseX, mouseY))
            if len(app.circleTrail)==app.maxCircles:
                app.circleTrail.pop(0)
        if app.cuttingMode:
            app.lineEndLocation=(mouseX, mouseY)

def cutting_onMouseRelease(app, mouseX, mouseY):
    #snaps the tools back into their position
    if not app.cuttingMode and inBounds(mouseX, mouseX, knife.ogXY, knife.w, knife.h):
        app.holdKnife=False
        knife.x, knife.y=knife.ogXY
    if not app.grindingMode and inBounds(mouseX, mouseY, mortar.ogXY, mortar.w, mortar.h):
        app.holdMortar=False
        mortar.x, mortar.y=mortar.ogXY
    
    if inBounds(mouseX, mouseY, cBoardCoordinates, cBoardWidth, cBoardHeight):
        if app.grindingMode:
            app.mousePress=False
            app.circleTrail=[]
        if app.cuttingMode and app.lineEndLocation!=None:
            app.doneCut=True
            app.dragLine=False
    
def cutting_onMouseMove(app, mouseX, mouseY):
    if app.holdKnife:
        knife.x, knife.y=mouseX, mouseY
    if app.holdMortar:
        mortar.x, mortar.y=mouseX, mouseY

def updateProgress(app):
    currTopping=getCurrTopping(app.prepList)
    if app.cuttingMode:
        if app.doneCut:
            app.showPrepped+=1
            resetPrep(app, currTopping)
    if app.grindingMode:
        if app.startGrinding==30:
            app.showPrepped+=1
            resetPrep(app, currTopping)

def resetPrep(app, currTopping):
    if app.cuttingMode:
        app.lineStartLocation,app.lineEndLocation=None, None
        app.cuttingMode=False
        app.doneCut=False
    if app.grindingMode:
        app.startGrinding=0
        app.mousePress=False
        app.grindingMode=False
    app.prepList.pop(0)
    app.donePrepList.append(currTopping)

def checkPrepProgress(app):
    if len(app.donePrepList)==2:
        return True
    return False

def main():
    runAppWithScreens(initialScreen='start')

main()
cmu_graphics.run()