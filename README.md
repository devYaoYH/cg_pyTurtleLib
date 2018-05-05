# cg_pyTurtleLib (python2/3 compatible!)
Versatile Python Tkinter (turtle) based drawing code for displaying the game state, debugging physics simulations etc...

## Drawing functions
```
def drawLine(s, e, c=None, thickness=1): ...
```
- Draws a line from starting point *s* to end point *e*.

```
def drawRect(p_tl, p_br, c=None, fill=None, thickness=1): ...
```
- Draws a rectangle from specified *top-left* point to *bottom-right* point.

```
def drawCircle(pos, radius, c=None, fill=None, thickness=1): ...
```
- Draw a circle centered around *pos* of size *radius*.

```
def drawLabel(pos, txt, c=None, fontType="Arial", size=11, style="normal"): ...
```
- Writes a *txt* string centered at *pos* and bottom-aligned to *pos* (words appear above pos.y).

## Config
Simply setup the value of *SIZE_X* and *SIZE_Y* to be the size of the game area and a suitable *SCALING* factor (depending on your screen resolution).
```
# Setup Display Configuration
SIZE_X = 1920
SIZE_Y = 900
SCALING = 0.5
```
And...you're good to go!

## Debugging Game State
One way I like to do this is to encapsulate my game simulation within a *game* object and call *game.turn()* to execute the turn and update visuals.
```
physSim = game()
while(PAUSE() != 'END'):
    physSim.turn()
```
The *PAUSE()* is there so I control and view the results of each round (alternative control is available in a *DELAY(ms)* to animate the simulation! :D


The code is loaded with an assortment of random lines and some test circles/rectangles :P
