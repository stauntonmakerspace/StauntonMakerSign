# LED SIGN

## Setup
``` pip install makersign```
## Integration

* Flash the `Symbol.ino` Arduino code to every Arduino within the chain
* Change the values within the config.py file to match the number of LED segments in each symbol
* Running this will create a config file called the sign.txt this stores the position of every symbol you have in your sign
* Re-running the config script will allow you to drag and drop the symbols until they're in their appropriate position clicking the down arrow will save any configuration to a text file
* Once configuration is done I recommend creating a back up just to have around
* If you want to test that everything's working in the chain just run the `Test.ino` code on the first LED symbol in your chain this should just flash all of the LEDs in the chain red green and blue.

* In order to use this code with another game create a pygame game
* Initialize an LED sign object with the config filename as the first argument and the Arduino port value as the second argument ```LedSign.load("sign.txt",'COM4')```
* And every frame that you want the sign to respond call ```LedSign.update(screen: Pygame.surface, events: list[Pygame.events])```
* In order to show the ui call ```LedSign.draw(screen: Pygame.surface)```

* Waverly Was Here