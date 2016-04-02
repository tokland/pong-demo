#!/usr/bin/env python
import collections
import time
import math
import pygame

struct = collections.namedtuple

Ball = struct("Ball", ["x", "y", "width", "height", "speed_x", "speed_y", "image", "sound"])
Paddle = struct("Paddle", ["x", "y", "width", "height", "max_speed_y", "image"])
Field = struct("Field", ["width", "height", "ball", "paddle", "image"])
Game = struct("Game", ["field", "screen"])

def ball_hits_paddle(ball, paddle):
    """Return True if the ball has hit the paddle."""
    return (
        ball.speed_x < 0 and 
        ball.x >= paddle.x + paddle.width / 2.0 and
        ball.x < paddle.x + paddle.width and
        ball.y + ball.height > paddle.y and
        ball.y <= paddle.y + paddle.height
    )

def get_new_ball(field, delta_t):
    """
    Return a new ball considering collisions with the field limits and the
    paddle. Return None if the ball went out of bounds.
    """
    ball = field.ball
    new_x = ball.x + delta_t * ball.speed_x
    new_y = ball.y + delta_t * ball.speed_y
    new_ball = ball._replace(x=new_x, y=new_y)
    ball_reached_wall = new_ball.x < 0
    
    if ball_reached_wall:
        return
    else:
        if ball_hits_paddle(new_ball, field.paddle):
            ball.sound.play()
            new_speed_x = abs(ball.speed_x)
            speed = math.sqrt(new_speed_x**2  + ball.speed_y**2)
        elif ball.speed_x > 0 and new_ball.x + ball.width >= field.width:
            ball.sound.play()
            new_speed_x = -abs(ball.speed_x)
        else:
            new_speed_x = ball.speed_x
            
        if ball.speed_y < 0 and new_ball.y < 0:
            ball.sound.play()
            new_speed_y = abs(ball.speed_y)
        elif ball.speed_y > 0 and new_ball.y + ball.height >= field.height:
            ball.sound.play()
            new_speed_y = -abs(ball.speed_y)
        else:
            new_speed_y = ball.speed_y

        factor = (1.0 + delta_t / 50.0)
        return new_ball._replace(speed_x=new_speed_x*factor, speed_y=new_speed_y*factor)

def get_new_paddle(field, keys, delta_t):
    """Return a new paddle (keys: UP/DOWN)."""
    paddle = field.paddle
    if keys[pygame.K_DOWN]:
        paddle_speed_y = paddle.max_speed_y
    elif keys[pygame.K_UP]:
        paddle_speed_y = -paddle.max_speed_y
    else:
        paddle_speed_y = 0

    new_paddle_y = paddle.y + delta_t * paddle_speed_y
    if new_paddle_y < 0 or new_paddle_y + paddle.height >= field.height:
        final_paddle_y = paddle.y
    else:
        final_paddle_y = new_paddle_y
    return paddle._replace(y=final_paddle_y)

def get_new_field(field, keys, delta_t):
    """Return the new field (None if the game finished)."""
    new_paddle = get_new_paddle(field, keys, delta_t)
    new_ball = get_new_ball(field, delta_t)
    return field._replace(ball=new_ball, paddle=new_paddle)

def draw_game(game):
    """Draw the game (field, ball and paddle) to the game screen."""
    field = game.field
    game.screen.blit(field.image, (0, 0))
    game.screen.blit(field.ball.image, (field.ball.x, field.ball.y))
    game.screen.blit(field.paddle.image, (field.paddle.x, field.paddle.y))
    pygame.display.flip()
      
def loop_game(game):
    """Loop the game state."""
    time0 = time.time()
    while 1:
        draw_game(game)
        time1 = time.time()
        keys = pygame.key.get_pressed()
        new_field = get_new_field(game.field, keys, time1 - time0)

        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            break
        elif not new_field.ball:
            break
        else:
            time0 = time1
            game = game._replace(field=new_field)

def build_game(screen_size):
    """Return the initial game object."""
    ball_image = pygame.image.load("media/ball.png")
    ball_sound = pygame.mixer.Sound("media/tap.wav")
    ball = Ball(image=ball_image, sound=ball_sound, x=100, y=200, 
        width=ball_image.get_width(), height=ball_image.get_height(),
        speed_x=550, speed_y=300)
    
    paddle_image = pygame.image.load("media/paddle.png")
    paddle = Paddle(image=paddle_image, x=10, y=100, max_speed_y=600, 
        width=paddle_image.get_width(), height=paddle_image.get_height())
    
    width, height = screen_size
    bg_image = pygame.transform.scale(pygame.image.load("media/m83.jpg"), screen_size)
    field = Field(ball=ball, paddle=paddle, image=bg_image, width=width, height=height)

    screen = pygame.display.set_mode(screen_size)
    return Game(field=field, screen=screen)

def run():
    """Run the loop game."""
    pygame.init()
    game = build_game(screen_size=(640, 480))
    pygame.mixer.music.load("media/tiger.stm")
    pygame.mixer.music.play()
    loop_game(game)

run()
