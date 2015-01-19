__author__ = 'Jasper'

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
    over_or_under_flow = []

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
        dL = self.image[central_row][central_col-1] - self.image[central_row][central_col]
        dR = self.image[central_row][central_col+1] - self.image[central_row][central_col]
        embeddable = 0
        capacity_bits = 0

        if -self.T_STAR <= dL <= self.T_STAR:
            dLPrime = dL * 2 + int(w[0])
            capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > dL:
            dLPrime = dL - self.T_STAR
        elif self.T_STAR < dL:
            dLPrime = dL + self.T_STAR + 1

        if -self.T_STAR <= dR <= self.T_STAR:
            dRPrime = dR * 2 + int(w[1])
            capacity_bits += 1
            embeddable = 1
        elif -self.T_STAR > dR:
            dRPrime = dR - self.T_STAR
        elif self.T_STAR < dR:
            dRPrime = dR + self.T_STAR + 1

        if embeddable:
            self.capacity_blocks += 1

        self.image[central_row][central_col-1] = dLPrime + self.image[central_row][central_col]
        if (self.image[central_row][central_col-1] > 255) or (self.image[central_row][central_col-1] < 0):
            print "overflow/underflow! 1"
            self.image[central_row][central_col-1] = self.copy_image[central_row][central_col-1]
            self.over_or_under_flow.append((central_row, central_col-1))
        self.image[central_row][central_col+1] = dRPrime + self.image[central_row][central_col]
        if (self.image[central_row][central_col+1] > 255) or (self.image[central_row][central_col+1] < 0):
            print "overflow/underflow! 2"
            self.image[central_row][central_col+1] = self.copy_image[central_row][central_col+1]
            self.over_or_under_flow.append((central_row, central_col+1))

    def hide(self):
        un_embeddable_block_image = [[255 for i in range(len(self.image))] for i in range(len(self.image[0]))]
        random_seed = random.random()
        random.seed(random_seed)


        image_row_bound = len(self.image) - self.BLOCK_SIZE + 1
        image_col_bound = len(self.image[0]) - self.BLOCK_SIZE + 1
        # Throughout entire Img block by block
        for row in xrange(0, image_row_bound, self.BLOCK_SIZE):
            for col in xrange(0, image_col_bound, self.BLOCK_SIZE):
                # Get satellites
                satellites = self.get_satellites(row, col)

                # Complexity computing
                if MAX_OR_RANGE == 0:
                    complexity = self.max_classify(row, col, satellites)
                elif MAX_OR_RANGE == 1:
                    complexity = self.range_classify(satellites)

                #Hiding
                #w = str(random.randint(0, 1))
                #w += str(random.randint(0, 1))
                w = "11"
                if complexity == "smooth":
                    self.hide_smooth(row, col, w)

        print self.image


if __name__ == '__main__':
    IMAGE_LIST = "C:\\Users\\Jasper\\Desktop\\debug.bmp"
    THRESHOLD_LIST = 50
    T_STAR_LIST = 2
    MAX_OR_RANGE = 0  # 0=max, 1=range

    img_misc = misc.imread(IMAGE_LIST)
    img_list = img_misc.tolist()

    embed_obj = Embed(img_list, THRESHOLD_LIST, T_STAR_LIST, MAX_OR_RANGE)
    embed_obj.hide()











