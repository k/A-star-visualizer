# Assignment 1

This is a Civilization-like grid map that will be used to calculate shortest paths with A*.

![Gif of path finding](http://io.k33.me/gifs/astar-visualizer.gif)

## Requirements

This project requires:
* Python 2.7
* Numpy
* Tkinter
* pqdict (default) or bintrees depending on which data structure is used for the fringe

## Quickstart

To install requirements run

```bash
pip install -r requirements.txt
```

Generate 10 text maps by running

```bash
python gen_maps.py -x <xsize> -y <ysize> <output_filename>
```

Then run the visualizer

```bash
python visualizer.py <output_filename><num-map>.txt
```
