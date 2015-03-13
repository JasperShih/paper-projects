__author__ = 'Jasper'

import unittest
import copy
import PFour


class EmbedTest(unittest.TestCase):
    # Setting up before any test cases run
    def setUp(self):
        pass

    # Tear down after any test cases end
    def tearDown(self):
        pass

    # If we want to verify this test,
    # change throughout_image_by_chessboard method
    # by hand before test
    def test_throughout_image_by_chessboard(self):
        self.image = [[149, 151, 152, 149, 150, 153, 155, 157],
                      [147, 150, 149, 150, 152, 155, 157, 159],
                      [147, 148, 150, 153, 153, 153, 153, 154],
                      [151, 150, 150, 153, 154, 153, 153, 154],
                      [148, 150, 150, 151, 155, 155, 157, 159],
                      [145, 148, 149, 151, 154, 154, 153, 156],
                      [148, 153, 151, 153, 153, 152, 154, 155],
                      [144, 146, 148, 150, 150, 148, 152, 156]]
        BLACK_ANSWER = [149, 152, 150, 155, 150, 150, 155, 159, 147, 150, 153, 153, 150, 153, 153, 154, 148, 150, 155,
                        157, 148, 151, 154, 156, 148, 151, 153, 154, 146, 150, 148, 156]
        buf = []
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                buf += [self.image[row][col]]

        self.assertEqual(buf, BLACK_ANSWER)

    def test_get_four_adjacent_pixels(self):
        self.image = [[149, 151, 152, 149, 150, 153, 155, 157],
                      [147, 150, 149, 150, 152, 155, 157, 159],
                      [147, 148, 150, 153, 153, 153, 153, 154],
                      [151, 150, 150, 153, 154, 153, 153, 154],
                      [148, 150, 150, 151, 155, 155, 157, 159],
                      [145, 148, 149, 151, 154, 154, 153, 156],
                      [148, 153, 151, 153, 153, 152, 154, 155],
                      [144, 146, 148, 150, 150, 148, 152, 156]]
        FOUR_PIXELS_ANSWER = [[None, None, 151, 147], [None, 151, 149, 149], [None, 149, 153, 152],
                              [None, 153, 157, 157], [151, 147, 149, 148], [149, 149, 152, 153], [153, 152, 157, 153],
                              [157, 157, None, 154], [147, None, 148, 151], [149, 148, 153, 150], [152, 153, 153, 154],
                              [157, 153, 154, 153], [148, 151, 150, 150], [153, 150, 154, 151], [153, 154, 153, 155],
                              [154, 153, None, 159], [151, None, 150, 145], [150, 150, 151, 149], [154, 151, 155, 154],
                              [153, 155, 159, 153], [150, 145, 149, 153], [151, 149, 154, 153], [155, 154, 153, 152],
                              [159, 153, None, 155], [145, None, 153, 144], [149, 153, 153, 148], [154, 153, 152, 150],
                              [153, 152, 155, 152], [153, 144, 148, None], [153, 148, 150, None], [152, 150, 152, None],
                              [155, 152, None, None]]
        embed_obj = PFour.Embed(self.image, 50, 2)
        buf = []

        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                buf += [embed_obj.get_four_adjacent_pixels(row, col)]

        self.assertEqual(buf, FOUR_PIXELS_ANSWER)


if __name__ == '__main__':
    unittest.main()
