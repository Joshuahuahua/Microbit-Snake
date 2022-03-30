# Snake for the MicroBit in 73 lines!
# Author: Joshua Hollander
from microbit import *
from random import randint


# Game settings
settings = {
    'time_incr': 500, # Time between each board update/snake movement
    'wrap': True, # If the snake can "wrap around" the board
    'startingLoc': [2, 2], # Snake's starting location
    'fruit_count': 3, # How many fruit are generated each "fruit cycle"
    'brightness': { # Brightness values for game elements
        'head': 9,
        'body': 5,
        'fruit': 2
    }
}


# The Snake class stores the "Score" and handles the movement and rendering of the snake itself
class Snake:
    # List containing the x and y coords for every 'block' of the snake's body (prepopulated with the starting coords)
    body = [{
        'x': settings['startingLoc'][0]%5,
        'y': settings['startingLoc'][1]%5
    }]
    # Variable used for calculating/validating the next position for the head of the snake
    next = {
        'x': body[0]['x'],
        'y': body[0]['y']
    }
    # Stores the current direction (5 = not moving)
    direction = 5
    # Score = number of fruit eaten
    score = 0

    def move(self, direction):
        
        # Calculate the next position;
        # Move Left
        if direction == 0:
            self.next['x'], self.next['y'] = self.next['x']-1, self.next['y']
        # Move Down
        elif direction == 1:
            self.next['x'], self.next['y'] = self.next['x'], self.next['y']+1
        # Move Right
        elif direction == 2:
            self.next['x'], self.next['y'] = self.next['x']+1, self.next['y']
        # Move Up
        elif direction == 3:
            self.next['x'], self.next['y'] = self.next['x'], self.next['y']-1
        # Dont move (direction set to 5 to implement "press button to start")
        else:
            pass
        
        # If the snake can "wrap around" the board, wrap coords accordingly
        if settings['wrap']:
            self.next['x'], self.next['y'] = self.next['x']%5, self.next['y']%5

        if len(self.body) > 1:
            # Reverse the body and work from back to front
            self.body.reverse()
            # Copy each body element over by 1 place
            for i in range(0, len(self.body)-1):
                self.body[i] = self.body[i+1].copy()
            # Restore origonal order
            self.body.reverse()
        # Replace snake's "Head" with the calculated "next position"
        self.body[0]['x'], self.body[0]['y'] = self.next['x'], self.next['y']
            
    # Render the snake
    def draw(self):
        # For every element in the snake, render it on the LED matrix with the appropriate brightnesses
        for i in range(0, len(self.body)):
            if i == 0: type = 'head'
            else: type = 'body'
            display.set_pixel(self.body[i]['x'], self.body[i]['y'], settings['brightness'][type])



# The Board class handles the tracking and rendering of fruit, and also handles the collision logic
class Board:
    fruits = []
    def start(self):
        # Create snake object
        snake = Snake()
        
        # Start the game
        while True:
            # Increment/Decrement the direction if button A/B were pressed respectfully (and constrain them to 0-3)
            if button_a.was_pressed(): snake.direction = (snake.direction+1)%4
            if button_b.was_pressed(): snake.direction = (snake.direction-1)%4
            # Store the snake's last head position
            snake_last_loc = snake.body[0].copy()
            
            # Move the snake
            snake.move(snake.direction)
            
            # If the snake collides with itself, break
            if len(snake.body[0]) > 1 and snake.body[0] in snake.body[1:]:
                break
            # If "wrap" is false, break if the snake has gone out of bounds
            if (not settings['wrap'] and
                (snake.body[0]['x'] not in range(0, 5) or
                snake.body[0]['y'] not  in range(0, 5))):
                snake.body[0] = snake_last_loc
                break
            
            # Render Board
            self.draw(snake)
            # Render Snake (done after the board so the head overrides any potential fruit)
            snake.draw()
            
            # If the snake's head is on top of a fruit
            if snake.body[0] in self.fruits:
                # Increase score
                snake.score+=1
                # Remove the fruit
                self.fruits.remove(snake.body[0])
                # Add the last location of the snake to the end
                snake.body.append(snake_last_loc)
            
            
            sleep(settings['time_incr'])
        
        # If snake collided with itself, play animation, and show score
        sleep(1000)
        snake.body[0] = snake_last_loc
        for i in snake.body[::-1]:
            snake.body.remove(i)
            display.clear()
            snake.draw()
            sleep(70)
        display.clear()
        display.set_pixel(snake_last_loc['x'], snake_last_loc['y'], settings['brightness']['head'])
        sleep(1000)
        display.scroll('Game Over!', 100)
        while True:
            display.scroll('Score:'+str(snake.score), 125)


    # Render Board
    def draw(self, snake):
        display.clear()
        # If all fruit were eaten, generate new batch
        if len(self.fruits) < 1:
            self.genFruit(snake)
        # Render fruit
        for fruit in self.fruits:
            display.set_pixel(fruit['x'], fruit['y'], settings['brightness']['fruit'])
    
    # Generates the fruit
    def genFruit(self, snake):
        while len(self.fruits) < settings['fruit_count'] and len(self.fruits)+len(snake.body) < 25:
            # Pick random spot on the board
            new_fruit = {'x': randint(0, 4), 'y': randint(0, 4)}
            # If location is not inside the snake or another fruit, add it to the list 
            if new_fruit not in self.fruits and new_fruit not in snake.body:
                self.fruits.append(new_fruit)



# Start of the script
def main():
    # Create the board
    board = Board()
    # Start the game
    board.start()

main()