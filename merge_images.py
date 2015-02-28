#!/usr/bin/python

# This script merges together a set of images.
# Requires Python 3 and Pillow, the friendly PIL fork (https://python-pillow.github.io/)

import os, sys
import math
from PIL import Image

# Determine the number of rows and columns for num_images images.
# The number of columns may be specified, or it can be left as None
# in which case round(sqrt(num_images)) will be used
def calculateTileDimensions(num_images, columns = None):
  if columns is None: 
    columns = int(round(math.sqrt(num_images), 0))
  elif columns <= 0:
    columns = num_images
  else:
    columns = min(num_images, columns)
  
  rows = math.ceil(num_images / columns)
  
  return rows, columns

# Find the largest width and height in the list of files.
def findLargestDimensions(files):
  width = 0
  height = 0
  
  for file in files:
    image = Image.open(file)
    width = max(image.size[0], width)
    height = max(image.size[1], height)
  
  return width, height

# Merge the specified images together into a single image.
def mergeImages(files, output, columns = None, tile_width = None, tile_height = None):
  rows, cols = calculateTileDimensions(len(files), columns)
  
  # find the tile size if not specified (uses largest image boundaries)
  if tile_width is None or tile_height is None:
    tile_width, tile_height = findLargestDimensions(files)
  
  out = Image.new('RGBA', (cols*tile_width, rows*tile_height))

  # copy all images to the new image
  row = 0
  col = 0
  for file in files:
    print('Processing', file)
    image = Image.open(file)
    out.paste(image, (col * tile_width, row * tile_height))
    
    col += 1
    if col == cols:
      row += 1
      col = 0

  out.save(output)

  print('\nMerged {} images into "{}".'.format(len(files), output))
  print('The images were arranged into {} rows and {} columns with {}x{} pixel tiles.'.format(rows, cols, tile_width, tile_height))

if __name__ == "__main__":
    mergeImages(sys.argv[1:], 'out.png', None)
