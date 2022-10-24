import pygame
import random

pygame.init()


yellow = (255, 255, 102)
black = (36, 33, 33)
red = (213, 50, 80) #
end_color = (71, 30, 30) #
snake_color = (0, 255, 0) #
grey = (79, 79, 77) #
gold = (255, 200, 0) #

dis_width = 800
dis_height = 700

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')
pygame.display.set_icon(pygame.image.load("img/snake_icon.png"))
fon = pygame.image.load("img/snake_background.png")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 14

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("serif", 40)

pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

sndcoin = pygame.mixer.Sound('sounds/soundcoin.wav')
sndcrash = pygame.mixer.Sound('sounds/crash.wav')


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [35, 630])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def barrier(barriers, snake, food):
    i = 0
    while i < 10:
        barrier_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        barrier_y = round(random.randrange(0, dis_height - 100 - snake_block) / 10.0) * 10.0
        bar_xy = []
        bar_xy.append(barrier_x)
        bar_xy.append(barrier_y)
        if bar_xy in barriers or bar_xy in snake or bar_xy in food:
            continue
        else:
            i += 1
            barriers.append(bar_xy)


def game():
    game_over = False
    game_stop = False
    last_key = None

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    barr = []

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - 100 - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_stop == True:
            dis.fill(end_color)
            message("You Lost! Press Esc-Quit or Space-Play Again", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_stop = False
                    if event.key == pygame.K_SPACE:
                        game()

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_key != pygame.K_RIGHT:
                    last_key = pygame.K_LEFT
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and last_key != pygame.K_LEFT:
                    last_key = pygame.K_RIGHT
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and last_key != pygame.K_DOWN:
                    last_key = pygame.K_UP
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and last_key != pygame.K_UP:
                    last_key = pygame.K_DOWN
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height - 100 or y1 < 0:
            sndcrash.play()
            game_stop = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(grey)
        fon.set_alpha(15)
        dis.blit(fon, (0, 0))

        if x1 == foodx and y1 == foody:
            sndcoin.play()
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - 100 - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        pygame.draw.circle(dis, gold, [foodx + 5, foody + 5], 5)

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_stop = True

        our_snake(snake_block, snake_List)
        pygame.draw.rect(dis, black, (0, 600, 800, 100))
        Your_score(Length_of_snake - 1)

        dictionary = {5: 0, 10: 10, 20: 20, 30: 30, 40: 40
                      }

        if Length_of_snake - 1 in dictionary and len(barr) == dictionary[Length_of_snake - 1]:
            barrier(barr, snake_List, [foodx, foody])

        for i in barr:
            pygame.draw.circle(dis, red, [i[0] + 5, i[1] + 5, ], 5)

        if snake_Head in barr:
            sndcrash.play()
            game_stop = True

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game()
