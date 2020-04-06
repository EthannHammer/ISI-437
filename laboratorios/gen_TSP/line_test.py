# draw lines and rectangles
 
import tkinter as tk
 
master = tk.Tk()
 
 
def rectangle(event):
    w.create_rectangle(event.x, event.y, event.x + 10, event.y + 10, fill="blue")
 
 
def line(event):
    w.create_line(0, 0, event.x, event.y)
 
 
def bind_rectangle():
    "Create a rectangle of 10x10"
    master.bind("<Button-1>", rectangle)
 
 
def bind_line():
    master.bind("<Button-1>", line)
 
 
w = tk.Canvas(master, width=400, height=400)
w.pack()
 
button_rectangle = tk.Button(text="Rectangle", command=bind_rectangle).pack()
button_line = tk.Button(text="line", command=bind_line).pack()
 
master.mainloop()