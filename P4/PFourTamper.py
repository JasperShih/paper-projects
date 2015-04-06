__author__ = 'Jasper'

import cPickle as Pickle
import scipy.misc as misc
import os


def picAnchor(Transparent, gray, baseImg, start, toBlack=0):
    Srow = start[0]
    Scol = start[1]
    for row in range(len(Transparent)):
        for col in range(len(Transparent[0])):
            if Transparent[row][col][3] == 0:
                pass
            elif toBlack == 0:
                baseImg[row + Srow][col + Scol] = gray[row][col]
            elif toBlack == 1:
                baseImg[row + Srow][col + Scol] = 0
                # list is called by ref, so we can directly use baseImg in caller rather return baseImg

def diffImg(stegoImg,tamperImg,blockSize):
    difPImg=[[255 for i in range(len(stegoImg))]for i in range(len(stegoImg))]
    difBImg=[[255 for i in range(len(stegoImg))]for i in range(len(stegoImg))]

    difPCount=0
    difBCount=0
    for bRowOfImg in range(0,len(stegoImg)-(blockSize-1),blockSize):
        for bColOfImg in range(0,len(stegoImg[0])-(blockSize-1),blockSize):
            bHighBound=bRowOfImg+blockSize
            bWidthBound=bColOfImg+blockSize

            tamBFlag=255
            for rowOfBlock in range(bRowOfImg,bHighBound,1):
                for colOfBlock in range(bColOfImg,bWidthBound,1):
                    if stegoImg[rowOfBlock][colOfBlock]!=tamperImg[rowOfBlock][colOfBlock]:
                        difPCount+=1
                        difPImg[rowOfBlock][colOfBlock]=0
                        tamBFlag=0
            if tamBFlag==0:
                difBCount+=1
                for rowOfBlock in range(bRowOfImg,bHighBound,1):
                    for colOfBlock in range(bColOfImg,bWidthBound,1):
                        difBImg[rowOfBlock][colOfBlock]=0

    return difPCount,difBCount,difPImg,difBImg

def path_list_sort(path_list):
    path_list.sort(key=(
        lambda x: int(x.split(",")[2].split(".")[0])
    ))
    path_list.sort(key=(
        lambda x: int(x.split(",")[1])
    ))
    path_list.sort(key=(
        lambda x: x.split(",")[0]
    ))


def main(anchor_position, block_size):
    # anchor_position = (294, 196)
    transparent_image = "C:\\Users\\Jasper\\Desktop\\Pps\\P4\\original\\lion.png"
    tran_misc = misc.imread(transparent_image)
    tran = tran_misc.tolist()

    gray_image = "C:\\Users\\Jasper\\Desktop\\Pps\\P4\\original\\lion.bmp"
    gray_misc = misc.imread(gray_image)
    gray = gray_misc.tolist()

    stego_list = filter(lambda path:
                        path if path[0:5] == "Stego" else None,
                        os.listdir("output"))
    path_list_sort(stego_list)

    result_list = []
    for stego in stego_list:
        base_image = "output\\" + stego
        base_misc = misc.imread(base_image)
        base = base_misc.tolist()

        picAnchor(tran, gray, base, anchor_position)
        difPCount, difBCount, difPImg, difBImg = \
            diffImg(base_misc, base, block_size)

        for row in xrange(len(base)):
            for col in xrange(len(base[0])):
                base_misc[row][col] = base[row][col]
        misc.imsave("output//Tampered" + stego, base_misc)

        for row in xrange(len(base)):
            for col in xrange(len(base[0])):
                base_misc[row][col] = difPImg[row][col]
        misc.imsave("output//DifferentPixel" + stego[5:], base_misc)

        for row in xrange(len(base)):
            for col in xrange(len(base[0])):
                base_misc[row][col] = difBImg[row][col]
        misc.imsave(u"output//DifferentBlock" + stego[5:], base_misc)

        result_list += [[difPCount, difBCount]]

    return result_list
    # result = [image name, threshold, T_STAR,
    #  capacity, over_or_under_flow_bits, PSNR,
    # different Pixel Count, different Block Count]

if __name__ == '__main__':
    main((20,20), 4)