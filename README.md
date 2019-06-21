# whack-a-trellis

An electronic whack-a-mole game which uses Adafruit's Trellis M4 in CircuitPython.

# Credits

Trellis M4 Circuit Python Libraries from Adafruit:https://github.com/adafruit/Adafruit_CircuitPython_TrellisM4

Minimum Alpha Font from jjmajava: https://gist.github.com/jjmajava/977646457e00be87bb2e

Sound: https://www.leshylabs.com/apps/sfMaker/

# Rule

## Title Screen

Title displays the current high-score.  Press any button to start game.

## Game Screen

```
# O O O O O O #
# O O O O O O #
# O O O O O O #
# O O O O O O #

# Life meter (blue)
O 6 x 4 game field button
```

## Game Play

A mole (white LED light) will appear randomly.  Press the corresponding button to hit the mole before it disappears.  If mole is hit, the field button turns green.  If the mole disappears, the field button will turn red and will decrease life (blue LED light on the  two sides.

In each game, user is given 9 lives.  When player misses the nineth mole, the game ends.

Game difficulty will increase as game progresses.  A simultaneous button press beyond 8 will be ignored and player will be penalized by sudden jump in difficulty.

## Score

A mole hit is worth 1 point.  At the end of game, the score will be displayed.

## Score Display System

Up to 2 least significant digits will be displayed, as well as green do to indicate 100 points.

e.g. 12 + 1 dot = 112

Normally the digits are displayed in blue LED. If player beats the current record, the points will be displayed in yellow LED.

Press any button to return to title screen.


