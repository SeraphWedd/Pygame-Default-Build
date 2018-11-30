8:40 PM 11/29/2018
This is my default game loop used in creating games with pygame.
This copy is free to use and anyone can use it.
If you want to credit me, credit me as @SeraphWedd or @SeraphGames


Modifications should be done to:

configuration.info -> if you want to add more configurations for your game

Resources/resources.load -> add all the images and audio that you will use in the game

setup.py -> Mostly, add the files you want to include that isn't included in the first two folders to where it should be.

Scripts/engine.py -> Edit the screens (splash, instruction, etc.)

Scripts/game.py -> This holds the main game. This is where you will place your game.


Other configurations can be done too. Though you need to get the outline of the game loop first. Edit at your own risk.

Main loop of the game:
gameloop.py -> Scripts/engine.py -> Scripts/game.py

 - gameloop.py handles the general loop involving the event handling (key presses, quit, etc.)

 - engine.py handles the display loop. It switches from splash -> instruction -> main menu -> game/credits/instructions with a transition screen ("alpha to black" fading)

 - game.py handles the main game loop. This is where your game lives. This file is where you put all your hard work into. Keep in mind that the Game class should always be a single pass, not an infinite loop, as it may turn the game into a wobbly buggy mess.



