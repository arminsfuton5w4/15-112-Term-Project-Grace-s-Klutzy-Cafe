from cmu_graphics import *
import random

class Waitress:
    def __init__(self, x, y, length, width):
        self.x, self.y = x,y
        self.length, self.width =length, width

class Customer:
    def __init__(self, x, y, length, width):
            self.x, self.y = x,y
            self.length, self.width =length, width

class Customers:
    def __init__(self, customerList):
        self.customers=[]
        for (x,y,length, width) in customerList:
            self.customers.append(Customer(x,y,length, width))

def distance(x0,y0,x1,y1):
    return (((x1-x0)**2+(y1-y0)**2)**0.5)

menu =['cake roll', 'milk tea', 'sunday', 'sago', 'crepe cake']
flavors=['fruits': {'strawberry', 'peach', 'mango'},
         'others': {'matcha', 'chocolate', 'ube', 'red bean'}]

 #table locations & boundaries
        


#MODEL
def onAppStart(app):
    app.width, app.height = 800,500

#VIEW
def drawTable(app):
    drawRect(200,200,50,50, fill='black')


def redrawAll(app):
    pass

def main():
    runApp()

main()
#CONTROLLER
cmu_graphics.run()
