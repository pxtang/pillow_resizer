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
    try:
      os.remove(new_name)
    except OSError:
      print "File %s could not deleted - please check if it exists and delete manually if so." % new_name
    print "Attempt done. Quitting."
    sys.exit()
  print "Success! %s created with resolution %d by %d!" % (new_name, resize_dims[0], resize_dims[1])

# resize image to fixed dimensions. resize_dims should be a 2-tuple or list of dimensions
def resize_fixed(f_input,resize_dims):
  if isinstance(f_input, (list, tuple)):
    print "Resizing all images found in provided .txt file"
    for infile in f_input:
      resize_save(infile,resize_dims)
    print_batch_done()
    sys.exit()
  else:
    if (f_input[0] != "*"):
      resize_save(f_input,resize_dims)
      sys.exit()
    else:
      print "Resizing all images matching %s" % f_input
      for infile in glob.glob(f_input):
        resize_save(infile,resize_dims)
      print_batch_done()
      sys.exit()

# get long edge and calculate scale for entire picture. 
# takes in int and tuple, returns float
def get_long_scale(resize_dim, im_size):
  long_edge = max(im_size)
  return float(resize_dim)/long_edge

# resize image to long edge length. resize_dim should be an int
def resize_long(f_input,resize_dim):
  if isinstance(f_input, (list, tuple)):
    print "Resizing all images found in provided .txt file"
    for infile in f_input:
      im = Image.open(infile)
      scale = get_long_scale(resize_dim,im.size)
      resize_dims = ( int(im.size[0] * scale), int(im.size[1] * scale))
      resize_save(infile,resize_dims)
    print_batch_done()
    sys.exit()
  else:
    if (f_input[0] != "*"):
      im = Image.open(f_input)
      scale = get_long_scale(resize_dim,im.size)
      resize_dims = (int(im.size[0] * scale), int(im.size[1] * scale))
      resize_save(f_input,resize_dims)
      sys.exit()
    else:
      print "Resizing all images matching %s" % f_input
      for infile in glob.glob(f_input):
        im = Image.open(infile)
        scale = get_long_scale(resize_dim,im.size)
        resize_dims = ( int(im.size[0] * scale), int(im.size[1] * scale))
        resize_save(infile,resize_dims)
      print_batch_done()
      sys.exit()

# resize image by a certain percent. scale should be a float > 0
def resize_scale(f_input,scale):
  if isinstance(f_input, (list, tuple)):
    print "Resizing all images found in provided .txt file"
    for infile in f_input:
      im = Image.open(infile)
      resize_dims = ( int(im.size[0] * scale), int(im.size[1] * scale))
      resize_save(infile,resize_dims)
    print_batch_done()
    sys.exit()
  else:
    if (f_input[0] != "*"):
      im = Image.open(f_input)
      resize_dims = (int(im.size[0] * scale), int(im.size[1] * scale))
      resize_save(f_input,resize_dims)
      sys.exit()
    else:
      print "Resizing all images matching %s" % f_input
      for infile in glob.glob(f_input):
        im = Image.open(infile)
        resize_dims = ( int(im.size[0] * scale), int(im.size[1] * scale))
        resize_save(infile,resize_dims)
      print_batch_done()
      sys.exit()

resize_formats = ("F","L","%")

print "Type quit to quit at any point!"

# get file to open
while (True):
  f_name = raw_input("What file would you like to input? Use *.jpg for all jpgs, or a .txt with list of files.\n")

  check_quit(f_name)
  if (os.path.isfile(f_name) or (len(f_name)>= len("*.ext") and f_name[0:2]=="*.")):
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

# parse .txt
if (f_name[-3:] == "txt"):
  f_list = []

  with open(f_name,'r') as f:
    f_lines = f.read().split('\n')

    for line in f_lines:
      if (not len(line)):
        continue

      if (os.path.isfile(line)):
        f_list.append(line)
      else:
        print "File %s could not be found. skipping..." % repr(line)

  if (not len(f_list)):
    print "No valid files in %s detected - now quitting..." % f_name
    sys.exit()

if (resize[-1] == resize_formats[0]): # F
  resize_dims = resize[:-1].split("x")
  try:
    resize_dims = ( int(resize_dims[0]), int(resize_dims[1]) )
  except ValueError:
    print "Bad resize dimensions - quitting. Please try again."
    sys.exit()

  if (f_name[-3:] == "txt"):
    resize_fixed(f_list, resize_dims)
  else:
    resize_fixed(f_name, resize_dims)
elif (resize[-1] == resize_formats[1]): # L
  try:
    resize_dim = float(resize[:-1])
  except ValueError:
    print "Bad resize dimension - quitting. Please try again."
    sys.exit()
  
  if (f_name[-3:] == "txt"):
    resize_fixed(f_list, resize_dim)
  else:
    resize_long(f_name,resize_dim)
elif (resize[-1] == resize_formats[2]): # %
  try:
    scale = float(resize[0:-1])/100
  except ValueError:
    print "Bad scaling dimensions - quitting. Please try again."
    sys.exit()
  if scale <= 0:
    print "Cannot scale by negative amount - quitting. Please try again."
    sys.exit()
  
  if (f_name[-3:] == "txt"):
    resize_scale(f_list,scale)
  else:
    resize_scale(f_name,scale)
  