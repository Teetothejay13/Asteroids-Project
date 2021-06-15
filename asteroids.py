"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random
import sys
#import pygame
#from pygame.math import Vector2
from abc import abstractmethod
from abc import ABC

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 5
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 30

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 20

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 10

#lets get to the point already
class Point:
    #but where? 
    def __init__(self, x, y):
        self.x = x
        self.y = y

#an object in motion tends to stay in motion, so lets get things moving
class Velocity:
    #but where are we going? we gotta start in a direction
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

#the abstract class for the space rocks, like those recent common ancestors they talk about in biology
class Asteroid(ABC):
    #lets get to know it before we tell it what to do
    def __init__(self):
        self.center = Point(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.velocity = Velocity(random.uniform(-1, 1), random.uniform(-1, 1))
        self.radius = 0
        self.health = 10
        self.alive = True
        self.angle = random.randint(0, 359)
        self.rotate_direction = random.randint(-1, 1)
    #unlike men, not all ateroids are created equally
    @abstractmethod
    def update(self):
        self.center.x += (self.velocity.dx * 1.5)
        self.center.y += (self.velocity.dy * 1.5)
        print("update")
    #so they'll do things differently from each other
    @abstractmethod
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, self.texture, self.angle)
    #the screen wrap around is gonna be the same for all the rocks though
    def is_off_screen(self):
        if self.center.x < 0:
            self.center.x = SCREEN_WIDTH
        elif self.center.x > SCREEN_WIDTH:
            self.center.x = 0

        if self.center.y < 0:
            self.center.y = SCREEN_HEIGHT
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y = 0
    #however they'll all be hit differently. bigger rocks are tougher, obviously
    @abstractmethod
    def hit(self):
        self.health -= 1

#now for the first big hunk of stone and metal and ice
class Big_Space_Rock(Asteroid):
    #This stuff is just redefining things to be more specific to the big rock
    def __init__(self):
        super().__init__()
        self.radius = BIG_ROCK_RADIUS
        self.texture = arcade.load_texture("big.png")
        self.size = 3   #this is different from the radius. it'll be used later to determine what to do when they break apart
        self.health = 50
    #The draw is the same, but I made it an abstract method in the asteroid class because I was lazy
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, self.texture, self.angle)
    #with this one, we want the rocks to rotate slowly, because it looks not boring
    def update(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        if self.rotate_direction == 0:
            self.rotate_direction = 1
            self.angle += 1 * self.rotate_direction
        else:
            self.angle += 1 * self.rotate_direction
    #this fella is worth 10 points
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return 10
        else:
            return 0
        
#lets take it from the top, but a bit smaller
class Medium_Space_Rock(Asteroid):
    #more reassignment to be specific to the rock
    def __init__(self):
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.texture = arcade.load_texture("medium.png")
        self.size = 2
        self.heatlh = 20
    #same draw function as the last one
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, self.texture, self.angle)
    #this one will rotate a bit faster than the big one, because...physics.
    def update(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        if self.rotate_direction == 0:
            self.rotate_direction = 1
            self.angle += 2 * self.rotate_direction
        else:
            self.angle += 2 * self.rotate_direction
    #this one is worth half as much, because rock segregation :D
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return 5
        else:
            return 0

#again, but even smaller
class Small_Space_Rock(Asteroid):
    #these global variables are really useful
    def __init__(self):
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.texture = arcade.load_texture("small.png")
        self.size = 1
        self.heatlh = 1
    #you know the drill
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, self.texture, self.angle)
    #this one is gonna be a speedy boy, because reasons and physics and all that
    def update(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        if self.rotate_direction == 0:
            self.rotate_direction = 1
            self.angle += 4 * self.rotate_direction
        else:
            self.angle += 4 * self.rotate_direction
    #much like men, small rocks aren't valued a whole lot
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return 1
        else:
            return 0

#now an abstract class for everything else, because more segregation
class Flying_object(ABC):
    #it has the same basic stuff though
    def __init__(self):
        self.center = Point(0, 0)
        self.velocity = Velocity(0, 0)
        self.angle = 0
        self.radius = 0
        self.alive = True
        self.texture = None
    #just like last time, the draw functions are all the same, i'm just lazy
    @abstractmethod
    def draw(self):
        print("Draw")
    #this one is a bit different though for each one
    @abstractmethod
    def update(self):
        print("Update")
    #this one is the same for all of them though, like the asteroids
    def is_off_screen(self):
        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0
        elif self.center.x < 0:
            self.center.x = SCREEN_WIDTH

        if self.center.y > SCREEN_HEIGHT:
            self.center.y = 0
        elif self.center.y < 0:
            self.center.y = SCREEN_HEIGHT

#now for our daring astronaut, tasked with...shooting...some rocks. on second thought, this job sucks.
class Ship(Flying_object):
    #well at least we get to fly a spaceship right?
    def __init__(self):
        super().__init__()
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2
        self.radius = SHIP_RADIUS
        self.texture = arcade.load_texture("ship.png")
        self.acceleration_x = 0
        self.acceleration_y = 0
    #this is the only property (I think) because they're annoying
    @property
    def angle(self):
        return self._angle
    #I vaguely remember someone saying that high numbers for the degrees of rotation can cause problems because reasons, so here's this
    @angle.setter
    def angle(self, value):
        self._angle = value % 360
    #same draw function as usual
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, self.texture, self.angle)
    #basic update function
    def update(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    #this one was bit difficult. I looked up the whole sin and cos part because I couldn't figure out how to get
    #it to add velocity in the proper direction. Even though I took trig in high school I don't understand how this
    #works, but I won't complain so long as it works
    def forward(self):
        self.acceleration_x = -math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.acceleration_y = math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

        self.velocity.dx += self.acceleration_x
        self.velocity.dy += self.acceleration_y
        #this part probably could have been a property, but I'm too lazy to fix it now
        if self.velocity.dx > 3:
            self.velocity.dx = 3
        elif self.velocity.dx < -3:
            self.velocity.dx = -3

        if self.velocity.dy > 3:
            self.velocity.dy = 3
        elif self.velocity.dy < -3:
            self.velocity.dy = -3    
    #this should be obvious
    def turn_left(self):
        self.angle += SHIP_TURN_AMOUNT
    #this too
    def turn_right(self):
        self.angle -= SHIP_TURN_AMOUNT
    #this too
    def hit(self):
        self.alive = False

#your standard issue laser
class Laser(Flying_object):
    #some more reassignment, because reasons
    def __init__(self, ship_x, ship_y, ship_dx, ship_dy, ship_angle):
        super().__init__()
        self.center.x = ship_x
        self.center.y = ship_y
        self.angle = ship_angle + 90
        self.velocity.dx = -math.sin(math.radians(ship_angle)) * BULLET_SPEED
        self.velocity.dy = math.cos(math.radians(ship_angle)) * BULLET_SPEED
        self.texture = arcade.load_texture("laser.png")
        self.radius = BULLET_RADIUS
        self.time_alive = 0
        self.damage = 1
    #we've been over this part before
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*6, self.radius*2, self.texture, self.angle)
    #this part too
    def update(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    #this part it to make the bullet dissapear after a certain amount of frames
    def is_alive(self):
        self.time_alive += 1
        if self.time_alive >= BULLET_LIFE:
            self.alive = False

#kaboom???
class Missle(Flying_object):
    #yes Rico, kaboom.
    def __init__(self, ship_x, ship_y, ship_dx, ship_dy, ship_angle):
        super().__init__()
        self.center.x = ship_x
        self.center.y = ship_y
        self.angle = ship_angle + 90
        self.velocity.dx = -math.sin(math.radians(ship_angle)) * BULLET_SPEED
        self.velocity.dy = math.cos(math.radians(ship_angle)) * BULLET_SPEED
        self.texture = arcade.load_texture("missle.png")
        self.radius = BULLET_RADIUS
        self.time_alive = 0
        self.damage = 10
    #we've been over this
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*12, self.radius*4, self.texture, self.angle)
    #this
    def update(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    #and this before
    def is_alive(self):
        self.time_alive += 1
        if self.time_alive >= BULLET_LIFE:
            self.alive = False

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        self.asteroids = [Big_Space_Rock(), Big_Space_Rock(), Big_Space_Rock(), Big_Space_Rock(), Big_Space_Rock()]
        self.lasers = []
        self.score = 0
        self.x_wing = Ship()
        self.missle_charge = 0
        self.no_full_auto_in_the_building = 0
        self.game_over_display_time = 0
        # TODO: declare anything here you need the game class to track

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        if self.x_wing.alive == False:
            self.lasers = []
            self.asteroids = []
            self.game_over_display_time += 1
            arcade.draw_text("Game Over", start_x=((SCREEN_WIDTH//2)-60), start_y=((SCREEN_HEIGHT//2)-10), font_size=24, color=arcade.color.WHITE)
            if self.game_over_display_time == 240:
                sys.exit()

        else:
            for asteroid in self.asteroids:
                asteroid.draw()
            for laser in self.lasers:
                laser.draw()
            self.x_wing.draw()
            score_text = "Score: {}".format(self.score)
            arcade.draw_text(score_text, start_x=10, start_y=(SCREEN_HEIGHT-20), font_size=12, color=arcade.color.WHITE)

        

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid.is_off_screen()
        
        for laser in self.lasers:
            laser.update()
            laser.is_alive()
            laser.is_off_screen()

        self.x_wing.update()
        self.x_wing.is_off_screen()

        #I wanna check for corpses too
        self.bring_out_your_dead()
        # TODO: Check for collisions
        for asteroid in self.asteroids:
            if asteroid.alive and self.x_wing.alive:
                    dont_scratch_my_ship = asteroid.radius + self.x_wing.radius
                    if (abs(self.x_wing.center.x - asteroid.center.x) < dont_scratch_my_ship and
                                abs(self.x_wing.center.y - asteroid.center.y) < dont_scratch_my_ship):
                            self.x_wing.hit()     

        for laser in self.lasers:
            for asteroid in self.asteroids:

                # Make sure they are both alive before checking for a collision
                if laser.alive and asteroid.alive:
                    too_close = laser.radius + asteroid.radius

                    if (abs(laser.center.x - asteroid.center.x) < too_close and
                                abs(laser.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        
                        laser.alive = False
                        self.score += asteroid.hit(laser.damage)
                        if (asteroid.size == 3) and (asteroid.alive == False):
                            New_rock_1 = Medium_Space_Rock()
                            New_rock_1.center.x = asteroid.center.x
                            New_rock_1.center.y = asteroid.center.y
                            New_rock_1.velocity.dx = asteroid.velocity.dx
                            New_rock_1.velocity.dy = asteroid.velocity.dy + 2

                            New_rock_2 = Medium_Space_Rock()
                            New_rock_2.center.x = asteroid.center.x 
                            New_rock_2.center.y = asteroid.center.y
                            New_rock_2.velocity.dx = asteroid.velocity.dx
                            New_rock_2.velocity.dy = asteroid.velocity.dy - 2

                            New_rock_3 = Small_Space_Rock()
                            New_rock_3.center.x = asteroid.center.x 
                            New_rock_3.center.y = asteroid.center.y
                            New_rock_3.velocity.dx = asteroid.velocity.dx + 5
                            New_rock_3.velocity.dy = asteroid.velocity.dy

                            self.asteroids.append(New_rock_1)
                            self.asteroids.append(New_rock_2)
                            self.asteroids.append(New_rock_3)

                        elif (asteroid.size == 2) and (asteroid.alive == False):
                            New_rock_1 = Small_Space_Rock()
                            New_rock_1.center.x = asteroid.center.x
                            New_rock_1.center.y = asteroid.center.y
                            New_rock_1.velocity.dx = asteroid.velocity.dx + 1.5
                            New_rock_1.velocity.dy = asteroid.velocity.dy + 1.5

                            New_rock_2 = Small_Space_Rock()
                            New_rock_2.center.x = asteroid.center.x 
                            New_rock_2.center.y = asteroid.center.y
                            New_rock_2.velocity.dx = asteroid.velocity.dx - 1.5
                            New_rock_2.velocity.dy = asteroid.velocity.dy - 1.5
                            
                            self.asteroids.append(New_rock_1)
                            self.asteroids.append(New_rock_2)

    def bring_out_your_dead(self):
        for laser in self.lasers:
            if not laser.alive:
                self.lasers.remove(laser)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.x_wing.turn_left()

        if arcade.key.RIGHT in self.held_keys:
            self.x_wing.turn_right()

        if arcade.key.UP in self.held_keys:
            self.x_wing.forward()

        if arcade.key.DOWN in self.held_keys:
            pass

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            self.no_full_auto_in_the_building += 1
            if self.no_full_auto_in_the_building == 5:
                self.lasers.append(Laser(self.x_wing.center.x, self.x_wing.center.y, self.x_wing.velocity.dx, self.x_wing.velocity.dy, self.x_wing.angle))
                self.no_full_auto_in_the_building = 0
            
            self.missle_charge += 1
            if self.missle_charge ==  60:
                self.lasers.append(Missle(self.x_wing.center.x, self.x_wing.center.y, self.x_wing.velocity.dx, self.x_wing.velocity.dy, self.x_wing.angle))
                self.missle_charge = 0
        #if it isn't held, reset

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.x_wing.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                self.lasers.append(Laser(self.x_wing.center.x, self.x_wing.center.y, self.x_wing.velocity.dx, self.x_wing.velocity.dy, self.x_wing.angle))

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()