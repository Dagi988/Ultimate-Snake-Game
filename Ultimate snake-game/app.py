import turtle
import random

# ============================================================
# 🐍 SNAKE GAME — SINGLE FILE EDITION
# ============================================================

# ---------------- CONFIG ----------------

WIDTH = 700
HEIGHT = 700
GAME_SIZE = 600
CELL_SIZE = 20

DIFFICULTIES = {
    "Easy": 130,
    "Normal": 95,
    "Hard": 65,
    "Insane": 45
}

# ---------------- GAME STATE ----------------

score = 0
high_score = 0
level = 1

difficulty = "Normal"
game_delay = DIFFICULTIES[difficulty]

direction = "stop"
next_direction = "stop"

game_running = False
paused = False

food_type = "normal"
special_food_timer = 0

segments = []


# ============================================================
# SCREEN
# ============================================================

screen = turtle.Screen()
screen.title("🐍 Snake — Python Edition")
screen.bgcolor("#080c12")
screen.setup(WIDTH, HEIGHT)
screen.tracer(0)


# ============================================================
# HELPER
# ============================================================

def create_pen():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.penup()
    pen.hideturtle()
    return pen


# ============================================================
# BACKGROUND
# ============================================================

background = create_pen()


def draw_background():

    background.clear()

    # Grid
    background.color("#121923")
    background.pensize(1)

    for x in range(-300, 301, CELL_SIZE):

        background.goto(x, -300)
        background.pendown()

        background.goto(x, 300)

        background.penup()

    for y in range(-300, 301, CELL_SIZE):

        background.goto(-300, y)
        background.pendown()

        background.goto(300, y)

        background.penup()

    # Border
    background.color("#405060")
    background.pensize(3)

    background.goto(-300, -300)
    background.pendown()

    for _ in range(4):

        background.forward(600)
        background.left(90)

    background.penup()


draw_background()


# ============================================================
# UI
# ============================================================

ui = create_pen()


def draw_ui():

    ui.clear()

    # Title
    ui.color("#ffffff")

    ui.goto(0, 325)

    ui.write(
        "SNAKE",
        align="center",
        font=("Arial", 28, "bold")
    )

    # Score
    ui.goto(-290, 285)

    ui.write(
        f"Score: {score}",
        align="left",
        font=("Arial", 14, "bold")
    )

    # Level
    ui.goto(0, 285)

    ui.write(
        f"Level: {level}",
        align="center",
        font=("Arial", 14, "bold")
    )

    # High score
    ui.goto(290, 285)

    ui.write(
        f"Best: {high_score}",
        align="right",
        font=("Arial", 14, "bold")
    )

    # Difficulty
    ui.goto(0, -330)

    ui.color("#8492a1")

    ui.write(
        f"{difficulty}  •  WASD / Arrow Keys  •  P Pause  •  R Restart  •  ESC Menu",
        align="center",
        font=("Arial", 10, "normal")
    )


# ============================================================
# MENU
# ============================================================

menu = create_pen()


def show_menu():

    global game_running
    global paused

    game_running = False
    paused = False

    menu.clear()
    ui.clear()

    menu.color("#ffffff")

    menu.goto(0, 170)

    menu.write(
        "🐍 SNAKE",
        align="center",
        font=("Arial", 44, "bold")
    )

    menu.goto(0, 110)

    menu.color("#6ee56b")

    menu.write(
        "PYTHON EDITION",
        align="center",
        font=("Arial", 15, "bold")
    )

    menu.goto(0, 35)

    menu.color("#ffffff")

    menu.write(
        "PRESS ENTER TO START",
        align="center",
        font=("Arial", 19, "bold")
    )

    menu.goto(0, -20)

    menu.color("#aab4bf")

    menu.write(
        "Press D to change difficulty",
        align="center",
        font=("Arial", 13, "normal")
    )

    menu.goto(0, -70)

    menu.color("#ffffff")

    menu.write(
        f"Difficulty: {difficulty}",
        align="center",
        font=("Arial", 16, "bold")
    )

    menu.goto(0, -125)

    menu.color("#ffd84d")

    menu.write(
        f"🏆 High Score: {high_score}",
        align="center",
        font=("Arial", 15, "bold")
    )

    menu.goto(0, -190)

    menu.color("#697583")

    menu.write(
        "WASD / Arrow Keys to move",
        align="center",
        font=("Arial", 11, "normal")
    )

    screen.update()


def change_difficulty():

    global difficulty
    global game_delay

    names = list(DIFFICULTIES.keys())

    current = names.index(difficulty)

    current += 1

    if current >= len(names):
        current = 0

    difficulty = names[current]

    game_delay = DIFFICULTIES[difficulty]

    show_menu()


# ============================================================
# SNAKE HEAD
# ============================================================

head = turtle.Turtle()

head.speed(0)
head.shape("square")
head.color("#6ee56b")
head.penup()
head.goto(0, 0)
head.hideturtle()


# ============================================================
# FOOD
# ============================================================

food = turtle.Turtle()

food.speed(0)
food.shape("circle")
food.color("#ff4655")
food.penup()
food.hideturtle()


def place_food():

    global food_type
    global special_food_timer

    # 15% chance of special food
    if random.random() < 0.15:

        food_type = "special"
        special_food_timer = 80

        food.color("#ffd84d")
        food.shapesize(1.25)

    else:

        food_type = "normal"
        special_food_timer = 0

        food.color("#ff4655")
        food.shapesize(1)

    while True:

        x = random.randrange(-280, 281, CELL_SIZE)
        y = random.randrange(-280, 281, CELL_SIZE)

        valid = True

        # Don't spawn on head
        if head.distance(x, y) < 40:
            valid = False

        # Don't spawn inside body
        for segment in segments:

            if segment.distance(x, y) < 20:

                valid = False
                break

        if valid:

            food.goto(x, y)
            break


# ============================================================
# MOVEMENT
# ============================================================

def go_up():

    global next_direction

    if direction != "down":
        next_direction = "up"


def go_down():

    global next_direction

    if direction != "up":
        next_direction = "down"


def go_left():

    global next_direction

    if direction != "right":
        next_direction = "left"


def go_right():

    global next_direction

    if direction != "left":
        next_direction = "right"


# ============================================================
# CREATE BODY
# ============================================================

def create_segment():

    segment = turtle.Turtle()

    segment.speed(0)
    segment.shape("square")
    segment.color("#36c95b")
    segment.penup()
    segment.hideturtle()

    return segment


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global score
    global level
    global direction
    global next_direction
    global game_delay
    global special_food_timer

    score = 0
    level = 1

    direction = "stop"
    next_direction = "stop"

    game_delay = DIFFICULTIES[difficulty]

    special_food_timer = 0

    head.goto(0, 0)

    for segment in segments:

        segment.hideturtle()

    segments.clear()

    place_food()

    head.showturtle()
    food.showturtle()

    draw_ui()

    screen.update()


# ============================================================
# START GAME
# ============================================================

def start_game():

    global game_running
    global paused

    menu.clear()

    reset_game()

    game_running = True
    paused = False

    draw_ui()

    screen.update()

    game_loop()


# ============================================================
# LEVEL SYSTEM
# ============================================================

def update_level():

    global level
    global game_delay

    new_level = min(10, (score // 5) + 1)

    if new_level != level:

        level = new_level

        base_speed = DIFFICULTIES[difficulty]

        game_delay = max(
            25,
            base_speed - ((level - 1) * 7)
        )


# ============================================================
# WALL COLLISION
# ============================================================

def hit_wall():

    return (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    )


# ============================================================
# SELF COLLISION
# ============================================================

def hit_self():

    for segment in segments:

        if segment.distance(head) < 15:

            return True

    return False


# ============================================================
# GAME OVER
# ============================================================

def game_over():

    global game_running
    global paused

    game_running = False
    paused = False

    overlay = create_pen()

    overlay.color("#ff4655")

    overlay.goto(0, 100)

    overlay.write(
        "GAME OVER",
        align="center",
        font=("Arial", 38, "bold")
    )

    overlay.goto(0, 45)

    overlay.color("#ffffff")

    overlay.write(
        f"Score: {score}",
        align="center",
        font=("Arial", 20, "bold")
    )

    overlay.goto(0, 5)

    overlay.color("#ffd84d")

    overlay.write(
        f"Best: {high_score}",
        align="center",
        font=("Arial", 17, "bold")
    )

    overlay.goto(0, -55)

    overlay.color("#6ee56b")

    overlay.write(
        "Press R to restart",
        align="center",
        font=("Arial", 15, "bold")
    )

    overlay.goto(0, -95)

    overlay.color("#9ba7b3")

    overlay.write(
        "Press ESC for menu",
        align="center",
        font=("Arial", 12, "normal")
    )

    screen.game_over_overlay = overlay

    screen.update()


# ============================================================
# PAUSE
# ============================================================

def toggle_pause():

    global paused

    if not game_running:
        return

    paused = not paused

    if paused:

        pause = create_pen()

        pause.color("#ffffff")

        pause.goto(0, 50)

        pause.write(
            "PAUSED",
            align="center",
            font=("Arial", 36, "bold")
        )

        pause.goto(0, -5)

        pause.color("#9ba7b3")

        pause.write(
            "Press P to continue",
            align="center",
            font=("Arial", 15, "normal")
        )

        screen.pause_overlay = pause

    else:

        if hasattr(screen, "pause_overlay"):

            screen.pause_overlay.clear()

    screen.update()


# ============================================================
# RESTART
# ============================================================

def restart_game():

    if not game_running:

        if hasattr(screen, "game_over_overlay"):

            screen.game_over_overlay.clear()

        start_game()

    else:

        reset_game()


# ============================================================
# RETURN TO MENU
# ============================================================

def back_to_menu():

    global game_running
    global paused
    global direction
    global next_direction

    game_running = False
    paused = False

    direction = "stop"
    next_direction = "stop"

    for segment in segments:

        segment.hideturtle()

    head.hideturtle()
    food.hideturtle()

    if hasattr(screen, "pause_overlay"):

        screen.pause_overlay.clear()

    if hasattr(screen, "game_over_overlay"):

        screen.game_over_overlay.clear()

    show_menu()


# ============================================================
# MAIN GAME LOOP
# ============================================================

def game_loop():

    global direction
    global next_direction
    global score
    global high_score
    global special_food_timer
    global food_type

    if not game_running:

        return

    # Pause
    if paused:

        screen.ontimer(game_loop, 100)

        return

    # Apply direction
    direction = next_direction

    # Move body backwards
    for index in range(
        len(segments) - 1,
        0,
        -1
    ):

        segments[index].goto(
            segments[index - 1].xcor(),
            segments[index - 1].ycor()
        )

    # First body segment follows head
    if segments:

        segments[0].goto(
            head.xcor(),
            head.ycor()
        )

    # Move head
    if direction == "up":

        head.sety(
            head.ycor() + CELL_SIZE
        )

    elif direction == "down":

        head.sety(
            head.ycor() - CELL_SIZE
        )

    elif direction == "left":

        head.setx(
            head.xcor() - CELL_SIZE
        )

    elif direction == "right":

        head.setx(
            head.xcor() + CELL_SIZE
        )

    # Wall collision
    if hit_wall():

        game_over()

        return

    # Self collision
    if hit_self():

        game_over()

        return

    # Food collision
    if head.distance(food) < 18:

        if food_type == "special":

            score += 3

        else:

            score += 1

        # High score
        if score > high_score:

            high_score = score

        # New body segment
        new_segment = create_segment()

        if segments:

            new_segment.goto(
                segments[-1].position()
            )

        else:

            new_segment.goto(
                head.position()
            )

        new_segment.showturtle()

        segments.append(new_segment)

        update_level()

        place_food()

        draw_ui()

    # Special food timer
    if special_food_timer > 0:

        special_food_timer -= 1

        if special_food_timer <= 0:

            place_food()

    screen.update()

    screen.ontimer(
        game_loop,
        game_delay
    )


# ============================================================
# KEYBOARD
# ============================================================

screen.listen()

# WASD
screen.onkeypress(go_up, "w")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_right, "d")

# Arrow keys
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# Controls
screen.onkeypress(start_game, "Return")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(restart_game, "r")
screen.onkeypress(back_to_menu, "Escape")

# Difficulty
screen.onkeypress(change_difficulty, "d")


# ============================================================
# START
# ============================================================

show_menu()

screen.mainloop()
