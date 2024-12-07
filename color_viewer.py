# color_viewer.py

from cmu_graphics import *
from PIL import Image

def onAppStart(app, path):
    app.path = path

    # load and convert the image to RGB using PIL
    pilImage = Image.open(app.path).convert('RGB')
    # resize the image to fit the screen manually
    maxWidth, maxHeight = 600, 400
    pilImage.thumbnail((maxWidth, maxHeight))
    app.imageWidth, app.imageHeight = pilImage.size

    # set canvas dimensions to accommodate the resized image
    app.width = max(app.imageWidth, 600)
    app.height = max(app.imageHeight + 100, 500)

    # convert the PIL image to a CMU image and store it
    app.pilImage = pilImage
    app.cmuImage = CMUImage(pilImage)
    app.mousePosition = None

def redrawAll(app):
    # draw the loaded image
    imageX = (app.width - app.imageWidth) / 2
    drawImage(app.cmuImage, imageX, 60)
    drawLabel('Color Viewer', app.width/2, 20, size=16, bold=True)
    drawLabel(f'file = {app.path}', app.width/2, 35, size=14)

    # if the mouse is inside the image boundaries, show the RGB value
    if app.mousePosition:
        x, y = app.mousePosition
        if imageX <= x < (imageX + app.imageWidth) and 60 <= y < (60 + app.imageHeight):
            adjustedX = x - imageX
            adjustedY = y - 60
            r, g, b = app.pilImage.getpixel((int(adjustedX), int(adjustedY)))
            drawLabel(f'({int(adjustedX)}, {int(adjustedY)}): ({r}, {g}, {b})', app.width/2, 55, size=14)

def onMouseMove(app, mouseX, mouseY):
    # update the current mouse position
    app.mousePosition = (mouseX, mouseY)

runApp(path='level3-8x6.png')
