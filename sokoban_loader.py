from PIL import Image
from cmu_graphics import CMUImage
import pickle
import os
import math

COLORS = {
    'red': (175, 72, 68),
    'green': (114, 187, 81),
    'blue': (66, 82, 182),
    'violet': (149, 69, 182),
    'cyan': (101, 186, 187),
    'brown': (218, 168, 75),  # wall
    'tan': (245, 218, 131),  # player

    # targets 
    'redTarget': (174, 72, 68), 
    'greenTarget': (114, 187, 82), 
    'blueTarget': (66, 82, 182),  
    'violetTarget': (149, 69, 182), 
    'cyanTarget': (101, 186 , 188), 
}

PIECE_COLORS = ['red', 'green', 'blue', 'violet', 'cyan']

def readPickleFile(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def writePickleFile(path, contents):
    with open(path, 'wb') as f:
        pickle.dump(contents, f)

def loadHardcodedLevel():
    level = [
        ['-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w'],
        ['-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w'],
        ['-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w'],
        ['-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w'],
        ['w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w'],
        ['w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w'],
        ['-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w'],
        ['-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w'],
        ['-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
    ]
    images = dict()
    return level, images

def determineCellContent(cellImage):
    # initialize pixel counts dictionary
    pixelCounts = {}
    for color in COLORS.keys():
        pixelCounts[color] = 0

    width, height = cellImage.size  # cell dimensions

    # count matching pixels for each color
    for x in range(width):
        for y in range(height):
            r, g, b = cellImage.getpixel((x, y))
            for color, rgbValues in COLORS.items():
                cr, cg, cb = rgbValues
                # euclidean distance
                distance = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
                if distance < 80: 
                    pixelCounts[color] += 1

    # thresholds for classification
    blockThreshold = 4000 
    targetThreshold = 500
    wallThreshold = 5000  
    playerThreshold = 500  

    # wall
    if pixelCounts['brown'] > wallThreshold:
        return 'w'

    # player
    if pixelCounts['tan'] > playerThreshold:
        return 'p'

    # green
    if pixelCounts['green'] > blockThreshold:
        return 'g'
    if pixelCounts['greenTarget'] > targetThreshold:
        return 'G'

    # red
    if pixelCounts['red'] > blockThreshold:
        return 'r'
    if pixelCounts['redTarget'] > targetThreshold:
        return 'R'

    # blue
    if pixelCounts['blue'] > blockThreshold:
        return 'b'
    if pixelCounts['blueTarget'] > targetThreshold:
        return 'B'

    # violet
    if pixelCounts['violet'] > blockThreshold:
        return 'v'
    if pixelCounts['violetTarget'] > targetThreshold:
        return 'V'

    # cyan
    if pixelCounts['cyan'] > blockThreshold:
        return 'c'
    if pixelCounts['cyanTarget'] > targetThreshold:
        return 'C'

    # empty
    return '-'

def getDimensions(filename):
    dimensions = filename.split('-')[-1].split('.')[0]
    rows, cols = dimensions.split('x')
    rows = int(rows)
    cols = int(cols)
    return rows, cols

def loadLevel(path):
    # first return a hardcoded level for testing
    if path is None:
        return loadHardcodedLevel()

    cachePath = f'{path}.pickle'
    
    # check for cached results
    if os.path.exists(cachePath):
        return readPickleFile(cachePath)

    pilImage = Image.open(path).convert('RGB')
    rows, cols = getDimensions(path)
    cellWidth = pilImage.width // cols
    cellHeight = pilImage.height // rows
    level = []
    images = {}

    for row in range(rows):
        levelRow = []
        for col in range(cols):
            # margins of 4
            left = col * cellWidth + 4
            top = row * cellHeight + 4
            right = (col + 1) * cellWidth - 4
            bottom = (row + 1) * cellHeight - 4
            cellImage = pilImage.crop((left, top, right, bottom))

            content = determineCellContent(cellImage)
            levelRow.append(content)

            if content not in images and content != '-':
                images[content] = CMUImage(cellImage)
        level.append(levelRow)
    # cache the result
    writePickleFile(cachePath, (level, images))

    return level, images

## TEST CASES ##

def testSokobanLoader():
    print('Testing sokoban_loader...')
    files = ['level1-10x10.png',
             'level2-7x9.png',
             'level3-8x6.png',
             'level4-8x6.png']
    
    correctLevels = [
        # level1-10x10.png
        [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
          [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
          [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
          [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
          [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ],

        # level2-7x9.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', '-' ],
          [ 'w', 'R', 'G', 'B', 'V', 'w', 'w', 'w', 'w' ],
          [ 'w', 'p', '-', 'r', 'g', 'b', '-', '-', 'w' ],
          [ 'w', 'w', '-', '-', 'v', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', '-', 'w', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level3-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'p', '-', 'w' ],
          [ 'w', '-', 'r', '-', '-', 'w' ],
          [ 'w', 'w', '-', 'w', 'g', 'w' ],
          [ 'w', '-', 'b', 'v', '-', 'w' ],
          [ 'w', '-', '-', 'c', 'B', 'w' ],
          [ 'w', 'C', 'R', 'V', 'G', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level4-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', 'B', 'G', 'p', 'R', 'w' ],
          [ 'w', '-', '-', 'r', '-', 'w' ],
          [ 'w', 'w', 'g', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'b', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ],
    ]

    for i in range(len(files)):
        file = files[i]
        correctLevel = correctLevels[i]
        level, images = loadLevel(file)
        if level != correctLevel:
            print(f'{file} is incorrect!')
            print('Correct result:')
            print(correctLevel)
            print('Your result:')
            print(level)
            assert(False)
        print(f'  {file} is correct')
    print('Passed!')

if __name__ == '__main__':
    testSokobanLoader()