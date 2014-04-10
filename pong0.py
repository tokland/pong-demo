from collections import namedtuple as struct
import pygame
import time

Ball = struct("Ball", 
    ["pos_x", "pos_y", "width", "height", "speed_x", "speed_y", "image"])
Paddle = struct("Paddle", 
    ["pos_x", "pos_y", "width", "height", "speed_y", "max_speed_y", "image"])
Field = struct("Field", ["width", "height", "ball", "paddle"])
Game = struct("Game", ["field", "screen"])

def ball_hits_paddle(ball, paddle):
    """Return True if the ball has hit the paddle."""
    return (ball.speed_x < 0 and 
        ball.pos_x >= paddle.pos_x + paddle.width / 2.0 and
        ball.pos_x < paddle.pos_x + paddle.width and
        ball.pos_y + ball.height > paddle.pos_y and
        ball.pos_y <= paddle.pos_y + paddle.height)

def get_new_ball(ball, field, delta_t):
    "Return a new ball considering collisions (None if the ball went out of bounds)"
    new_pos_x = ball.pos_x + delta_t*ball.speed_x
    new_pos_y = ball.pos_y + delta_t*ball.speed_y
    new_ball = ball._replace(pos_x=new_pos_x, pos_y=new_pos_y)
    
    if (new_ball.pos_x + new_ball.width) < 0:
        return
    else:
        if ball_hits_paddle(new_ball, field.paddle):
            new_speed_x = abs(ball.speed_x)
        elif ball.speed_x > 0 and (new_ball.pos_x + ball.width) >= field.width:
            new_speed_x = -abs(ball.speed_x)
        else:
            new_speed_x = ball.speed_x
            
        if ball.speed_y < 0 and new_ball.pos_y < 0:
            new_speed_y = abs(ball.speed_y)
        elif ball.speed_y > 0 and (new_ball.pos_y + ball.height) >= field.height:
            new_speed_y = -abs(ball.speed_y)
        else:
            new_speed_y = ball.speed_y

        return new_ball._replace(speed_x=new_speed_x, speed_y=new_speed_y)

def get_new_paddle(paddle, field, keys, delta_t):
    """Return a new paddle (keys: UP/DOWN)."""
    new_paddle_pos_y = paddle.pos_y + delta_t*paddle.speed_y
    
    if keys[pygame.K_DOWN]:
        speed_y = paddle.max_speed_y
    elif keys[pygame.K_UP]:
        speed_y = -paddle.max_speed_y
    else:
        speed_y = 0
    if new_paddle_pos_y < 0 or (new_paddle_pos_y + paddle.height) >= field.height:
        final_paddle_pos_y = paddle.pos_y
    else:
        final_paddle_pos_y = new_paddle_pos_y
    return paddle._replace(pos_y=final_paddle_pos_y, speed_y=speed_y)

def get_new_game(game, keys, delta_t):
    """Return the new field (None if the game finished)."""
    field = game.field
    new_paddle = get_new_paddle(field.paddle, field, keys, delta_t)
    new_ball = get_new_ball(field.ball, field, delta_t)
    new_field = field._replace(ball=new_ball, paddle=new_paddle)
    return game._replace(field=new_field)

def draw_game(game):
    """Draw the game (field, ball and paddle) onto the game screen."""
    field = game.field
    game.screen.fill((0, 0, 0))
    game.screen.blit(field.ball.image, (field.ball.pos_x, field.ball.pos_y))
    game.screen.blit(field.paddle.image, (field.paddle.pos_x, field.paddle.pos_y))
    pygame.display.flip()
      
def loop_game(game):
    """State loop of a game."""
    time0 = time.time()
    while 1:  
        draw_game(game)
        
        time1 = time.time()
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        new_game = get_new_game(game, keys, delta_t=time1-time0)
        
        if any(event.type == pygame.QUIT for event in events):
            break
        elif not new_game.field.ball:
            break
        else:
            time0 = time1
            game = new_game

def build_game(screen_size):
    """Load multimedia files and return the initial game object."""
    ball_image = pygame.image.load("media/ball.png")
    ball = Ball(image=ball_image, pos_x=100, pos_y=200, speed_x=550, speed_y=300, 
        width=ball_image.get_width(), height=ball_image.get_height())
    
    paddle_image = pygame.image.load("media/paddle.png")
    paddle = Paddle(image=paddle_image, pos_x=10, pos_y=100, max_speed_y=600, 
        speed_y=0, width=paddle_image.get_width(), height=paddle_image.get_height())
    
    width, height = screen_size
    field = Field(ball=ball, paddle=paddle, width=width, height=height)

    screen = pygame.display.set_mode(screen_size)
    return Game(field=field, screen=screen)

def run():
    """Run the loop game."""
    pygame.init()
    game = build_game(screen_size=(640, 480))
    loop_game(game)

run()
