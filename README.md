# Sokoban

Project Title & Description

- This is Sokoban, which translates from Japanese to literally mean "warehouse keeper".
- This is a puzzle game that involves moving around a warehouse worker to push various-colored boxes to their target locations. Due to the layout of each level, there is a specific way and order the player must follow to win. This game tests the player's logic and helps tackle problem solving capabilities.

Run Instructions:

- To run the game, the player must have a png file of a Sokoban map, and the name of the file must specifically be leveln-ixj.png, where n stands for the level number and i and j stand for the number of rows and columns of the given level, respectively. 
- This must be put into the loadLevel() function in sokoban_loader.py, where the png file will then be analyzed and a 2D list rendering of the inputted map will be created. This will then be converted to an actual Sokoban map on a canvas where the player will be able to play.
- To be able to properly take in images and use them, PIL image and CMUImages must be installed. For PIL Images, "python3 -m pip install pillow" should be typed into the terminal, and CMUImages should be included in the cmu_graphics library by calling "from cmu_graphics import CMUImage".
- Note that the pickle and os modules are used in sokoban_loader.py to cache files for quicker analysis. The math module was also used to compute the Euclidean Distance between RGB values for color classification. In sokoban_player.py, we used "from sokoban_loader.py import *" to be able to load the levels.
- https://academy.cs.cmu.edu/desktop this must also be installed to run this project

Shortcut Commands:

- press the arrow keys to move the player in each direction (up, down, left, right)
- press u to undo the last move made
- press r to restart the level
- press 1-4 to load the respective levels
- (NOTE: this is only for level 1 for grading purposes) press a to nearly solve the map by bringing it to nearly one move left
