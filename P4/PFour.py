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
    def __init__(self, image_path, threshold, t_star, rounds, block_size):
        self.image_path = image_path
        self.image_misc = misc.imread(image_path)
        self.image = self.image_misc.tolist()
        self.threshold = threshold
        self.t_star = t_star
        self.rounds = rounds

        self.capacity_bits = 0
        self.over_or_under_flow = []
        self.over_or_under_flow_bits = 0
        self.un_embeddable_img_pixel = [[0 for i in xrange(len(self.image))] for i in xrange(len(self.image[0]))]
        self.un_embeddable_img_block = [[0 for i in xrange(len(self.image))] for i in xrange(len(self.image[0]))]
        self.block_size = block_size
        self.hidden_str = ""

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

    def difference_expand(self, value, watermark_bit, embeddable):
        if -self.t_star <= value <= self.t_star:
            value_prime = value * 2 + watermark_bit
            self.capacity_bits += 1
            embeddable = 1
        elif -self.t_star > value:
            value_prime = value - self.t_star
        elif self.t_star < value:
            value_prime = value + self.t_star + 1
        return value_prime, embeddable

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

    def hide_same_part(self, row, col):
        # We filtered elements which are None
        filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
        filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)
        complexity = max(
            map(lambda a: a - filtered_4pixels_avg, filtered_4pixels)
        )

        random_bit = random.randint(0, 1)

        embeddable = 0
        if complexity <= self.threshold:
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

            if embeddable:
                self.un_embeddable_img_pixel[row][col] = 255
                self.hidden_str += str(random_bit)
            else:
                self.hidden_str += "*"
        else:
            self.hidden_str += "*"

    def hide_black(self):
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                self.hide_same_part(row, col)

    def hide_white(self):
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 1
            # If current row is even, first_of_row = 0
            first_of_row = (row + 1) % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                self.hide_same_part(row, col)

    # Save content_image by stored_image with save_name
    def save_image(self, content_image, stored_image, save_name):
        for row in xrange(len(content_image)):
            for col in xrange(len(content_image[0])):
                stored_image[row][col] = content_image[row][col]
        misc.imsave(save_name, stored_image)

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

    def hide(self):
        random_seed = random.random()
        random.seed(random_seed)

        # Throughout_image_by_chessboard
        for i in xrange(self.rounds):
            self.hidden_str = ""
            self.hide_black()
            self.hide_white()
        self.hidden_str = self.str_to_2Dlist(self.black_white_interlock(self.hidden_str))
        # print self.hidden_str
        # ============================= Executed ================================
        image_row_bound = len(self.image) - self.block_size + 1
        image_col_bound = len(self.image[0]) - self.block_size + 1
        for row in xrange(0, image_row_bound, self.block_size):
            for col in xrange(0, image_col_bound, self.block_size):
                paint = 0
                for row_within_this_block in xrange(row, row + self.block_size):
                    for col_within_this_block in xrange(col, col + self.block_size):
                        if self.un_embeddable_img_pixel[row_within_this_block][col_within_this_block] == 255:
                            paint = 1
                if paint:
                    for row_within_this_block in xrange(row, row + self.block_size):
                        for col_within_this_block in xrange(col, col + self.block_size):
                            self.un_embeddable_img_block[row_within_this_block][col_within_this_block] = 255


        output_name = get_output_name(self.image_path, self.threshold, self.t_star)
        # Save data for recovering(seed, over/under flow)
        data_file = file(u"output//" + output_name + u".data", 'w')
        Pickle.dump([random_seed, self.over_or_under_flow], data_file)
        data_file.close()

        psnr = self.PSNR(self.image_misc, self.image)
        # Save stego image
        self.save_image(self.image, self.image_misc, u"output//Stego" + output_name + u".bmp")
        #  Save unbeddable-block image (Pixel unit)
        self.save_image(self.un_embeddable_img_pixel, self.image_misc, u"output//UnembeddablePixel" + output_name + u".bmp")
        #  Save unbeddable-block image (Block unit)
        self.save_image(self.un_embeddable_img_block, self.image_misc, u"output//UnembeddableBlock" + output_name + u".bmp")

        return [self.capacity_bits, self.over_or_under_flow_bits, psnr]


# integer to unicode string
def int_to_uni(integer):
    return str(integer).decode("utf-8")


def get_output_name(image, threshold, t_star):
    # picture_name_without_extension name
    pic_name_without_ext = os.path.splitext(os.path.basename(image))[0]
    return pic_name_without_ext + u"," + int_to_uni(threshold) + u"," + int_to_uni(t_star)


def main(image_path, threshold, t_star, rounds, block_size):
    embed_obj = Embed(image_path, threshold, t_star, rounds, block_size)
    return embed_obj.hide()


if __name__ == '__main__':
    # image, threshold, t_star
    main("C:\\Users\\Jasper\\Desktop\\image\\Lena.bmp",
         5, 2, 1, 2)











