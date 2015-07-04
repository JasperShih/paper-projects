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
    def __init__(self, image_path, threshold_left, threshold_right, capacity_given):
        self.image_path = image_path
        self.image_misc = misc.imread(image_path)
        self.image = self.image_misc.tolist()
        self.threshold_left = threshold_left
        self.threshold_right = threshold_right
        self.capacity_given = capacity_given

        # =============================================
        self.capacity_bits = 0
        self.over_or_under_flow = []
        self.over_or_under_flow_bits = 0
        self.hidden_str = ""

    def PSNR(self, oriNumImg, stegoImg):
        imgSize = len(oriNumImg) * len(oriNumImg)
        MSE = float(0)
        for row in range(len(oriNumImg)):
            for col in range(len(oriNumImg[0])):
                tem = oriNumImg[row][col] - stegoImg[row][col]
                MSE += tem * tem
        MSE /= imgSize
        psnr = 10 * math.log((255 * 255) / MSE, 10)
        return psnr

    def get_4adjacent_pixels(self, row, col):
        # Left, top, right, bot
        return [
            self.image[row][col - 1] if col - 1 >= 0 else None,
            self.image[row - 1][col] if row - 1 >= 0 else None,
            self.image[row][col + 1] if col + 1 < len(self.image[0]) else None,
            self.image[row + 1][col] if row + 1 < len(self.image) else None]

    # threshold_left already multiply -1 automatically
    def difference_expand(self, value, watermark_bit, embeddable):
        if -self.threshold_left <= value <= self.threshold_right:
            value_prime = value * 2 + watermark_bit
            self.capacity_bits += 1
            embeddable = 1
        elif -self.threshold_left > value:
            value_prime = value - self.threshold_left
        elif self.threshold_right < value:
            value_prime = value + self.threshold_right + 1
        return value_prime, embeddable

    def chessboard_difference_expansion_black(self, locations):
        for loc in xrange(len(locations)):
            row = locations[loc][0]
            col = locations[loc][1]
            # We filtered elements which are None
            filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
            filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

            random_bit = random.randint(0, 1)
            embeddable = 0
            difference_prime, embeddable = \
                self.difference_expand(self.image[row][col] - filtered_4pixels_avg,
                                       random_bit, embeddable)
            modified_value = difference_prime + filtered_4pixels_avg

            if (modified_value > 255) or (modified_value < 0):
                self.over_or_under_flow.append((row, col))
                self.over_or_under_flow_bits += 1
                if embeddable:
                    self.capacity_bits -= 1
                    embeddable = 0
            else:
                self.image[row][col] = modified_value

            if self.capacity_bits == math.ceil(self.capacity_given / 2):
                break

    def chessboard_difference_expansion_white(self, locations):
        for loc in xrange(len(locations)):
            row = locations[loc][0]
            col = locations[loc][1]
            # We filtered elements which are None
            filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
            filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

            random_bit = random.randint(0, 1)
            embeddable = 0
            difference_prime, embeddable = \
                self.difference_expand(self.image[row][col] - filtered_4pixels_avg,
                                       random_bit, embeddable)
            modified_value = difference_prime + filtered_4pixels_avg

            if (modified_value > 255) or (modified_value < 0):
                self.over_or_under_flow.append((row, col))
                self.over_or_under_flow_bits += 1
                if embeddable:
                    self.capacity_bits -= 1
                    embeddable = 0
            else:
                self.image[row][col] = modified_value

            if self.capacity_bits == self.capacity_given:
                break

    def avg_reduce(self, func, seq):
        first_element = seq[0]
        count = 1
        for next_element in seq[1:]:
            first_element = func(first_element, next_element)
            count += 1
        return float(first_element) / count

    def sort_by_variance(self, locations):
        for loc in xrange(len(locations)):
            adjacent_4pixels = self.get_4adjacent_pixels(locations[loc][0], locations[loc][1])
            tmp_buf = []
            for i in xrange(len(adjacent_4pixels)):
                i_next = (i + 1) % 4
                if (adjacent_4pixels[i] is not None) & \
                        (adjacent_4pixels[i_next] is not None):
                    tmp_buf += [abs(adjacent_4pixels[i] - adjacent_4pixels[i_next])]

            avg = self.avg_reduce(lambda a, b: a + b, tmp_buf)
            variance = reduce(lambda a, b: a + b, map(lambda a: (a - avg) ** 2, tmp_buf))
            locations[loc] += [variance]

            # print tmp_buf
            # print avg
            # print map(lambda a: (a-avg)**2, tmp_buf)
            # print variance
            # print ""
        locations.sort(key=lambda x: x[2])
        return locations

    def black_throughout(self):
        black_locations = []
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in xrange(first_of_row, len(self.image[0]), 2):
                black_locations += [[row, col]]
        return black_locations

    def white_throughout(self):
        white_locations = []
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 1
            # If current row is even, first_of_row = 0
            first_of_row = (row + 1) % 2
            for col in xrange(first_of_row, len(self.image[0]), 2):
                white_locations += [[row, col]]
        return white_locations

    def hide_black(self):
        black_location = self.black_throughout()
        hiding_order = self.sort_by_variance(black_location)
        self.chessboard_difference_expansion_black(hiding_order)

    def hide_white(self):
        white_location = self.white_throughout()
        hiding_order = self.sort_by_variance(white_location)
        self.chessboard_difference_expansion_white(hiding_order)

    def hide(self):
        random_seed = random.random()
        random.seed(random_seed)
        self.hide_black()
        self.hide_white()

        psnr = self.PSNR(self.image_misc, self.image)

        print self.capacity_bits
        if self.capacity_bits < self.capacity_given:
            psnr = 0
        return psnr  # , self.over_or_under_flow_bits


def main(image_path, threshold_left, threshold_right, capacity_given):
    embed_obj = Embed(image_path, threshold_left, threshold_right, capacity_given)
    print embed_obj.hide()
    # return embed_obj.hide()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\Baboon.bmp", 2, 0, 6555)