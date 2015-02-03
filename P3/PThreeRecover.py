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

    def extract_complex(self, row, col):
        central_row = row + self.MID[0]
        central_col = col + self.MID[1]
        left_difference = self.image[central_row][central_col - 1] - self.image[central_row][central_col]
        right_difference = self.image[central_row][central_col + 1] - self.image[central_row][central_col]
        upper_difference = self.image[central_row - 1][central_col] - self.image[central_row][central_col]
        lower_difference = self.image[central_row + 1][central_col] - self.image[central_row][central_col]
        block_watermark = ""

        if self.vertical_difference >= self.horizontal_difference:
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
            # complete for upper, lower
            block_watermark += "**"

        elif self.vertical_difference < self.horizontal_difference:
            # complete for left, right
            block_watermark += "**"
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

    def refine(self, detectUnImg, blockSize):
        mark = 1
        while mark:
            mark = 0
            ReBCount = 0
            for bRowOfImg in range(0, len(detectUnImg), blockSize):
                for bColOfImg in range(0, len(detectUnImg[0]), blockSize):
                    if detectUnImg[bRowOfImg][bColOfImg] == 255:
                        # print bRowOfImg-blockSize,bColOfImg          ,bRowOfImg+blockSize,bColOfImg
                        mark += self.boundCheckPaint(
                            [bRowOfImg - blockSize, bColOfImg, bRowOfImg + blockSize, bColOfImg],
                            detectUnImg, bRowOfImg, bColOfImg, blockSize)

                        # print bRowOfImg          ,bColOfImg-blockSize,bRowOfImg          ,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg, bColOfImg - blockSize, bRowOfImg, bColOfImg + blockSize],
                            detectUnImg, bRowOfImg, bColOfImg, blockSize)

                        # print bRowOfImg-blockSize,bColOfImg-blockSize,bRowOfImg+blockSize,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg - blockSize, bColOfImg - blockSize, bRowOfImg + blockSize,
                             bColOfImg + blockSize],
                            detectUnImg, bRowOfImg, bColOfImg, blockSize)

                        # print bRowOfImg+blockSize,bColOfImg-blockSize,bRowOfImg-blockSize,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg + blockSize, bColOfImg - blockSize, bRowOfImg - blockSize,
                             bColOfImg + blockSize],
                            detectUnImg, bRowOfImg, bColOfImg, blockSize)
                    else:
                        ReBCount += 1
        return ReBCount, detectUnImg

    def black_block_count(self, image):
        count = 0
        for row in xrange(0, len(self.image) - self.BLOCK_SIZE + 1, self.BLOCK_SIZE):
            for col in xrange(0, len(self.image[0]) - self.BLOCK_SIZE + 1, self.BLOCK_SIZE):
                if image[row][col] == 0:
                    count += 1
        return count


    def extract(self):
        random.seed(self.RANDOM_SEED)
        image_row_bound = len(self.image) - self.BLOCK_SIZE + 1
        image_col_bound = len(self.image[0]) - self.BLOCK_SIZE + 1

        collected_watermark = ""
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

                # Smooth block
                if complexity <= self.THRESHOLD:
                    collected_watermark += self.extract_smooth(row, col)
                elif complexity > self.THRESHOLD:
                    collected_watermark += self.extract_complex(row, col)

        # Same as original image: white block
        # Different with original image: black block
        # Paint to black
        detect_image = [[255 for i in range(len(self.image))] for i in range(len(self.image[255]))]
        watermark = ""
        for i in xrange(
                                (len(self.image) / self.BLOCK_SIZE) *
                                (len(self.image[0]) / self.BLOCK_SIZE) * 4):
            watermark += str(random.randint(0, 1))

        tampered = 0
        count = 0
        for row in xrange(0, image_row_bound, self.BLOCK_SIZE):
            for col in xrange(0, image_col_bound, self.BLOCK_SIZE):
                tampered_block = 0
                for i in xrange(count, count + 4, 1):
                    if tampered_block == 1:
                        break
                    elif (watermark[i] == collected_watermark[i]) or \
                            (collected_watermark[i] == '*'):
                        pass
                    else:
                        tampered = 1
                        tampered_block = 1
                        for row_within_this_block in xrange(row, row + self.BLOCK_SIZE):
                            for col_within_this_block in xrange(col, col + self.BLOCK_SIZE):
                                detect_image[row_within_this_block][col_within_this_block] = 0
                count += 4

        if tampered == 1:
            # Save raw detected image
            for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = detect_image[row][col]
            misc.imsave(u"output//Detected" + file_name_without_ext[13:] + u".bmp", img_misc)
            print "Detected image generated."
            # Count blocks of detected image
            # Blocks of detected image
            blocks_detected_image = self.black_block_count(detect_image)
            # Count raw detected image NCC
            different_pixel_misc = misc.imread("output//DifferentPixel" +
                                               file_name_without_ext[13:] + ".bmp")
            different_pixel_img = different_pixel_misc.tolist()
            NCC_detected_image = NCC(detect_image, different_pixel_img)

            #  =======================Refine image=================================
            ReBCount, refined_detected_image = self.refine(detect_image, self.BLOCK_SIZE)
            #  Save refine detected image
            for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = refined_detected_image[row][col]
            misc.imsave(u"output//RefinedDetected" + file_name_without_ext[13:] + u".bmp", refined_detected_image)
            print "Refined detected image generated."
            #  Count blocks of detected image
            #  Blocks of refine_detected_image
            blocks_refine_detected_image = self.black_block_count(refined_detected_image)
            #  Count refine detected image NCC
            NCC_refine_detected_image = NCC(refined_detected_image, different_pixel_img)

            return [NCC_detected_image, NCC_refine_detected_image,
                    blocks_detected_image, blocks_refine_detected_image]

        elif tampered == 0:
            for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = self.image[row][col]
            misc.imsave(u"output//Recovered" + file_name_without_ext + u".bmp", img_misc)

            ORIGINAL_IMAGE = "original//" + split_name[0][5:] + ".bmp"
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


if __name__ == '__main__':
    # tampered img path list
    tampered_list = filter(lambda path:
                           path if path[0:8] == "Tampered" else None,
                           os.listdir("output"))
    stego_list = filter(lambda path:
                        path if path[0:5] == "Stego" else None,
                        os.listdir("output"))
    merge_list = tampered_list + stego_list
    path_list_sort(merge_list)
    file_name_without_ext = u""
    split_name = u""
    result_list = []

    print merge_list
    for path in merge_list:
        # path = u"output\\StegoLena,5,2.bmp"
        path = "output//" + path
        THRESHOLD, T_STAR, RANDOM_SEED, OVER_OR_UNDER_FLOW = name_analysis(path)
        img_misc = misc.imread(path)
        img = img_misc.tolist()

        recover_obj = Recover(copy.deepcopy(img), THRESHOLD, T_STAR, RANDOM_SEED, OVER_OR_UNDER_FLOW)
        return_value = recover_obj.extract()

        # Detected image, not a stego
        if return_value:
            result_list += [return_value]

    # Read summary list
    summary_file = file("summary.data", 'r')
    summary_list = Pickle.load(summary_file)
    summary_file.close()

    # Append data to summary list
    for idx in xrange(len(summary_list)):
        summary_list[idx] += result_list[idx]

    # Save summary list
    summary_file = file("summary.data", 'w')
    Pickle.dump(summary_list, summary_file)
    summary_file.close()

    # result = [image name, threshold, T_STAR,
    # capacity, over_or_under_flow_bits, PSNR,
    # different Pixel Count, different Block Count,
    # NCC of detected_image, NCC of refine_detected_image,
    # blocks of detected_image, blocks of refine_detected_image]

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    # Widen the first column to make the text clearer.
    worksheet.set_column('C:G', 9)
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 31)
    T_STAR_LEN = 5  # TODO

    worksheet.write(0, 1, "T*")
    for num in xrange(T_STAR_LEN):
        worksheet.write(0, 2 + num, summary_list[0 + num][2])

    t_star_count = 0
    th_count = 0
    for summary in summary_list:
        worksheet.write(1 + 9 * th_count, 2 + t_star_count, summary[3])
        worksheet.write(2 + 9 * th_count, 2 + t_star_count, summary[5])
        worksheet.write(3 + 9 * th_count, 2 + t_star_count, summary[8])
        worksheet.write(4 + 9 * th_count, 2 + t_star_count, summary[9])
        worksheet.write(5 + 9 * th_count, 2 + t_star_count, summary[4])
        worksheet.write(6 + 9 * th_count, 2 + t_star_count, summary[6])
        worksheet.write(7 + 9 * th_count, 2 + t_star_count, summary[7])
        worksheet.write(8 + 9 * th_count, 2 + t_star_count, summary[10])
        worksheet.write(9 + 9 * th_count, 2 + t_star_count, summary[11])
        t_star_count += 1

        #TH changed or first
        if t_star_count == T_STAR_LEN:
            worksheet.write(1 + 9 * th_count, 0, summary[0] + u", TH=" + str(summary[1]).decode("utf-8"))
            worksheet.write(1 + 9 * th_count, 1, "Capacity")
            worksheet.write(2 + 9 * th_count, 1, "PSNR")
            worksheet.write(3 + 9 * th_count, 1, "NCC of raw detected image")
            worksheet.write(4 + 9 * th_count, 1, "NCC of refine detected image")
            worksheet.write(5 + 9 * th_count, 1, "Overflow bits")
            worksheet.write(6 + 9 * th_count, 1, "Number of different pixels")
            worksheet.write(7 + 9 * th_count, 1, "Number of different blocks")
            worksheet.write(8 + 9 * th_count, 1, "Blocks of raw detected image")
            worksheet.write(9 + 9 * th_count, 1, "Blocks of refine detected image")
            t_star_count = 0
            th_count += 1

    workbook.close()
    print summary_list









