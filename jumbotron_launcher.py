import os
import subprocess
import time
from gamepad_wrapper import Gamepad_wrapper

##########################################################
# RGB matrix inits
##########################################################
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
from matrix import read_matrix

# open the config file and read the size of our matrix
matrix_data = read_matrix()

# this is the size of ONE of our matrixes. 
matrix_rows = matrix_data[1] 
matrix_columns = matrix_data[0] 

# how many matrixes stacked horizontally and vertically 
matrix_horizontal = matrix_data[2] 
matrix_vertical = matrix_data[3] 

total_rows = matrix_rows * matrix_vertical
total_columns = matrix_columns * matrix_horizontal

options = RGBMatrixOptions()
options.rows = matrix_rows 
options.cols = matrix_columns 
options.chain_length = matrix_horizontal
options.parallel = matrix_vertical 
options.hardware_mapping = 'regular'  
options.gpio_slowdown = 2

# I'm gonna treat the matrix and wrapper as globals.
matrix = RGBMatrix(options = options)
wrapper = Gamepad_wrapper(4) 

###################################
#  centered_text()
###################################
def centered_text(my_text, box_color, text_color, font, delay):
    global total_columns
    global total_rows
    global matrix

    # getsize returns a tuple of the x and y size of the font string.
    text_size = font.getsize(my_text)
    
    # we're going to draw a box around that text, so we need a little buffer
    # this is going to be the buffer for each side.
    pixel_buffer = 2
    box_size_x = text_size[0] + (2*pixel_buffer)
    box_size_y = text_size[1] + (2*pixel_buffer)

    text_image = Image.new("RGB", (box_size_x, box_size_y))
    text_draw = ImageDraw.Draw(text_image)
    box = (0,0,box_size_x-1,box_size_y-1)
    text_draw.rectangle(box, outline=box_color)

    # do some math to center our box
    # box_x and box_y define the top left corner
    box_x = (total_columns - box_size_x)/2 
    box_y = (total_rows - box_size_y)/2

    text_draw.text((pixel_buffer,pixel_buffer),my_text, fill=text_color, font=font)

    matrix.SetImage(text_image,box_x,box_y)
    time.sleep(delay)

###########################################################
# INIT STATE
###########################################################
def init_state():
  print("Init state")
  
  box_color = (255, 0, 0)  # Red
  text_color = (0, 0, 255) # Blue 
  splash_font = ImageFont.truetype('Pillow/Tests/font/Courier_New_Bold.ttf', 10)

  centered_text("booting", box_color, text_color, splash_font, 0)   

  return "waitForGamepad"

###########################################################
# WAITFORGAMEPAD STATE
###########################################################
def waitForGamepad_state():
  global wrapper

  box_color = (255, 0, 0)  # Red
  text_color = (0, 0, 255) # Blue 
  splash_font = ImageFont.truetype('Pillow/Tests/font/Courier_New_Bold.ttf', 10)

  centered_text("waiting for joystick to connect", box_color, text_color, splash_font, 0)   

  if (wrapper.player_count() == 0):
    return "waitForGamepad"
  else:
    return "processInput"

###########################################################
# PROCESSINPUT STATE
###########################################################
def processInput_state():
  global wrapper
  
  box_color = (255, 0, 0)  # Red
  text_color = (0, 0, 255) # Blue 
  splash_font = ImageFont.truetype('Pillow/Tests/font/Courier_New_Bold.ttf', 10)

  centered_text("connected", box_color, text_color, splash_font, 0)   

  input = wrapper.get_next_input()
  if (input != None):
    print("Got "+input[0]+" "+input[1])
    proc = subprocess.Popen(['sudo','python', '../matrix_test/matrix_test.py'])
    exit(1)

  return "processInput"

###########################################################
# MAIN 
###########################################################
def main():
  current_state = "init"
  
  
  while (True):

    if (current_state == "init"):
      current_state = init_state()
    elif (current_state == "waitForGamepad"):
      current_state = waitForGamepad_state()
    elif (current_state == "processInput"):
      current_state = processInput_state()
    else:  
      print("Unknown state: ", current_state)
      exit(1)

if __name__ == "__main__":
  main()
