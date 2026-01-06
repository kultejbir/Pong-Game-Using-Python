import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH, HEIGHT = 640, 480
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 70, 100  # Set paddle width to 70
FPS = 60
BALL_SPEED = 3
SCORE_FONT_SIZE = 36
WINNING_SCORE = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Global variables for ball position and speed
ball_position_x, ball_position_y = WIDTH / 2, HEIGHT / 2
ball_speed_x, ball_speed_y = BALL_SPEED, BALL_SPEED

# Path to the new font
FONT_PATH = 'love.ttf'

# Function to handle text input
def get_text_input(prompt, screen):
    font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)
    input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 15, 200, 30)
    text = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(BLACK)
        prompt_surface = font.render(prompt, True, WHITE)
        screen.blit(prompt_surface, (WIDTH // 2 - prompt_surface.get_width() // 2, HEIGHT // 2 - 50))  # Centered prompt position
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()
        pygame.time.wait(30)

    return text

# Function to wait for a key press to start the game
def wait_for_start(screen):
    screen.fill(BLACK)  # Clear the screen before displaying the start message
    font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)
    start_text = "Press ENTER to start the game"
    start_surface = font.render(start_text, True, WHITE)
    screen.blit(start_surface, (WIDTH // 2 - start_surface.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Load images
background_img = pygame.image.load('background.png')
paddle_img = pygame.image.load('paddle.png')
ball_img = pygame.image.load('ball.png')

# Scale images
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
ball_img = pygame.transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))

# Load fonts
score_font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)

# Function to update player names
def update_player_info(screen):
    player1_name = get_text_input("Enter Player 1 Name: ", screen)
    player2_name = get_text_input("Enter Player 2 Name: ", screen)
    return player1_name, player2_name

# Set up sounds
hit_sound = pygame.mixer.Sound('hit.wav')

# Function to update ball position
def update_ball_position():
    global ball_position_x, ball_position_y, ball_speed_x, ball_speed_y
    ball_position_x += ball_speed_x
    ball_position_y += ball_speed_y

    # Update ball rect
    global ball_rect
    ball_rect = ball_img.get_rect(center=(ball_position_x, ball_position_y))

    # Bounce the ball off the walls
    if ball_position_y < 0 or ball_position_y > HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

# Function to detect collisions
def detect_collisions():
    global ball_speed_x, ball_speed_y, score1, score2
    if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
        ball_speed_x *= -1.1  # Increase speed after each paddle hit
        hit_sound.play()

    if ball_position_x < 0:
        score2 += 1
        reset_ball()
    elif ball_position_x > WIDTH - BALL_SIZE:
        score1 += 1
        reset_ball()

# Function to reset ball position
def reset_ball():
    global ball_position_x, ball_position_y, ball_speed_x, ball_speed_y
    ball_position_x, ball_position_y = WIDTH / 2, HEIGHT / 2
    ball_speed_x = BALL_SPEED if ball_speed_x > 0 else -BALL_SPEED
    ball_speed_y = BALL_SPEED if ball_speed_y > 0 else -BALL_SPEED

# Function to draw paddles
def draw_paddles():
    screen.blit(paddle_img, paddle1_rect)
    screen.blit(paddle_img, paddle2_rect)

# Function to draw ball
def draw_ball():
    screen.blit(ball_img, ball_rect)

# Function to draw scores
def draw_scores(player1_name, player2_name, score1, score2):
    text_player1 = score_font.render(f"{player1_name}: {score1}", True, WHITE)
    text_player2 = score_font.render(f"{player2_name}: {score2}", True, WHITE)
    screen.blit(text_player1, (20, 20))
    screen.blit(text_player2, (WIDTH - 200, 20))

# Function to display the winner
def display_winner(winner_name):
    screen.fill(BLACK)
    winner_text = f"{winner_name} Wins!"
    winner_surface = score_font.render(winner_text, True, WHITE)
    screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds

# Function to ask to play again
def ask_play_again(screen):
    screen.fill(BLACK)  # Clear the screen before displaying the play again message
    font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)
    text_surface = font.render("Play again? (Y/N)", True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

# Main game loop
def main():
    global paddle1_position_y, paddle2_position_y, paddle1_rect, paddle2_rect, score1, score2
    paddle1_position_y, paddle2_position_y = HEIGHT // 2, HEIGHT // 2
    paddle1_rect = paddle_img.get_rect(topleft=(10, paddle1_position_y - PADDLE_HEIGHT // 2))
    paddle2_rect = paddle_img.get_rect(topright=(WIDTH - 10, paddle2_position_y - PADDLE_HEIGHT // 2))

    play_again = True
    while play_again:
        # Get player names
        player1_name, player2_name = update_player_info(screen)

        # Wait for user to start the game
        wait_for_start(screen)

        # Reset scores
        score1, score2 = 0, 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            process_user_input()
            update_ball_position()
            detect_collisions()

            # Check for winning condition
            if score1 >= WINNING_SCORE:
                display_winner(player1_name)
                running = False
            elif score2 >= WINNING_SCORE:
                display_winner(player2_name)
                running = False

            screen.blit(background_img, (0, 0))
            draw_paddles()
            draw_ball()
            draw_scores(player1_name, player2_name, score1, score2)

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

        play_again = ask_play_again(screen)

    pygame.quit()
    sys.exit()

# Function to process user input
def process_user_input():
    global paddle1_position_y, paddle2_position_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_position_y -= 5
    if keys[pygame.K_s]:
        paddle1_position_y += 5
    if keys[pygame.K_UP]:
        paddle2_position_y -= 5
    if keys[pygame.K_DOWN]:
        paddle2_position_y += 5

    # Boundary checking for paddles
    paddle1_position_y = max(PADDLE_HEIGHT // 2, min(paddle1_position_y, HEIGHT - PADDLE_HEIGHT // 2))
    paddle2_position_y = max(PADDLE_HEIGHT // 2, min(paddle2_position_y, HEIGHT - PADDLE_HEIGHT // 2))

    # Update paddle rect positions
    paddle1_rect.topleft = (10, paddle1_position_y - PADDLE_HEIGHT // 2)
    paddle2_rect.topright = (WIDTH - 10, paddle2_position_y - PADDLE_HEIGHT // 2)

if __name__ == "__main__":
    main()







