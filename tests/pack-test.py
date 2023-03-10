import tkinter as tk
from numpy.random import randint, choice

DIFF = 2
N = 10

WIDTH = 800
HEIGHT = 600

wd = 70
hd = 20

root = tk.Tk()
root.minsize(WIDTH, HEIGHT)
root.maxsize(WIDTH, HEIGHT)

chars = ['6','6','?','x','X','#','+']
#chars = ['o','O']

sides = ['top','bottom','left', 'right']

codes = [''.join(choice(chars) for i in range(DIFF)) for _ in range(N)]
correct = randint(N)

points = 0

def cmd_success():
    global butts, DIFF, var, pts, points
    print('Found it!')
    points += 1

    for b in butts:
        b.destroy()
    butts = []

    DIFF += 1

    codes = [''.join(choice(chars) for i in range(DIFF)) for _ in range(N)]
    correct = randint(N)

    var.set(codes[correct])
    pts.set("Points: %d" % points)

    print('Find me %s' % codes[correct])

    for i in range(N):
        btn = tk.Button(root, text=codes[i], command=cmd_success if codes[i]==codes[correct] else cmd_fail)
        btn.place(x = randint(0,WIDTH-wd), y =randint(0,HEIGHT-hd))
        butts.append(btn)

def cmd_fail():
    global pts, points
    points -= 1
    pts.set("Points: %d" % points)
    for b in butts:
        b.place(x = randint(0,WIDTH-wd), y =randint(0,HEIGHT-hd))
    print('Bad one...')

print('Find me %s' % codes[correct])

butts = []
for i in range(N):
    btn = tk.Button(root, text=codes[i], command=cmd_success if codes[i]==codes[correct] else cmd_fail)
    btn.place(x = randint(wd,WIDTH-wd), y =randint(hd,HEIGHT-hd), anchor=tk.CENTER)
    butts.append(btn)

var = tk.StringVar()
target = tk.Label(root, textvariable=var, relief=tk.RAISED)
var.set(codes[correct])
target.place(x = WIDTH / 2, y = HEIGHT / 2)

pts = tk.StringVar()
plab = tk.Label(root, textvariable=pts)
pts.set("Points: %d" % points)
plab.place(x = WIDTH / 2, y = 30 , anchor=tk.CENTER)

root.mainloop()
