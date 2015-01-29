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
        self.copy_image = copy.deepcopy(self.image)
        self.THRESHOLD = threshold  # Th
        self.T_STAR = t_star  # T*

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
        upper_right = self.image[row][col+2]
        lower_left = self.image[row+2][col]
        lower_right = self.image[row+2][col+2]

        self.horizontal_difference = abs(upper_left-upper_right) + abs(lower_left-lower_right)
        self.vertical_difference = abs(upper_left-lower_left) + abs(upper_right-lower_right)

        # return complexity
        return self.horizontal_difference + self.vertical_difference

    def difference_expand(self, value, watermark_bit, embeddable):
        if -self.T_STAR <= value <= self.T_STAR:
            value_prime = value * 2 + int(watermark_bit)
            self.capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > value:
            value_prime = value - self.T_STAR
        elif self.T_STAR < value:
            value_prime = value + self.T_STAR + 1

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
            right_difference_prime, embeddable = self.difference_expand(right_difference, block_watermark[1], embeddable)

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
            upper_difference_prime, embeddable = self.difference_expand(upper_difference, block_watermark[2], embeddable)
            lower_difference_prime, embeddable = self.difference_expand(lower_difference, block_watermark[3], embeddable)

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
        # generate a black image. Black(0) means un_embeddable_block.
        un_embeddable_block_image = [[0 for i in range(len(self.image))] for i in range(len(self.image[0]))]
        random_seed = random.random()
        random.seed(random_seed)

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

                block_watermark = ""
                for i in xrange(4):
                    block_watermark += str(random.randint(0, 1))

                # Smooth block
                if complexity <= self.THRESHOLD:
                    embeddable = self.hide_smooth(row, col, block_watermark)
                    self.all_smooth_blocks += 1
                    if embeddable:
                        self.all_embeddable_smooth_blocks += 1

                elif complexity > self.THRESHOLD:
                    embeddable = self.hide_complex(row, col, block_watermark)
                    self.all_complex_blocks += 1
                    if embeddable:
                        self.all_embeddable_complex_blocks += 1


                # Paint un_embeddable_block_image to white
                # if this block is embeddable, we paint this entire block to white(255).
                # row_within_this_block/col_within_this_block = {0, 1, ......, self.BLOCK_SIZE}
                if embeddable:
                    for row_within_this_block in xrange(row, row + self.BLOCK_SIZE):
                        for col_within_this_block in xrange(col, col + self.BLOCK_SIZE):
                            un_embeddable_block_image[row_within_this_block][col_within_this_block] = 255


        print IMAGE
        print "TH:", self.THRESHOLD, "  T*:", self.T_STAR
        #print self.image
        #print "capacity_blocks:", str(self.capacity_blocks)
        print "capacity_bits:", str(self.capacity_bits)
        print "over_or_under_flow_bits:", self.over_or_under_flow_bits
        #print un_embeddable_block_image
        print "PSNR:" + str(self.PSNR(self.copy_image, self.image))
        #print "all_smooth_blocks:", self.all_smooth_blocks
        #print "all_embeddable_smooth_blocks:", self.all_embeddable_smooth_blocks
        #print "all_complex_blocks:", self.all_complex_blocks
        #print "all_embeddable_complex_blocks:", self.all_embeddable_complex_blocks
        print "====================================="

        if count_T_STAR is 0:
            print "Next TH"
            worksheet.write(1+count_THRESHOLD, 0, "TH=" + str(self.THRESHOLD))
            #worksheet.write(0+count_THRESHOLD, 1, 'T*')
            worksheet.write(1+count_THRESHOLD, 1, 'Capacity')
            worksheet.write(2+count_THRESHOLD, 1, 'PSNR')

        if count_THRESHOLD is 0:
            worksheet.write(0, 2+count_T_STAR, self.T_STAR)  # T*
        worksheet.write(1+count_THRESHOLD, 2+count_T_STAR, self.capacity_bits)  # Capacity
        worksheet.write(2+count_THRESHOLD, 2+count_T_STAR, self.PSNR(self.copy_image, self.image))  # PSNR


        output_name = get_output_name(IMAGE, self.THRESHOLD, self.T_STAR)
        #  Save data for recovering(seed, over/under flow)
        data_file = file(u"output//" + output_name + u".data", 'w')
        Pickle.dump([random_seed, self.over_or_under_flow], data_file)
        data_file.close()

        #  Save stego image
        for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = self.image[row][col]
        misc.imsave(u"output//Stego" + output_name + u".bmp", img_misc)

        #  Save unbeddable-block image
        for row in xrange(len(un_embeddable_block_image)):
                for col in xrange(len(un_embeddable_block_image[0])):
                    img_misc[row][col] = un_embeddable_block_image[row][col]
        misc.imsave(u"output//Unembeddable" + output_name + u".bmp", img_misc)

#  integer to unicode string
def int_to_uni(integer):
    return str(integer).decode("utf-8")


def get_output_name(image, threshold, t_star):
    # picture_name_without_extension name
    pic_name_without_ext = os.path.splitext(os.path.basename(image))[0]
    return pic_name_without_ext + u"," + int_to_uni(threshold) + u"," + int_to_uni(t_star)


if __name__ == '__main__':
    IMAGE_LIST = [u"C:\\Users\\Jasper\\Desktop\\Lena.bmp"]
    THRESHOLD_LIST = [-1, 1020]  # 1020 is max THRESHOLD, -1
    T_STAR_LIST = [0,1,2,3,4]


    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:O', 9)
    worksheet.write(0, 1, 'T*')
    count_THRESHOLD = 0
    for IMAGE in IMAGE_LIST:
        img_misc = misc.imread(IMAGE)
        img = img_misc.tolist()
        for THRESHOLD in THRESHOLD_LIST:
            count_T_STAR = 0
            for T_STAR in T_STAR_LIST:
                embed_obj = Embed(copy.deepcopy(img), THRESHOLD, T_STAR)
                embed_obj.hide()
                count_T_STAR += 1
            count_THRESHOLD += 2
    workbook.close()





# 取出, excel, paper4






