# merge-images.py
This script merges multiple images into a single image. The images are tiled by the dimensions of the largest image and output as a PNG with transparency. This could be used, for example, to create a sprite sheet from a series of separate images.

## Requirements
  - Python 3
  - Pillow, the friendly PIL fork (https://python-pillow.github.io/), installed with zlib present

## Usage
```
usage: merge_images.py [-h] [-c COLUMNS] [-f] [-H HEIGHT] [-W WIDTH]
                       [-o OUTPUT]
                       file [file ...]

Merge images into a single image.

positional arguments:
  file                  the image files to merge

optional arguments:
  -h, --help            show this help message and exit
  -c COLUMNS, --columns COLUMNS
                        the number of columns to use, where 0 means to use 1
                        row (default: square root of the number of files)
  -f, --force           overwrite output file without prompting
  -H HEIGHT, --height HEIGHT
                        the height of the tiles; ignored if width not
                        specified (default: the tallest image)
  -W WIDTH, --width WIDTH
                        the width of the tiles; ignored if height not
                        specified (default: the widest image)
  -o OUTPUT, --output OUTPUT
                        the output file (default: out.png)
```
