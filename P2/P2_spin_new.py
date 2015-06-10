__author__ = 'Jasper'

import math
import sys
import scipy.misc as misc, random
import matplotlib.pyplot as plt
import cPickle as Pickle


class omitOutIndex:
    def __init__(self):
        pass

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception_value, exception_traceback):
        return True


class Embed():
    def __init__(self, image_path, max_or_range, threshold,
                 t_star_smooth, t_star_complex, mul_smooth, mul_complex):
        self.image_path = image_path
        self.image_misc = misc.imread(image_path)
        self.image = self.image_misc.tolist()
        self.image_original = self.image_misc.tolist()
        self.threshold = threshold
        self.max_or_range = max_or_range  # maxOrRange 0:max 1:range
        self.t_star_smooth = t_star_smooth
        self.t_star_complex = t_star_complex
        self.mul_smooth = mul_smooth
        self.mul_complex = mul_complex

        self.overflow_bits = 0

        self.mid = (1, 1)
        self.block_size = 3


    def maxS(self, start, satellites, thresholdmaxS):
        buf = []
        # buf=(|SL-C|,|SR-C|,|SU-C|,|SD-C|)
        for sat in satellites:
            if sat:
                buf.append(abs(
                    sat - self.image[start[0] + self.mid[0]]
                    [start[1] + self.mid[1]]
                )
                )
        if max(buf) < thresholdmaxS:
            return "smooth"
        else:
            return "complex"

    def rangeS(self, satellites, thresholdrangeS):
        buf = []
        # buf=(SL,SR,SU,SD)
        for sat in satellites:
            if sat:
                buf.append(sat)

        dif = max(buf) - min(buf)
        if dif < thresholdrangeS:
            return "smooth"
        else:
            return "complex"

    def PSNR(self, oriNumImg, stegoImg):
        imgSize = len(oriNumImg) * len(oriNumImg)
        MSE = float(0)
        for row in xrange(len(oriNumImg)):
            for col in xrange(len(oriNumImg[0])):
                tem = oriNumImg[row][col] - stegoImg[row][col]
                MSE += tem * tem
        MSE /= imgSize
        psnr = 10 * math.log((255 * 255) / MSE, 10)
        return psnr

    def hiding(self):
        secret = ""
        # Count length of hidden secret bits (seqSmoothLen & seqComplexLen)
        # with different mulSmooth and mulComplex
        seqSmoothLen = 0
        tmp = self.mul_smooth + 1
        while tmp != 1:
            tmp /= 2
            seqSmoothLen += 1

        seqComplexLen = 0
        tmp = self.mul_complex + 1
        while tmp != 1:
            tmp /= 2
            seqComplexLen += 1


        for row in xrange(0, len(self.image) - self.block_size + 1, self.block_size):
            for col in xrange(0, len(self.image[0]) - self.block_size + 1, self.block_size):

                # Get satellites. If IndexError occurs, the satellite=None
                # [SU, SD, SR, SL] are values, not indexes
                with omitOutIndex() as SU:
                    if (row + self.mid[0] - 3) >= 0:
                        SU = self.image[row + self.mid[0] - 3][col + self.mid[1]]
                with omitOutIndex() as SD:
                    SD = self.image[row + self.mid[0] + 3][col + self.mid[1]]
                with omitOutIndex() as SR:
                    SR = self.image[row + self.mid[0]][col + self.mid[1] + 3]
                with omitOutIndex() as SL:
                    if (col + self.mid[1] - 3) >= 0:
                        SL = self.image[row + self.mid[0]][col + self.mid[1] - 3]
                satellites = [SU, SD, SR, SL]

                # max
                if self.max_or_range == 0:
                    complexity = self.maxS([row, col], satellites, self.threshold)
                # range
                elif self.max_or_range == 1:
                    complexity = self.rangeS(satellites, self.threshold)


                if complexity == "smooth":
                    for rowInBlock in xrange(row, row + self.block_size, 1):
                        for colInBlock in xrange(col, col + self.block_size, 1):
                            if rowInBlock == (row + self.mid[0]) and colInBlock == (col + self.mid[0]):
                                pass
                            else:
                                # ==================Spin dif Algo============================v
                                block_map_row = rowInBlock - row
                                block_map_col = colInBlock - col
                                if (block_map_row == 0 and
                                            block_map_col == 0):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock + 1]

                                elif (block_map_row == 0 and
                                              block_map_col == 1):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock + 1][colInBlock]

                                elif (block_map_row == 0 and
                                              block_map_col == 2):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock + 1][colInBlock]

                                elif (block_map_row == 1 and
                                              block_map_col == 0):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock + 1]

                                elif (block_map_row == 1 and
                                              block_map_col == 2):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock - 1]

                                elif (block_map_row == 2 and
                                              block_map_col == 0):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock - 1][colInBlock]

                                elif (block_map_row == 2 and
                                              block_map_col == 1):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock - 1][colInBlock]

                                elif (block_map_row == 2 and
                                              block_map_col == 2):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock - 1]

                                # ==================Spin dif Algo End========================^

                                embeddable = 0

                                if -self.t_star_smooth <= dif and dif <= self.t_star_smooth:
                                    seq = ""
                                    for lenIndex in xrange(seqSmoothLen):
                                        seq += str(random.randint(0, 1))
                                    secret += seq
                                    seq = int(seq, 2)
                                    dif = (self.mul_smooth + 1) * dif + seq
                                    embeddable = 1

                                elif dif < -self.t_star_smooth:
                                    dif = dif - self.mul_smooth * self.t_star_smooth

                                elif dif > self.t_star_smooth:
                                    dif = dif + (self.t_star_smooth + 1) * self.mul_smooth

                                # ==============spin new self.image Algo====================v
                                if block_map_row == 0 and block_map_col == 0:
                                    if 0 <= dif + self.image_original[rowInBlock][colInBlock + 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock][colInBlock + 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 0 and block_map_col == 1:
                                    if 0 <= dif + self.image_original[rowInBlock + 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock + 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 0 and block_map_col == 2:
                                    if 0 <= dif + self.image_original[rowInBlock + 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock + 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 1 and block_map_col == 0:
                                    if 0 <= dif + self.image_original[rowInBlock][colInBlock + 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock][colInBlock + 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 1 and block_map_col == 2:
                                    if 0 <= dif + self.image_original[rowInBlock][colInBlock - 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock][colInBlock - 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 2 and block_map_col == 0:
                                    if 0 <= dif + self.image_original[rowInBlock - 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock - 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 2 and block_map_col == 1:
                                    if 0 <= dif + self.image_original[rowInBlock - 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock - 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]

                                elif block_map_row == 2 and block_map_col == 2:
                                    if 0 <= dif + self.image_original[rowInBlock][colInBlock - 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif + self.image_original[rowInBlock][colInBlock - 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqSmoothLen]
                                        # ==============spin new imgList Algo=====================^

                elif complexity == "complex":
                    buf = []
                    for sat in satellites:
                        if sat:
                            buf.append(int(abs(
                                math.floor((3 * self.image[row + self.mid[0]][col + self.mid[1]] + sat) / 4 - \
                                    self.image[row + self.mid[0]][col + self.mid[1]])
                            )
                            )
                            )

                    minLambda = min(buf)

                    #print minLambda
                    for rowInBlock in xrange(row, row + self.block_size, 1):
                        for colInBlock in xrange(col, col + self.block_size, 1):
                            if rowInBlock == (row + self.mid[0]) and colInBlock == (col + self.mid[0]):
                                pass
                            else:
                                # ==================Spin dif Algo============================v
                                block_map_row = rowInBlock - row
                                block_map_col = colInBlock - col
                                if (block_map_row == 0 and
                                            block_map_col == 0):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock + 1]

                                elif (block_map_row == 0 and
                                              block_map_col == 1):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock + 1][colInBlock]

                                elif (block_map_row == 0 and
                                              block_map_col == 2):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock + 1][colInBlock]

                                elif (block_map_row == 1 and
                                              block_map_col == 0):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock + 1]

                                elif (block_map_row == 1 and
                                              block_map_col == 2):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock - 1]

                                elif (block_map_row == 2 and
                                              block_map_col == 0):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock - 1][colInBlock]

                                elif (block_map_row == 2 and
                                              block_map_col == 1):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock - 1][colInBlock]

                                elif (block_map_row == 2 and
                                              block_map_col == 2):
                                    dif = self.image_original[rowInBlock][colInBlock] - \
                                          self.image_original[rowInBlock][colInBlock - 1]

                                # ==================Spin dif Algo End========================^

                                dif_prime = dif - minLambda

                                embeddable = 0
                                if -self.t_star_complex <= dif_prime and dif_prime <= self.t_star_complex:
                                    seq = ""
                                    for lenIndex in xrange(seqComplexLen):
                                        seq += str(random.randint(0, 1))
                                    secret += seq
                                    seq = int(seq, 2)

                                    dif_double_prime = (self.mul_complex + 1) * dif_prime + seq
                                    embeddable = 1

                                elif dif_prime < -self.t_star_complex:
                                    dif_double_prime = dif_prime - self.mul_complex * self.t_star_complex

                                else:  # dif>TStarComplex
                                    dif_double_prime = dif_prime + (self.t_star_complex + 1) * self.mul_complex

                                dif_star = dif_double_prime + minLambda


                                # ==============spin new self.image Algo====================v
                                if block_map_row == 0 and block_map_col == 0:
                                    if 0 <= dif_star + self.image_original[rowInBlock][colInBlock + 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock][colInBlock + 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 0 and block_map_col == 1:
                                    if 0 <= dif_star + self.image_original[rowInBlock + 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock + 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 0 and block_map_col == 2:
                                    if 0 <= dif_star + self.image_original[rowInBlock + 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock + 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 1 and block_map_col == 0:
                                    if 0 <= dif_star + self.image_original[rowInBlock][colInBlock + 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock][colInBlock + 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 1 and block_map_col == 2:
                                    if 0 <= dif_star + self.image_original[rowInBlock][colInBlock - 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock][colInBlock - 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 2 and block_map_col == 0:
                                    if 0 <= dif_star + self.image_original[rowInBlock - 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock - 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 2 and block_map_col == 1:
                                    if 0 <= dif_star + self.image_original[rowInBlock - 1][colInBlock] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock - 1][colInBlock]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]

                                elif block_map_row == 2 and block_map_col == 2:
                                    if 0 <= dif_star + self.image_original[rowInBlock][colInBlock - 1] <= 255:
                                        self.image[rowInBlock][colInBlock] = \
                                            dif_star + self.image_original[rowInBlock][colInBlock - 1]
                                    else:
                                        self.overflow_bits += 1
                                        if embeddable:
                                            secret = secret[0:-seqComplexLen]
                                        # ==============spin new imgList Algo=====================^

        bbpList.append(float(len(secret)) /
                            (
                                len(self.image) * len(self.image[0])
                            )
        )
        PSNRList.append(self.PSNR(self.image_misc, self.image))

        return self.overflow_bits



def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def main():
    global bbpList, PSNRList
    bbpList = []
    PSNRList = []

    max_or_range = 0
    threshold_list = [4, 5, 6, 8, 10, 15, 20, 30, 40]

    mul_smooth_list = [1, 3, 7, 15]
    t_star_smooth_list = [2,3,4,6,8,10]

    mul_complex_list = [1, 3, 7, 15]
    t_star_complex_list = [0, 2, 4, 6, 8, 10]

    argument = []
    for threshold in threshold_list:
        for mul_smooth in mul_smooth_list:
            for t_star_smooth in t_star_smooth_list:
                for mul_complex in mul_complex_list:
                    for t_star_complex in t_star_complex_list:
                        embed_obj = Embed("C:\\Users\\Jasper\\Desktop\\image\\Baboon.bmp", max_or_range, threshold,
                                          t_star_smooth, t_star_complex, mul_smooth, mul_complex)
                        overflow_bits = embed_obj.hiding()
                        argument += [[max_or_range, threshold, t_star_smooth, t_star_complex,
                                      mul_smooth, mul_complex, overflow_bits]]
    """
    data_file = file("Lena.data", 'r')
    previous = Pickle.load(data_file)
    data_file.close()
    bbpList += previous[0]
    PSNRList += previous[1]
    argument += previous[2]
    """
    output_buf = [bbpList, PSNRList, argument]
    data_file = file(u"Baboon.data", 'w')
    Pickle.dump(output_buf, data_file)
    data_file.close()

    plt.xlim(0, 5)
    plt.xticks([tick for tick in frange(0, 5.1, 0.5)])
    plt.ylim(10, 60)
    plt.yticks([tick for tick in frange(10, 61, 5)])

    plt.xlabel("BBP")
    plt.ylabel("PSNR")
    plt.title("maxTH")

    plt.plot(bbpList, PSNRList, "ko")
    plt.show()


if __name__ == '__main__':
    main()