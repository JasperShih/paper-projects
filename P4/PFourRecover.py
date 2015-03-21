# -*- coding: utf8 -*-
__author__ = 'Jasper'

import math
import copy
import random
import scipy.misc as misc
import os
import cPickle as Pickle
import xlsxwriter


class Recover():
    def __init__(self, image_path):
        self.image_misc = misc.imread(image_path)
        self.image = self.image_misc.tolist()
        self.threshold = 255
        self.t_star = 255
        self.round = 1
        self.block_size = 3  # TODO

        data_file = file(u"output//stego.data", 'r')
        # [(row, col), (row, col), ......]
        self.random_seed, self.over_or_under_flow = Pickle.load(data_file)
        data_file.close()

        self.buf = ""

    def get_4adjacent_pixels(self, row, col):
        # Top, left, right, bot
        return [
            self.image[row - 1][col] if row - 1 >= 0 else None,
            self.image[row][col - 1] if col - 1 >= 0 else None,
            self.image[row][col + 1] if col + 1 < len(self.image[0]) else None,
            self.image[row + 1][col] if row + 1 < len(self.image) else None
        ]

    # reduce then compute avg
    def avg_reduce(self, func, seq):
        first_element = seq[0]
        count = 1
        for next_element in seq[1:]:
            first_element = func(first_element, next_element)
            count += 1
        return first_element / count

    def undifference_expand(self, difference_value):
        two_t_star = 2 * self.t_star
        if -two_t_star <= difference_value <= (two_t_star + 1):
            watermark_bit = str(difference_value % 2)
            original_value = difference_value / 2
        elif difference_value <= -(two_t_star + 1):  # dL-T*
            watermark_bit = '*'
            original_value = difference_value + self.t_star
        elif (two_t_star + 2) <= difference_value:  # T*<dL
            watermark_bit = '*'
            original_value = difference_value - self.t_star - 1

        return watermark_bit, original_value

    def extract_same_part(self, row, col):
        # We filtered elements which are None
        filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
        filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

        complexity = max(
            map(lambda a: a - filtered_4pixels_avg, filtered_4pixels)
        )

        watermark_bit = '*'
        if complexity < self.threshold:
            # un_difference_expand
            # If current processing pixel belong overflow pixel, recover it and skip it.
            # Else, un_difference_expand
            for pair in self.over_or_under_flow:
                if pair[0] == row and pair[1] == col:
                    watermark_bit = '*'
                    break
            else:
                watermark_bit, original_value = self.undifference_expand(
                    self.image[row][col] - filtered_4pixels_avg)
                self.image[row][col] = original_value + filtered_4pixels_avg
        self.buf += watermark_bit

    def extract_white(self):
        self.buf = ""
        for row in reversed(xrange(0, len(self.image))):
            # If current row is odd, first_of_row = 1
            # If current row is even, first_of_row = 0
            first_of_row = (row + 1) % 2
            for col in reversed(
                    xrange(first_of_row, len(self.image[0]), 2)):
                self.extract_same_part(row, col)
        # extracted_watermark is reversed order
        return self.buf[::-1]

    def extract_black(self):
        self.buf = ""
        for row in reversed(xrange(0, len(self.image))):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in reversed(
                    xrange(first_of_row, len(self.image[0]), 2)):
                self.extract_same_part(row, col)
        # extracted_watermark is reversed order
        return self.buf[::-1]

    def generated_watermark(self):
        generated_watermark = ""
        for i in xrange(len(self.image) * len(self.image[0]) * self.round):
            generated_watermark += str(random.randint(0, 1))
        return generated_watermark

    def black_white_interlock(self, input_str):
        # input_str = black + white
        white_start = int(math.ceil(float(len(input_str)) / 2))
        output_str = ""
        anchor = 0
        for row in xrange(len(self.image)):
            for col in xrange(len(self.image[0])):
                # If (row and col belong even) and
                # (row and col belong odd), we take black part
                if (row % 2 == 0 and col % 2 == 0) or \
                        (row % 2 == 1 and col % 2 == 1):
                    output_str += input_str[anchor]

                # If (row belong even and col belong odd) and
                # (row belong odd and col belong even),
                # we take white part
                else:
                    output_str += input_str[white_start + anchor]
                if col % 2 == 1:
                    anchor += 1
        return output_str

    def str_to_2Dlist(self, input_str):
        output_list = []
        for row in xrange(len(self.image)):
            row_start = row*len(self.image[0])
            output_list += [input_str[row_start:row_start+len(self.image[0])]]
        return output_list

    # Save content_image by stored_image with save_name
    def save_image(self, content_image, stored_image, save_name):
        for row in xrange(len(content_image)):
            for col in xrange(len(content_image[0])):
                stored_image[row][col] = content_image[row][col]
        misc.imsave(save_name, stored_image)

    def extract(self):
        extracted_watermark = ""
        for i in xrange(self.round):
            # Backwardly throughout_image_by_chessboard
            # White part first
            extracted_watermark_white = self.extract_white()
            # Black part
            extracted_watermark_black = self.extract_black()
            extracted_watermark = extracted_watermark_black + extracted_watermark_white + extracted_watermark

        # =================================== Result ========================================
        ori_image_misc = misc.imread("C:\\Users\\Jasper\\Desktop\\image\\Lena.bmp")
        ori_image = ori_image_misc.tolist()
        if ori_image == self.image:
            print "Same"
            # print ori_image
            # print self.image

        random.seed(self.random_seed)
        regenerated_watermark = self.generated_watermark()

        for i in xrange(len(extracted_watermark)):
            if extracted_watermark[i] == '*' or \
                            extracted_watermark[i] == regenerated_watermark[i]:
                pass
            else:
                print "GG"
                break
        else:
            print "Yes"

        # Reorder watermark string by black_and_white_interlocking
        # and transform into 2d list
        inter2d_regenerated_watermark = self.str_to_2Dlist(
            self.black_white_interlock(regenerated_watermark))
        inter2d_extracted_watermark = self.str_to_2Dlist(
            self.black_white_interlock(extracted_watermark))
        detected_image = [[255 for i in xrange(len(self.image))] for i in xrange(len(self.image[0]))]

        image_row_bound = len(self.image) - self.block_size + 1
        image_col_bound = len(self.image[0]) - self.block_size + 1
        for row in xrange(0, image_row_bound, self.block_size):
            for col in xrange(0, image_col_bound, self.block_size):
                paint = 0
                for row_within_this_block in xrange(row, row + self.block_size):
                    for col_within_this_block in xrange(col, col + self.block_size):
                        if inter2d_extracted_watermark[row_within_this_block][col_within_this_block] == '*' or\
                                        inter2d_extracted_watermark[row_within_this_block][col_within_this_block] == \
                                        inter2d_regenerated_watermark[row_within_this_block][col_within_this_block]:
                            pass
                        else:
                            paint = 1

                if paint:
                    for row_within_this_block in xrange(row, row + self.block_size):
                        for col_within_this_block in xrange(col, col + self.block_size):
                            detected_image[row_within_this_block][col_within_this_block] = 0

        #  Save detected image
        self.save_image(detected_image, self.image_misc, u"output//detected.bmp")


def main(image_path):
    extract_obj = Recover(image_path)
    extract_obj.extract()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\Pps\\P4\\output\\TamperedStego.bmp")











