import learm
import time
import cv2
import maze
import matplotlib.pylab as plt


def find_directions(plot):
    """
    translates directions into wasd inputs
    :param plot: array of arrays that have the paths
    :return: array of wasd characters
    """
    directions = []
    direction_count = 0

    prev_x = plot[0][0]
    prev_y = plot[1][0]

    # handle the initial direction
    if plot[1][1] > prev_y:
        current_direction = 'w'
    elif plot[1][1] < prev_y:
        current_direction = 's'
    else:
        current_direction = 'x'  # placeholder for no direction

    if plot[0][1] > prev_x:
        current_direction = 'd'
    elif plot[0][1] < prev_x:
        current_direction = 'a'

    direction_count += 1

    for x, y in zip(plot[0][1:], plot[1][1:]):
        # determine direction along y-axis
        if y > prev_y:
            y_dir = 's'
        elif y < prev_y:
            y_dir = 'w'
        else:
            y_dir = ''

        # determine direction along x-axis
        if x > prev_x:
            x_dir = 'd'
        elif x < prev_x:
            x_dir = 'a'
        else:
            x_dir = ''

        # combine directions
        direction = y_dir if y_dir else x_dir

        # check if the direction has changed or not
        if direction != current_direction:
            directions.append((current_direction, direction_count))
            current_direction = direction
            direction_count = 1
        else:
            direction_count += 1

        prev_x = x
        prev_y = y

    # append the last direction count
    directions.append((current_direction, direction_count))

    return directions


def moveLaser(my_arm, paths, start, x0, y0, step_size_up=1.0, step_size_down=1.0, step_size_h=1.0):
    """
    moves the arm according to img path
    :param my_arm: arm object
    :param paths: path array
    :param start: start pos
    :param x0: original img start
    :param y0: original img start
    :param step_size_up: step size for moving up
    :param step_size_down: step size for moving down
    :param step_size_h: step size for horizontal movement
    :return: none
    """
    current_servo_pos = start
    current_laser_pos = [x0, y0]

    directions = find_directions(paths)
    print(directions)
    for direction in directions:

        if direction[0] == 'w':
            current_servo_pos[1] = int(current_servo_pos[1] + (step_size_up * direction[1]))
            current_laser_pos[1] = current_laser_pos[1] + direction[1]
        elif direction[0] == 's':
            current_servo_pos[1] = int(current_servo_pos[1] - (step_size_down * direction[1]))
            current_laser_pos[1] = current_laser_pos[1] - direction[1]
        elif direction[0] == 'd':
            current_servo_pos[4] = int(current_servo_pos[4] - (step_size_h * direction[1]))
            current_laser_pos[0] = current_laser_pos[0] + direction[1]
        elif direction[0] == 'a':
            current_servo_pos[4] = int(current_servo_pos[4] + (step_size_h * direction[1]))
            current_laser_pos[0] = current_laser_pos[0] - direction[1]
        my_arm.moveToPosition(current_servo_pos)
        time.sleep(1)


if __name__ == "__main__":
    # main program

    start = [1500, 630, 937, 1112, 1441]

    x0 = 133
    y0 = 432
    x1 = 412
    y1 = 287
    # init arm
    my_arm = learm.LeArm()
    time.sleep(1)

    # move to picture position
    picture = [1500, 500, 799, 1000, 1500]
    my_arm.moveToPosition(picture)

    # take picture
    cam = cv2.VideoCapture(0)
    result, img = cam.read()
    if result:
        cv2.imwrite('../img/maze_pic.jpg', img)
    # wait and ensure picture was taken
    time.sleep(2)

    # create maze solver
    maze_solver = maze.maze_solver()

    # define paths
    paths = maze_solver.define_maze('img/maze_pic.jpg', x0=x0, y0=y0, x1=x1, y1=y1)
    print(paths[0])
    print(paths[1])

    my_arm.moveToPosition(start)
    time.sleep(1)
    moveLaser(my_arm, paths, start, x0, y0, step_size_up=0.65, step_size_down=0.8, step_size_h=0.83)
    # show image with paths
    rgb_img = plt.imread('../img/maze_pic.jpg')
    plt.figure(figsize=(14, 14))
    plt.imshow(rgb_img)
    plt.plot(paths[0], paths[1], 'r-', linewidth=5)
    plt.show()
