import random
import time
import pygame

pygame.font.init()

clock = pygame.time.Clock()  # defining a clock
FONT1 = pygame.font.SysFont("Tahoma", 24)  # the font we will use to render text

# Game screen
WIN_WIDTH, WIN_LENGTH = 850, 650
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH))  # display a window
pygame.display.set_caption("Patrick's first game")
image = pygame.transform.scale(pygame.image.load('universe1.jpg'),
                               (WIN_WIDTH, WIN_LENGTH))

# Player info
PLAYER_WID, PLAYER_LEN = 40, 60
player = pygame.Rect((WIN_WIDTH - PLAYER_WID) / 2, WIN_LENGTH - PLAYER_LEN,
                     PLAYER_WID, PLAYER_LEN)

OBJECT_WID, OBJECT_LEN = 10, 15  # falling objects dimentions


def collision__should_continue(
        time_elapsed):  # a collision happened. returns True/False for should_continue?
    lost_message = FONT1.render(
        f'''You lost! Your score is {round(time_elapsed, 1)} seconds''', True,
        'Green')
    SCREEN.blit(lost_message, (WIN_WIDTH / 4, WIN_LENGTH / 2))
    while True:
        pygame.display.update()
        for event in pygame.event.get():  # checks for exit event
            if event.type == pygame.QUIT:
                return False


def graphics(player, time_elapsed: float, falling_objects: list):
    SCREEN.blit(image, (0, 0))  # creating a background
    pygame.draw.rect(SCREEN, 'blue', player)  # creating a player sprite

    # display falling objects
    for object in falling_objects:
        pygame.draw.rect(SCREEN, 'red', object)

    # displaying time elapsed
    display_time = FONT1.render(f"Time elapsed: {round(time_elapsed, 1)}s",
                                True, 'white')
    SCREEN.blit(display_time, (0.7 * WIN_WIDTH, 15))

    pygame.display.update()


def main():
    run_game = True
    start_time = time.time()

    ticks = 0  # number of clock ticks
    frequency = 3000  # milliseconds
    number_of_objects = 3
    falling_objects = []

    while run_game:
        ticks += clock.tick(
            150)  # loop will run a maximum of 150 times per second. clock.tick should return 1000/550
        time_elapsed = time.time() - start_time

        for event in pygame.event.get():  # list of all the events that happen
            if event.type == pygame.QUIT:  # checks for pygame.QUIT
                run_game = False
                break

        # player movements
        keys = pygame.key.get_pressed()  # dictionary of all the pressed keys
        if keys[pygame.K_LEFT] and player.x != 0:  # if left key is pressed
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x != WIN_WIDTH - PLAYER_WID:
            player.x += 5
        if keys[pygame.K_UP] and player.y != 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.y != WIN_LENGTH - PLAYER_LEN:
            player.y += 5

        # create falling objects
        if not ticks < frequency:  # every frequency milliseconds
            for object in range(
                    int(number_of_objects)):  # create falling objects
                object = pygame.Rect(random.randint(0, WIN_WIDTH - OBJECT_WID),
                                     -OBJECT_LEN, OBJECT_WID, OBJECT_LEN)
                falling_objects.append(object)

            number_of_objects = max(10,
                                    number_of_objects + 1 / 3)  # 10 is the maximum number of objects
            frequency = max(500,
                            frequency - 30)  # increasing the frequency because the ACTUAL_frequency = 1/frequency
            ticks = 0

        # move the objects in falling_objects down
        for object in falling_objects[:]:
            object.y += 1
            if object.y > WIN_LENGTH:
                falling_objects.remove(object)
            elif object.colliderect(player):
                falling_objects.remove(object)
                run_game = collision__should_continue(time_elapsed)

        graphics(player, time_elapsed, falling_objects)

    pygame.quit()


if __name__ == '__main__':
    main()
