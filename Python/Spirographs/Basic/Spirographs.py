import turtle as t
import math

def drawCircleTurtle(x, y, r, res):
    #move to the start of circle
    t.up()
    t.setpos(x + r, y)
    t.down()

    circleSteps = range(0,360 + res,res)
    #draw the circle
    for i in circleSteps:
        a = math.radians(i)
        exe = x + r * math.cos(a)
        why = y + r * math.sin(a)
        t.setpos(exe,why)

drawCircleTurtle(100,100,50, 5)
t.mainloop()