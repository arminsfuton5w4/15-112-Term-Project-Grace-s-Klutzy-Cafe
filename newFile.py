from cmu_graphics import *
import random
import copy

class Waitress:
    def __init__(self, x, y):
        self.x, self.y = x,y
    
    def move(self):
        self.y-=3
    
    def draw(self):
        drawRect(self.x, self.y,50,20, fill='purple')


class Customer:
    def __init__(self, x, y, length, width):
            self.x, self.y = x,y
            self.length, self.width =length, width
        
    def customerOrder(self):
        return generateOrder(menu, allToppings)
    
    def draw(self):
        drawRect(self.x, self.y, 50,20, fill='red')

# class Customers:
#     def __init__(self, customerList):
#         self.customers=[]
#         for (x,y,length, width) in customerList:
#             self.customers.append(Customer(x,y,length, width))

def distance(x0,y0,x1,y1):
    return (((x1-x0)**2+(y1-y0)**2)**0.5)

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
    app.customers=[]
    app.isCooking=False

#VIEW
def drawTable(app):          
    for i in range(3):
        drawRect(200+i*100,200,50,50, fill='black')
    
def drawOrders(app):
    drawRect(375, 50, 150, 160, fill='blue', opacity=30)


def redrawAll(app):
    drawTable(app)
    drawOrders(app)
    for 

def main():
    runApp()

main()
#CONTROLLER

cmu_graphics.run()
