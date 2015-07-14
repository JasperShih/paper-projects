__author__ = 'Jasper'

import scipy.misc as misc


def read_img(image_path):
    img_misc = misc.imread(image_path)
    img_list = img_misc.tolist()
    return img_list


def get_tp_fp_fn(pixel_different_img_path, detected_img_path):
    pixel_dif_img = read_img(pixel_different_img_path)
    detected_img = read_img(detected_img_path)

    true_positive = 0
    false_positive = 0
    false_negative = 0
    for row in xrange(len(pixel_dif_img)):
        for col in xrange(len(pixel_dif_img[0])):
            pix = pixel_dif_img[row][col]
            det = detected_img[row][col]
            if (pix == 0) and (det == 0):
                true_positive += 1
            elif (pix == 255) and (det == 0):
                false_positive += 1
            elif (pix == 0) and (det == 255):
                false_negative += 1

    return true_positive, false_positive, false_negative


def get_f1(true_positive, false_positive, false_negative):
    precision = float(true_positive) / (true_positive + false_positive)
    recall = float(true_positive) / (true_positive + false_negative)
    f1 = float(2 * precision * recall) / (precision + recall)
    return f1, precision, recall


true_positive, false_positive, false_negative = get_tp_fp_fn(
    "C:\\Users\\Jasper\\Desktop\\USB1\\move\\imageAbout\\lenaTstart3\\pixelDifftamperedLenaStego,max,200,3,.bmp",
    "C:\\Users\\Jasper\\Desktop\\USB1\\move\\imageAbout\\lenaTstart3\\DetecImgtamperedLenaStego,max,200,3,.bmp")

f1, precision, recall = get_f1(true_positive, false_positive, false_negative)

print f1, precision, recall
