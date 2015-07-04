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
    def __init__(self, image, threshold, t_star_left, t_star_right, capacity_limit):
        self.image = image
        self.copy_image = copy.deepcopy(self.image)
        self.THRESHOLD = threshold  # Th
        self.T_STAR_LEFT = t_star_left
        self.T_STAR_RIGHT = t_star_right
        self.capacity_limit = capacity_limit

        self.BLOCK_SIZE = 3
        self.MID = (1, 1)

        # capacity_blocks = all_embeddable_smooth_blocks+all_embeddable_complex_blocks
        self.capacity_bits = 0
        self.over_or_under_flow_bits = 0
        self.over_or_under_flow = []

        # all_smooth_blocks in the image, no matter it can be embed or not
        self.all_smooth_blocks = 0
        self.all_complex_blocks = 0

        # all_embeddable_smooth_blocks in the image
        self.all_embeddable_smooth_blocks = 0
        self.all_embeddable_complex_blocks = 0

        self.horizontal_difference = None
        self.vertical_difference = None


    def corner_classify(self, row, col):
        # upper_left corner
        upper_left = self.image[row][col]
        upper_right = self.image[row][col + 2]
        lower_left = self.image[row + 2][col]
        lower_right = self.image[row + 2][col + 2]

        self.horizontal_difference = abs(upper_left - upper_right) + abs(lower_left - lower_right)
        self.vertical_difference = abs(upper_left - lower_left) + abs(upper_right - lower_right)

        # return complexity
        return self.horizontal_difference + self.vertical_difference

    def difference_expand(self, value, watermark_bit, embeddable):
        if -self.T_STAR_LEFT <= value <= self.T_STAR_RIGHT:
            value_prime = value * 2 + int(watermark_bit)
            self.capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR_LEFT > value:
            value_prime = value - self.T_STAR_LEFT
        elif self.T_STAR_RIGHT < value:
            value_prime = value + self.T_STAR_RIGHT + 1

        return value_prime, embeddable

    def hide_smooth(self, row, col, block_watermark):
        central_row = row + self.MID[0]
        central_col = col + self.MID[1]
        left_difference = self.image[central_row][central_col - 1] - self.image[central_row][central_col]
        right_difference = self.image[central_row][central_col + 1] - self.image[central_row][central_col]
        upper_difference = self.image[central_row - 1][central_col] - self.image[central_row][central_col]
        lower_difference = self.image[central_row + 1][central_col] - self.image[central_row][central_col]

        embeddable = 0
        left_difference_prime, embeddable = self.difference_expand(left_difference, block_watermark[0], embeddable)
        right_difference_prime, embeddable = self.difference_expand(right_difference, block_watermark[1], embeddable)
        upper_difference_prime, embeddable = self.difference_expand(upper_difference, block_watermark[2], embeddable)
        lower_difference_prime, embeddable = self.difference_expand(lower_difference, block_watermark[3], embeddable)


        # left stego
        modified_value = left_difference_prime + self.image[central_row][central_col]
        if (modified_value > 255) or (modified_value < 0):
            self.over_or_under_flow.append((central_row, central_col - 1))
            self.over_or_under_flow_bits += 1
        else:
            self.image[central_row][central_col - 1] = modified_value
        # right stego
        modified_value = right_difference_prime + self.image[central_row][central_col]
        if (modified_value > 255) or (modified_value < 0):
            self.over_or_under_flow.append((central_row, central_col + 1))
            self.over_or_under_flow_bits += 1
        else:
            self.image[central_row][central_col + 1] = modified_value
        # upper stego
        modified_value = upper_difference_prime + self.image[central_row][central_col]
        if (modified_value > 255) or (modified_value < 0):
            self.over_or_under_flow.append((central_row - 1, central_col))
            self.over_or_under_flow_bits += 1
        else:
            self.image[central_row - 1][central_col] = modified_value
        # lower stego
        modified_value = lower_difference_prime + self.image[central_row][central_col]
        if (modified_value > 255) or (modified_value < 0):
            self.over_or_under_flow.append((central_row + 1, central_col))
            self.over_or_under_flow_bits += 1
        else:
            self.image[central_row + 1][central_col] = modified_value

        return embeddable

    def hide_complex(self, row, col, block_watermark):
        central_row = row + self.MID[0]
        central_col = col + self.MID[1]
        left_difference = self.image[central_row][central_col - 1] - self.image[central_row][central_col]
        right_difference = self.image[central_row][central_col + 1] - self.image[central_row][central_col]
        upper_difference = self.image[central_row - 1][central_col] - self.image[central_row][central_col]
        lower_difference = self.image[central_row + 1][central_col] - self.image[central_row][central_col]

        embeddable = 0

        if self.vertical_difference >= self.horizontal_difference:
            left_difference_prime, embeddable = self.difference_expand(left_difference, block_watermark[0], embeddable)
            right_difference_prime, embeddable = self.difference_expand(right_difference, block_watermark[1],
                                                                        embeddable)

            # left stego
            modified_value = left_difference_prime + self.image[central_row][central_col]
            if (modified_value > 255) or (modified_value < 0):
                self.over_or_under_flow.append((central_row, central_col - 1))
                self.over_or_under_flow_bits += 1
            else:
                self.image[central_row][central_col - 1] = modified_value
            # right stego
            modified_value = right_difference_prime + self.image[central_row][central_col]
            if (modified_value > 255) or (modified_value < 0):
                self.over_or_under_flow.append((central_row, central_col + 1))
                self.over_or_under_flow_bits += 1
            else:
                self.image[central_row][central_col + 1] = modified_value

        elif self.vertical_difference < self.horizontal_difference:
            upper_difference_prime, embeddable = self.difference_expand(upper_difference, block_watermark[2],
                                                                        embeddable)
            lower_difference_prime, embeddable = self.difference_expand(lower_difference, block_watermark[3],
                                                                        embeddable)

            # upper stego
            modified_value = upper_difference_prime + self.image[central_row][central_col]
            if (modified_value > 255) or (modified_value < 0):
                self.over_or_under_flow.append((central_row - 1, central_col))
                self.over_or_under_flow_bits += 1
            else:
                self.image[central_row - 1][central_col] = modified_value
            # lower stego
            modified_value = lower_difference_prime + self.image[central_row][central_col]
            if (modified_value > 255) or (modified_value < 0):
                self.over_or_under_flow.append((central_row + 1, central_col))
                self.over_or_under_flow_bits += 1
            else:
                self.image[central_row + 1][central_col] = modified_value

        return embeddable

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


    def hide(self):
        random_seed = random.random()
        random.seed(random_seed)

        image_row_bound = len(self.image) - self.BLOCK_SIZE + 1
        image_col_bound = len(self.image[0]) - self.BLOCK_SIZE + 1
        # Throughout entire Img block by block
        break_flag = 0
        for row in xrange(0, image_row_bound, self.BLOCK_SIZE):
            for col in xrange(0, image_col_bound, self.BLOCK_SIZE):
                complexity = self.corner_classify(row, col)
                # Hiding
                # we will set embeddable to 0/1 because complexity is either smooth or complex
                # i.e. we have to go through either smooth_hide or complex_hide.
                # And we will update embeddable value in hide function of every block

                # block_watermark sequence for be hided position of block:
                # left, right, upper, lower

                block_watermark = ""
                for i in xrange(4):
                    block_watermark += str(random.randint(0, 1))

                # Smooth block
                if complexity <= self.THRESHOLD:
                    embeddable = self.hide_smooth(row, col, block_watermark)
                    self.all_smooth_blocks += 1
                    if embeddable:
                        self.all_embeddable_smooth_blocks += 1

                if self.capacity_bits >= self.capacity_limit:
                    break_flag = 1
                    break
            if break_flag:
                break

        if self.capacity_bits >= self.capacity_limit:
            psnr = self.PSNR(self.copy_image, self.image)
        else:
            psnr = 0

        print IMAGE
        print "TH:", self.THRESHOLD, "  T*:", self.T_STAR_LEFT, self.T_STAR_RIGHT
        print self.capacity_bits, self.over_or_under_flow_bits, psnr
        print ""
        return psnr


# integer to unicode string
def int_to_uni(integer):
    return str(integer).decode("utf-8")


def get_output_name(image, threshold, t_star):
    # picture_name_without_extension name
    pic_name_without_ext = os.path.splitext(os.path.basename(image))[0]
    return pic_name_without_ext + u"," + int_to_uni(threshold) + u"," + int_to_uni(t_star)


if __name__ == '__main__':
    IMAGE_LIST = [u"C:\\Users\\Jasper\\Desktop\\image\\Baboon.bmp"]  # TODO
    THRESHOLD_LIST = [30,40,50,60,70,80,90,100]  # 1020 is max THRESHOLD, -1 TODO
    # 2, 4, 6, 8, 10, 12, 14, 16, 18, 20
    T_STAR_LIST = [0, 1, 2, 3, 4]  # TODO
    Capacity = [5243, 10486, 15729, 20972, 26215]

    IMAGE_LIST.sort()
    THRESHOLD_LIST.sort()
    T_STAR_LIST.sort()

    result = []
    for IMAGE in IMAGE_LIST:
        img_misc = misc.imread(IMAGE)
        img = img_misc.tolist()

        for Capacity_limit in Capacity:
            buf = []
            for THRESHOLD in THRESHOLD_LIST:
                for T_STAR_LEFT in T_STAR_LIST:
                    for T_STAR_RIGHT in T_STAR_LIST:

                        embed_obj = Embed(copy.deepcopy(img), THRESHOLD, T_STAR_LEFT, T_STAR_RIGHT, Capacity_limit)
                        # capacity, over_or_under_flow_bits, PSNR
                        buf += [embed_obj.hide()]


                        # result = [image name, threshold, T_STAR,
                        #  capacity, over_or_under_flow_bits, PSNR]

                        # stego = threshold, t_star
            result += [max(buf)]

    print result