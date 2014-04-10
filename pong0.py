from collections import namedtuple as struct

Ball = struct("Ball", 
    ["pos_x", "pos_y", "width", "height", "speed_x", "speed_y", "image"])
Paddle = struct("Paddle", 
    ["pos_x", "pos_y", "width", "height", "speed_y", "max_speed_y", "image"])
Field = struct("Field", ["width", "height", "ball", "paddle"])
Game = struct("Game", ["field", "screen"])
