# SpareSomeChange
Re-Creation of 'Spare Change' video game 
README.txt

This is my re-creation of the classic (Apple IIe) area video game, Spare Change.
https://en.wikipedia.org/wiki/Spare_Change_(video_game)
It was created by Dan and Mike Zeller and published in 1983 by Broderbund.
As the owner of a video arcade, your goal is to fill your token bin to earn enough credits to go on to the next level.
Unlike most video games, the two enemy Zerks can't harm you, but if they fill up their token bin first, its game over.

Status:
Beta

How to launch:
 - The main function is in SpareSomeChange.py

Required Libraries:
 - Python
 - Arcade  https://api.arcade.academy/en/latest/

How to Play:
The game requires moving around resources to keep the tokens flowing while preventing the Zerks from getting their hands (?) on tokens.  Collect enough tokens to open the exit before the Zerks fill up their bin.

The controls:
Only the arrow keys are used. Multiple keys can be pressed down at the same time to move diagonaly.  To interact with a machine, tap the arrow key in the direction of the machine. If you walked up to the machine in that direction, you will have to release the key and hit it again.  (If your player raises her hand, you interacted with the machine.)

You:
You are the human figure. You can carry one object at a time.

Them:
The Zerks have esacped their video game machine and are running a-muck. A Zerk can carry a token.

The game field:

Each level has a variety of machines that make up your video arcade. Some have doors/drawers that need to be opened first. (Not yet implemented)

Your Token Bin:
This is the two stacked squares near the middle of the screen. To drop a token in the bin, stand on top and tap the down key.

Token Machines:
These machines start with two tokens, which can be accessed from the bottom. Token machines can be re-filled (up to a point) by putting bills in the notch on the side.

Cash Register:
By accessing the left side, you can get bills or refill it by putting in money bags.

Safe:
By accessing the right side, you can get money bags.

Slot Machine: (Not yet implemented)
By accessing the left side, you can put in bills to win (maybe) some tokens

Zerk Bank:
Zerk's put their tokens in their piggy bank. Too many and its game over.

Exit:
Once you have 10 tokens in your bin, the exit will open. Access it from the bottom. Exiting is the only way to reset the Zerk bank.

Distractions: These machines distract the Zerks, for a time...

JukeBox: Put tokens in the right side.

Pay Phone: If the level has two pay phones, you can put a token into the left side of either.

Popcorn Machine: Tokens can be put in the right side.

Level Rules: 
When you exit the level, you will recieve points for each token in your upper bin (each token over 9). Once you aquire 9 points, you will advance to the next level. Since its a classic video game, levels loop forever, gradually getting harder.  (Not yet implemented)

Uses Python Arcade Features:
- Window, Views, draw/update
- Sprites
- Collision detection
- Pathfinding
- Particles

Arcade Version:
 - Developed on Arcade version 2.5.7

What works:
- Player movement and carrying of objects
- Player collision detection
- Machines and bins accept and dispence objects
- Zerks visit and interact with machines
- Zerks take collision fee paths
- Player can steal from Zerks
- Jukebox, paired phones, and popcorn machine will distract Zerk
- Interaction animation for player and Zerks
- Zerk's are animated while distracted
- Welcome screen
- Esc to pause, any key to un-pause
- Level and points displayed in game view
- Player can exit
- Tokens in upper bin become points
- Enough points trigger the next level
- Level 0: Easier tutorial level with machine interaction hints
- Levels 1, 2, 3

Missing Features:
- Goal and mood based behavior for Zerks
- Game over condition
- Token machine can only be refilled a number of times
- More varied layout of machines between levels
- Coin deposit animations for Zerks (toss to bank, lob to bank, kick to bank, toss to Zerk)
- Drawer/door states for cash register and safe
- Walk animation for player and Zerks
- Numeric token counter for Zerk bank
- Colored icons for machines
- Sound
- Better way of teaching players how to play
- Demo mode
- Invent new features: Zerks play video game, Zerks chaced by Roomba, etc
