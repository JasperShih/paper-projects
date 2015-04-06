__author__ = 'Jasper'

import PFour
import PFourTamper
import PFourRecover
import xlsxwriter

image_path = "original\\Lena.bmp"

threshold_list = [0,1,2,3,4,6,8,10,12,14,16]

t_star_list = [0,1,2,3]
rounds = 1
block_size = 4

result = []
for threshold in threshold_list:
    for t_star in t_star_list:
        result += [[image_path[9:-4], threshold, t_star]+PFour.Embed(image_path, threshold, t_star, rounds, block_size).hide()]
# 397, 251
# cat 20,20
buf1 = PFourTamper.main((20,20), block_size)
buf2 = PFourRecover.main(block_size)

for i in xrange(len(result)):
    result[i] += buf1[i]+buf2[i]+[block_size]


print result
# result = [image name, threshold, t_star, capacity, over_or_under_flow_bits,
# PSNR, different Pixel Count, different BlockCount, NCC of detected_image,
# NCC of refine_detected_image, blocks of detected_image, blocks of refine_detected_image]


def write_xlsx(input_result):
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 31)
    worksheet.set_column('C:G', 9)
    T_STAR_LEN = len(t_star_list)

    worksheet.write(0, 1, "T*")
    for num in xrange(T_STAR_LEN):
        worksheet.write(0, 2 + num, input_result[0 + num][2])

    t_star_count = 0
    th_count = 0
    for summary in input_result:
        worksheet.write(1 + 10 * th_count, 2 + t_star_count, summary[3])
        worksheet.write(2 + 10 * th_count, 2 + t_star_count, summary[5])
        worksheet.write(3 + 10 * th_count, 2 + t_star_count, summary[8])
        worksheet.write(4 + 10 * th_count, 2 + t_star_count, summary[9])
        worksheet.write(5 + 10 * th_count, 2 + t_star_count, summary[4])
        worksheet.write(6 + 10 * th_count, 2 + t_star_count, summary[6])
        worksheet.write(7 + 10 * th_count, 2 + t_star_count, summary[7])
        worksheet.write(8 + 10 * th_count, 2 + t_star_count, summary[10])
        worksheet.write(9 + 10 * th_count, 2 + t_star_count, summary[11])
        worksheet.write(10 + 10 * th_count, 2 + t_star_count, summary[12])
        t_star_count += 1

        #TH changed or first
        if t_star_count == T_STAR_LEN:
            worksheet.write(1 + 10 * th_count, 0, summary[0] + u", TH=" + str(summary[1]).decode("utf-8"))
            worksheet.write(1 + 10 * th_count, 1, "Capacity")
            worksheet.write(2 + 10 * th_count, 1, "PSNR")
            worksheet.write(3 + 10 * th_count, 1, "NCC of raw detected image")
            worksheet.write(4 + 10 * th_count, 1, "NCC of refine detected image")
            worksheet.write(5 + 10 * th_count, 1, "Overflow bits")
            worksheet.write(6 + 10 * th_count, 1, "Number of different pixels")
            worksheet.write(7 + 10 * th_count, 1, "Number of different blocks")
            worksheet.write(8 + 10 * th_count, 1, "Blocks of raw detected image")
            worksheet.write(9 + 10 * th_count, 1, "Blocks of refine detected image")
            worksheet.write(10 + 10 * th_count, 1, "Block size")
            t_star_count = 0
            th_count += 1
    workbook.close()

write_xlsx(result)