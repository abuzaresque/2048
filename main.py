import pygame as pg
import random

x_offset = 20
y_offset = 20
block_array = []
possible_keys = [pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT]
score = 0


class block:
    def __init__(self, x, y):
        self.number = 0
        self.x, self.y = x, y
        self.pixel_coordinates = (x_offset + x * 95, y_offset + y * 95)
        self.index = 0
        self.picture = ''
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.merged = False

    def update_pixel_coordinates(self, pixel_x, pixel_y):
        self.pixel_coordinates = pixel_x, pixel_y


BG_COLOR = pg.Color(255, 255, 255)


def invalid_coordinates(x, y):
    for i in block_array:
        if i != None:
            if i.x == x and i.y == y:
                return 1
    return 0


def new_block_generator():
    if len(block_array) != 16:
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        while invalid_coordinates(x, y):
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        print(x, y)

        new_block = block(x, y)
        new_block.number = 2 if random.randint(1, 10) > 1 else 4
        new_block.picture = pg.image.load(f'Media\{new_block.number}.png')
        block_array.append(new_block)


def find_block(x, y):
    for i in range(len(block_array)):
        if block_array[i] != None:
            if block_array[i].x == x and block_array[i].y == y:
                return i
    return None


def update_blocks():
    for i in range(len(block_array)):
        if block_array[i] == None:
            continue
        x = block_array[i].x
        y = block_array[i].y

        # setting lefts
        if x == 0:
            block_array[i].left = -1
        else:
            block_array[i].left = find_block(x-1, y)

        # setting rights
        if x == 3:
            block_array[i].right = -1
        else:
            block_array[i].right = find_block(x+1, y)

        # setting ups
        if y == 0:
            block_array[i].up = -1
        else:
            block_array[i].up = find_block(x, y-1)

        # setting downs
        if y == 3:
            block_array[i].down = -1
        else:
            block_array[i].down = find_block(x, y+1)


def print_():
    for i in range(len(block_array)):
        try:
            print("block index:", i, end=' ')
            print("x =", block_array[i].x, end=' ')
            print("y =", block_array[i].y, end='==>>')
            print("n =", block_array[i].number, end=' ')
            print("co", block_array[i].pixel_coordinates, end='==>>')
            print("right:", block_array[i].right, end=' ')
            print("left:", block_array[i].left, end=' ')
            print("up:", block_array[i].up, end=' ')
            print("down:", block_array[i].down, end='\n\n')
        except:
            pass


def right_shift():
    n = 1  # number of blocks shifted
    while n != 0:
        n = 0
        for i in range(len(block_array)):
            temp = block_array[i].right
            cond1 = (temp != None and temp != -
                     1) and (block_array[i].number == block_array[temp].number)
            cond2 = (temp != None and temp != -
                     1) and (block_array[temp].merged == False and block_array[i].merged == False)
            cond3 = cond1 and cond2

            cond4 = (temp == None)
            cond5 = ((temp != None and temp != -1) and
                     (block_array[temp].right != None and block_array[temp].right != -1) and
                     (block_array[block_array[temp].right].number == block_array[i].number))

            if cond5:
                continue

            if (cond3) or cond4:
                y = block_array[i].y
                x = block_array[i].x
                animate(i, (block_array[i].x, block_array[i].y), 'r')
                block_array[i].x += 1

                x = block_array[i].x
                if x == 3:
                    block_array[i].right = -1

                else:
                    block_array[i].right = find_block(x + 1, y)
                n += 1

            if cond3 and not cond5:
                block_array[temp].merged = True
                block_array[i].merged = True
                merge_blocks.append([i, temp])


def left_shift():
    n = 1  # number of blocks shifted
    while n != 0:
        n = 0
        for i in range(len(block_array)):
            temp = block_array[i].left
            cond1 = (temp != None and temp != -
                     1) and (block_array[i].number == block_array[temp].number)
            cond2 = (temp != None and temp != -
                     1) and (block_array[temp].merged == False and block_array[i].merged == False)
            cond3 = cond1 and cond2
            cond4 = (temp == None)

            cond5 = ((temp != None and temp != -1) and
                     (block_array[temp].left != None and block_array[temp].left != -1) and
                     (block_array[block_array[temp].left].number == block_array[i].number))

            if cond5:
                continue

            if (cond3) or cond4:
                y = block_array[i].y
                x = block_array[i].x
                animate(i, (block_array[i].x, block_array[i].y), 'l')
                block_array[i].x -= 1

                x = block_array[i].x
                if x == 0:
                    block_array[i].left = -1

                else:
                    block_array[i].left = find_block(x - 1, y)
                n += 1

            if cond3 and not cond5:
                block_array[temp].merged = True
                block_array[i].merged = True
                merge_blocks.append([i, temp])


def up_shift():
    n = 1  # number of blocks shifted
    while n != 0:
        n = 0
        for i in range(len(block_array)):
            temp = block_array[i].up
            cond1 = (temp != None and temp != -
                     1) and (block_array[i].number == block_array[temp].number)
            cond2 = (temp != None and temp != -
                     1) and (block_array[temp].merged == False and block_array[i].merged == False)
            cond3 = cond1 and cond2

            cond4 = (temp == None)
            cond5 = ((temp != None and temp != -1) and
                     (block_array[temp].up != None and block_array[temp].up != -1) and
                     (block_array[block_array[temp].up].number == block_array[i].number))

            if cond5:
                continue

            if (cond3) or cond4:
                y = block_array[i].y
                x = block_array[i].x
                animate(i, (block_array[i].x, block_array[i].y), 'u')
                block_array[i].y -= 1

                y = block_array[i].y
                if y == 0:
                    block_array[i].up = -1

                else:
                    block_array[i].up = find_block(x, y - 1)
                n += 1

            if cond3 and not cond5:
                block_array[temp].merged = True
                block_array[i].merged = True
                merge_blocks.append([i, temp])


def down_shift():
    n = 1  # number of blocks shifted
    while n != 0:
        n = 0
        for i in range(len(block_array)):
            temp = block_array[i].down
            cond1 = (temp != None and temp != -
                     1) and (block_array[i].number == block_array[temp].number)
            cond2 = (temp != None and temp != -
                     1) and (block_array[temp].merged == False and block_array[i].merged == False)
            cond3 = cond1 and cond2

            cond4 = (temp == None)
            cond5 = ((temp != None and temp != -1) and
                     (block_array[temp].down != None and block_array[temp].down != -1) and
                     (block_array[block_array[temp].down].number == block_array[i].number))

            if cond5:
                continue

            if (cond3) or cond4:
                y = block_array[i].y
                x = block_array[i].x
                animate(i, (block_array[i].x, block_array[i].y), 'd')
                block_array[i].y += 1

                y = block_array[i].y
                if y == 3:
                    block_array[i].down = -1

                else:
                    block_array[i].down = find_block(x, y+1)
                n += 1

            if cond3 and not cond5:
                block_array[temp].merged = True
                block_array[i].merged = True
                merge_blocks.append([i, temp])


speed = 2
tick = [1, 5, 19, 95][speed]


def animate(block_index, old_coordinates, direction):
    x, y = x_offset + old_coordinates[0] * \
        95, x_offset + old_coordinates[1] * 95
    block_array[block_index].update_pixel_coordinates(x, y)
    screen.blit(block_array[block_index].picture,
                block_array[block_index].pixel_coordinates)
    pg.display.update()
    for i in range(95//tick):
        if direction == 'r':
            x += tick
        elif direction == 'l':
            x -= tick
        elif direction == 'u':
            y -= tick
        elif direction == 'd':
            y += tick
        block_array[block_index].update_pixel_coordinates(x, y)
        screen.blit(block_array[block_index].picture,
                    block_array[block_index].pixel_coordinates)
        for i in range(len(block_array)):
            screen.blit(block_array[i].picture,
                        block_array[i].pixel_coordinates)
        pg.display.update()


def merge():
    global score
    for i in merge_blocks:
        block_array[i[0]].number *= 2
        # pg.mixer.music.play()
        score += block_array[i[0]].number
        block_array[i[0]].picture = pg.image.load(
            f'Media\{block_array[i[0]].number}.png')
        block_array[i[1]] = None

    for i in range(len(block_array)):
        if None in block_array:
            for i in range(block_array.count(None)):
                block_array.remove(None)

    for i in range(len(block_array)):
        if block_array[i] != None:
            screen.blit(block_array[i].picture,
                        block_array[i].pixel_coordinates)


def start():
    arr = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 2],
           [0, 4, 0, 0]]
    for i in range(4):
        for j in range(4):
            if arr[i][j] != 0:
                new_block = block(j, i)
                new_block.number = arr[i][j]
                new_block.picture = pg.image.load(f'Media\{new_block.number}.png')
                block_array.append(new_block)

    update_blocks()


# def grid_fill():
#     if len(block_array) != 16:
#         return True
#     for i in range(len(block_array)):
#         X = [block_array[block_array[i].right].number,block_array[block_array[i].left].number,
#         block_array[block_array[i].up].number,block_array[block_array[i].down].number]
#         if (block_array[i].number == block_array[block_array[i].right].number or
#             block_array[i].number == block_array[block_array[i].left].number or
#             block_array[i].number == block_array[block_array[i].up].number or
#                 block_array[i].number == block_array[block_array[i].down].number):
#             return True

#     return False


def right_possible():
    for i in range(len(block_array)):
        if block_array[i].right == None:
            return True
        if (block_array[i].number == block_array[block_array[i].right].number):
            return True

    return False


def left_possible():
    for i in range(len(block_array)):
        if block_array[i].left == None:
            return True
        if (block_array[i].number == block_array[block_array[i].left].number):
            return True

    return False


def up_possible():
    for i in range(len(block_array)):
        if block_array[i].up == None:
            return True
        if (block_array[i].number == block_array[block_array[i].up].number):
            return True

    return False


def down_possible():
    for i in range(len(block_array)):
        if block_array[i].down == None:
            return True
        if (block_array[i].number == block_array[block_array[i].down].number):
            return True

    return False


def main():
    global screen, merge_blocks, pop_sound
    merge_blocks = []
    start()
    screen = pg.display.set_mode((400, 400))
    clock = pg.time.Clock()

    grid_image = pg.image.load('Media\grid.png')
    screen.blit(grid_image, (0, 200))

    pg.mixer.init()

    # pg.mixer.music.load('pop_sound.mp3')

    running = True

    while running:

        screen.fill(BG_COLOR)
        screen.blit(grid_image, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key in possible_keys:
                r= right_possible()
                l= left_possible()
                u= up_possible()
                d= down_possible()

                if event.key == pg.K_RIGHT and r:
                    right_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    right_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    right_shift()

                if event.key == pg.K_LEFT and l:
                    left_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    left_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    left_shift()
                if event.key == pg.K_UP and u:
                    up_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    up_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    up_shift()
                if event.key == pg.K_DOWN and d:
                    down_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    down_shift()
                    merge()
                    update_blocks()
                    merge_blocks.clear()
                    down_shift()

                new_block_generator()
                update_blocks()
                if not(r or l or u or d):
                    pg.quit()
                print_()

        for i in range(len(block_array)):
            block_array[i].merged = False
            screen.blit(block_array[i].picture,
                        block_array[i].pixel_coordinates)
        pg.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('2048')
    pg.display.set_icon(pg.image.load('Media\icon.png'))
    main()
    pg.quit()
