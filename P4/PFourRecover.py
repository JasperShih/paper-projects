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
    def __init__(self, image_path, threshold, t_star, random_seed, over_or_under_flow, block_size):
        self.image_misc = misc.imread(image_path)
        self.image = self.image_misc.tolist()
        self.threshold = threshold
        self.t_star = t_star
        self.block_size = block_size
        self.random_seed = random_seed
        # [(row, col), (row, col), ......]
        self.over_or_under_flow = over_or_under_flow

        self.round = 1
        self.buf = ""
        self.un_embeddable_img_pixel = [[0 for i in xrange(len(self.image))] for i in xrange(len(self.image[0]))]
        self.un_embeddable_img_block = [[0 for i in xrange(len(self.image))] for i in xrange(len(self.image[0]))]

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
        if complexity <= self.threshold:
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

    def black_block_count(self, image):
        count = 0
        for row in xrange(0, len(self.image) - self.block_size + 1, self.block_size):
            for col in xrange(0, len(self.image[0]) - self.block_size + 1, self.block_size):
                if image[row][col] == 0:
                    count += 1
        return count


    def boundCheckPaint(self, indList, detectUnImg, bRowOfImg, bColOfImg, blockSize):
        flag = 0
        for ind in indList:
            if 0 <= ind < len(detectUnImg):
                flag += 1
        if flag < 4:
            return 0
        else:
            if (detectUnImg[indList[0]][indList[1]] == 0) & (detectUnImg[indList[2]][indList[3]] == 0):
                bHighBound = bRowOfImg + blockSize
                bWidthBound = bColOfImg + blockSize
                for rowOfBlock in range(bRowOfImg, bHighBound, 1):
                    for colOfBlock in range(bColOfImg, bWidthBound, 1):
                        detectUnImg[rowOfBlock][colOfBlock] = 0
                return 1
            else:
                return 0


    def refine(self, detectUnImg):
        mark = 1
        while mark:
            mark = 0
            ReBCount = 0
            for bRowOfImg in xrange(0, len(detectUnImg), self.block_size):
                for bColOfImg in xrange(0, len(detectUnImg[0]), self.block_size):
                    if detectUnImg[bRowOfImg][bColOfImg] == 255:
                        # print bRowOfImg-blockSize,bColOfImg          ,bRowOfImg+blockSize,bColOfImg
                        mark += self.boundCheckPaint(
                            [bRowOfImg - self.block_size, bColOfImg, bRowOfImg + self.block_size, bColOfImg],
                            detectUnImg, bRowOfImg, bColOfImg, self.block_size)

                        # print bRowOfImg          ,bColOfImg-blockSize,bRowOfImg          ,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg, bColOfImg - self.block_size, bRowOfImg, bColOfImg + self.block_size],
                            detectUnImg, bRowOfImg, bColOfImg, self.block_size)

                        # print bRowOfImg-blockSize,bColOfImg-blockSize,bRowOfImg+blockSize,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg - self.block_size, bColOfImg - self.block_size, bRowOfImg + self.block_size,
                             bColOfImg + self.block_size],
                            detectUnImg, bRowOfImg, bColOfImg, self.block_size)

                        # print bRowOfImg+blockSize,bColOfImg-blockSize,bRowOfImg-blockSize,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg + self.block_size, bColOfImg - self.block_size, bRowOfImg - self.block_size,
                             bColOfImg + self.block_size],
                            detectUnImg, bRowOfImg, bColOfImg, self.block_size)
                    else:
                        ReBCount += 1
        return ReBCount, detectUnImg


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
        random.seed(self.random_seed)
        regenerated_watermark = self.generated_watermark()


        # Reorder watermark string by black_and_white_interlocking
        # and transform into 2d list
        inter2d_regenerated_watermark = self.str_to_2Dlist(
            self.black_white_interlock(regenerated_watermark))
        inter2d_extracted_watermark = self.str_to_2Dlist(
            self.black_white_interlock(extracted_watermark))

        # Generate detected image
        detected_image = [[255 for i in xrange(len(self.image))] for i in xrange(len(self.image[0]))]
        image_row_bound = len(self.image) - self.block_size + 1
        image_col_bound = len(self.image[0]) - self.block_size + 1
        tampered = 0
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
                            tampered = 1
                if paint:
                    for row_within_this_block in xrange(row, row + self.block_size):
                        for col_within_this_block in xrange(col, col + self.block_size):
                            detected_image[row_within_this_block][col_within_this_block] = 0

        if tampered == 1:


            for row in xrange(0, image_row_bound, self.block_size):
                for col in xrange(0, image_col_bound, self.block_size):
                    paint = 0
                    for row_within_this_block in xrange(row, row + self.block_size):
                        for col_within_this_block in xrange(col, col + self.block_size):
                            if inter2d_extracted_watermark[row_within_this_block][col_within_this_block] != '*':
                                self.un_embeddable_img_pixel[row_within_this_block][col_within_this_block] = 255
                                paint = 1
                    if paint:
                        for row_within_this_block in xrange(row, row + self.block_size):
                            for col_within_this_block in xrange(col, col + self.block_size):
                                self.un_embeddable_img_block[row_within_this_block][col_within_this_block] = 255

            self.save_image(self.un_embeddable_img_pixel, self.image_misc, u"output//ExtractablePixel" + file_name_without_ext[13:] + u".bmp")
            self.save_image(self.un_embeddable_img_block, self.image_misc, u"output//ExtractableBlock" + file_name_without_ext[13:] + u".bmp")

            #  Save detected image
            self.save_image(detected_image, self.image_misc, u"output//Detected" + file_name_without_ext[13:] + u".bmp")

            # Blocks of detected image
            blocks_detected_image = self.black_block_count(detected_image)
            # Count raw detected image NCC
            different_pixel_misc = misc.imread("output//DifferentPixel" +
                                               file_name_without_ext[13:] + ".bmp")
            different_pixel_img = different_pixel_misc.tolist()
            NCC_detected_image = NCC(detected_image, different_pixel_img)

            #  =======================Refine image=================================
            ReBCount, refined_detected_image = self.refine(detected_image)
            #  Save refine detected image
            self.save_image(refined_detected_image, self.image_misc,
                            u"output//RefinedDetected" + file_name_without_ext[13:] + u".bmp")
            #  Blocks of refine_detected_image
            blocks_refine_detected_image = self.black_block_count(refined_detected_image)
            #  Count refine detected image NCC
            NCC_refine_detected_image = NCC(refined_detected_image, different_pixel_img)

            return [NCC_detected_image, NCC_refine_detected_image,
                    blocks_detected_image, blocks_refine_detected_image]

        elif tampered == 0:
            self.save_image(self.image, self.image_misc, u"output//Recovered" + file_name_without_ext + u".bmp")

            ORIGINAL_IMAGE = "original//" + split_name[0][5:] + ".bmp"
            Oimg_misc = misc.imread(ORIGINAL_IMAGE)
            Oimg = Oimg_misc.tolist()
            if Oimg == self.image:
                pass
            else:
                print "Recover error!"


def NCC(img1, img2):
    sum = 0
    sum2 = 0
    for i in range(len(img2)):
        for j in range(len(img2[0])):
            sum += img1[i][j]
            sum2 += img2[i][j]
    mean = float(sum) / (len(img1) * len(img1[0]))
    mean2 = float(sum2) / (len(img2) * len(img2[0]))

    sum = 0
    sum2 = 0
    for i in range(len(img2)):
        for j in range(len(img2[0])):
            sum += (img1[i][j] - mean) ** 2
            sum2 += (img2[i][j] - mean2) ** 2

    mother = math.sqrt(sum * sum2)

    sum = 0
    for i in range(len(img2)):
        for j in range(len(img2[0])):
            sum += (img1[i][j] - mean) * (img2[i][j] - mean2)
    return sum / mother

def path_list_sort(path_list):
    path_list.sort(key=(
        lambda x: int(x.split(",")[2].split(".")[0])
    ))
    path_list.sort(key=(
        lambda x: int(x.split(",")[1])
    ))
    path_list.sort(key=(
        lambda x: x.split(",")[0]
    ))


def name_analysis(image):
    # file_name_without_extension suffix
    global file_name_without_ext, split_name
    file_name_without_ext = os.path.splitext(os.path.basename(image))[0]
    if file_name_without_ext[0:5] == "Stego":
        data_file = file(os.path.split(image)[0] + u"\\" + file_name_without_ext[5:] + ".data", 'r')
    elif file_name_without_ext[0:8] == "Tampered":
        data_file = file(os.path.split(image)[0] + u"\\" + file_name_without_ext[13:] + ".data", 'r')
    random_seed, over_or_under_flow = Pickle.load(data_file)
    data_file.close()
    split_name = file_name_without_ext.split(",")

    # return THRESHOLD, T*, random_seed, over_or_under_flow
    return int(split_name[1]), int(split_name[2]), random_seed, over_or_under_flow


def main(block_size):
    # tampered img path list
    tampered_list = filter(lambda path:
                           path if path[0:8] == "Tampered" else None,
                           os.listdir("output"))
    stego_list = filter(lambda path:
                        path if path[0:5] == "Stego" else None,
                        os.listdir("output"))
    merge_list = tampered_list + stego_list
    path_list_sort(merge_list)
    result_list = []

    for path in merge_list:
        # path = u"output\\StegoLena,5,2.bmp"
        path = "output//" + path
        threshold, t_star, random_seed, over_or_under_flow = name_analysis(path)

        extract_obj = Recover(path, threshold, t_star, random_seed, over_or_under_flow, block_size)
        return_value = extract_obj.extract()

        # Detected image, not a stego
        if return_value:
            result_list += [return_value]
    return result_list


if __name__ == '__main__':
    main(2)











