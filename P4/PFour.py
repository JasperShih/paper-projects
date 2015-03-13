# -*- coding: utf8 -*-
__author__ = 'Jasper'

import math
import copy
import random
import scipy.misc as misc
import os
import cPickle as Pickle
import xlsxwriter


class Embed():
    def __init__(self, image, threshold, t_star):
        self.image = image
        self.threshold = threshold
        self.t_star = t_star

    def get_four_adjacent_pixels(self, row, col):
        # Top, left, right, bot
        return [
            self.image[row - 1][col] if row - 1 >= 0 else None,
            self.image[row][col - 1] if col - 1 >= 0 else None,
            self.image[row][col + 1] if col + 1 < len(self.image[0]) else None,
            self.image[row + 1][col] if row + 1 < len(self.image) else None
        ]

    def hide(self):
        # Throughout_image_by_chessboard
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                print self.get_four_adjacent_pixels(row, col)


def main(image, threshold, t_star):
    # 1020 is max THRESHOLD, -1 TODO
    img_misc = misc.imread(image)
    img = img_misc.tolist()

    embed_obj = Embed(img, threshold, t_star)
    embed_obj.hide()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\image\\invest.bmp",
         50, 2)











