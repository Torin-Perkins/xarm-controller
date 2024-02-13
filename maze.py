import matplotlib.pylab as plt
from skimage.morphology import skeletonize
import numpy as np

"""
-------------------------
Author: Torin Perkins
-------------------------
Gives path that solves a maze
Tutorial: https://www.youtube.com/watch?v=1KHgCRs-x1M&t=2550s&ab_channel=Odlogo
"""


class maze_solver:
    def define_maze(self, img_name, x0=0, y0=0, x1=600, y1=600):
        # show original image with points plotted
        rgb_img = plt.imread(img_name)

        plt.figure(figsize=(14, 14))
        plt.imshow(rgb_img)
        plt.plot(x0, y0, 'gx', markersize=14)
        plt.plot(x1, y1, 'rx', markersize=14)
        plt.show()

        # threshold image
        thr_img = rgb_img[:, :, 0] > 128
        # skeletonize
        skeleton = skeletonize(thr_img)

        # map routes
        mapT = ~skeleton
        plt.imshow(mapT)
        plt.plot(x0, y0, 'gx', markersize=14)
        plt.plot(x1, y1, 'rx', markersize=14)
        plt.show()
        _mapt = np.copy(mapT)

        # searching for end point and connect to path
        boxr = 30
        cpys, cpxs = np.where(_mapt[y1 - boxr:y1 + boxr, x1 - boxr:x1 + boxr] == 0)
        # calibrate points to main scale
        cpys += y1 - boxr
        cpxs += x1 - boxr

        # find the closest point of possible path
        idx = np.argmin(np.sqrt((cpys - y1) ** 2 + (cpxs - x1) ** 2))
        y, x = cpys[idx], cpxs[idx]
        plt.plot(x, y, 'ro')

        pts_x = [x]
        pts_y = [y]
        pts_c = [0]

        # mesh of displacements
        xmesh, ymesh = np.meshgrid(np.arange(-1, 2), np.arange(-1, 2))
        xmesh = xmesh.reshape(-1)
        ymesh = ymesh.reshape(-1)

        dst = np.zeros(thr_img.shape)

        # breadth first search
        while True:
            # update distance
            idc = np.argmin(pts_c)
            ct = pts_c.pop(idc)
            x = pts_x.pop(idc)
            y = pts_y.pop(idc)
            # search 3x3 neighborhood
            ys, xs = np.where(_mapt[y - 1:y + 2, x - 1:x + 2] == 0)
            # invalidate points from future search
            _mapt[ys + y - 1, xs + x - 1] = ct  # ct?
            _mapt[y, x] = 999999

            # set distance in dst image
            dst[ys + y - 1, xs + x - 1] = ct + 1  # ct?

            pts_x.extend(xs + x - 1)
            pts_y.extend(ys + y - 1)
            pts_c.extend([ct + 1] * xs.shape[0])

            # run out of points
            if not pts_x:
                break
            if np.sqrt((x - x0) ** 2 + (y - y0) ** 2) < boxr:
                edx = x
                edy = y
                break

        path_x = []
        path_y = []

        y = edy
        x = edx

        while True:
            nbh = dst[y - 1:y + 2, x - 1:x + 2]
            nbh[1, 1] = 999999
            nbh[nbh == 0] = 999999

            # deadend
            if np.min(nbh) == 999999:
                break
            idx = np.argmin(nbh)
            # find direction

            y += ymesh[idx]
            x += xmesh[idx]

            if np.sqrt((x - x1) ** 2 + (y - y1) ** 2) < boxr:
                print("Route found")
                break
            path_y.append(y)
            path_x.append(x)

            # path_y.append(y1)
            # path_x.append(x1)

        # plt.figure(figsize=(14, 14))
        # plt.imshow(rgb_img)
        # plt.plot(path_x, path_y, 'r-', linewidth=5)
        return [path_x, path_y]
if __name__ == "__main__":
    ms = maze_solver()
    x0 = 133
    y0 = 432
    x1 = 412
    y1 = 287
    paths = ms.define_maze('img/maze_pic.jpg', x0=x0, y0=y0, x1=x1, y1=y1)

