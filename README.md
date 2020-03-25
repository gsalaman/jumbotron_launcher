# Jumbotron Launcher
## High Level Requirements
* Runs on boot.
* Start with splash screen, message "waiting for joystick to connect".
* Once joystick has connected, present list of apps.
  * Joystick scrolls through list
  * Area on right for "run".  Select by pushing right, then up or down.
  * That then launches the app.
* First apps:
  * Cycles
  * Wormgame
  * Audio Visualizer
  * Donuts
* If joystick disconnects when selecting app, go back to splash screen

## High Level Design Overview
We'll use a simple state machine in main().  Main will keep track of "current state", and will call the appropriate function based on which state we're in.  That function will return when a state change is necessaray, returning "next state".  Main can then call that next state.

The rgbmatrix library will provide our interface with the jumbotron.  We'll use the Python Imagaing Library (PIL) for helper functions.  See the "matrix" section below for design details. 

The launcher will reuse gamepad_wrapper.py (from mqtt_gamepad) in order to interface with the broker and register gamepads.  First thought:  this will also be a global, able to be accessed from any state. 

### States:
#### Init
Enters on Boot. 

This state will be responsible for power-up.  It'll initialize the rgbmatrix and provide a booting "splash screen".  It will also initialize the gamepad_wrapper, which will connect us to the broker. 

Exit condition:  On broker connect, we'll go to "WaitForGamepad" state.

#### WaitForGamepad
This state waits for a gamepad to connect.
Exit condition:  any gamepads connected will exit to "processInput" state.

#### ProcessInput State
We'll treat ANY gamepad input as valid...meaning we *could* have conflicitng joystick input.  I like this better than only processing the first joystick, as we'll always have input.

We'll display a list of the applications and instructions:
"Move joystick up or down to select app.  Move right to run"

We'll have a list of the apps, containing a display string and a launch command.
We'll keep track of current index to move up or down the list.  Rollover will be allowed.
First cut assumes the number of apps will fit on the screen.
Unselected apps will be Red.
The current "highlighted" app will be white. 

The loop for this state will confirm that we still have gamepads connected.  We'll use the "get next input" command from the wrapper to move up, down, or launch the app.

### Matrix
We'll create a "Screen" object to abstract the matrix implementation.  Since we only need to display text, we'll break the "screen" into rows, and provide APIs to set text and color for each row.  The object will abstract the PIL concepts; it will internally have a PIL "Image" and "Draw" object.  We'll only use one default font, and that will not be user settable.

The init function for this object will calculate the number of text rows available and initialize the matrix.  

We'll provide a method for "set row"...this will take a string, color, and row number parameter.  It will blank the existing row, and set the new text to the provided string and color.

We'll also have an "erase row" and "erase all" method.

