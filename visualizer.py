#!/usr/bin/python
"""
Search Algorithm Visualizer
"""

from space import Space, Type
from maps import input_file
from grid import blank_grid
from search import uniform_cost_search, a_star, path as gen_path
from heuristic import *
import numpy as np
from functools import partial

import argparse

from PIL import Image, ImageTk
from Tkinter import (
        Tk, Canvas, Scrollbar, Text,
        TOP, BOTTOM, BOTH,
        X, Y, N, S, E, W,
        LEFT, RIGHT, RAISED,
        HORIZONTAL, VERTICAL
    )

from ttk import Frame, Button, Label, Entry, Style


# A space with some additional properties to store g, h, f values
class TileVM(Space):
    colors = {
         Type.blocked: "#000000",
         Type.regular: "#33cc33",
         Type.rough: "#4d0000",
         Type.highway_regular: "#666699",
         Type.highway_rough: "#996600"}

    def __init__(self, space, canvas_id=None, in_fringe=False, in_path=False, is_start=False, is_goal=False):
        super(TileVM, self).__init__(space.coords, space.type)
        self.canvas_id = canvas_id
        self.is_start = is_start
        self.is_goal = is_goal
        self.in_fringe = in_fringe
        self.in_path = in_path


# The Grid where the Tiles will be placed
# Give this an array of view models
# TODO This will have to be a canvas
class Grid(Frame):
    def __init__(self, parent, tile_size, grid_vm=None):
        Frame.__init__(self, parent, relief=RAISED, borderwidth=1)
        self.parent = parent
        self.tile_size = tile_size
        self.grid_vm = grid_vm
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, pad=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, pad=3)
        hbar = Scrollbar(self, orient=HORIZONTAL)
        vbar = Scrollbar(self, orient=VERTICAL)
        canvas = Canvas(self,
                        xscrollcommand=hbar.set,
                        yscrollcommand=vbar.set
                        )
        self.canvas = canvas
        self.lines = []

        canvas.bind_all("<MouseWheel>", self._on_mousewheel_vertical)
        canvas.bind_all("<Shift-MouseWheel>", self._on_mousewheel_horizontal)

        # Set up scroll bars
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvas.xview)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)

        canvas.grid(column=0, row=0, sticky=N+W+E+S)
        hbar.grid(column=0, row=1, sticky=W+E)
        vbar.grid(column=1, row=0, sticky=N+S)

        if grid_vm:
            self.set_vm(grid_vm)

    def _on_mousewheel_vertical(self, event):
        self.canvas.yview_scroll(-1*(event.delta), "units")

    def _on_mousewheel_horizontal(self, event):
        self.canvas.xview_scroll(-1*(event.delta), "units")

    def set_vm(self, grid_vm):
        if self.grid_vm:  # Clear all old rectangles if there were any
            for tileVM in grid_vm:
                self.canvas.delete(tileVM.canvas_id)

        self.grid_vm = grid_vm
        (c, r) = grid_vm.shape
        tile_size = self.tile_size
        width = c*tile_size
        height = r*tile_size
        canvas = self.canvas
        canvas.configure(scrollregion=(0, 0, width, height))

        for line in self.lines:  # Delete existing lines
            self.canvas.delete(line)

        self.lines = []
        for i in range(0, c+1):
            self.lines.append(canvas.create_line(i*tile_size, 0, i*tile_size, height))
        for i in range(0, r+1):
            self.lines.append(canvas.create_line(0, i*tile_size, width, i*tile_size))

        for tile in grid_vm.flatten():
            self.drawTile(tile)

    def drawTile(self, tileVM):
        (c, r) = tileVM.coords
        x1 = c*self.tile_size+1
        y1 = r*self.tile_size+1
        x2 = (c+1)*self.tile_size-1
        y2 = (r+1)*self.tile_size-1
        if tileVM.is_goal:
            color = "red"
        elif tileVM.is_start:
            color = "blue"
        elif tileVM.in_path:
            color = "#ffcc00"
        else:
            color = TileVM.colors[tileVM.type]
        if tileVM.canvas_id:
            self.canvas.delete(tileVM.canvas_id)
        tileVM.canvas_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def updateFringe(self, fringe):
        pass

    def updatePath(self, path):
        for s in path:
            self.drawTile(s)

    def clicked_tile(self, event):
        pass

    def show_info_window(self, space):
        pass


# The Tk application
# Also acts as the controller for this application
class SearchVisualizerApp(Frame):

    def __init__(self, parent, speed=100, fname='map.txt', algo=uniform_cost_search, run=False):
        Frame.__init__(self, parent)

        self.parent = parent
        self.path = None
        self.grid_view = None
        self.speed = speed
        self.algo = algo
        self.run = run
        self.parent.title("Search Visualizer")
        self.style = Style().configure("TFrame", background="#333")
        self.tile_size = tile_size = 12

        self.grid_view = Grid(self, self.tile_size)
        self.grid_view.pack(fill=BOTH, expand=True)
        self.grid_view.canvas.bind('<Motion>', self._on_mouse_move)

        self.g = None
        self.h = None
        self.last_hover = None

        self.load_map(fname)
        self.pack(fill=BOTH, expand=True)

        self.algoLabel = Label(self, text="g:  h:  f:")
        self.algoLabel.pack(side=LEFT)

# TODO Check boxes to select heuristic
# TODO Button to select algorithm and restart

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        stepButton = Button(self, text="Step", command=self._step_button)
        stepButton.pack(side=RIGHT, padx=5, pady=5)
        pauseButton = Button(self, text="Start/Stop", command=self._pause_toggle)
        pauseButton.pack(side=RIGHT)
        self.bind("<space>", self._pause_toggle)
        self.bind("<q>", self._quit)

        self.centerWindow()

    def _quit(self, event):
        self.quit()

    def _on_mouse_move(self, event):
        x, y = self.grid_view.canvas.canvasx(event.x), self.grid_view.canvas.canvasy(event.y)
        c, r = np.floor(x/self.tile_size), np.floor(y/self.tile_size)
        if (c, r) is self.last_hover:
            return
        self.last_hover = (c, r)
        tile_size = self.grid_view.tile_size
        grid_vm = self.grid_view.grid_vm
        s = grid_vm[c, r]
        if self.g and self.h:
            h = self.h(s)
            g = float("inf")
            if s in self.g:
                g = self.g[s]
            f = g+h
            self.algoLabel.configure(text="g: {0} | h: {1} | f: {2}".format(g, h, f))

    def _pause_toggle(self, event=None):
        self.run = not self.run
        if self.run:
            self.loop()

    def _step_button(self):
        self.run = False
        self.step()

    # Change the search generator to use
    def set_search(self, search):
        pass

    def load_map(self, fname):
        (grid, start, goal) = input_file(fname)
        grid_vm = np.array([TileVM(v) for v in grid.flatten()]).reshape(grid.shape)
        grid_vm[start].is_start = True
        grid_vm[goal].is_goal = True
        self.search = self.algo(grid_vm, grid_vm[start], grid_vm[goal])
        self.grid_view.set_vm(grid_vm)

    # Update the Grid
    def loop(self):
        if self.run:
            self.step()
            self.parent.after(self.speed, self.loop)

    def step(self):
        try:
            (g, h, parent, curr) = self.search.next()
            self.g = g
            self.h = h

# TODO Change fringe to binary heap show nodes that are in the fringe
            if self.path:
                for s in self.path:
                    s.in_path = False
                    self.grid_view.drawTile(s)
            self.path = gen_path(parent, curr)
            for s in self.path:
                s.in_path = True
                self.grid_view.drawTile(s)
        except StopIteration:
            self.run = False

    def centerWindow(self):
        # TODO: Modify this to instead show second window to specific position
        grid = self.grid_view.grid_vm
        tile_size = self.grid_view.tile_size
        (x, y) = grid.shape
        w = x*tile_size + 50
        h = y*tile_size + 150
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (min(sw, w), min(sh, h), x, y))


def main():
    (fname, algo, speed) = process_args()
    root = Tk()
    app = SearchVisualizerApp(root, fname=fname, speed=speed, algo=algo)
    app.loop()
    root.mainloop()

def process_args():
    parser = argparse.ArgumentParser(description='Run a visualization of search algoirthms')
    parser.add_argument('input_file', metavar='map', type=str, nargs=1, default='map.txt',
                        help='The map text input file')
    parser.add_argument('--speed', '-s', metavar='S', type=int, default=100,
                        help='The speed of the visualization (default 100)')
    parser.add_argument('--algorithm', '-a', metavar='algo', type=str, choices=['u', 'a'], default='a',
                        help='The search algorithm to use\n \
                                u: Uniform Cost Search\n \
                                a: A star search\n \
                                aw: A star weighted')
    parser.add_argument('--heuristic', '-f', metavar='h(n)', type=str, choices=['m', 'ma', 'd', 'e'], default='d',
                        help='The heuristic to use\n\
                                m: Manhattan Distance\n\
                                ma: Manhattan Distance admissible \n\
                                d: Diagonal Distance\n \
                                e: Euclidian Distance')
    parser.add_argument('--weight', '-w', metavar='W', type=float, default=1.,
                        help="The weight to use for A Star weighted")
    parser.add_argument('--favor-highways', '-g', action='store_true',
                        help="Whether the heuristic should favor highways")
    args = parser.parse_args()

    algorithms = {'u': uniform_cost_search, 'a': a_star}
    heuristics = {'m': manhattan_distance,
                  'ma': make_admissible(manhattan_distance),
                  'd': diagonal_distance,
                  'e': euclidian_distance,
                  }
    print args
    algo = algorithms[args.algorithm]
    h = heuristics[args.heuristic]
    w = args.weight
    fh = args.favor_highways

    if algo is a_star:
        if fh:
            h = favor_highways(h)
        algo = partial(algo, heuristic=h, w=w)

    speed = args.speed
    return (args.input_file[0], algo, speed)



if __name__ == '__main__':
    main()
