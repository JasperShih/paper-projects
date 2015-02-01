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
                        #print bRowOfImg-blockSize,bColOfImg          ,bRowOfImg+blockSize,bColOfImg
                        mark += self.boundCheckPaint([bRowOfImg - blockSize, bColOfImg, bRowOfImg + blockSize, bColOfImg],
                                                detectUnImg, bRowOfImg, bColOfImg, blockSize)

                        #print bRowOfImg          ,bColOfImg-blockSize,bRowOfImg          ,bColOfImg+blockSize
                        mark += self.boundCheckPaint([bRowOfImg, bColOfImg - blockSize, bRowOfImg, bColOfImg + blockSize],
                                                detectUnImg, bRowOfImg, bColOfImg, blockSize)

                        #print bRowOfImg-blockSize,bColOfImg-blockSize,bRowOfImg+blockSize,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg - blockSize, bColOfImg - blockSize, bRowOfImg + blockSize, bColOfImg + blockSize],
                            detectUnImg, bRowOfImg, bColOfImg, blockSize)

                        #print bRowOfImg+blockSize,bColOfImg-blockSize,bRowOfImg-blockSize,bColOfImg+blockSize
                        mark += self.boundCheckPaint(
                            [bRowOfImg + blockSize, bColOfImg - blockSize, bRowOfImg - blockSize, bColOfImg + blockSize],
                            detectUnImg, bRowOfImg, bColOfImg, blockSize)
                    else:
                        ReBCount += 1
        return ReBCount, detectUnImg

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
            for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = detect_image[row][col]
            misc.imsave(u"output//Detected" + file_name_without_ext + u".bmp", img_misc)
            print "Detected image generated."

            ReBCount, refined_detected_image = self.refine(detect_image, self.BLOCK_SIZE)
            for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = refined_detected_image[row][col]
            misc.imsave(u"output//RefinedDetected" + file_name_without_ext + u".bmp", refined_detected_image)
            print "Refined detected image generated."

            # TODO 還未算AC值

        elif tampered == 0:
            for row in xrange(len(self.image)):
                for col in xrange(len(self.image[0])):
                    img_misc[row][col] = self.image[row][col]
            misc.imsave(u"output//Recovered" + file_name_without_ext + u".bmp", img_misc)

            ORIGINAL_IMAGE = u"C:\\Users\\joker\\Desktop\\Img.bmp"
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
    global file_name_without_ext
    file_name_without_ext = os.path.splitext(os.path.basename(image))[0]
    data_file = file(os.path.split(image)[0] + u"\\" + file_name_without_ext[5:] + ".data", 'r')
    random_seed, over_or_under_flow = Pickle.load(data_file)
    data_file.close()
    tmp = file_name_without_ext.split(",")

    # return THRESHOLD, T*, random_seed, over_or_under_flow
    return int(tmp[1]), int(tmp[2]), random_seed, over_or_under_flow

if __name__ == '__main__':
    IMAGE_PATH = u"C:\\Users\\joker\\Desktop\\Pps\\P3\\output\\StegoImg,5,2.bmp"
    file_name_without_ext = u""
    THRESHOLD, T_STAR, RANDOM_SEED, OVER_OR_UNDER_FLOW = name_analysis(IMAGE_PATH)
    img_misc = misc.imread(IMAGE_PATH)
    img = img_misc.tolist()

    recover_obj = Recover(copy.deepcopy(img), THRESHOLD, T_STAR, RANDOM_SEED, OVER_OR_UNDER_FLOW)
    recover_obj.extract()
    # random.seed(rSeed)













