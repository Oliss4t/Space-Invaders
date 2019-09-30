# Space-Invaders
# by Tassilo Henninger

This is a Space-Invaders clone i programmed during the september 2019 it-talents code competition (https://www.it-talents.de).
The Code is commented via docstring, so you can get info of an method or class via help(name)

The goal was to develop your own version of Space Invaders, including the basic game mechanics like:
--> a controllable defense ship
--> aliens attacking from the top of the screen
--> and the alies should be able to come closer and shoot

In additon to the basic game mechanics i implemented the following features:
--> player ship envolement (lvl 1: one bullet, lvl 2: two bullets, lvl 3: four bullets)
--> bonus alien ship (give 100 extra points, but are hard to hit)
--> asteroid blockers (protect the playership from alien bullets)
--> progressing game diffcultie by changing the amount of spawning aliens after each completed game round.
--> different game difficulties (regarding amount of lifes,levelup ranges, amount of asteroid blockers and alien rows and columns at the start)
--> encryption of the highscore list with AES (you are not abel to cheat via eddeting the json highscore file)
--> two player offline multiplayer mode. each player can only attack the alins with the same colour as their own ship. Therfore a good coordination is needed.


How to start the game:
The game is developed in python 3.7 using the following libraries:
--> pycryptodome
--> pygame
--> pygame-menu

If you have the correct python version and libraries installed, you can run the game via the command prompt : "python main.py"
If you don't have Python or Pygame installed, you can simply double click the .exe file to play the game. Note: The .exe file needs to stay in the same directory as the sounds, images, and font folders.

The game is played on 1200/900 resolution.
The player gamescore is on the left hand side, the current gameround in the middle top and the player lifes on the top right hand side.







 , have fun




