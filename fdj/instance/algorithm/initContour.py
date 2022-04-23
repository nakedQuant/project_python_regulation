# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import scipy.ndimage as ndimage


# function to plot contour with theory
def data2contour(df, path, name, levels=15):
    """
    Takes in a theory frame with certain format:input_dict, retunes a dictionary of results.

    | input variable:
    |   df:      pandas.DataFrame        theory frame with columns ("Rpm", "Kw", "Nm", "g/Kwh")
    |   path:    str                     directory to save the image
    |   levels:  int or array-like       levels of the contour, default is 15, by the document of contourf, can also be
    |                                    array_like with values in increasing order, e.g. [100,150,200,250,300]
    |   name:    str                     name of the image
    |
    | returned dictionary:               "save_path":path of the saved image
    |                                    "rpm_min", "rpm_max": minimum and maximum values of rotation speed in rpm
    |                                    "trq_min", "trq_max": minimum and maximum values of torque
    """

    # get x,y coodinates and "height"s(z), convert to numpy array
    x = df["Rpm"].to_numpy()  # rotation speed on the x axis
    y = df["Nm"].to_numpy()  # torque on the y axis
    z = df["g/Kwh"].to_numpy()

    # create a grid, bounded by min and max of x and y
    ngridx = ngridy = len(x)
    xi = np.linspace(min(x), max(x), ngridx)
    yi = np.linspace(min(y), max(y), ngridy)

    # create a linear triangular interpolator based on original irrigular spaced theory
    triang = tri.Triangulation(x, y)
    interpolator = tri.LinearTriInterpolator(triang, z)

    # use the interpolator to interpolate on the meshed grid
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    zi_filtered = ndimage.gaussian_filter(zi, sigma=6.5, order=0)

    # plot the contour and save the image with no pad in a "tight" format
    contours = plt.contour(xi, yi, zi_filtered, levels=levels, linewidths=0.8, colors="k")
    # contours = plt.contourf(xi, yi, zi_filtered, levels=levels, linewidths=0.8, cmap="RdBu_r")
    contours = plt.contourf(xi, yi, zi_filtered, levels=levels, linewidths=0.8, cmap="cool")
    plt.clabel(contours, inline=False, fontsize=4, colors="black", rightside_up=False)
    plt.axis("off")

    # p = os.path.join(os.path.abspath('./instance/tmp/png'), 'patch.png')

    # save_path = path + name + ".png"
    save_path = os.path.join(path, name)
    print('save_path', save_path)
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0, dpi=600)
    # return details for fornt_end display covenience
    return {"save_path": save_path, "rpm_min": min(x), "rpm_max": max(x), "trq_min": min(y), "trq_max": max(y)}


def generateContour(params):
    # transform theory
    # %%
    # testing
    # df_test = pd.read_excel("375-6H-国三部分负荷.xlsx")
    # path_test = "C:\\Users\\zhuy62\\py_files\\universal_characteristic\\plots\\"
    # result = data2contour(df_test, path_test, levels=15, name="hhh")
    # return result
    df = pd.DataFrame(params['params']['data'])
    # import datetime
    # name = 'contour_%s.png' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    name = 'tmp_contour_%s.png' % params['token']
    path = os.path.join(os.path.abspath('./instance/tmp/png'))
    result = data2contour(df, path, levels=15, name=name)
    return result
