import pygame
import numpy as np
import pandas as pd
from numpy.random import randint
from pathlib import Path

from classes import Ball, Bat, Rect, Triangle, Vector

colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'red': (255, 0 , 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255),
          'tuerkis': '#03fcb1',
          'lila': '#6203fc',
          }

# file name of highscores
Highscore = "Highscore.csv"

# read highscores from file "Highscore.csv" or creates a new file if it does not exist
def load_highscores():
    try:
        df = pd.read_csv(Highscore, header=0)
        da = True
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Score"])
        da = False
    return df, da

# save highscore to file "Highscore.csv"
def save_highscore(name, score):
    df, _ = load_highscores()
    df = df._append({"Name": name, "Score": score}, ignore_index=True)
    df.to_csv(Highscore, index=False)

# start screen to enter the name of the player
def start_screen(screen):
    font = pygame.font.Font(None, 40)
    input_rect = pygame.Rect(220, 300, 200, 50)
    player_name = ''
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill(colors['white'])
        text_surface = font.render('Enter Your Name:', True, colors['black'])
        text_rect = text_surface.get_rect(center=(300, 250))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, colors['black'], input_rect, 2)
        text_surface = font.render(player_name, True, colors['black'])
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()

    return player_name

# main function
def main():
    
    ball2_here = False
    starter1 = True
    starter2 = False
    balls = []
    time = 0
    fps_multiplyer = 5
    
    # start function to start the game
    def start1():
        
        ball1.velocity = Vector(0, -8.5 * fps_multiplyer) * 1.1
        
    def start2():
        
        ball2.velocity = Vector(0, -8.5 * fps_multiplyer) * 1.1
    
    # Initialize PyGame
    pygame.init()
    
    #Setup
    running = True
    scores = []
    score = 0
    roundnr = 0
    scores.append(score)

    # display screen
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption('Flipper')
    player_name = start_screen(screen)
    
    # Clock
    clock = pygame.time.Clock()

    # Initialisation
    ball1 = Ball(screen, Vector(20, 660),Vector(0,0),10)
    ball2 = Ball(screen, Vector(20, 660),Vector(0,0),10)
    big_ball = Ball(screen, Vector(300,300), Vector(0,0), 30, grav=Vector(0,0))
    big_ball2 = Ball(screen, Vector(450,200), Vector(0,0), 20, grav=Vector(0,0))
    
    # Colors, Background
    bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg2.png")).convert_alpha()
    text_font = pygame.font.Font(None,25)
    
    # Music
    music = pygame.mixer.music.load(Path(__file__).parents[0] / Path("Clown.mp3")) # Quelle https://www.chosic.com/download-audio/53609/
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.1)

    # Surfaces
    text_surface = text_font.render('Start: "Space", Reset: "R", Bats: Arrow "Left/Right"', False, 'white')
    text_rect = text_surface.get_rect(midbottom = (320,50))
    hole_w = 150
    hole_h = 100
    hole1_surface = pygame.Surface((hole_w,hole_h))
    hole1_surface.fill(colors['white'])
    hole2_surface = pygame.Surface((hole_w,hole_h))
    hole2_surface.fill(colors['white'])
    
    # Shapes begin
    rect1 = Rect(Vector(300,400),100,20)
    start_rect = Rect(Vector(35,150),5, 550)
    start_rect2 = Rect(Vector(0,60), 5, 640)
    start_tri = Triangle(Vector(0,0), Vector(60,0), Vector(0,60))    

    nlb_height = Vector(0,15)
    nlb_width = Vector(130,0)
    nlb_bottomleft = Vector(145,725)
    nlb_points = (nlb_bottomleft , nlb_bottomleft + nlb_width, nlb_bottomleft + nlb_width + nlb_height , nlb_bottomleft + nlb_height)
    new_left_bat = Bat(screen, colors['green'], nlb_points) 

    nrb_height = Vector(0,15)
    nrb_width = Vector(-130,0)
    nrb_bottomright = Vector(455,725)
    nrb_points = (nrb_bottomright , nrb_bottomright + nrb_width, nrb_bottomright + nrb_width + nrb_height , nrb_bottomright + nrb_height)
    new_right_bat = Bat(screen, colors['green'], nrb_points, right=True)
    
    starter_bat_points = (Vector(100,700), Vector(10,700), Vector(10,710), Vector(100,710))
    starter_bat = Bat(screen, colors['red'], starter_bat_points, right=True, anschlag=10) # setzt den Anschlag des Schlägers fest
    # Shapes end
    
    # Movement
    rect_speed = 0.5
    big_ball_speed = 2
    
    # Read highscores
    df, da = load_highscores()
    
    # Times
    ball2_time_begin = 0
    time = 0
    
    # Main event loop
    while running:
        
        # Adjust screen
        s_width, s_height = screen.get_width(), screen.get_height()
        bg = pygame.transform.scale(bg_orig, (s_width, s_height))
        screen.blit(bg, (0, 0))
        
        # Display elemnts
        screen.blit(text_surface,text_rect)
        score_surface = text_font.render(f'Score: {score}', False, 'White')
        score_rect = score_surface.get_rect(midbottom = (300,100))
        screen.blit(score_surface,score_rect)
        hole1_rect = hole1_surface.get_rect(bottomleft = (0,screen.get_height()))
        hole2_rect = hole2_surface.get_rect(bottomright = (screen.get_width(),screen.get_height()))
        screen.blit(hole1_surface,hole1_rect)
        screen.blit(hole2_surface,hole2_rect)   
        
        # Screen borders
        ground_level = screen.get_height() - hole_h
        screen_borders = Vector(screen.get_width(), ground_level)
        
        
        # Check if ball2 is here
        if ball2_here and not starter1 and ball2.velocity.abs() <= 1:
            
            # Ball2 darf starten 
            starter2 = True
        
        
        # Check if ball2 is allowed to spawn
        if ball1.check_collision(big_ball) == True: 
            
            ball2_here = True
            ball2_time_begin = pygame.time.get_ticks()


        # After ball2 is 20 sec in the game, code checks if ball2 is allowed to spawn
        if pygame.time.get_ticks() - ball2_time_begin > 20000:
            
            ball2_here = ball1.check_collision(big_ball)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                
                running = False
              
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    
                    # Check if one of the balls is allowed to start
                    if starter1 or starter2: 
                        
                        # Bat can hit the ball again
                        starter_bat.count = 0
                    
                    if starter1: 
                        
                        start1()
                        starter1 = False
                        
                    if starter2: 
                        
                        start2()
                        starter2 = False
                        
                if event.key == pygame.K_LEFT:
                    
                    # Left Bat can move again
                    new_left_bat.count = 0
                    
                if event.key == pygame.K_RIGHT:
                    
                    # Right Bat can move again
                    new_right_bat.count = 0
                    
                if event.key == pygame.K_r:
                    
                    # If Reset is pressed, the game will be reset
                    starter1 = True
                    starter2 = False
                    ball2_here = False
                    ball1.reset()
                    ball2.reset()
                    roundnr += 1
                    score = 0
                    scores.append(score)
                    
                if event.key == pygame.K_m:
                    
                    pass
                    # Random Ball Movement cheat code
                    # m = 5
                    # ball1.velocity.x += randint(-m,m)
                    # ball1.velocity.y += randint(-m,m)
                    # if ball2_here: ball2.velocity.x += randint(-m,m)
                    # if ball2_here: ball2.velocity.y += randint(-m,m)


        # Gameplay is happening here

        # Bats
        new_left_bat.update()
        new_right_bat.update()
        starter_bat.update()
        
        # Balls
        if ball2_here: 
            balls = [ball1, ball2]
        else:
            balls = [ball1]

        for ball in balls:
            
            # Check if the ball is too slow, so the game gives a score penalty
            if ball.velocity.abs() < 1 * fps_multiplyer:
        
                time = pygame.time.get_ticks()
                
                if time % 5000 <= 3: score -= 1 
                
            else:
                # If the ball is fast enough:
                time = 0

            for bat in [new_left_bat, new_right_bat]:
                
                ball.sat_algo(bat.points_tuple, bat)
                
  
        # Let objects that are supposed to move, move
        if rect1.position.x < 45 + 2*ball1.radius or (rect1.position.x + rect1.width) > screen.get_width() - 2*ball1.radius:
            
            rect_speed *= -1
            
        rect1.position.x += rect_speed
        
        if big_ball.position.x - big_ball.radius < 46 + 4*ball1.radius:
            
            big_ball_speed *= -1

        elif big_ball.position.x + big_ball.radius > screen.get_width() - 4*ball1.radius:
            
            big_ball_speed *= -1

        big_ball.position.x += big_ball_speed * 0.2

        # Draw objects
        pygame.draw.circle(screen, (35, 161, 224), [ball1.position.x, ball1.position.y] , ball1.radius)
        if ball2_here: pygame.draw.circle(screen, colors['tuerkis'], [ball2.position.x,ball2.position.y] , ball2.radius)
        pygame.draw.circle(screen, colors['lila'], [big_ball.position.x,big_ball.position.y] , big_ball.radius)
        pygame.draw.circle(screen, colors['lila'], [big_ball2.position.x, big_ball2.position.y] , big_ball2.radius)
        pygame.draw.rect(screen, 'blue', (rect1.position.x, rect1.position.y, rect1.width, rect1.height))
        pygame.draw.rect(screen, 'green', (start_rect.position.x, start_rect.position.y, start_rect.width, start_rect.height))
        pygame.draw.rect(screen, 'green', (start_rect2.position.x, start_rect2.position.y, start_rect2.width, start_rect2.height))
        pygame.draw.line(screen, 'red', (35,690), (25,700))
        pygame.draw.line(screen, 'red', (5,690), (15,700))
        start_tri.draw_triangle(screen)
        
        # Motion 
        if ball2_here: 
            ball1.check_collision(ball2)
        else:
            ball2.reset()
        
        for ball in balls:
            
            ball.check_collision(big_ball2)
            ball.check_collision(big_ball)
            ball.gravitate()
            
            for obj in [start_rect, start_rect2, start_tri, rect1]:
                
                if ball.is_object_collision(obj):
                    
                    _,normal = obj.is_collision(ball)
                    tangent = normal.rotate(90)
                    prevelo = ball.velocity
                    velo = tangent * ball.velocity.dot(tangent) * (1) + normal * ball.velocity.dot(normal) * (-1)
                    ball.position -= prevelo.normalize()*10
                    ball.velocity =  velo*prevelo.abs()
                    if obj == rect1: score += 1
            
            if ball.velocity.abs() > 10:
                
                # Velocity cap
                ball.velocity = ball.velocity * 0.7
            
            if (abs(ball.position.x - screen.get_width()/2) < (screen.get_width() - 2*hole_w)/2
                and screen.get_height() - ball.position.y < 200):
                
                # Above checks two things:
                    # 1. Is the distance in x-distance of the ball from the middle of the screen smaller than the half the x-distance of the hole from the middle of the screen?
                    # 2. Is ball y-distance from the bottom of the screen smaller than height of the hole?
                
                # If those conditions are met, the ball is not colliding at the bottom
                
                if screen.get_height() - ball.position.y < 1:
                    
                    # If the ball is now even at the bottom, then the game is over
                    roundnr += 1
                    score = 0
                    scores.append(score)
                    ball.check_screen_collide(screen_borders)
                    starter1 = True
                    starter2 = True
                    ball2_here = False
                    ball1.reset()
                    ball2.reset()
                    
            else:
                
                ball.check_screen_collide(screen_borders)
            
            
        # Highscore
        scores[roundnr] = score
        highscore = max(scores)
    
        if da:
            
            max_score = df["Score"].max()
            max_name = df.loc[df["Score"] == max_score]["Name"].values[0]
            your_max_score = df.loc[df["Name"] == player_name]["Score"].max()
            
            if highscore < max_score:
                
                highscore_surface = text_font.render(f'Highscore: {max_name}, {max_score}', False, 'White')
                
            elif highscore == max_score:
                
                highscore_surface = text_font.render(f'Highscore: {max_name}, {player_name}, {max_score}', False, 'White')
                
            else:
                
                highscore_surface = text_font.render(f'Highscore: {player_name}, {highscore}', False, 'White')
                
            if your_max_score > highscore:
                
                your_highscore = text_font.render(f'Your Highscore: {player_name}, {your_max_score}', False, 'White')
                
            else:
                
                your_highscore = text_font.render(f'Your Highscore: {player_name}, {highscore}', False, 'White')
        else:
            
            if highscore > 0:
                
                highscore_surface = text_font.render(f'Highscore: {player_name}, {highscore}', False, 'White')
                your_highscore = text_font.render(f'Your Highscore: {player_name}, {highscore}', False, 'White')
                
            else:
                
                highscore_surface = text_font.render(f'Highscore: No Score', False, 'White')
                your_highscore = text_font.render(f'Your Highscore: No Score', False, 'White')
                
        # Display highscores  
        your_highscore_rect = your_highscore.get_rect(midbottom = (300,150))
        highscore_rect = highscore_surface.get_rect(midbottom = (300,120))
        screen.blit(your_highscore,your_highscore_rect)
        screen.blit(highscore_surface,highscore_rect)
        
        # Settings
        pygame.display.flip() # Update the display of the full screen
        clock.tick(200 * fps_multiplyer) # 1000 frames per second for smooth movement     


    save_highscore(player_name, highscore)
    
if __name__ == '__main__':
    main()
