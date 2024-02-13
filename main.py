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
if __name__ == "__main__":
    # main program

    # init arm
    my_arm = learm.LeArm()
    time.sleep(1)

    # move to picture position
    picture = [1500, 742, 799, 1228, 500]
    my_arm.moveToPosition(picture)

    # take picture
    cam = cv2.VideoCapture(0)
    result, img = cam.read()
    if result:
        cv2.imwrite('img/maze_pic.jpg', img)
    # wait and ensure picture was taken
    time.sleep(10)

    # create maze solver
    maze_solver = maze.maze_solver()


    # define paths
    paths = maze_solver.define_maze('img/maze_pic.jpg', x0=275, y0=363, x1=565, y1=232)
    print(paths[0])
    print(paths[1])

    # get directions
    directions = find_directions(paths)
    print(directions)
    time.sleep(5)

    w_ready = [1500, 665, 519, 1305, 2500]
    w_press = [1500, 665, 519, 1450, 2500]

    a_ready = [1500, 626, 519, 1305, 2403]
    a_press = [1500, 626, 519, 1450, 2403]

    s_ready = [1500, 723, 519, 1305, 2433]
    s_press = [1500, 723, 519, 1450, 2433]

    d_ready = [1500, 723, 646, 1403, 2422]
    d_press = [1500, 723, 646, 1530, 2422]

    # get ready to feed keyboard inputs
    my_arm.closeClaw(True)
    my_arm.moveToPosition(w_ready, wait=True)


    for direction in directions:
        if direction[0] == 'd':
            my_arm.moveToPosition(d_ready)
            time.sleep(1)
            my_arm.moveToPosition(d_press)
            time.sleep(max(1, 0.1 * direction[1]))
        if direction[0] == 'w':
            my_arm.moveToPosition(w_ready)
            time.sleep(1)
            my_arm.moveToPosition(w_press)
            time.sleep(max(1, 0.1 * direction[1]))
        if direction[0] == 's':
            my_arm.moveToPosition(s_ready)
            time.sleep(1)
            my_arm.moveToPosition(s_press)
            time.sleep(max(1, 0.1 * direction[1]))
        if direction[0] == 'a':
            my_arm.moveToPosition(a_ready)
            time.sleep(1)
            my_arm.moveToPosition(a_press)
            time.sleep(max(1, 0.1 * direction[1]))
    # show image with paths
    rgb_img = plt.imread('img/maze_pic.jpg')
    plt.figure(figsize=(14, 14))
    plt.imshow(rgb_img)
    plt.plot(paths[0], paths[1], 'r-', linewidth=5)
    plt.show()