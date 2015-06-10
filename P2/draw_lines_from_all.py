__author__ = 'Jasper'

import cPickle as Pickle
import matplotlib.pyplot as plt


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


# sort list_a according list_b
def multi_list_sort(list_a, list_b):
    return [a for (a, b) in sorted(zip(list_a, list_b), key=lambda zip_tuple: zip_tuple[1], reverse=True)]


def draw_line(merge_list):
    max_bbp = merge_list[0][0]
    line = [merge_list[0]]
    for sub_list in merge_list:
        if sub_list[0] > max_bbp:
            max_bbp = sub_list[0]
            line += [sub_list]
    return line


def get_best_line(filename):
    data_file = file(filename, 'r')
    bbpList, PSNRList, argument = Pickle.load(data_file)
    data_file.close()
    merge_list = zip(bbpList, PSNRList, argument)

    merge_5 = []
    merge_10 = []
    merge_15 = []
    merge_20 = []
    for i in merge_list:
        if i[-1][1] == 5:
            merge_5 += [i]
        elif i[-1][1] == 10:
            merge_10 += [i]
        elif i[-1][1] == 15:
            merge_15 += [i]
        elif i[-1][1] == 20:
            merge_20 += [i]


    merge_5.sort(key=lambda x: x[1], reverse=True)
    merge_10.sort(key=lambda x: x[1], reverse=True)
    merge_15.sort(key=lambda x: x[1], reverse=True)
    merge_20.sort(key=lambda x: x[1], reverse=True)

    line5 = draw_line(merge_5)
    line10 = draw_line(merge_10)
    line15 = draw_line(merge_15)
    line20 = draw_line(merge_20)

    line5_bbp = [i for i, j, k in line5]
    line5_PSNR = [j for i, j, k in line5]
    line10_bbp = [i for i, j, k in line10]
    line10_PSNR = [j for i, j, k in line10]
    line15_bbp = [i for i, j, k in line15]
    line15_PSNR = [j for i, j, k in line15]
    line20_bbp = [i for i, j, k in line20]
    line20_PSNR = [j for i, j, k in line20]

    return line5_bbp, line5_PSNR, line10_bbp, line10_PSNR, line15_bbp, line15_PSNR, line20_bbp, line20_PSNR


# max_or_range, threshold, t_star_smooth, t_star_complex, mul_smooth, mul_complex, overflow_bits

bound_left = 0
bound_right = 3.01
plt.xlim(bound_left, bound_right)
plt.xticks([tick for tick in frange(bound_left, bound_right, 0.5)])

bound_left2 = 10
bound_right2 = 50.1
plt.ylim(bound_left2, bound_right2)
plt.yticks([tick for tick in frange(bound_left2, bound_right2, 5)])

plt.xlabel("Embedding Rate (BBP)")
plt.ylabel("PSNR (dB)")
plt.title("Tiffany")

line5_bbp, line5_PSNR, line10_bbp, line10_PSNR, line15_bbp, line15_PSNR, line20_bbp, line20_PSNR = \
    get_best_line("Tiffany.data")

plt.plot(line5_bbp, line5_PSNR, "r.:", linewidth=2)
plt.plot(line10_bbp, line10_PSNR, "b.:", linewidth=2)
plt.plot(line15_bbp, line15_PSNR, "g.:", linewidth=2)
plt.plot(line20_bbp, line20_PSNR, "k.:", linewidth=2)

fig = plt.gcf()
fig.set_size_inches(10.8, 7.2)
fig.savefig('test2png.png',dpi=100)

plt.show()
