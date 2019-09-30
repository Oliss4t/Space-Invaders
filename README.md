# Space-Invaders
# by Tassilo Henninger

This is a Space-Invaders clone I programmed during the September 2019 [it-talents](https://www.it-talents.de/foerderung/code-competition/airbus-code-competition-09-2019) code competition.
The code is commented via docstring, so you can get info of a method or class via `help(name)`.

# Basic game elements
The goal was to develop your own version of Space Invaders, including the basic game mechanics like:
* a controllable defense ship
* aliens attacking from the top of the screen
* and the aliens should be able to come closer and shoot

# Features
In addition to the basic game mechanics I implemented the following features:
* game menu
* player ship evolvement (lvl 1: one bullet, lvl 2: two bullets, lvl 3: four bullets)
* bonus alien ship (give 100 extra points, but is hard to hit)
* asteroid blockers (protect the playership from alien bullets)
* progressing game diffculty, by changing the amount of spawning aliens after each completed game round.
* different game difficulties (regarding amount of lives, levelup ranges, amount of asteroid blockers and alien rows and columns at the start)
* encryption of the highscore list with AES (you are not able to cheat via editing the json highscore file)
* two player offline multiplayer mode. Each player can only attack the aliens with the same colour as their own ship. Therefore a good coordination is needed.

# How to start the game
The game is developed in python 3.7 using the libraries: pycryptodome, pygame, pygame-menu.

* If you have the correct python version and libraries installed, you can run the game via the command prompt: `python main.py`
* If you don't have python and the libraries installed, you can simply double click the `.exe file` to play the game. The `.exe file` is located at `\dist\main.exe`. Note: The `.exe file` needs to stay in the same directory as the sounds and images folders, aswell as gamescores.json.enc file.

# How to play the game
The game is played on 1200/900 resolution.
The player game score is in the left top, the current game round in the middle top and the player lives on the top right hand side.
## Controls
* Move: left and right arrow key or 'a' and 'd' key
* Shoot: SPACEBAR or RETURN + 'L-' and 'R-' Shift in multiplayer mode
* Pause: ESC key


---
>Thanks for checking out my game and I hope you enjoy it! Feel free to contact me.
>Tassilo Henninger
>[tassilo.henninger@gmail.com](mailto:tassilo.henninger@gmail.com)
---
![alt text](https://github.com/Oliss4t/Space-Invaders/blob/docu/readme_images/gamemenu.PNG)
---
![alt text](https://github.com/Oliss4t/Space-Invaders/blob/docu/readme_images/game_singleplayer.PNG)
---
![alt text](https://github.com/Oliss4t/Space-Invaders/blob/docu/readme_images/game_multiplayer.PNG)
---
![alt text](https://github.com/Oliss4t/Space-Invaders/blob/docu/readme_images/gameover.PNG)
---







