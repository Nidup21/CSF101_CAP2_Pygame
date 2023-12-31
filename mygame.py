import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
width = 800
height = 800
window = pygame.display.set_mode((width, height))

# Get the absolute path to the image files
current_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_directory, 'tree.png')
bird_path = os.path.join(current_directory, 'bird.png')
knife_path = os.path.join(current_directory, 'knife.png')

# Load the background image, bird image, and knife image
background = pygame.image.load(image_path)
bird = pygame.image.load(bird_path)
knife = pygame.image.load(knife_path)

# Adjust the size of the bird and knife images (change the width and height as needed)
bird_width = 50
bird_height = 50
bird = pygame.transform.scale(bird, (bird_width, bird_height))

knife_width = 30
knife_height = 30
knife = pygame.transform.scale(knife, (knife_width, knife_height))

# Bird initial position and velocity
bird_x = 50
bird_y = height // 2
bird_velocity = 5

# Knife initial position and velocity
knife_x = width - 50
knife_y = height // 2 - knife_height // 2  # Position in the center vertically
knife_velocity = 10
knife_shot = False  # Indicates whether the knife is in flight

# Score
score = 0

# Chances and Game Over
chances = 4
game_over = False

# Initialize the clock to control the frame rate
clock = pygame.time.Clock()

# Define font for displaying text
font = pygame.font.Font(None, 36)

# Define font for the game menu
menu_font = pygame.font.Font(None, 72)

# Game state
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
current_state = STATE_MENU  # Start with the menu

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_state == STATE_MENU:
        # Display the menu
        menu_text = menu_font.render('Knife Hit Game', True, (255, 255, 255))
        play_again_text = font.render('Press Enter to Play', True, (139,131,120))
        window.blit(menu_text, (width // 2 - 180, height // 2 - 50))
        window.blit(play_again_text, (width // 2 - 100, height // 2 + 50))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Enter key
            current_state = STATE_PLAYING

    elif current_state == STATE_PLAYING:
        if not game_over:
            # Update the bird's position in the vertical direction
            bird_y += bird_velocity

            # Check if the bird reaches the screen's boundaries and reverse direction if needed
            if bird_y <= 0:
                bird_y = 0
                bird_velocity = abs(bird_velocity)  # Change direction to down
            elif bird_y >= height - bird_height:
                bird_y = height - bird_height
                bird_velocity = -abs(bird_velocity)  # Change direction to up

            # Handle knife movement based on player input (tap)
            if knife_shot:
                if knife_x > 0:
                    knife_x -= knife_velocity
                else:
                    knife_shot = False  # Reset the knife's position
                    knife_x = width - 50
                    knife_y = height // 2 - knife_height // 2  # Position in the center vertically

            # Check if the screen was tapped (left mouse button)
            if pygame.mouse.get_pressed()[0]:  # 0 represents the left mouse button
                if not knife_shot and chances > 0:
                    knife_shot = True
                    knife_x = width - 50
                    knife_y = height // 2 - knife_height // 2  # Position in the center vertically
                    chances -= 1

            # Check for collision between knife and bird
            if knife_shot and knife_x < bird_x + bird_width and knife_x + knife_width > bird_x and knife_y < bird_y + bird_height and knife_y + knife_height > bird_y:
                # Collision occurred, increment the score and reset the knife
                score += 1
                knife_shot = False
                knife_x = width - 50
                knife_y = height // 2 - knife_height // 2

            # Check for "Game Over" condition
            if chances == 0:
                game_over = True

        # Draw the background image on the window
        window.blit(background, (0, 0))

        # Draw the bird at the left side
        window.blit(bird, (bird_x, bird_y))

        # Draw the knife on the right side in the center
        window.blit(knife, (knife_x, knife_y))

        # Display the score on the window
        score_text = font.render(f'Score: {score}', True, (0,0,0))
        window.blit(score_text, (10, 10))

        # Display the remaining chances on the window
        chances_text = font.render(f'Chances: {chances}', True, (0,0,0,))
        window.blit(chances_text, (10, 50))

        if game_over:
            current_state = STATE_GAME_OVER

    elif current_state == STATE_GAME_OVER:
        # Display the game over menu
        game_over_text = menu_font.render('Game Over', True, (255, 0, 0))
        play_again_text = font.render('Press Enter to Play Again', True, (255, 255, 255))
        window.blit(game_over_text, (width // 2 - 130, height // 2 - 50))
        window.blit(play_again_text, (width // 2 - 100, height // 2 + 50))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Enter key
            current_state = STATE_PLAYING
            # Reset the game state
            bird_y = height // 2
            score = 0
            chances = 4
            game_over = False

    pygame.display.update()

    # Control the frame rate (e.g., 60 FPS)
    clock.tick(60)

pygame.quit()

