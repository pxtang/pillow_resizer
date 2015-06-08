from PIL import Image
import glob, os, sys

def check_quit(string):
  if (string.lower() == "quit"):
    sys.exit()

size = 320, 180

print "Type quit to quit at any point!"

while (True):
  f_name = raw_input("What file would you like to input? Use *.jpg for all jpgs.\n")

  check_quit(f_name)
  if (os.path.isfile(f_name) or (len(f_name)>0 and f_name[0]=="*")):
    break
  else:
    print "Invalid file - please try again.\n"

while (True):
  print "Please indicate how to resize."
  print "e.g: 800x800F to resize to fixed size"
  print "800L to reduce long side to 800px"
  print "50% to reduce both edges by 50%"

  resize = raw_input("")

  check_quit(resize)
  if (len(resize)>0 and resize[-1] in ("F","L","%")):
    break
  else:
    print "I didn't understand your request - try again?\n"

print "Success!"