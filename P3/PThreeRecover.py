__author__ = 'Jasper'

import math
import copy
import random
import scipy.misc as misc
import os
import cPickle as Pickle


class Recover():
    def __init__(self, image, threshold, t_star, random_seed, over_or_under_flow):
        self.BLOCK_SIZE = 3
        self.MID = (1, 1)

        self.horizontal_difference = None
        self.vertical_difference = None

        self.image = image
        self.THRESHOLD = threshold
        self.T_STAR = t_star
        self.TWO_T_STAR = 2 * t_star
        self.RANDOM_SEED = random_seed
        self.OVER_OR_UNDER_FLOW = over_or_under_flow

    def undifference_expand(self, difference_value):
        if -self.TWO_T_STAR <= difference_value <= (self.TWO_T_STAR + 1):
            watermark_bit = str(difference_value % 2)
            original_value = difference_value / 2
        elif difference_value <= -(self.TWO_T_STAR + 1):  # dL-T*
            watermark_bit = '*'
            original_value = difference_value + self.T_STAR
        elif (self.TWO_T_STAR + 2) <= difference_value:  # T*<dL
            watermark_bit = '*'
            original_value = difference_value - self.T_STAR - 1
        return watermark_bit, original_value


    def extract_smooth(self, row, col):
        central_row = row + self.MID[0]
        central_col = col + self.MID[1]
        left_difference = self.image[central_row][central_col - 1] - self.image[central_row][central_col]
        right_difference = self.image[central_row][central_col + 1] - self.image[central_row][central_col]
        upper_difference = self.image[central_row - 1][central_col] - self.image[central_row][central_col]
        lower_difference = self.image[central_row + 1][central_col] - self.image[central_row][central_col]
        block_watermark = ""


        # undifference_expand left_difference
        overflow_flag = 0
        for pair in self.OVER_OR_UNDER_FLOW:
            if pair[0] == central_row and pair[1] == (central_col - 1):
                overflow_flag = 1
                block_watermark += '*'
                break
        if overflow_flag is 0:
            watermark_bit, original_value = self.undifference_expand(left_difference)
            block_watermark += watermark_bit
            self.image[central_row][central_col - 1] = original_value + self.image[central_row][central_col]

        # undifference_expand right_difference
        overflow_flag = 0
        for pair in self.OVER_OR_UNDER_FLOW:
            if pair[0] == central_row and pair[1] == (central_col + 1):
                overflow_flag = 1
                block_watermark += '*'
                break
        if overflow_flag is 0:
            watermark_bit, original_value = self.undifference_expand(right_difference)
            block_watermark += watermark_bit
            self.image[central_row][central_col + 1] = original_value + self.image[central_row][central_col]

        # undifference_expand upper_difference
        overflow_flag = 0
        for pair in self.OVER_OR_UNDER_FLOW:
            if pair[0] == (central_row - 1) and pair[1] == central_col:
                overflow_flag = 1
                block_watermark += '*'
                break
        if overflow_flag is 0:
            watermark_bit, original_value = self.undifference_expand(upper_difference)
            block_watermark += watermark_bit
            self.image[central_row - 1][central_col] = original_value + self.image[central_row][central_col]

        # undifference_expand lower_difference
        overflow_flag = 0
        for pair in self.OVER_OR_UNDER_FLOW:
            if pair[0] == (central_row + 1) and pair[1] == central_col:
                overflow_flag = 1
                block_watermark += '*'
                break
        if overflow_flag is 0:
            watermark_bit, original_value = self.undifference_expand(lower_difference)
            block_watermark += watermark_bit
            self.image[central_row + 1][central_col] = original_value + self.image[central_row][central_col]

        return block_watermark



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

    def extract(self):
        random.seed(self.RANDOM_SEED)

        image_row_bound = len(self.image) - self.BLOCK_SIZE + 1
        image_col_bound = len(self.image[0]) - self.BLOCK_SIZE + 1
        # Throughout entire Img block by block
        for row in xrange(0, image_row_bound, self.BLOCK_SIZE):
            for col in xrange(0, image_col_bound, self.BLOCK_SIZE):

                complexity = self.corner_classify(row, col)
                # Hiding
                # we will set embeddable to 0/1 because complexity is either smooth or complex
                # i.e. we have to go through either smooth_hide or complex_hide.
                # And we will update embeddable value in hide function of every block

                # block_watermark sequence for be hided position of block:
                # left, right, upper, lower


                # block_watermark = ""
                #for i in xrange(4):
                #    block_watermark += str(random.randint(0, 1))



                # Smooth block
                if complexity <= self.THRESHOLD:
                    self.extract_smooth(row, col)


                """
                elif complexity > self.THRESHOLD:
                    embeddable = self.hide_complex(row, col, block_watermark)

                # Paint un_embeddable_block_image to white
                # if this block is embeddable, we paint this entire block to white(255).
                # row_within_this_block/col_within_this_block = {0, 1, ......, self.BLOCK_SIZE}
                if embeddable:
                    for row_within_this_block in xrange(row, row + self.BLOCK_SIZE):
                        for col_within_this_block in xrange(col, col + self.BLOCK_SIZE):
                            un_embeddable_block_image[row_within_this_block][col_within_this_block] = 255
                """

        ORIGINAL_IMAGE = u"C:\\Users\\Jasper\\Desktop\\Peppers.bmp"
        Oimg_misc = misc.imread(ORIGINAL_IMAGE)
        Oimg = Oimg_misc.tolist()
        if Oimg == self.image:
            print "Recover is done!"
        else:
            for row in xrange(len(Oimg)):
                for col in xrange(len(Oimg[0])):
                    if Oimg[row][col] != self.image[row][col]:
                        print row, col
                        print Oimg[row][col], self.image[row][col]


def name_analysis(image):
    # file_name_without_extension suffix
    file_name_without_ext = os.path.splitext(os.path.basename(image))[0]
    data_file = file(os.path.split(image)[0] + u"\\" + file_name_without_ext[5:] + ".data", 'r')
    random_seed, over_or_under_flow = Pickle.load(data_file)
    data_file.close()
    tmp = file_name_without_ext.split(",")

    # return THRESHOLD, T*, random_seed, over_or_under_flow
    return int(tmp[1]), int(tmp[2]), random_seed, over_or_under_flow


if __name__ == '__main__':
    IMAGE_PATH = u"C:\\Users\\Jasper\\Desktop\\Pps\\P3\\output\\StegoPeppers,1020,10.bmp"
    THRESHOLD, T_STAR, RANDOM_SEED, OVER_OR_UNDER_FLOW = name_analysis(IMAGE_PATH)
    img_misc = misc.imread(IMAGE_PATH)
    img = img_misc.tolist()

    recover_obj = Recover(copy.deepcopy(img), THRESHOLD, T_STAR, RANDOM_SEED, OVER_OR_UNDER_FLOW)
    recover_obj.extract()
    # random.seed(rSeed)













