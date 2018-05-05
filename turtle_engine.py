from __future__ import print_function
import sys
import math
import time
import turtle
import random

##########################
##########################
## pyTurtle Drawing Lib ##
##~~~~~ K O D L E ~~~~~~##
##########################
##########################

# Compatibility
if (sys.version_info.major > 2):
    xrange = range
    raw_input = input

##################
# TIMER FUNCTION #
##################
def debug_time(msg, init, now):
    print("{} {}ms".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

################
# MATH HELPERS #
################
EPSILON = 0.00000001

def absRad(r):
    if (r >= -math.pi and r <= math.pi):
        return r
    return r-(r//math.pi)*math.pi

def vectorFromRad(r):
    return Vector(math.cos(r), math.sin(r))

##############
# PRIMITIVES #
##############
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({} {})".format(self.x, self.y)

    def __add__(self, o):
        if (isinstance(o, Vector)):
            return Point(self.x+o.vx, self.y+o.vy)
        print("TYPE ERROR (Point-Vector Addition): ", o, file=sys.stderr)
        return None

    def __sub__(self, o):
        if (isinstance(o, Point)):
            return Vector(self.x-o.x, self.y-o.y)
        elif (isinstance(o, Vector)):
            return Point(self.x-o.vx, self.y-o.vy)
        return None

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __abs__(self):
        return math.sqrt(self.x**2+self.y**2)

    def round(self):
        return Point(round(self.x), round(self.y))

    def distTo(self, o):
        if (isinstance(o, Point)):
            return abs(o-self)
        print("TYPE ERROR (distance to point): ", o, file=sys.stderr)
        return None

    def vecTo(self, o):
        if (isinstance(o, Point)):
            return o-self
        print("TYPE ERROR (vector between points): ", o, file=sys.stderr)
        return None

    def dirTo(self, o):
        if (isinstance(o, Point)):
            return self.vecTo(o).rad
        return None

    def setPoint(self, x, y):
        self.x = x
        self.y = y

    def movePt(self, p):
        self.x = p.x
        self.y = p.y

class Vector(object):
    def __init__(self, vx, vy):
        self.v = (vx, vy)
        self.vx = vx
        self.vy = vy
        self.rad = math.atan2(float(vy), float(vx))
        self.length = abs(self)
        self.norm = self
        if (abs(self.length - 1) > EPSILON and self.length != 0):
            self.norm = Vector(self.vx/self.length, self.vy/self.length)

    def __str__(self):
        return "({} {})".format(self.vx, self.vy)

    def __add__(self, o):
        if (isinstance(o, Point)):
            return Point(o.x+self.vx, o.y+self.vy)
        elif(isinstance(o, Vector)):
            return Vector(self.vx+o.vx, self.vy+o.vy)
        print("TYPE ERROR (Vector addition): ", o, file=sys.stderr)
        return None

    def __sub__(self, o):
        if (isinstance(o, Vector)):
            return Vector(self.vx-o.vx, self.vy-o.vy)
        print("TYPE ERROR (Vector subtraction): ", o, file=sys.stderr)
        return None

    def __mul__(self, k):
        if (isinstance(k, int) or isinstance(k, float)):
            return Vector(self.vx*k, self.vy*k)
        print("TYPE ERROR (Vector multiplication with constant): ", k, file=sys.stderr)
        return None

    def __xor__(self, o): # DOT PDT
        if (isinstance(o, Vector)):
            return self.vx*o.vx+self.vy*o.vy
        print("TYPE ERROR (Vector dot-pdt): ", o, file=sys.stderr)
        return None

    def __neg__(self):
        return Vector(-self.vx, -self.vy)

    def __abs__(self):
        return math.sqrt(self.vx**2+self.vy**2)

    def round(self):
        return Vector(round(self.vx), round(self.vy))

    def dirTo(self, o):
        if (isinstance(o, Vector)):
            return absRad(self.rad-o.rad)
        print("TYPE ERROR (Vector angular difference): ", o, file=sys.stderr)
        return None

    def proj(self, o):
        if (isinstance(o, Vector)):
            return o.norm*(self^o.norm)
        print("TYPE ERROR (Vector projection): ", o, file=sys.stderr)
        return None

##########
# CONFIG #
##########
# COLORS
col_black = (0, 0, 0)
col_grey = (216, 216, 216)
col_red = (196, 32, 32)
col_green = (32, 196, 32)
col_blue = (32, 32, 196)
col_purple = (196, 32, 196)

# Setup Display Configuration
SIZE_X = 1920
SIZE_Y = 900
SCALING = 0.5

############################
# Turtle-drawing functions #
############################
turtle.setup(SIZE_X*SCALING+50, SIZE_Y*SCALING+50)

SCREEN = turtle.Screen()
SCREEN.colormode(255)               # Set to RGB color mode

TPEN = turtle.RawTurtle(SCREEN)
TPEN.speed('fastest')               # Speed optimisations for turtle
TPEN.ht()                           # Hide the little turtle that helps us draw

if (sys.version_info.major > 2):    # Disable animations => Faster drawing of graphics
    SCREEN.tracer(0, 0)
else:
    TPEN.tracer(0, 0)

# (0, 0) adjusted to TOP-LEFT corner
def setPos(pos):
    x = pos.x - SIZE_X/2
    y = -(pos.y -SIZE_Y/2)
    TPEN.up()
    TPEN.setpos(x*SCALING, y*SCALING)
    TPEN.down()

def drawLine(s, e, c=None, thickness=1):
    TPEN.color('black' if c is None else c)
    TPEN.pensize(thickness)
    setPos(s)
    x = e.x - SIZE_X/2
    y = -(e.y -SIZE_Y/2)
    TPEN.setpos(x*SCALING, y*SCALING)

# point(top-left) to point(bottom-right)
def drawRect(p_tl, p_br, c=None, fill=None, thickness=1):
    TPEN.color('black' if c is None else c, 'white' if fill is None else fill)
    TPEN.pensize(thickness)
    setPos(p_tl)
    width = p_br.x - p_tl.x
    height = p_br.y - p_tl.y
    if (fill is not None):
        TPEN.begin_fill()
    TPEN.forward(width*SCALING)
    TPEN.right(90)
    TPEN.forward(height*SCALING)
    TPEN.right(90)
    TPEN.forward(width*SCALING)
    TPEN.right(90)
    TPEN.forward(height*SCALING)
    TPEN.right(90)
    if (fill is not None):
        TPEN.end_fill()

def drawCircle(pos, radius, c=None, fill=None, thickness=1):
    TPEN.color('black' if c is None else c, 'white' if fill is None else fill)
    TPEN.pensize(thickness)
    setPos(pos)
    TPEN.up()
    TPEN.right(90)
    TPEN.forward(radius*SCALING)
    TPEN.left(90)
    TPEN.down()
    if (fill is not None):
        TPEN.begin_fill()
    TPEN.circle(radius*SCALING)
    if (fill is not None):
        TPEN.end_fill()
    TPEN.up()
    TPEN.left(90)
    TPEN.forward(radius*SCALING)
    TPEN.right(90)
    TPEN.down()

def drawLabel(pos, txt, c=None, fontType="Arial", size=11, style="normal"):
    TPEN.color('black' if c is None else c)
    setPos(pos)
    TPEN.write(txt, align='center', font=(fontType, size, style))

# Delay Function
def DELAY(t):
    turtle.update()
    time.sleep(t)

# Pause Function
def PAUSE():
    turtle.update()
    return raw_input("ENTER to continue (END to stop):")

##################################
# SIM SPECIFIC DRAWING FUNCTIONS #
##################################
def t_BEGIN():      # Splash Screen!
    drawRect(Point(0, 0), Point(SIZE_X, SIZE_Y))
    drawLabel(Point(SIZE_X/2, SIZE_Y/2), "pyTurtle Graphics Lib", size=30, style="bold")

def t_REFRESH():    # Refresh each turn
    TPEN.clear()
    drawRect(Point(0, 0), Point(SIZE_X, SIZE_Y))

############
# GAME SIM #
############
class game(object):
    def __init__(self):
        t_BEGIN()

    def turn(self):
        t_REFRESH()
        turnT = time.time()
        drawCircle(Point(400, 200), 30)
        drawCircle(Point(700, 200), 30, fill=col_blue, thickness=3)
        drawRect(Point(500, 500), Point(700, 600), c=col_blue)
        drawRect(Point(900, 500), Point(1100, 600), c=col_blue, fill=col_purple, thickness=3)
        for i in xrange(5):
            s = Point(random.randint(900, 1900), random.randint(50, 350))
            e = Point(random.randint(900, 1900), random.randint(50, 350))
            drawLine(s, e, thickness=3, c=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        drawRect(Point(1200, 60), Point(1600, 110), c=col_grey, fill=col_grey)
        drawLabel(Point(1400, 100), "Wheee, Random Lines!")
        debug_time("Turn time:", turnT, time.time())

################
# Begin Visual #
################
physSim = game()
while(PAUSE() != 'END'):
    physSim.turn()