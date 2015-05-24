#!/usr/bin/python3

"""
Merge a set of images into a single image.
Execute with the -h option to see usage information.

Requires Python 3 and Pillow, the friendly PIL fork (https://python-pillow.github.io/).
Pillow must be installed with zlib.
"""

import math
from PIL import Image

def calculateTileDimensions(num_images, columns = None):
  """
  Determine the number of rows and columns for num_images images.
  The number of columns may be specified, or it can be left as None in which case round(sqrt(num_images)) will be used.
  """
  if columns is None: 
    columns = int(round(math.sqrt(num_images), 0))
  elif columns <= 0:
    columns = num_images
  else:
    columns = min(num_images, columns)
  
  rows = math.ceil(num_images / columns)
  
  return rows, columns

def findLargestDimensions(files):
  """Find the largest width and height in the list of files."""
  width = 0
  height = 0
  
  for file in files:
    image = Image.open(file)
    width = max(image.size[0], width)
    height = max(image.size[1], height)
  
  return width, height

def mergeImages(files, output, columns = None, tile_width = None, tile_height = None):
  """Merge the specified images together into a single image."""
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

  print('\nMerged {} images into {}x{} pixel image "{}".'.format(len(files), out.size[0], out.size[1], output))
  print('The images were arranged into {} rows and {} columns with {}x{} pixel tiles.'.format(rows, cols, tile_width, tile_height))

if __name__ == "__main__":
  import os, sys
  import argparse
  
  parser = argparse.ArgumentParser(prog=sys.argv[0], description='Merge images into a single image.')
  parser.add_argument('file', nargs='+', help='the image files to merge')
  parser.add_argument('-c', '--columns', type=int, help='the number of columns to use, where 0 means to use 1 row (default: square root of the number of files)')
  parser.add_argument('-f', '--force', action='store_true', help='overwrite output file without prompting')
  parser.add_argument('-H', '--height', type=int, help='the height of the tiles; ignored if width not specified (default: the tallest image)')
  parser.add_argument('-W', '--width', type=int, help='the width of the tiles; ignored if height not specified (default: the widest image)')
  parser.add_argument('-o', '--output', default='out.png', help='the output file (default: out.png)')
  args = parser.parse_args()
  
  if not args.force and os.path.exists(args.output):
    ans = input('"{}" already exists, overwrite? '.format(args.output))
    if ans.lower() != 'y' and ans.lower() != 'yes' and ans.lower() != 'yes, please':
      print('Aborted.')
      exit()
   
  mergeImages(args.file, args.output, columns=args.columns, tile_width=args.width, tile_height=args.height)
