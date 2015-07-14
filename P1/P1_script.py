__author__ = 'Jasper'

import POne as P1
import scipy.misc as misc

import os
import copy
import xlsxwriter


os.chdir("C:\\Users\\Jasper\\Desktop\\kodim")

# C:\\Users\\Jasper\\Desktop\\kodim

IMAGE_LIST = os.listdir(".")
THRESHOLD_LIST = [50, 100, 150]
T_STAR_LIST = [0, 1, 2, 3, 4]
MAX_OR_RANGE = 0  # 0=max, 1=range

result_buf = []
for image in IMAGE_LIST:
    img_misc = misc.imread(image)
    img_list = img_misc.tolist()
    for THRESHOLD in THRESHOLD_LIST:
        for T_STAR in T_STAR_LIST:
            embed_obj = P1.Embed(copy.deepcopy(img_list), THRESHOLD, T_STAR, MAX_OR_RANGE)
            capcity, psnr = embed_obj.hide()
            result_buf += [[image, THRESHOLD, T_STAR, capcity, psnr]]

print result_buf



# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook("C:\\Users\\Jasper\\Desktop\\result.xlsx")
worksheet = workbook.add_worksheet()

# Set parameters
pic_row = 1
pic_col = 2
row_image_offset = len(IMAGE_LIST)
col_counter = 0
row_counter = 0

# Write capacity
for result in result_buf:
    if col_counter == len(T_STAR_LIST):
        col_counter = 0
        pic_row += row_image_offset + 1
        row_counter += 1
        if row_counter == len(THRESHOLD_LIST):
            pic_row %= row_image_offset + 1
            pic_row += 1
            row_counter = 0

    worksheet.write(pic_row, pic_col + col_counter, round(result[-1], 2))
    col_counter += 1

workbook.close()