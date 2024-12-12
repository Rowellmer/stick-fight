import pygame
import sys

# Constants and colors
WIDTH = 1370
HEIGHT = 710
slategray = (112, 128, 144)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)           
fps = 120

def main_menu():
    print("=== MAIN MENU ===")
    print("1. Start Game")
    print("2. Exit")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        player1_name = input("Enter a name for Player 1: ")
        player2_name = input("Enter a name for Player 2: ")

        print(f"Starting game with Player 1: {player1_name} and Player 2: {player2_name}...")
        start_game(player1_name, player2_name)
    elif choice == '2':
        print("Exiting... Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def start_game(player1_name, player2_name):
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stick Fight")

    timer = pygame.time.Clock()

    # Player variables
    player1 = {
        "x": 120,
        "y": 400,
        "health": 500,
        "animation": ['sprites/pixil-frame-0.png', 'sprites/pixil-frame-1.png', 'sprites/pixil-frame-2.png', 'sprites/pixil-frame-3.png', 'sprites/pixil-frame-4.png', 'sprites/pixil-frame-5.png', 'sprites/pixil-frame-6.png', 'sprites/pixil-frame-7.png'],
        "attack_animation": ['sprites/sprites2/1attack_0.png', 'sprites/sprites2/1attack_1.png', 'sprites/sprites2/1attack_2.png'],
        "frame": 0,
        "mode": 0,
        "count": 0,
        "in_air": False,
        "y_change": 0,
        "attacking": False,
        "attack_counter": 0,  # Keeps track of attack presses
        "attack_offset": {"x": -260, "y": -225}  # Offset for attack animation
    }

    player2 = {
        "x": 1020,
        "y": 400,
        "health": 500,
        "animation": ['sprites/2pixil-frame-0.png', 'sprites/2pixil-frame-1.png', 'sprites/2pixil-frame-5.png', 'sprites/2pixil-frame-4.png', 'sprites/2pixil-frame-3.png', 'sprites/2pixil-frame-2.png', 'sprites/2pixil-frame-6.png', 'sprites/2pixil-frame-7.png'],
        "attack_animation": ['sprites/sprites2/2attack_3.png', 'sprites/sprites2/2attack_4.png', 'sprites/sprites2/2attack_5.png'],
        "frame": 0,
        "mode": 0,
        "count": 0,
        "in_air": False,
        "y_change": 0,
        "attacking": False,
        "attack_counter": 0,  # Keeps track of attack presses
        "attack_offset": {"x": -250, "y": -225}  # Offset for attack animation
    }

    gravity = 0.5
    x_speed = 3
    attack_range = 500

    def update_player(player, counter):
        if counter >= 120:
            counter = 0
        # Depending on the mode, select the appropriate animation frame
        if player["mode"] == 0:
            player["frame"] = 0 if counter < 60 else 1
        elif player["mode"] == 1:
            player["frame"] = 2 if counter < 60 else 3
        elif player["mode"] == 2:
            player["frame"] = 4 if counter < 60 else 5
        elif player["mode"] == 3:
            player["frame"] = 6
        elif player["mode"] == 4:
            player["frame"] = 7
        elif player["attacking"]:
            player["frame"] = player["attack_counter"]  # Use attack_counter for attack frames
        counter += 1
        return counter

    def draw_attack(player):
        if player["attacking"]:
            attack_sprite = pygame.image.load(player["attack_animation"][player["attack_counter"]]).convert_alpha()
            attack_sprite = pygame.transform.scale(attack_sprite, (850, 850))  # Resize attack sprite
            attack_x = player["x"] + player["attack_offset"]["x"]
            attack_y = player["y"] + player["attack_offset"]["y"]
            screen.blit(attack_sprite, (attack_x, attack_y))

    def check_collision(attacker, target):
        attack_x = attacker["x"] + attacker["attack_offset"]["x"]
        attack_y = attacker["y"] + attacker["attack_offset"]["y"]
        if abs(attacker["x"] - target["x"]) < attack_range and abs(attacker["y"] - target["y"]) < 50:
            return True
        return False

    def draw_health_bar(x, y, health):
        pygame.draw.rect(screen, red, (x, y, 500, 10))
        pygame.draw.rect(screen, green, (x, y, health, 10)) 

    # Main game loop
    running = True
    while running:
        timer.tick(fps)
        screen.fill(slategray)
        floor = pygame.draw.rect(screen, gray, (0, 650, WIDTH, HEIGHT - 650))
        floor_line = pygame.draw.line(screen, black, (0, 650), (WIDTH, 650), 5)

        # Update animations
        player1["count"] = update_player(player1, player1["count"])
        player2["count"] = update_player(player2, player2["count"])

        # Determine which animation to use based on attacking status
        if not player1["attacking"]:
            sprite1 = pygame.image.load(player1["animation"][player1["frame"]]).convert_alpha()
            resized_sprite1 = pygame.transform.scale(sprite1, (300, 300))
            screen.blit(resized_sprite1, (player1["x"], player1["y"]))
        else:
            draw_attack(player1)

        if not player2["attacking"]:
            sprite2 = pygame.image.load(player2["animation"][player2["frame"]]).convert_alpha()
            resized_sprite2 = pygame.transform.scale(sprite2, (300, 300))
            screen.blit(resized_sprite2, (player2["x"], player2["y"]))
        else:
            draw_attack(player2)

        # Draw health bars
        draw_health_bar(50, 50, player1["health"])
        draw_health_bar(WIDTH - 550, 50, player2["health"])

        # Display player names
        font = pygame.font.Font(None, 36)
        player1_text = font.render(f"Player 1: {player1_name}", True, (255, 255, 255))
        player2_text = font.render(f"Player 2: {player2_name}", True, (255, 255, 255))
        screen.blit(player1_text, (50, 20))
        screen.blit(player2_text, (WIDTH - 300, 20))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key == pygame.K_d and not player1["in_air"]:
                    player1["mode"] = 1
                if event.key == pygame.K_a and not player1["in_air"]:
                    player1["mode"] = 2
                if event.key == pygame.K_w and not player1["in_air"]:
                    player1["in_air"] = True
                    player1["y_change"] = -15
                    player1["mode"] = 3
                if event.key == pygame.K_s and not player1["in_air"]:
                    player1["mode"] = 4
                if event.key == pygame.K_e:
                    player1["attacking"] = True
                    # Increment attack animation counter on each press
                    player1["attack_counter"] = (player1["attack_counter"] + 1) % 3  # Cycles through 0, 1, 2

                # Player 2 controls
                if event.key == pygame.K_RIGHT and not player2["in_air"]:
                    player2["mode"] = 1
                if event.key == pygame.K_LEFT and not player2["in_air"]:
                    player2["mode"] = 2
                if event.key == pygame.K_UP and not player2["in_air"]:
                    player2["in_air"] = True
                    player2["y_change"] = -15
                    player2["mode"] = 3
                if event.key == pygame.K_DOWN and not player2["in_air"]:
                    player2["mode"] = 4
                if event.key == pygame.K_0:
                    player2["attacking"] = True
                    # Increment attack animation counter on each press
                    player2["attack_counter"] = (player2["attack_counter"] + 1) % 3  # Cycles through 0, 1, 2

            if event.type == pygame.KEYUP:
                if not player1["in_air"]:
                    player1["mode"] = 0
                    player1["attacking"] = False
                if not player2["in_air"]:
                    player2["mode"] = 0
                    player2["attacking"] = False

        # Update vertical positions
        for player in [player1, player2]:
            player["y"] += player["y_change"]
            if player["in_air"]:
                player["y_change"] += gravity
            if player["y"] > 400:
                player["y"] = 400
                player["y_change"] = 0
                player["in_air"] = False
                player["mode"] = 0

        # Horizontal movement
        if player1["mode"] == 1 and player1["x"] + x_speed + 120 < WIDTH:
            player1["x"] += x_speed
        if player1["mode"] == 2 and player1["x"] - x_speed + 90 > 0:
            player1["x"] -= x_speed

        if player2["mode"] == 1 and player2["x"] + x_speed + 120 < WIDTH:
            player2["x"] += x_speed
        if player2["mode"] == 2 and player2["x"] - x_speed + 90 > 0:
            player2["x"] -= x_speed

        # Check for attacks
        if player1["attacking"] and check_collision(player1, player2):
            player2["health"] -= 1
        if player2["attacking"] and check_collision(player2, player1):
            player1["health"] -= 1

        # Check for game over
        if player1["health"] <= 0 or player2["health"] <= 0:
            running = False
            winner = "Player 1" if player2["health"] <= 0 else "Player 2"
            print(f"Game Over! {winner} wins!")

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
