__author__ = 'Jasper'

import math
import sys
import scipy.misc as pnimg, random
import matplotlib.pyplot as plt

NumImg = pnimg.imread("C:\\Users\\Jasper\\Desktop\\Lena.bmp")
imgList = NumImg.tolist()

blockSize = 3
mid = (1, 1)

bbpList = []
PSNRList = []


class omitOutIndex:
    def __init__(self):
        pass

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception_value, exception_traceback):
        return True


def maxS(start, satellites, thresholdmaxS):
    buf = []
    # buf=(|SL-C|,|SR-C|,|SU-C|,|SD-C|)
    for sat in satellites:
        if sat:
            buf.append(abs(
                sat - imgList[start[0] + mid[0]]
                [start[1] + mid[1]]
            )
            )
    if max(buf) < thresholdmaxS:
        return "smooth"
    else:
        return "complex"


def rangeS(satellites, thresholdrangeS):
    buf = []
    # buf=(SL,SR,SU,SD)
    for sat in satellites:
        if sat:
            buf.append(sat)

    dif = max(buf) - min(buf)
    if dif < thresholdrangeS:
        return "smooth"
    else:
        return "complex"


def PSNR(oriNumImg, stegoImg):
    imgSize = len(oriNumImg) * len(oriNumImg)
    MSE = float(0)
    for row in xrange(len(oriNumImg)):
        for col in xrange(len(oriNumImg[0])):
            tem = oriNumImg[row][col] - stegoImg[row][col]
            MSE += tem * tem
    MSE /= imgSize
    psnr = 10 * math.log((255 * 255) / MSE, 10)
    return psnr


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


# maxOrRange 0:max 1:range
def hiding(maxOrRange, threshold,
           mulSmooth, TStarSmooth,
           mulComplex, TStarComplex):
    imgList = NumImg.tolist()
    imgListOri = NumImg.tolist()  # Original imgList(Unchanged)

    # ---------------------------------------parameter---------------------------------
    """    thresholdmaxS = 200
    thresholdrangeS = 255"""
    # ---------------------------------------parameter End------------------------------

    # SU=imgList, if outofIndex SU = None


    # -----------------------------------Parameter--------------------------------------

    """    mulSmooth = 1 # k
    TStarSmooth = 1

    mulComplex = 1 # K
    TStarComplex = 1"""
    secret = ""

    # Count length of hidden secret bits (seqSmoothLen & seqComplexLen)
    # with different mulSmooth and mulComplex
    seqSmoothLen = 0
    tmp = mulSmooth + 1
    while tmp != 1:
        tmp /= 2
        seqSmoothLen += 1

    seqComplexLen = 0
    tmp = mulComplex + 1
    while tmp != 1:
        tmp /= 2
        seqComplexLen += 1
    # -----------------------------------Parameter end----------------------------------

    # -----------------------------------maxS-------------------------------------------

    # Throughout entire Img block by block.
    for row in xrange(0, len(imgList) - blockSize + 1, blockSize):
        for col in xrange(0, len(imgList[0]) - blockSize + 1, blockSize):
            # Get satellites. If IndexError occurs, the satellite=None
            # [SU, SD, SR, SL] are values, not indexes
            with omitOutIndex() as SU:
                if (row + mid[0] - 3) >= 0:
                    SU = imgList[row + mid[0] - 3][col + mid[1]]
            with omitOutIndex() as SD:
                SD = imgList[row + mid[0] + 3][col + mid[1]]
            with omitOutIndex() as SR:
                SR = imgList[row + mid[0]][col + mid[1] + 3]
            with omitOutIndex() as SL:
                if (col + mid[1] - 3) >= 0:
                    SL = imgList[row + mid[0]][col + mid[1] - 3]

            satellites = [SU, SD, SR, SL]
            # max
            if maxOrRange == 0:
                complexity = maxS([row, col],
                                  satellites, threshold)
            # range
            elif maxOrRange == 1:
                complexity = rangeS(satellites, threshold)

            if complexity == "smooth":
                for rowInBlock in xrange(row, row + blockSize, 1):
                    for colInBlock in xrange(col, col + blockSize, 1):
                        if (rowInBlock == (row + mid[0]) and
                                    colInBlock == (col + mid[0])
                        ):
                            pass
                        else:

                            block_map_row = rowInBlock - row
                            block_map_col = colInBlock - col
                            # ==================Spin dif Algo============================v
                            if (block_map_row == 0 and
                                        block_map_col == 0):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock][colInBlock + 1]

                            elif (block_map_row == 0 and
                                          block_map_col == 1):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 0 and
                                          block_map_col == 2):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 1][colInBlock + 2]

                            elif (block_map_row == 1 and
                                          block_map_col == 0):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 1 and
                                          block_map_col == 2):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 2 and
                                          block_map_col == 0):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 1][colInBlock + 0]

                            elif (block_map_row == 2 and
                                          block_map_col == 1):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 2 and
                                          block_map_col == 2):
                                dif = imgListOri[rowInBlock][colInBlock] - \
                                      imgListOri[rowInBlock + 2][colInBlock + 1]
                            # ==================Spin dif Algo End========================^

                            if -TStarSmooth <= dif and dif <= TStarSmooth:
                                seq = ""
                                for lenIndex in xrange(seqSmoothLen):
                                    seq += str(random.randint(0, 1))
                                secret += seq
                                seq = int(seq, 2)
                                dif = (mulSmooth + 1) * dif + seq

                            elif dif < -TStarSmooth:
                                dif = dif - mulSmooth * TStarSmooth

                            elif dif > TStarSmooth:
                                dif = dif + (TStarSmooth + 1) * mulSmooth

                            # TODO overflowUnderflow
                            # ==============spin new imgList Algo====================v
                            if (block_map_row == 0 and
                                        block_map_col == 0):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock][colInBlock + 1]

                            elif (block_map_row == 0 and
                                          block_map_col == 1):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 1][colInBlock + 1]
                            elif (block_map_row == 0 and
                                          block_map_col == 2):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 1][colInBlock + 2]

                            elif (block_map_row == 1 and
                                          block_map_col == 0):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 1 and
                                          block_map_col == 2):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 2 and
                                          block_map_col == 0):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 1][colInBlock + 0]

                            elif (block_map_row == 2 and
                                          block_map_col == 1):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 1][colInBlock + 1]

                            elif (block_map_row == 2 and
                                          block_map_col == 2):
                                imgList[rowInBlock][colInBlock] = \
                                    dif + imgListOri[rowInBlock + 2][colInBlock + 1]
                                # ==============spin new imgList Algo=====================^

            elif complexity == "complex":
                buf = []
                for sat in satellites:
                    if sat:
                        buf.append(int(math.floor(
                            (3 * imgList[row + mid[0]][col + mid[1]] + sat) / 4  # more capacity, lower PSNR
                        )
                        )
                        )

                minLambda = min(buf)
                # print minLambda
                for rowInBlock in xrange(row, row + blockSize, 1):
                    for colInBlock in xrange(col, col + blockSize, 1):
                        if (rowInBlock == (row + mid[0]) and
                                    colInBlock == (col + mid[0])
                        ):
                            pass
                        else:
                            """dif = imgList[row+mid[0]][col+mid[1]]- \
                                  imgList[rowInBlock][colInBlock]
                            dif = dif-minLambda"""
                            dif = minLambda - imgList[rowInBlock][colInBlock]

                            if -TStarComplex <= dif and dif <= TStarComplex:
                                seq = ""
                                for lenIndex in xrange(seqComplexLen):
                                    seq += str(random.randint(0, 1))
                                secret += seq
                                seq = int(seq, 2)

                                dif = (mulComplex + 1) * dif + seq

                            elif dif < -TStarComplex:
                                dif = dif - mulComplex * TStarComplex

                            else:  # dif>TStarComplex
                                dif = dif + (TStarComplex + 1) * mulComplex

                            """dif = dif+minLambda
                            #TODO overflowUnderflow
                            imgList[rowInBlock][colInBlock] = \
                            imgList[row+mid[0]][col+mid[1]]-dif"""
                            imgList[rowInBlock][colInBlock] = minLambda - dif

    """strList=""
    for i in range(len(imgList)):
        if i%3 == 0:
            print ""
        for j in range(len(imgList[0])):
            if j%3 == 0:
                strList+="   "+str(imgList[i][j])+","
            else:
                strList+=str(imgList[i][j])+","

        print strList
        strList="""""
    """
    if maxOrRange==0 :
        print "MaxTH = "+str(threshold)
    elif maxOrRange==1 :
        print "RangeTH = "+str(threshold)
    print "k of Smooth = "+str(mulSmooth)+"    T* of Smooth = "+str(TStarSmooth)
    print "k of Complex = "+str(mulComplex)+"   T* of Complex = "+str(TStarComplex)

    print "capacity = "+str(len(secret))
    print "PSNR = "+str(PSNR(NumImg,imgList))
    print "----------------------------------------------"
    """
    bbpList.append(float(len(secret)) /
                   (
                       len(imgList) * len(imgList[0])
                   )
    )
    PSNRList.append(PSNR(NumImg, imgList))
    # pnimg.imsave(outName,saveNum )
    # -----------------------------------maxS End-------------------------------------


"""stdoutFd=sys.stdout
writeFd=open("C:\\Users\\Jasper\\Desktop\\out.txt",'w')
sys.stdout=writeFd
"""
# P2.hiding(maxOrRange, threshold, mulSmooth, TStarSmooth, mulComplex, TStarComplex)
# maxOrRange 0:max 1:range
maxOrRange = 0
thresholdmaxS_List = [20]
thresholdrangeS_List = [1, 2, 3, 4, 5, 10, 15, 20, 30, 50]

mulSmoothList = [3,7]
TStarSmoothList = [2,3]

mulComplexList = [1, 3, 7]
TStarComplexList = [0, 1, 2, 3, 4]

if maxOrRange == 0:
    for thresholdmaxS in thresholdmaxS_List:
        for mulSmooth in mulSmoothList:
            for TStarSmooth in TStarSmoothList:
                for mulComplex in mulComplexList:
                    for TStarComplex in TStarComplexList:
                        hiding(0, thresholdmaxS, mulSmooth, TStarSmooth, mulComplex, TStarComplex)
elif maxOrRange == 1:
    for thresholdrangeS in thresholdrangeS_List:
        for mulSmooth in mulSmoothList:
            for TStarSmooth in TStarSmoothList:
                for mulComplex in mulComplexList:
                    for TStarComplex in TStarComplexList:
                        hiding(1, thresholdrangeS, mulSmooth, TStarSmooth, mulComplex, TStarComplex)
"""sys.stdout=stdoutFd
writeFd.close()"""

# hiding(1, 20, 1, 1, 1, 0)

plt.xlim(0, 5)
plt.xticks([tick for tick in frange(0, 5.1, 0.5)])
plt.ylim(10, 60)
plt.yticks([tick for tick in frange(10, 61, 5)])

plt.xlabel("BBP")
plt.ylabel("PSNE")
plt.title("RangeTH")

plt.plot(bbpList, PSNRList, "ko")
plt.show()

