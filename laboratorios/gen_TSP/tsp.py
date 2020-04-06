from tkinter import *
from tkinter.ttk import *
from time import sleep
import random
from random import randint
from genetic import *

class TSPApp():
    SIZE = 3
    def __init__(self):
        self.cities = []
        self.lines = []
        self.root = Tk()
        self.root.title("Genetic TSP")
        self.root.geometry('720x480')

        self.map = Canvas(self.root, width=720, height=370)
        self.map.grid(column=0, row=0, columnspan=5)
        self.map.configure(bg='white')

        self.cities_lbl = Label(self.root, text='Numero de ciudades')
        self.cities_lbl.grid(column=0, row=1)

        self.cities_spin = Spinbox(self.root, from_=5, to=50, width=5)
        self.cities_spin.grid(column=1, row=1)

        self.generate_btn = Button(self.root, text='Generar  \nCiudades', command=self.generateHandler)
        self.generate_btn.grid(column=2, row=1)

        self.init_lbl = Label(self.root, text='Tamaño de la poblacion')
        self.init_lbl.grid(column=0, row=2)

        self.init_txt = Entry(self.root, width=10)
        self.init_txt.grid(column=1, row=2)

        self.init_btn = Button(self.root, text='Iniciar Poblacion', command=self.initHandler)
        self.init_btn.grid(column=2, row=2)

        self.root.mainloop()

    def generateHandler(self):
        for c in self.cities:
            self.map.delete(c['id'])

        for l in self.lines:
            self.map.delete(l)

        n = int(self.cities_spin.get())
        w = int(self.map.config('width')[-1])
        h = int(self.map.config('height')[-1])
        print(f'Generando: {n} ciudades...')
        print(f'Map Size: ({w},{h})')
        for i in range(n):
            x = randint(0, w - self.SIZE)
            y = randint(0, h - self.SIZE)
            city = {'position': (x, y), 'id': self.map.create_rectangle(x, y, x + self.SIZE, y + self.SIZE, fill='red', tags=str(i))}
            self.cities.append(city)

    def draw_solution(self, candidate):
        self.lines = []
        for i in range(len(candidate) - 1):
            l = self.map.create_line(self.cities[candidate[i]]['position'][0], 
                                    self.cities[candidate[i]]['position'][1],
                                    self.cities[candidate[i+1]]['position'][0],
                                    self.cities[candidate[i+1]]['position'][1])
            self.lines.append(l)
        # return lines

    def initHandler(self):
        for l in self.lines:
            self.map.delete(l)
        pop_size = int(self.init_txt.get())
        first = initPopulation(self.cities, pop_size)
        # draw a candidate
        random_candidate = random.choice(first)
        self.draw_solution(random_candidate)
        print(first)
        for f in first:
            print(f)
            print(cost(f, self.cities))


if __name__ == '__main__':
    app = TSPApp()