__author__ = 'Jasper'
import unittest
import POne


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
    IMAGE2 = [[126, 119, 115, 116, 121, 179, 220, 207, 200, 186, 179, 154, 141, 133],
              [121, 120, 117, 115, 120, 175, 216, 209, 196, 183, 164, 144, 148],
              [119, 116, 115, 116, 124, 193, 215, 203, 191, 178, 158, 150, 141],
              [121, 117, 114, 116, 141, 210, 211, 200, 194, 163, 163, 150, 147],
              [115, 114, 116, 117, 153, 212, 209, 202, 191, 160, 157, 156, 153],
              [113, 109, 118, 119, 163, 211, 209, 199, 189, 171, 165, 160, 147],
              [115, 113, 110, 122, 181, 216, 204, 196, 182, 178, 166, 151, 150],
              [115, 114, 111, 131, 204, 214, 205, 196, 184, 173, 163, 159, 150],
              [109, 113, 115, 142, 205, 210, 207, 196, 192, 164, 169, 166, 151],
              [109, 109, 110, 154, 207, 207, 205, 196, 182, 166, 180, 168, 148],
              [111, 110, 116, 170, 213, 213, 204, 192, 179, 178, 170, 160, 153],
              [113, 113, 123, 187, 214, 207, 201, 189, 183, 181, 163, 165, 157],
              [113, 115, 130, 192, 220, 207, 200, 196, 180, 171, 176, 163, 155]]
    IMAGE3 = [[126, 119, 115, 116, 121, 179, 220, 207, 200, 186, 179, 154],
              [121, 120, 117, 115, 120, 175, 216, 209, 196, 183, 164, 144],
              [119, 116, 115, 116, 124, 193, 215, 203, 191, 178, 158, 150],
              [121, 117, 114, 116, 141, 210, 211, 200, 194, 163, 163, 150],
              [115, 114, 116, 117, 153, 212, 209, 202, 191, 160, 157, 156],
              [113, 109, 118, 119, 163, 211, 209, 199, 189, 171, 165, 160],
              [115, 113, 110, 122, 181, 216, 204, 196, 182, 178, 166, 151],
              [115, 114, 111, 131, 204, 214, 205, 196, 184, 173, 163, 159],
              [109, 113, 115, 142, 205, 210, 207, 196, 192, 164, 169, 166],
              [109, 109, 110, 154, 207, 207, 205, 196, 182, 166, 180, 168],
              [111, 110, 116, 170, 213, 213, 204, 192, 179, 178, 170, 160],
              [113, 113, 123, 187, 214, 207, 201, 189, 183, 181, 163, 165]]
    THRESHOLD = 50
    T_STAR = 2
    MAX_OR_RANGE = 0  # 0=max; 1=range

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

    def test_get_satellites(self):
        satellites_answer = [[None, 114, 120, None],
                             [None, 153, 209, 120],
                             [None, 202, 164, 120],
                             [None, 157, None, 209],
                             [120, 114, 153, None],
                             [120, 204, 202, 114],
                             [209, 196, 157, 153],
                             [164, 163, None, 202],
                             [114, 110, 204, None],
                             [153, 213, 196, 114],
                             [202, 192, 163, 204],
                             [157, 170, None, 196],
                             [114, None, 213, None],
                             [204, None, 192, 110],
                             [196, None, 170, 213],
                             [163, None, None, 192]]
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(self.embed_obj.get_satellites(row, col))
        self.assertEqual(buf, satellites_answer)

    def test_get_satellites2(self):
        satellites_answer = [[None, 114, 120, None],
                             [None, 153, 209, 120],
                             [None, 202, 164, 120],
                             [None, 157, None, 209],
                             [120, 114, 153, None],
                             [120, 204, 202, 114],
                             [209, 196, 157, 153],
                             [164, 163, None, 202],
                             [114, 110, 204, None],
                             [153, 213, 196, 114],
                             [202, 192, 163, 204],
                             [157, 170, None, 196],
                             [114, None, 213, None],
                             [204, None, 192, 110],
                             [196, None, 170, 213],
                             [163, None, None, 192]]
        self.embed_obj = POne.Embed(self.IMAGE2, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        for row in xrange(0,
                          len(self.IMAGE2) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE2[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(self.embed_obj.get_satellites(row, col))
        self.assertEqual(buf, satellites_answer)

    def test_get_satellites3(self):
        satellites_answer = [[None, 114, 120, None],
                             [None, 153, 209, 120],
                             [None, 202, 164, 120],
                             [None, 157, None, 209],
                             [120, 114, 153, None],
                             [120, 204, 202, 114],
                             [209, 196, 157, 153],
                             [164, 163, None, 202],
                             [114, 110, 204, None],
                             [153, 213, 196, 114],
                             [202, 192, 163, 204],
                             [157, 170, None, 196],
                             [114, None, 213, None],
                             [204, None, 192, 110],
                             [196, None, 170, 213],
                             [163, None, None, 192]]
        self.embed_obj = POne.Embed(self.IMAGE3, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        for row in xrange(0,
                          len(self.IMAGE3) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE3[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(self.embed_obj.get_satellites(row, col))
        self.assertEqual(buf, satellites_answer)

    def test_max_classify(self):
        input_satellites = [[None, 114, 120, None],
                            [None, 153, 209, 120],
                            [None, 202, 164, 120],
                            [None, 157, None, 209],
                            [120, 114, 153, None],
                            [120, 204, 202, 114],
                            [209, 196, 157, 153],
                            [164, 163, None, 202],
                            [114, 110, 204, None],
                            [153, 213, 196, 114],
                            [202, 192, 163, 204],
                            [157, 170, None, 196],
                            [114, None, 213, None],
                            [204, None, 192, 110],
                            [196, None, 170, 213],
                            [163, None, None, 192]]
        complexity_answer = ["smooth", "complex", "complex", "smooth", "smooth", "complex", "smooth", "smooth",
                             "complex", "complex", "smooth", "smooth", "complex", "complex", "smooth", "smooth"]
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        count = 0
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(
                    self.embed_obj.max_classify(row, col, input_satellites[count])
                )
                count += 1
        self.assertEqual(buf, complexity_answer)

    def test_max_classify(self):
        input_satellites = [[None, 114, 120, None],
                            [None, 153, 209, 120],
                            [None, 202, 164, 120],
                            [None, 157, None, 209],
                            [120, 114, 153, None],
                            [120, 204, 202, 114],
                            [209, 196, 157, 153],
                            [164, 163, None, 202],
                            [114, 110, 204, None],
                            [153, 213, 196, 114],
                            [202, 192, 163, 204],
                            [157, 170, None, 196],
                            [114, None, 213, None],
                            [204, None, 192, 110],
                            [196, None, 170, 213],
                            [163, None, None, 192]]
        complexity_answer = ["smooth", "complex", "complex", "complex", "smooth", "complex", "complex", "smooth",
                             "complex", "complex", "smooth", "smooth", "complex", "complex", "smooth", "smooth"]
        self.MAX_OR_RANGE = 1
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        count = 0
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(
                    self.embed_obj.range_classify(input_satellites[count])
                )
                count += 1
        self.assertEqual(buf, complexity_answer)

    def test_hide_smooth(self):
        image_answer = [[126, 119, 115, 116, 121, 179, 220, 207, 200, 186, 179, 154, 141, 133],
                        [123, 120, 115, 113, 120, 178, 219, 209, 194, 186, 164, 142, 148, 135],
                        [119, 116, 115, 116, 124, 193, 215, 203, 191, 178, 158, 150, 141, 145],
                        [121, 117, 114, 116, 141, 210, 211, 200, 194, 163, 163, 150, 147, 148],
                        [117, 114, 119, 115, 153, 215, 212, 202, 189, 163, 157, 156, 153, 141],
                        [113, 109, 118, 119, 163, 211, 209, 199, 189, 171, 165, 160, 147, 136],
                        [115, 113, 110, 122, 181, 216, 204, 196, 182, 178, 166, 151, 150, 144],
                        [117, 114, 109, 129, 204, 217, 208, 196, 182, 176, 163, 157, 150, 149],
                        [109, 113, 115, 142, 205, 210, 207, 196, 192, 164, 169, 166, 151, 145],
                        [109, 109, 110, 154, 207, 207, 205, 196, 182, 166, 180, 168, 148, 149],
                        [113, 110, 119, 168, 213, 214, 207, 192, 177, 181, 170, 158, 153, 152],
                        [113, 113, 123, 187, 214, 207, 201, 189, 183, 181, 163, 165, 157, 153],
                        [113, 115, 130, 192, 220, 207, 200, 196, 180, 171, 176, 163, 155, 151],
                        [111, 115, 131, 203, 220, 204, 200, 195, 173, 181, 184, 160, 152, 156]]
        # We set self.THRESHOLD = 255 rather than self.THRESHOLD = 50.
        # It is because if self.THRESHOLD = 50,
        # we have to decide to do smooth_hide or complex_hide.
        # But we just want to test smooth_hide.
        # We don't want to combine complexity classify function
        self.THRESHOLD = 255
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                self.embed_obj.hide_smooth(row, col, "11")
        self.assertEqual(self.embed_obj.image, image_answer)

    def test_get_adjacent_2blocks_and_bias(self):
        # [SU, SD, SR, SL]l
        input_satellites = [[None, 114, 120, None],
                            [None, 153, 209, 120],
                            [None, 202, 164, 120],
                            [None, 157, None, 209],
                            [120, 114, 153, None],
                            [120, 204, 202, 114],
                            [209, 196, 157, 153],
                            [164, 163, None, 202],
                            [114, 110, 204, None],
                            [153, 213, 196, 114],
                            [202, 192, 163, 204],
                            [157, 170, None, 196],
                            [114, None, 213, None],
                            [204, None, 192, 110],
                            [196, None, 170, 213],
                            [163, None, None, 192]]
        satellites_answer = [[114, 120], [209, 120], [164, 120], [157, 209], [120, 114], [202, 114], [157, 153],
                             [164, 163], [114, 110], [196, 114], [163, 204], [157, 170], [114, 213], [192, 110],
                             [170, 213], [163, 192]]
        bias_answer = [[[1, 0], [0, 1]], [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[1, 0], [0, -1]], [[-1, 0], [1, 0]],
                       [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[-1, 0], [1, 0]], [[-1, 0], [1, 0]], [[0, 1], [0, -1]],
                       [[0, 1], [0, -1]], [[-1, 0], [1, 0]], [[-1, 0], [0, 1]], [[0, 1], [0, -1]], [[0, 1], [0, -1]],
                       [[-1, 0], [0, -1]]]

        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        buf2 = []
        for sat in input_satellites:
            tem, tem2 = self.embed_obj.get_adjacent_2blocks_and_bias(sat)
            buf.append(tem)
            buf2.append(tem2)
        self.assertEqual(buf, satellites_answer)
        self.assertEqual(buf2, bias_answer)

    def test_get_stars(self):
        input_adjacent_2blocks = [[114, 120], [209, 120], [164, 120], [157, 209], [120, 114], [202, 114], [157, 153],
                                  [164, 163], [114, 110], [196, 114], [163, 204], [157, 170], [114, 213], [192, 110],
                                  [170, 213], [163, 192]]

        stars_answer = [[118, 120, 0], [149, 120, 0], [194, 179, 15], [161, 179, 3], [116, 114, 0], [169, 140, 13],
                        [187, 185, 15], [159, 159, 2], [114, 112, 0], [201, 174, 3], [185, 198, 2], [161, 165, 2],
                        [111, 144, 1], [206, 178, 7], [184, 199, 7], [167, 177, 3]]
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        buf = []
        count = 0
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(
                    self.embed_obj.get_stars(row, col, input_adjacent_2blocks[count])
                )
                count += 1
        self.assertEqual(buf, stars_answer)

    def test_get_lr_locate_d(self):
        input_location_bias = [[[1, 0], [0, 1]], [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[1, 0], [0, -1]],
                               [[-1, 0], [1, 0]], [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[-1, 0], [1, 0]],
                               [[-1, 0], [1, 0]], [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[-1, 0], [1, 0]],
                               [[-1, 0], [0, 1]], [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[-1, 0], [0, -1]]]

        lr_locate_d_answer = [[(2, 1), (1, 2), -4, -3], [(1, 5), (1, 3), 55, -5], [(1, 8), (1, 6), -13, 7],
                              [(2, 10), (1, 9), -6, 19], [(3, 1), (5, 1), 3, -5], [(4, 5), (4, 3), 59, -36],
                              [(4, 8), (4, 6), -11, 7], [(3, 10), (5, 10), 6, 8], [(6, 1), (8, 1), -1, -1],
                              [(7, 5), (7, 3), 10, -73], [(7, 8), (7, 6), -12, 9], [(6, 10), (8, 10), 3, 6],
                              [(9, 1), (10, 2), -1, 6], [(10, 5), (10, 3), 0, -43], [(10, 8), (10, 6), -13, 12],
                              [(9, 10), (10, 9), 10, 8]]
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)
        count = 0
        buf = []
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                buf.append(
                    self.embed_obj.get_lr_locate_d(row, col, input_location_bias[count])
                )
                count += 1
        self.assertEqual(buf, lr_locate_d_answer)

    def test_hide_complex(self):
        input_satellites = [[None, 114, 120, None],
                            [None, 153, 209, 120],
                            [None, 202, 164, 120],
                            [None, 157, None, 209],
                            [120, 114, 153, None],
                            [120, 204, 202, 114],
                            [209, 196, 157, 153],
                            [164, 163, None, 202],
                            [114, 110, 204, None],
                            [153, 213, 196, 114],
                            [202, 192, 163, 204],
                            [157, 170, None, 196],
                            [114, None, 213, None],
                            [204, None, 192, 110],
                            [196, None, 170, 213],
                            [163, None, None, 192]]
        image_answer = [[126, 119, 115, 116, 121, 179, 220, 207, 200, 186, 179, 154, 141, 133],
                        [121, 120, 115, 113, 120, 178, 199, 209, 179, 183, 164, 144, 148, 135],
                        [119, 114, 115, 116, 124, 193, 215, 203, 191, 178, 153, 150, 141, 145],
                        [121, 120, 114, 116, 141, 210, 211, 200, 194, 163, 164, 150, 147, 148],
                        [115, 114, 116, 102, 153, 202, 192, 202, 174, 160, 157, 156, 153, 141],
                        [113, 107, 118, 119, 163, 211, 209, 199, 189, 171, 166, 160, 147, 136],
                        [115, 112, 110, 122, 181, 216, 204, 196, 182, 178, 165, 151, 150, 144],
                        [115, 114, 111, 126, 204, 214, 206, 196, 180, 173, 163, 159, 150, 149],
                        [109, 113, 115, 142, 205, 210, 207, 196, 192, 164, 170, 166, 151, 145],
                        [109, 106, 110, 154, 207, 207, 205, 196, 182, 166, 180, 168, 148, 149],
                        [111, 110, 118, 161, 213, 204, 200, 192, 170, 178, 170, 160, 153, 152],
                        [113, 113, 123, 187, 214, 207, 201, 189, 183, 181, 163, 165, 157, 153],
                        [113, 115, 130, 192, 220, 207, 200, 196, 180, 171, 176, 163, 155, 151],
                        [111, 115, 131, 203, 220, 204, 200, 195, 173, 181, 184, 160, 152, 156]]
        # We set self.THRESHOLD = 0 rather than self.THRESHOLD = 50.
        # It is because if self.THRESHOLD = 50,
        # we have to decide to do smooth_hide or complex_hide.
        # But we just want to test smooth_hide.
        # We don't want to combine complexity classify function
        self.THRESHOLD = 0
        self.embed_obj = POne.Embed(self.IMAGE, self.THRESHOLD, self.T_STAR, self.MAX_OR_RANGE)

        count = 0
        for row in xrange(0,
                          len(self.IMAGE) - self.BLOCK_SIZE + 1,
                          self.BLOCK_SIZE):
            for col in xrange(0,
                              len(self.IMAGE[0]) - self.BLOCK_SIZE + 1,
                              self.BLOCK_SIZE):
                self.embed_obj.hide_complex(row, col, input_satellites[count], "01")
                count += 1

        self.assertEqual(self.embed_obj.image, image_answer)


"""
    def test_max_classify(self):
        self.assertEqual(self.embed_obj.max_classify(SATELLITES), COMPLEXITY)

    def test_range_classify(self):
        self.assertEqual(self.embed_obj.range_classify(SATELLITES), COMPLEXITY)

    def test_smooth_hide(self):
        self.assertEqual(self.embed_obj.smooth_hide(BLOCK), STEGO_BLOCK)

    def test_complex_hide(self):
        self.assertEqual(self.embed_obj.complex_hide(BLOCK), STEGO_BLOCK)
"""

if __name__ == '__main__':
    unittest.main()























