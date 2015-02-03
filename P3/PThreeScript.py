__author__ = 'Jasper'

import scipy.misc as misc


execfile('PThree.py')
execfile('PThreeTamper.py')
execfile('PThreeRecover.py')



"""
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

transparent_image = "original\\small.png"
tran_misc = misc.imread(transparent_image)
tran = tran_misc.tolist()

gray_image = "original\\small.bmp"
gray_misc = misc.imread(gray_image)
gray = gray_misc.tolist()

base_image = "original\\Lena.bmp"
base_misc = misc.imread(base_image)

base = [[255 for i in range(len(base_misc))] for i in range(len(base_misc[0]))]


picAnchor(tran, gray, base, (294, 196), 0)

for row in xrange(len(base)):
    for col in xrange(len(base[0])):
        base_misc[row][col] = base[row][col]
misc.imsave("original//TamperedObject.bmp", base_misc)
"""
