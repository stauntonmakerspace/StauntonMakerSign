# LED SIGN

## Setup

In order to use the kinect:
    Install Anaconda **32 Bit** 
    Install the Microsoft kinect 1.8 SDK and Toolkit
    Open the Anaconda prompt
    Run the ```conda env create --file environment.yml``` command using the environment file provided
    An uininstall and reinstall of both pyserial and opencv-contrib may be required
    run ```conda activate sign```
    run ```python run.py```

## Integration

* Flash the `Symbol.ino` Arduino code to every Arduino within the chain
* Change the values within the config.py file to match the number of LED segments in each symbol
* Running this will create a config file called the sign.txt this stores the position of every symbol you have in your sign
* Re-running the config script will allow you to drag and drop the symbols until they're in their appropriate position clicking the down arrow will save any configuration to a text file
* Once configuration is done I recommend creating a back up just to have around

* In order to use this code with another project create a pygame game
* Initialize an LED sign object with the File name as the first argument and the Arduino port value as the second argument ```LedSign.load("sign.txt",'COM4')```
* And every frame that you want the sign to respond call ```LedSign.update(screen: Pygame.surface, events: list<Pygame.events>)```
* In order to show the ui call ```LedSign.draw(screen: Pygame.surface)```

## Optimize 

## Build test.py functionality in C++ (if necessary after testing)

Testing is showing that a minimal delay is not necessary but it would be best in the future

A 50 Microsecond delay between commands has shown to be the minimum delay to ensure commands are read properly
From my reading python is unable to consistently delay to this precision

Symbol setpoint should scalable to match display size allow for configuration across devices
