from PIL import Image
import glob, os, sys

# quits if string is equal to quit
def check_quit(string):
  if (string.lower() == "quit"):
    sys.exit()

def print_batch_done():
  print "Batch operation complete. Quitting."

# does resizing work based on dims. resize_dims should be a 2-tuple or list of dimensions
def resize_save(f_name,resize_dims):
  im = Image.open(f_name)
  new_im = im.resize(resize_dims,Image.ANTIALIAS)
  name, ext = f_name.split(".")
  new_name = name + "_resized." + ext
  try:
    new_im.save(new_name)
  except IOError:
    print "Something bad happened... attempting to delete newly made %s" % new_name
    os.remove(new_name)
    print "Attempt done. Quitting."
    sys.exit()
  print "Success! %s created with resolution %d by %d!" % (new_name, resize_dims[0], resize_dims[1])

# resize image to fixed dimensions. resize_dims should be a 2-tuple or list of dimensions
def resize_fixed(f_name,resize_dims):
  if (f_name[0] != "*"):
    resize_save(f_name,resize_dims)
    sys.exit()
  else:
    print "Resizing all images matching %s" % f_name
    for infile in glob.glob(f_name):
      resize_save(infile,resize_dims)
    print_batch_done()
    sys.exit()

# resize image to long edge length. resize_dim should be an int
def resize_long(f_name,resize_dim):
  pass

# resize image by a certain percent. scale should be a float > 0
def resize_scale(f_name,scale):
  pass

resize_formats = ("F","L","%")

print "Type quit to quit at any point!"

# get file to open
while (True):
  f_name = raw_input("What file would you like to input? Use *.jpg for all jpgs.\n")

  check_quit(f_name)
  if (os.path.isfile(f_name) or (len(f_name)>0 and f_name[0:2]=="*.")):
    break
  else:
    print "Invalid file - please try again.\n"

# get resizing request
while (True):
  print "Please indicate how to resize."
  print "e.g: 800x800F to resize to fixed size"
  print "800L to reduce long side to 800px"
  print "50% to reduce both edges by 50%"

  resize = raw_input("")

  check_quit(resize)
  if (len(resize)>0 and resize[-1] in resize_formats):
    # if no x specified for fixed
    if (resize[-1] == resize_formats[0] and len(resize.split("x")) != 2):
      pass
    else:
      break
  print "I didn't understand your request - try again?\n"

if (resize[-1] == resize_formats[0]):
  resize_dims = resize[:-1].split("x")
  try:
    resize_dims = ( int(resize_dims[0]), int(resize_dims[1]) )
  except ValueError:
    print "Bad resize dimensions - quitting. Please try again."
    sys.exit()
  resize_fixed(f_name, resize_dims)
elif (resize[-1] == resize_formats[1]):
  # resize_long()
  pass
elif (resize[-1] == resize_formats[2]):
  # resize_scale()
  pass