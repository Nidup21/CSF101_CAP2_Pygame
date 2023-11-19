import unittest
import pygame
from unittest.mock import patch

# Screen dimensions
width = 800
height = 800
bird_height = 50

class Bird:
   def __init__(self, x, y, velocity):
       self.x = x
       self.y = y
       self.velocity = velocity

   def move(self):
       self.y += self.velocity
       if self.y <= 0:
           self.y = 0
           self.velocity = abs(self.velocity)
       elif self.y >= height - bird_height:
           self.y = height - bird_height
           self.velocity = -abs(self.velocity)

class Knife:
   def __init__(self, x, y, velocity):
       self.x = x
       self.y = y
       self.velocity = velocity
       self.shot = False

   def move(self):
       if self.shot:
           self.x -= self.velocity
           if self.x <= 0:
               self.x = 0
               self.shot = False

class GameLogic:
 def __init__(self):
     self.bird = Bird(50, height // 2, 5)
     self.knife = Knife(width - 50, height // 2 - bird_height // 2, 10)
     self.chances = 4
     self.game_over = False

 def update(self):
     self.bird.move()
     self.knife.move()
     mouse_pressed = pygame.mouse.get_pressed()
     key_pressed = pygame.key.get_pressed()
     if mouse_pressed[0] and not self.knife.shot and self.chances > 0:
         self.knife.shot = True
         self.chances -= 1


class TestGameLogic(unittest.TestCase):
 @patch('pygame.mouse.get_pressed')
 @patch('pygame.key.get_pressed')
 def test_bird_movement(self, mock_key_pressed, mock_mouse_pressed):
     # Arrange
     game_logic = GameLogic()
     mock_key_pressed.return_value = [False, False, False, False] # Simulating no key being pressed
     mock_mouse_pressed.return_value = [0, 0, 0] # Simulating no mouse button being pressed

     # Act
     game_logic.update()

     # Assert
     self.assertEqual(game_logic.bird.y, height // 2 + 5) # Checking if the bird's y position has changed correctly

 @patch('pygame.mouse.get_pressed')
 @patch('pygame.key.get_pressed')
 def test_knife_movement(self, mock_key_pressed, mock_mouse_pressed):
     # Arrange
     game_logic = GameLogic()
     mock_key_pressed.return_value = [False, False, False, False] # Simulating no key being pressed
     mock_mouse_pressed.return_value = [1, 0, 0] # Simulating the left mouse button being pressed

     # Act
     game_logic.update()

     # Assert
     self.assertEqual(game_logic.knife.x, width - 50) # Checking if the knife's x position has changed correctly

if __name__ == '__main__':
   unittest.main()


