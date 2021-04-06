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

In order to use this code with another project create a pygame game
And every frame that you want the sign to respond call ```LedSign.update(screen: Pygame.surface, events: list<Pygame.events>)```
In order to show the ui call ```LedSign.draw(screen: Pygame.surface)```

## Optimize 

## Build test.py functionality in C++ (if necessary after testing)

Testing is showing that a minimal delay is not necessary but it would be best in the future

A 50 Microsecond delay between commands has shown to be the minimum delay to ensure commands are read properly
From my reading python is unable to consistently delay to this precision

Symbol setpoint should scalable to match display size allow for configuration across devices
