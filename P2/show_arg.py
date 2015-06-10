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
    merge_list.sort(key=lambda x: x[1], reverse=True)

    line = draw_line(merge_list)

    line_bbp = [i for i, j, k in line]
    line_PSNR = [j for i, j, k in line]
    line_argument = [k for i, j, k in line]

    return line_bbp, line_PSNR, line

"""
count = {}
for i in line_argument:
    tmp = i[1]
    if tmp not in count:
        count[tmp] = 1
    else:
        count[tmp] += 1
for key, value in sorted(count.iteritems(), key=lambda (k,v): (v,k), reverse = True):
    print "%s: %s" % (key, value)
"""



# max_or_range, threshold, t_star_smooth, t_star_complex, mul_smooth, mul_complex, overflow_bits

bound_left = 0
bound_right = 3.01
plt.xlim(bound_left, bound_right)
plt.xticks([tick for tick in frange(bound_left, bound_right, 0.5)])

bound_left2 = 10
bound_right2 = 55.1
plt.ylim(bound_left2, bound_right2)
plt.yticks([tick for tick in frange(bound_left2, bound_right2, 5)])

plt.xlabel("Embedding Rate (BBP)")
plt.ylabel("PSNR (dB)")
plt.title("Lena")

line_bbp1, line_PSNR1, line = get_best_line("baboon.data")
for i in line:
    print i

plt.plot(line_bbp1, line_PSNR1, "ro-", linewidth = 2)


fig = plt.gcf()
fig.set_size_inches(11, 8)
#fig.savefig('test2png.png',dpi=100)

#plt.show()
