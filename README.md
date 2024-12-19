# zinescape
tools for making zines with inkscape

![screenshot.png](screenshot.png)

# installation

- install python
- `pip install setuptools`
- run `setup.py`

## `zinescape template`

this command makes a blank zine template for inkscape. options:

- N=<number of pages,>
- W=<width of page, inches>
- H=<height of page, inches>

## `zinescape compile`

this command takes a .pdf file you've saved from inkscape and arranges it into a zine format. also does image compression. autogenerates output filenames.

# notes
doesn't support metric (yet?)
only does single fold flip on long edge
