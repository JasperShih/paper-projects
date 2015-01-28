__author__ = 'Jasper'

import unittest
import copy
import PThree


class EmbedTest(unittest.TestCase):
    IMAGE = [[126, 119, 115, 116, 121, 179, 220, 207, 200, 186, 179, 154, 141, 133],
             [121, 120, 117, 115, 120, 175, 216, 209, 196, 183, 164, 144, 148, 135],
             [119, 116, 115, 116, 124, 193, 215, 203, 191, 178, 158, 150, 141, 145],
             [121, 117, 114, 116, 141, 210, 211, 200, 194, 163, 163, 150, 147, 148],
             [115, 114, 116, 117, 153, 212, 209, 202, 191, 160, 157, 156, 153, 141],
             [113, 109, 118, 119, 163, 211, 209, 199, 189, 171, 165, 160, 147, 136],
             [115, 113, 110, 122, 181, 216, 204, 196, 182, 178, 166, 151, 150, 144],
             [115, 114, 111, 131, 204, 214, 205, 196, 184, 173, 163, 159, 150, 149],
             [109, 113, 115, 142, 205, 210, 207, 196, 192, 164, 169, 166, 151, 145],
             [109, 109, 110, 154, 207, 207, 205, 196, 182, 166, 180, 168, 148, 149],
             [111, 110, 116, 170, 213, 213, 204, 192, 179, 178, 170, 160, 153, 152],
             [113, 113, 123, 187, 214, 207, 201, 189, 183, 181, 163, 165, 157, 153],
             [113, 115, 130, 192, 220, 207, 200, 196, 180, 171, 176, 163, 155, 151],
             [111, 115, 131, 203, 220, 204, 200, 195, 173, 181, 184, 160, 152, 156]]

    THRESHOLD = 50
    T_STAR = 2

    BLOCK_SIZE = 3

    embed_obj = None

    # Setting up before any test cases run
    def setUp(self):
        pass

    # Tear down after any test cases end
    def tearDown(self):
        pass

    # If we want to verify this test,
    # change throughout_image_by_block method
    # by hand before test
    def test_throughout_image_by_block(self):
        blocks_star = [126, 116, 220, 186, 121, 116, 211, 163, 115, 122, 204, 178, 109, 154, 205, 166]
        # Throughout entire Img block by block
        buf = []
        # ===============Throughout_image_by_block method=============v
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(self.IMAGE[row][col])
        # ===============Throughout_image_by_block method end=========^
        self.assertEqual(buf, blocks_star)

    def test_corner_classify(self):
        complex_answer = [22, 154, 58, 72, 24, 190, 44, 42, 22, 188, 50, 58, 28, 106, 46, 36]
        self.embed_obj = PThree.Embed(copy.deepcopy(self.IMAGE), self.THRESHOLD, self.T_STAR)
        buf = []

        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(
                    self.embed_obj.corner_classify(row, col)
                )

        self.assertEqual(buf, complex_answer)


    def test_hide_smooth(self):
        image_answer = [[126, 119, 115, 116, 123, 179, 220, 206, 200, 186, 182, 154, 141, 133],
                        [123, 120, 115, 113, 120, 178, 219, 209, 194, 186, 164, 142, 148, 135],
                        [119, 114, 115, 116, 127, 193, 215, 201, 191, 178, 156, 150, 141, 145],
                        [121, 120, 114, 116, 139, 210, 211, 199, 194, 163, 166, 150, 147, 148],
                        [117, 114, 118, 115, 153, 215, 212, 202, 189, 163, 157, 155, 153, 141],
                        [113, 107, 118, 119, 166, 211, 209, 197, 189, 171, 168, 160, 147, 136],
                        [115, 113, 110, 122, 179, 216, 204, 197, 182, 178, 169, 151, 150, 144],
                        [117, 114, 109, 129, 204, 217, 208, 196, 182, 176, 163, 157, 150, 149],
                        [109, 112, 115, 142, 206, 210, 207, 196, 192, 164, 172, 166, 151, 145],
                        [109, 109, 110, 154, 205, 207, 205, 199, 182, 166, 183, 168, 148, 149],
                        [113, 110, 119, 168, 213, 213, 207, 192, 177, 181, 170, 158, 153, 152],
                        [113, 116, 123, 187, 215, 207, 201, 187, 183, 181, 161, 165, 157, 153],
                        [113, 115, 130, 192, 220, 207, 200, 196, 180, 171, 176, 163, 155, 151],
                        [111, 115, 131, 203, 220, 204, 200, 195, 173, 181, 184, 160, 152, 156]]
        # We set self.THRESHOLD = 255 rather than self.THRESHOLD = 50.
        # It is because if self.THRESHOLD = 50,
        # we have to decide to do smooth_hide or complex_hide.
        # But we just want to test smooth_hide.
        # We don't want to combine complexity classify function
        self.THRESHOLD = 255
        self.embed_obj = PThree.Embed(copy.deepcopy(self.IMAGE), self.THRESHOLD, self.T_STAR)
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                self.embed_obj.hide_smooth(row, col, "1010")

        self.assertEqual(self.embed_obj.image, image_answer)

    def test_hide_complex(self):
        image_answer = [[126, 119, 115, 116, 123, 179, 220, 206, 200, 186, 182, 154, 141, 133],
                        [121, 120, 117, 115, 120, 175, 216, 209, 196, 183, 164, 144, 148, 135],
                        [119, 114, 115, 116, 127, 193, 215, 201, 191, 178, 156, 150, 141, 145],
                        [121, 117, 114, 116, 139, 210, 211, 199, 194, 163, 166, 150, 147, 148],
                        [117, 114, 118, 117, 153, 212, 209, 202, 191, 160, 157, 156, 153, 141],
                        [113, 109, 118, 119, 166, 211, 209, 197, 189, 171, 168, 160, 147, 136],
                        [115, 113, 110, 122, 179, 216, 204, 197, 182, 178, 166, 151, 150, 144],
                        [117, 114, 109, 131, 204, 214, 205, 196, 184, 176, 163, 157, 150, 149],
                        [109, 113, 115, 142, 206, 210, 207, 196, 192, 164, 169, 166, 151, 145],
                        [109, 109, 110, 154, 205, 207, 205, 199, 182, 166, 180, 168, 148, 149],
                        [113, 110, 119, 170, 213, 213, 204, 192, 179, 181, 170, 158, 153, 152],
                        [113, 113, 123, 187, 215, 207, 201, 187, 183, 181, 163, 165, 157, 153],
                        [113, 115, 130, 192, 220, 207, 200, 196, 180, 171, 176, 163, 155, 151],
                        [111, 115, 131, 203, 220, 204, 200, 195, 173, 181, 184, 160, 152, 156]]
        vertical_horizontal_difference = [[7, 15], [14, 140], [14, 44], [12, 60], [12, 12], [4, 186], [7, 37], [18, 24],
                                          [11, 11], [26, 162], [13, 37], [29, 29], [17, 11], [33, 73], [5, 41],
                                          [18, 18]]

        # We set self.THRESHOLD = -1 rather than self.THRESHOLD = 50.
        # It is because if self.THRESHOLD = 50,
        # we have to decide to do smooth_hide or complex_hide.
        # But we just want to test smooth_hide.
        # We don't want to combine complexity classify function
        self.THRESHOLD = -1
        self.embed_obj = PThree.Embed(copy.deepcopy(self.IMAGE), self.THRESHOLD, self.T_STAR)
        count = 0
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                self.embed_obj.vertical_difference = vertical_horizontal_difference[count][0]
                self.embed_obj.horizontal_difference = vertical_horizontal_difference[count][1]
                self.embed_obj.hide_complex(row, col, "1010")
                count += 1


        self.assertEqual(self.embed_obj.image, image_answer)


if __name__ == '__main__':
    unittest.main()
