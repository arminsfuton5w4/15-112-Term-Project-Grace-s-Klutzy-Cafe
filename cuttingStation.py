from cmu_graphics import *

################################################################################
    # cutting station
################################################################################

# if order is "completed" on the counter:
# instead of showing the final product, pops into the cutting station
# pauses the rest of the game until the cutting is finished

# Toppings that can be cut: strawberries, mango, chocolate
# Toppings to be grinded: matcha, red bean, ube

# cut once (draw 1 line), in that case need line class?
# grind once (draw 1 circle) - arc tool?

# player can pick up either the mortar or the knife. But if the topping property
# doesn't match the tool, then the player cannot do anything with the tool
# if the player picks up a tool that MATCHES the topping property, then...
# the player can cut/grind the topping.

# there are two toppings to PREP each time. Once the first topping has been
# prepped, the second topping needs to be prepped.
# once the second topping is prepped, the screen goes back to the game.

#new app variables:
def onScreenActivate(app):
    app.stepsPerSecond=3

    app.currOrder=orderList.orders[0]

    app.grindingMode, app.cuttingMode=False, False

    app.holdKnife, app.holdMortar=False, False

    app.lineStartLocation, app.lineEndLocation=None

    app.circleTrail=[]
    app.maxCircles=7
    app.mousePress=False
    app.startGrinding=0

    for topping in prepList:
        topping.finishedPrep=False

topping1, topping2=app.currOrder[1], app.currOrder[2]
prepList=(topping1, topping2)

def cutting_onStep(app):
    if checkPrepProgress():
        app.orderComplete=True
        waitressG.whichOrder=app.currOrder
        orderList.finished.append(currOrder)
        app.isCooking=False
        orderList.orders.pop(0)
        print('order is complete!')
        whenOrderReady(app)
        
        setActiveScreen('game')
    if app.grindingMode and app.mousePress:
        app.startGrinding+=1

class Tool:
    def __init__(self, name, link, x,y, ogXY, bounds):
        self.name=name
        self.image=link
        self.x, self.y=x,y
        self.size=25
        self.ogXY=ogXY
        self.bounds=bounds
        self.w, self.h=64, 80

    def draw(link, x, y):
        drawImage(fixImage(self.image), x, y)

cBoardCoordinates=(375, 150)
cBoardWidth=375
cBoardHeight=240
# center (563, 270)

knife=Tool('knife','images/knife.PNG',320, 210, (320, 210), )
mortar=Tool('mortar', 'images/mortar.PNG',320, 210, (320, 210))

def cutting_redrawAll (app):
    drawImage(fixImage('images/cuttingStation.PNG'), 0,0, app.width, app.height)

    knife.draw()
    mortar.draw()

    if app.cuttingMode:
        if ((app.lineStartLocation !=None) and
            (app.lineEndLocation !=None)):
                drawCut(app)
    if app.grindingMode:
        drawGrind(app)
    
# Inspiration from checkpoint in 4.4.2 Mouse Moves and Drags
# Grinding animation/UI taught by Austin!!
def drawCut(app):
    x0, y0=app.lineStartLocation
    x1, y1=app.lineEndLocation
    drawLine(x0, y0, x1, y1, dashes=app.draggingLine)

def drawGrind(app):
    for i in range(len(app.circleTrail)):
        cx, cy=app.circleTrail[i]
        opacity=(len(app.circleTrail)-1)*100
        drawCircle(cx, cy, 20, fill='gray', opacity=opacity)

def inBounds(mouseX, mouseY, coordinates, width, height):
    left, top=coordinates[0], coordinates[1]
    right=left+width
    bottom=top+height
    if (left <=mouseX<=right) and (top<=mouseY<=bottom):
        return True
    return False

def cutting_onMousePress(app, mouseX, mouseY):
    if inBounds(mouseX, mouseY, ):
        pass
    if app.cuttingMode:
        app.lineStartLocation=(mouseX, mouseY)
        app.lineEndLocation=None
    if app.grindingMode:
        app.mousePress=True

def cutting_onMouseDrag(app, mouseX, mouseY):
    if app.holdKnife:
        knife.x, knife.y=mouseX, mouseY
    if app.holdMortar:
        mortar.x, mortar.y=mouseX, mouseY
    if inBounds(mouseX, mouseY, cuttingBoardCoordinate):
        app.lineEndLocation=(mouseX, mouseY)

def cutting_onMouseRelease(app, mouseX, mouseY):
    if not app.holdKnife and inBounds(mouseX, mouseX, knife.bounds, knife.w, knife.h):
        app.holdKnife=False
        knife.x, knife.y=knife.ogXY
    if not app.holdMortar and inBounds(mouseX, mouseY, mortar.bounds, mortar.w, mortar.h):
        app.holdMortar=False
        mortar.x, mortar.y=mortar.ogXY
    if inBounds(mouseX, mouseY, cuttingBoardCoordinate, ):
        app.dragLine=False
    
def cutting_onMouseMove(app, mouseX, mouseY):
    if app.holdKnife:
        knife.x, knife.y=mouseX, mouseY
    if app.holdMortar:
        mortar.x, mortar.y=mouseX, mouseY

def doPrep(app):
    for topping in prepList:
        if topping.finishedPrep==False:
            if topping.property=='grind':
                app.holdMortar==True
            elif topping.property=='cut':
                pass

def checkPrepProgress():
    for topping in prepList:
        if topping.state==False:
            return False
    return True