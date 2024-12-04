################################################################################
    # start screen
################################################################################

def start_redrawAll(app):
    drawImage(fixImage('images/start.PNG'), 0,0, app.width, app.height)

def start_onMousePress(app, mouseX, mouseY):
    setActiveScreen('game')