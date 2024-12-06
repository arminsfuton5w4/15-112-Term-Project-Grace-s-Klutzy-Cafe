################################################################################
    # start screen
################################################################################

def start_redrawAll(app):
    drawImage(fixImage('images/start.PNG'), 0,0, width=app.width,
              height=app.height)

def start_onMousePress(app, x, y):
    setActiveScreen('game')