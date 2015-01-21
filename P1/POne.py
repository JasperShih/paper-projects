__author__ = 'Jasper'

import math
import copy
import random

import scipy.misc as misc


class IgnoreOutIndex:
    def __init__(self):
        pass

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception_value, exception_traceback):
        return True


class Embed():
    THRESHOLD = None  # Th
    T_STAR = None  # T*
    MAX_OR_RANGE = None

    BLOCK_SIZE = 3
    MID = (1, 1)

    image = None
    copy_image = None
    capacity_blocks = 0
    capacity_bits = 0
    over_or_under_flow = []

    # all_smooth_blocks in the image, no matter it can be embed or not
    all_smooth_blocks = 0
    all_complex_blocks = 0

    # all_embeddable_smooth_blocks in the image
    all_embeddable_smooth_blocks = 0
    all_embeddable_complex_blocks = 0

    def __init__(self, image, threshold, t_star, max_or_range):
        self.image = image
        self.copy_image = copy.deepcopy(self.image)
        self.THRESHOLD = threshold
        self.T_STAR = t_star
        self.MAX_OR_RANGE = max_or_range

    def get_satellites(self, row, col):
        # Get satellites. If IndexError occurs, the satellite=None
        # [SU, SD, SR, SL] are values, not indexes
        with IgnoreOutIndex() as SU:
            if (row + self.MID[0] - 3) >= 0:
                SU = self.image[row + self.MID[0] - 3][col + self.MID[1]]
        with IgnoreOutIndex() as SD:
            # not the bottom block
            if (row + 2 * self.BLOCK_SIZE) <= len(self.image):
                SD = self.image[row + self.MID[0] + 3][col + self.MID[1]]
        with IgnoreOutIndex() as SR:
            # not the most right block
            if (col + 2 * self.BLOCK_SIZE) <= len(self.image[0]):
                SR = self.image[row + self.MID[0]][col + self.MID[1] + 3]
        with IgnoreOutIndex() as SL:
            if (col + self.MID[1] - 3) >= 0:
                SL = self.image[row + self.MID[0]][col + self.MID[1] - 3]

        # return satellites
        return [SU, SD, SR, SL]

    def max_classify(self, row, col, satellites):
        buf = []
        # buf=(|SL-C|,|SR-C|,|SU-C|,|SD-C|)
        for sat in satellites:
            if sat:
                buf.append(abs(
                    sat - self.image[row + self.MID[0]][col + self.MID[1]]
                )
                )
        if max(buf) < self.THRESHOLD:
            return "smooth"
        else:
            return "complex"

    def range_classify(self, satellites):
        buf = []
        # buf=(SL,SR,SU,SD)
        for sat in satellites:
            if sat:
                buf.append(sat)

        dif = max(buf) - min(buf)
        if dif < self.THRESHOLD:
            return "smooth"
        else:
            return "complex"

    def hide_smooth(self, row, col, w):
        central_row = row + self.MID[0]
        central_col = col + self.MID[1]
        dL = self.image[central_row][central_col - 1] - self.image[central_row][central_col]
        dR = self.image[central_row][central_col + 1] - self.image[central_row][central_col]
        embeddable = 0

        if -self.T_STAR <= dL <= self.T_STAR:
            dLPrime = dL * 2 + int(w[0])
            self.capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > dL:
            dLPrime = dL - self.T_STAR
        elif self.T_STAR < dL:
            dLPrime = dL + self.T_STAR + 1

        if -self.T_STAR <= dR <= self.T_STAR:
            dRPrime = dR * 2 + int(w[1])
            self.capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > dR:
            dRPrime = dR - self.T_STAR
        elif self.T_STAR < dR:
            dRPrime = dR + self.T_STAR + 1

        if embeddable:
            self.capacity_blocks += 1

        self.image[central_row][central_col - 1] = dLPrime + self.image[central_row][central_col]
        if (self.image[central_row][central_col - 1] > 255) or (self.image[central_row][central_col - 1] < 0):
            print "overflow/underflow! 1"
            self.image[central_row][central_col - 1] = self.copy_image[central_row][central_col - 1]
            self.over_or_under_flow.append((central_row, central_col - 1))
        self.image[central_row][central_col + 1] = dRPrime + self.image[central_row][central_col]
        if (self.image[central_row][central_col + 1] > 255) or (self.image[central_row][central_col + 1] < 0):
            print "overflow/underflow! 2"
            self.image[central_row][central_col + 1] = self.copy_image[central_row][central_col + 1]
            self.over_or_under_flow.append((central_row, central_col + 1))

        return embeddable

    def get_adjacent_2blocks_and_bias(self, satellites):
        # [SU, SD, SR, SL]
        if (satellites[2] is not None) & (satellites[3] is not None):
            # return adjacent_2blocks, location_bias[SR, SL]
            return [satellites[2], satellites[3]], [[0, 1], [0, -1]]
        elif (satellites[0] is not None) & (satellites[1] is not None):
            # return adjacent_2blocks, location_bias[SU, SD]
            return [satellites[0], satellites[1]], [[-1, 0], [1, 0]]
        else:
            buf = []
            buf2 = []
            adjacent_block_bias = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            for idx in xrange(len(satellites)):
                if satellites[idx]:
                    buf.append(satellites[idx])
                    buf2.append(adjacent_block_bias[idx])
            return buf, buf2

    def get_stars(self, row, col, adjacent_2block):
        LStar = int(math.floor((self.image[row + self.MID[0]][col + self.MID[1]] * 2 + adjacent_2block[0]) / 3))
        RStar = int(math.floor((self.image[row + self.MID[0]][col + self.MID[1]] * 2 + adjacent_2block[1]) / 3))
        minStar = min(abs(LStar - self.image[row + self.MID[0]][col + self.MID[1]]),
                      abs(RStar - self.image[row + self.MID[0]][col + self.MID[1]]))
        return [LStar, RStar, minStar]

    def get_lr_locate_d(self, row, col, location_bias):
        Llocat = (row + self.MID[0] + location_bias[0][0],
                  col + self.MID[1] + location_bias[0][1])
        Rlocat = (row + self.MID[0] + location_bias[1][0],
                  col + self.MID[1] + location_bias[1][1])
        dL = self.image[Llocat[0]][Llocat[1]] - self.image[row + self.MID[0]][col + self.MID[1]]
        dR = self.image[Rlocat[0]][Rlocat[1]] - self.image[row + self.MID[0]][col + self.MID[1]]
        return [Llocat, Rlocat, dL, dR]


    def hide_complex(self, row, col, satellites, w):
        adjacent_2blocks, location_bias = self.get_adjacent_2blocks_and_bias(satellites)
        LStar, RStar, minStar = self.get_stars(row, col, adjacent_2blocks)
        Llocat, Rlocat, dL, dR = self.get_lr_locate_d(row, col, location_bias)
        dLStar = dL - minStar
        dRStar = dR - minStar

        embeddable = 0
        if -self.T_STAR <= dLStar <= self.T_STAR:
            dLPrime = dLStar * 2 + int(w[0])
            self.capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > dLStar:
            dLPrime = dLStar - self.T_STAR
        elif self.T_STAR < dLStar:
            dLPrime = dLStar + self.T_STAR + 1

        if -self.T_STAR <= dRStar <= self.T_STAR:
            dRPrime = dRStar * 2 + int(w[1])
            self.capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > dRStar:
            dRPrime = dRStar - self.T_STAR
        elif self.T_STAR < dRStar:
            dRPrime = dRStar + self.T_STAR + 1

        if embeddable == 1:
            self.capacity_blocks += 1


        # ======modify C this time=========
        self.image[Llocat[0]][Llocat[1]] = dLPrime + self.image[row + self.MID[0]][col + self.MID[1]]
        if (self.image[Llocat[0]][Llocat[1]] > 255) or (self.image[Llocat[0]][Llocat[1]] < 0):
            print "overflow/underflow! 3"
            self.image[Llocat[0]][Llocat[1]] = self.copy_image[Llocat[0]][Llocat[1]]
            self.over_or_under_flow.append((Llocat[0], Llocat[1]))

        self.image[Rlocat[0]][Rlocat[1]] = dRPrime + self.image[row + self.MID[0]][col + self.MID[1]]
        if (self.image[Rlocat[0]][Rlocat[1]] > 255) or (self.image[Rlocat[0]][Rlocat[1]] < 0):
            print "overflow/underflow! 4"
            self.image[Rlocat[0]][Rlocat[1]] = self.copy_image[Rlocat[0]][Rlocat[1]]
            self.over_or_under_flow.append((Rlocat[0], Rlocat[1]))

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
        print "TH:", self.THRESHOLD, "  T*:", self.T_STAR
        # generate a black image. Black(0) means un_embeddable_block.
        un_embeddable_block_image = [[0 for i in range(len(self.image))] for i in range(len(self.image[0]))]
        random_seed = random.random()
        random.seed(random_seed)

        image_row_bound = len(self.image) - self.BLOCK_SIZE + 1
        image_col_bound = len(self.image[0]) - self.BLOCK_SIZE + 1
        # Throughout entire Img block by block
        for row in xrange(0, image_row_bound, self.BLOCK_SIZE):
            for col in xrange(0, image_col_bound, self.BLOCK_SIZE):
                # Get satellites. If IndexError occurs, the satellite=None
                # [SU, SD, SR, SL] are values, not indexes
                satellites = self.get_satellites(row, col)

                # Complexity computing
                if MAX_OR_RANGE == 0:
                    complexity = self.max_classify(row, col, satellites)
                elif MAX_OR_RANGE == 1:
                    complexity = self.range_classify(satellites)

                # Hiding
                # we will set embeddable to 0/1 because complexity is either smooth or complex
                # i.e. we have to go through either smooth_hide or complex_hide.
                # And we will update embeddable value in hide function of every block

                w = str(random.randint(0, 1))
                w += str(random.randint(0, 1))
                if complexity == "smooth":
                    embeddable = self.hide_smooth(row, col, w)
                    self.all_smooth_blocks += 1
                    if embeddable:
                        self.all_embeddable_smooth_blocks += 1
                elif complexity == "complex":
                    embeddable = self.hide_complex(row, col, satellites, w)
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

        #print self.image
        #print "capacity_blocks:", str(self.capacity_blocks)
        print "capacity_bits:", str(self.capacity_bits)
        #print self.over_or_under_flow
        #print un_embeddable_block_image
        print "PSNR:" + str(self.PSNR(self.copy_image, self.image))
        # We have to save T*, THRESHOLD, seed, over_underflow

        print "all_smooth_blocks:", self.all_smooth_blocks
        print "all_embeddable_smooth_blocks:", self.all_embeddable_smooth_blocks
        print "all_complex_blocks:", self.all_complex_blocks
        print "all_embeddable_complex_blocks:", self.all_embeddable_complex_blocks
        print "====================================="


if __name__ == '__main__':
    IMAGE_LIST = "C:\\Users\\Jasper\\Desktop\\Lena.bmp"
    THRESHOLD_LIST = [40]
    T_STAR_LIST = [1]
    MAX_OR_RANGE = 0  # 0=max, 1=range

    img_misc = misc.imread(IMAGE_LIST)
    img_list = img_misc.tolist()

    for THRESHOLD in THRESHOLD_LIST:
        for T_STAR in T_STAR_LIST:
            embed_obj = Embed(copy.deepcopy(img_list), THRESHOLD, T_STAR, MAX_OR_RANGE)
            embed_obj.hide()











