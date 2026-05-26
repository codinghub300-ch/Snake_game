# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:59:52 2023

@author: Ammar
"""

import turtle
import time
import random
import threading
import sys
import pygame

try:
    import pygame
except ImportError:
    print("Installing pygame for sound...")
    import os
    os.system(f"{sys.executable} -m pip install pygame")
    import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Sounds
eat_sound = "eating.mp3"  
crash_sound = "crash.mp3"  
bg_music = "background.mp3"  

# Constants
delay = 0.08
score = 0
high_score = 0
paused = False
game_started = False
timer_mode = False
timer_seconds = 60
difficulty_selected = False

# Rainbow colors
colors = ["cyan", "magenta", "orange", "light green", "yellow", "pink", "light blue"]

# Set up the screen
window = turtle.Screen()
window.title("Snake Game by Ammar")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Snake body
segments = []

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)

# Start message
start_message = turtle.Turtle()
start_message.speed(0)
start_message.color("white")
start_message.penup()
start_message.hideturtle()
start_message.goto(0, 0)
start_message.write("Press 1 (Easy), 2 (Normal), 3 (Hard)", align="center", font=("Courier", 20, "bold"))

# Timer Display
timer_display = turtle.Turtle()
timer_display.speed(0)
timer_display.color("white")
timer_display.penup()
timer_display.hideturtle()
timer_display.goto(0, 220)

# Functions
def play_sound(sound_file):
    threading.Thread(target=lambda: pygame.mixer.Sound(sound_file).play()).start()

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)

def update_score():
    scoreboard.clear()
    scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

def update_timer():
    if timer_mode and game_started and not paused:
        global timer_seconds
        timer_seconds -= 1
        timer_display.clear()
        timer_display.write(f"Time: {timer_seconds}s", align="center", font=("Courier", 20, "normal"))
        if timer_seconds <= 0:
            reset_game()
        window.ontimer(update_timer, 1000)

def move():
    if head.direction == "Up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "Down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "Left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "Right":
        x = head.xcor()
        head.setx(x + 20)

def go_up():
    if head.direction != "Down":
        head.direction = "Up"

def go_down():
    if head.direction != "Up":
        head.direction = "Down"

def go_left():
    if head.direction != "Right":
        head.direction = "Left"

def go_right():
    if head.direction != "Left":
        head.direction = "Right"

def toggle_pause():
    global paused
    if not game_started:
        return
    paused = not paused
    if paused:
        scoreboard.goto(0, 0)
        scoreboard.write("Paused", align="center", font=("Courier", 24, "bold"))
    else:
        scoreboard.goto(0, 260)
        update_score()

def start_easy():
    global delay, game_started, difficulty_selected
    if not difficulty_selected:
        delay = 0.12
        start()
        
def start_normal():
    global delay, game_started, difficulty_selected
    if not difficulty_selected:
        delay = 0.08
        start()

def start_hard():
    global delay, game_started, difficulty_selected
    if not difficulty_selected:
        delay = 0.05
        start()

def start():
    global game_started, difficulty_selected
    start_message.clear()
    play_music(bg_music)
    game_started = True
    difficulty_selected = True
    update_score()
    update_timer()

def generate_food():
    x = random.randint(-14, 14) * 20
    y = random.randint(-14, 14) * 20
    food.goto(x, y)

def move_snake():
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

def extend_snake():
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color(random.choice(colors))
    new_segment.penup()
    segments.append(new_segment)

def check_collision():
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        return True
    for segment in segments:
        if segment.distance(head) < 20:
            return True
    return False

def reset_game():
    global score, timer_seconds
    play_sound(crash_sound)
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "Stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    timer_seconds = 60
    update_score()
    timer_display.clear()

def update_high_score():
    global high_score
    if score > high_score:
        high_score = score

# Keyboard bindings
window.listen()
window.onkeypress(go_up, "w")
window.onkeypress(go_down, "s")
window.onkeypress(go_left, "a")
window.onkeypress(go_right, "d")
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")
window.onkeypress(toggle_pause, "p")
window.onkeypress(start_easy, "1")
window.onkeypress(start_normal, "2")
window.onkeypress(start_hard, "3")

# Main game loop
while True:
    window.update()

    if game_started and not paused:
        if check_collision():
            update_high_score()
            reset_game()

        if head.distance(food) < 20:
            play_sound(eat_sound)
            generate_food()
            extend_snake()
            score += 10
            update_high_score()
            update_score()

        move_snake()

    time.sleep(delay)

window.mainloop()
