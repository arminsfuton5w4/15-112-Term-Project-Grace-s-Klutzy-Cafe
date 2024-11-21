from cmu_graphics import *
import random
import copy

class Waitress:
    def __init__(self, x, y):
        self.x, self.y = x,y

    def move(self, app):
        self.y-=3
    
    def draw(self, app):
        drawRect(self.x, self.y,50,100, fill='purple')

class Customer:
    def __init__(self, x, y):
            self.x, self.y = x,y
        
    def customerOrder(self):
        return generateOrder(menu, allToppings)
    
    def moveCustomer(self, app):
        self.x+=5
        self.y+=5

class Ingredient:
    def __init__(self, link):
        self.image=link
    
    def draw(self, app):
        for i in range(len(self.ingredients)):
            drawImage(self.image, 50+i*70, 150-i*35,50, fill='green')

def distance(x0,y0,x1,y1):
    return (((x1-x0)**2+(y1-y0)**2)**0.5)

cakeRoll=Ingredient('cmu://903290/33748782/0c726d7f441baf1ab17eb76c5f755f13.png')

menu =['cake-roll', 'milk-tea', 'sunday', 'crepe-cake']
flavors={'fruits': {'strawberry', 'peach', 'mango'},'others': {'matcha', 'chocolate', 'ube', 'red-bean'}}
allToppings=['strawberry', 'mango', 'matcha', 'chocolate', 'ube', 'red-bean']


def generateOrder(menu, allToppings):
    toppings=copy.copy(allToppings)
    topping1=allToppings[random.randint(0,len(allToppings))]
    toppings.remove(topping1)
    topping2=toppings[random.randint(0,len(allToppings))]
    return f'{topping1} {topping2} {menu[random.randint(0,len(menu))]}'

def makeDish(order):
    t1, t2, base=getIngredients(order)


def getIngredients(order):
    items=order.split()
    topping1=items[0]
    topping2=items[1]
    base=items[2]
    return (topping1, topping2, base) 

#table locations & boundaries
#kitchen area boundaries (waitress + customers cannot go in)
#within kitchen area, drag and drop ingredients onto platter occurs      

#MODEL
def onAppStart(app):
    app.width, app.height = 800,500
    app.rows, app.cols=10,16
    app.board=[([None] * app.cols) for row in range(app.rows)]

    app.customers=[]
    app.isCooking=False
    app.StepsPerSecond=2
    app.counter=0
    app.translucence=0 #0: opacity=0, 1: opacity=50, 2: opacity=100

    app.foodX, app.foodY=100,50

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

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = 50,50
    cellLeft = 0 + col * cellWidth
    cellTop = 0 + row * cellHeight
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
    drawTable(app)
    drawOrderList(app)
    drawBoard(app)

    drawDisplay(app)
    w=Waitress(200,200)
    w.draw(app)
    
    for customer in app.customers:
        drawRect(customer.x, customer.y, 50,100, fill='red')

#CONTROLLER

def onStep(app):
    app.counter+=1
    newCustomer=Customer(700,200)
    if app.counter%50==0 and len(app.customers)<=3:
        app.customers.append(newCustomer)
    for customer in app.customers:
        customer.moveCustomer(app)

def onMousePress(app, mouseX, mouseY):
    # if (mouseX, mouseY) in #any of the ingredient coordinates

    # if (mouseX, mouseY) in #table coordinates

    if app.isCooking:
        app.foodX=mouseX
        app.foodY=mouseY
        app.isDragging=True
        app.translucence=1

def onMouseDrag(app, mouseX, mouseY):
    if app.isCooking:
        app.foodX=mouseX
        app.foodY=mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.isCooking:
        app.isDragging=False
        app.translucence=2 

def main():
    runApp()

main()
cmu_graphics.run()