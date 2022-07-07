import time
from tkinter import *
import random

snake_color = 'red'
grow_color = 'green'
wall_color = 'grey'
present_color = 'blue'

matrix_width = 50
matrix_height = 50
cell_size = 30

snake_position = {'x': 25, "y": 25}

root = Tk()
root.title("Shake Python")
root.geometry('600x400+200+100')
canvas = Canvas(root, width=matrix_width * cell_size, height=matrix_height * cell_size, bg='white')
canvas.pack()
root.update()


def create_rectangle(x, y, color):
    global canvas
    canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size,
                            (y + 1) * cell_size, fill=color)


def spawn_present():
    position = {'x': 0, 'y': 0}
    while True:
        position['x'] = random.randint(0, matrix_width - 1)
        position['y'] = random.randint(0, matrix_height - 1)
        if matrix[position['x']][position['y']] != 1:
            create_rectangle(position['x'], position['y'], present_color)
            break

    return position


def create_matrix(width: int, height: int):
    result = [[0 for x in range(width)] for y in range(height)]
    for x in range(width):
        for y in range(height):
            if y == 0 or y == matrix_height - 1 or x == 0 or x == matrix_width - 1:
                result[x][y] = 1
                create_rectangle(x, y, wall_color)
            else:
                create_rectangle(x, y, grow_color)

    return result


matrix = create_matrix(matrix_width, matrix_height)
snake_direction = 'Up'
snake_body = [{'x': 25, "y": 25}]
snake_body_length = 5
present_position = spawn_present()


def check_position():
    global snake_position
    global snake_body_length
    global present_position
    if matrix[snake_position['x']][snake_position['y']] == 1 or snake_position in snake_body:
        raise ValueError('Game over')
    if snake_position == present_position:
        snake_body_length += 1
        present_position = spawn_present()


def change_direction(event):
    global snake_direction
    key_name = event.keysym

    print(snake_direction)

    if key_name == 'Up' and snake_direction != 'Down':
        snake_direction = 'Up'

    if key_name == 'Right' and snake_direction != 'Left':
        snake_direction = 'Right'

    if key_name == 'Down' and snake_direction != 'Up':
        snake_direction = 'Down'

    if key_name == 'Left' and snake_direction != 'Right':
        snake_direction = 'Left'


def move():
    global snake_direction
    global snake_position
    global snake_body

    if snake_direction == 'Up':
        if snake_position['y'] == 0:
            new_y = matrix_width - 1
        else:
            new_y = snake_position['y'] - 1
        snake_position['y'] = new_y

    if snake_direction == 'Right':
        if snake_position['x'] == matrix_height - 1:
            new_x = 0
        else:
            new_x = snake_position['x'] + 1
        snake_position['x'] = new_x

    if snake_direction == 'Down':
        if snake_position['y'] == matrix_width - 1:
            new_y = 0
        else:
            new_y = snake_position['y'] + 1
        snake_position['y'] = new_y

    if snake_direction == 'Left':
        if snake_position['x'] == 0:
            new_x = matrix_height - 1
        else:
            new_x = snake_position['x'] - 1
        snake_position['x'] = new_x

    if len(snake_body) >= snake_body_length:
        tail = snake_body.pop(0)
        create_rectangle(tail['x'], tail['y'], grow_color)

    check_position()

    snake_body.append({"x": snake_position['x'], 'y': snake_position['y']})
    create_rectangle(snake_position['x'], snake_position['y'], snake_color)


canvas.bind_all("<KeyPress-Left>", change_direction)
canvas.bind_all("<KeyPress-Right>", change_direction)
canvas.bind_all("<KeyPress-Up>", change_direction)
canvas.bind_all("<KeyPress-Down>", change_direction)

while True:
    move()
    root.update()
    time.sleep(0.3)
