import curses
import random

'''
Things to improve: 
1. add colors
2. change shapes
3. restructure code
4. change size of window
5. illegal control handling
'''


def main(stdscr):
    scr = curses.initscr()  # initialize new window
    curses.start_color() # enable color
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.curs_set(0)  # hide cursor
    height, width = scr.getmaxyx()  # get max screen height, width
    w = curses.newwin(height, width, 0, 0)  # set dimension of new window
    w.keypad(1)
    w.timeout(100)

    # initial position of the snake
    y = int(height/4)
    x = int(width/2)

    # print("x: {x} y: {y}".format(x=x, y=y))

    # create body parts
    # start with 3 segs
    snake = [
        [y, x],
        [y, x - 1],
        [y, x - 2]
    ]

    # initial position of food
    food = [int(height/2), int(width/2)]

    print("snake = {snake}".format(snake=snake))
    print("food = {food}".format(food=food))

    # add food to screen
    w.addch(food[0], food[1], curses.ACS_CKBOARD, curses.color_pair(1))

    key = curses.KEY_RIGHT

    # infinite loop to move the snake around till it fails
    while True:
        next_key = w.getch()
        # update key if next_key exists
        key = key if next_key == -1 else next_key

        # check if game is lost
        if snake[0][0] in [0, height] or snake[0][1] in [0, width] or snake[0] in snake[1:]:
            curses.endwin()
            quit()

        # new position of head
        new_head = [snake[0][0], snake[0][1]]

        # move new_head according to the directions
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # if food is eaten
        if snake[0] == food:
            food = None
            # food got eaten, need to display new food
            while food is None:
                new_food = [
                    random.randint(1, height - 1),
                    random.randint(1, width - 1)
                ]
                # check to make sure food isn't in snake
                food = new_food if new_food not in snake else None
            print("new food = {food}", food)
            w.addch(food[0], food[1], curses.ACS_CKBOARD, curses.color_pair(1))
        else:
            # move snake
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD, curses.color_pair(2))

curses.wrapper(main)