'''
Created on 2014/3/6

@author: Jasper
'''
import random,math

def overProcessing(img):
    overStr=""
    overCount=0
    for row in range(len(img)):
        for col in range(len(img[0])):
            if img[row][col]==0:
                img[row][col]+=1
                overStr+="{0:010b}".format(row)+"{0:010b}".format(col)
                overCount+=1
            elif img[row][col]==255:
                img[row][col]-=1
                overStr+="{0:010b}".format(row)+"{0:010b}".format(col)
                overCount+=1
    overStr="{0:010b}".format(overCount)+overStr
    return img,overStr
#Can we use (zero<x<=peak)&(x=255 or x=0) to determine embedding or not?


"""
img       :a normal array(Do not pass numpy array)
blocation :basic pixel location in the block;(x,y)
creatHis  :creating histogram or not
inverse   :inversely prediction or not

bRowOfImg :block-row of img(units:bolck)
bColOfImg :block-column of img
bHighBound:new block high boundary
bWidthBound:new block width boundary
basicPRow: basic pixel at which row
basicPCol: basic pixel at which column
"""
def prediction(img,blockSize,blocation,creatHis=1,inverse=0):
    histogram={}
    mul=1
    if inverse==1:
        mul=-1

    if (len(img)%blockSize)+(len(img[0])%blockSize)!=0:
        print "blocksize wrong!"
        exit(1)
    for bRowOfImg in range(0,len(img),blockSize):
        for bColOfImg in range(0,len(img[0]),blockSize):
            bHighBound=bRowOfImg+blockSize
            bWidthBound=bColOfImg+blockSize
            basicPRow=bRowOfImg+blocation[1]
            basicPCol=bColOfImg+blocation[0]
            for rowOfBlock in range(bRowOfImg,bHighBound,1):
                for colOfBlock in range(bColOfImg,bWidthBound,1):
                    if (rowOfBlock==basicPRow) & (colOfBlock==basicPCol):
                        pass
                    else:
                        tem=img[rowOfBlock][colOfBlock]-(img[basicPRow][basicPCol]*mul)
                        img[rowOfBlock][colOfBlock]=tem
                        if creatHis==1:
                            if tem not in histogram:
                                histogram[tem]=1
                            else:
                                histogram[tem]+=1
    return histogram

"""
zeroRec : zero point record,it records all zero point(buf,list)
zeroBuf : zero point buffer;just a buffer
zeroList: zero point list,placed zero point which be really selected
state:0 stateless, 1 last zero point is positive, -1 last one is negative
pnScale: positive/negative scale

A pair of peak&zero will form a interval and every interval would not overlap
(Even a point would not intersect too).
We want to pick peakPair zero points, we follow 0,1,-1,2,-2......sequence to search,
and we ask one positive one negative order(or inverse).
Maybe we can't find zero point. However, this case is unusual, so I didn't implement it
"""
def pickZero(histogram,peakPair):
    zeroRec=[]
    zeroBuf=[]
    zeroList=[]
    state=0
    if 0 not in histogram:  #non add 0
        zeroRec.append(0)
        zeroList.append(0)

    for scale in range(1,256,1):
        for pnScale in [scale,-scale]:
            if peakPair==len(zeroList):
                return zeroList
            elif pnScale not in histogram:
                if (state==0) & (bigThan2(zeroRec,pnScale)):
                    zeroRec.append(pnScale)
                    zeroList.append(pnScale)
                    state=pnScale/abs(pnScale)
                else:
                    if bigThan2(zeroRec,pnScale):
                        zeroRec.append(pnScale)
                        zeroBuf.append(pnScale)
                        if state*pnScale<0:
                            state=pnScale/abs(pnScale)
                            zeroList.append(pnScale)
                            zeroBuf.remove(pnScale)
                            if peakPair==len(zeroList):
                                return zeroList
                            state=bufChain(zeroList,zeroBuf,state,peakPair)

def bigThan2(zeroRec,betested):
    flag=1
    for Rec in zeroRec:
        if abs(Rec-betested)<=2:
            flag=0
    return flag
#It need more than 2 scale between zero points

def bufChain(zeroList,zeroBuf,state,peakPair):
    flag=1
    while(flag&(len(zeroBuf)>0)):
        for zero in zeroBuf:
            if state*zero<0:
                state=zero/abs(zero)
                zeroList.append(zero)
                zeroBuf.remove(zero)
                if peakPair==len(zeroList):
                    return
                flag=1
                break
            else:
                flag=0
    return state
#If we added a new zero point to list,
#we try to add some zero points from buffer

"""
resiLow: residual lower boundary
"""
def pickPeak(histogram,zeroList):
    resiLow=-255
    resiUp=256
    peakList=[]
    zeroList.sort()
    for ind in range(len(zeroList)+1):
        if ind==0:
            peakList.append(search(resiLow,zeroList[0],1,histogram))
        elif ind==(len(zeroList)):
            peakList.append(search(zeroList[-1],resiUp,1,histogram))
            #undo:We search last peak from end to start to improve psnr
        else:
            pL,pR=search(zeroList[ind-1],zeroList[ind],2,histogram)
            peakList.append(pL)
            peakList.append(pR)
    tem=peakList
    peakList=[]
    for i in range(0,len(tem),2):
        if tem[i] not in histogram:
            ternL=0
        else:
            ternL=histogram[tem[i]]
        if tem[i+1] not in histogram:
            ternR=0
        else:
            ternR=histogram[tem[i+1]]

        if ternL>ternR:
            peakList.append(tem[i])
        else:
            peakList.append(tem[i+1])
    return peakList

def search(start,end,peakNum,histogram):
    maxi=0
    maxScalL=start #maxScalL:Left peak point
    maxScalR=start
    for scale in range(start,end,1):
        if scale in histogram:
            if histogram[scale]>=maxi:
                maxi=histogram[scale]
                maxScalL=maxScalR
                maxScalR=scale
    if maxScalL>maxScalR:
        tem=maxScalR
        maxScalR=maxScalL
        maxScalL=tem
    if(peakNum==2):
        return maxScalL,maxScalR
    return maxScalR

def mergePZ(peakList,zeroList):
    peakZeroList=[]
    for i in range(0,len(peakList),1):
        if peakList[i]<zeroList[i]:
            peakZeroList.append({"p":peakList[i],"z":zeroList[i],"sign":1})
        else:
            peakZeroList.append({"p":peakList[i],"z":zeroList[i],"sign":-1})
    return peakZeroList

def capacityCheckOver(peakZeroList,histogram,overStr):
    count=0
    for dic in peakZeroList:
        if dic["p"] not in histogram:
            count+=0
        else:
            count+=histogram[dic["p"]]
    if (count/16)<len(overStr):
        print"Recording overflow/underflow bits are more than payload!"
        exit(1)
    return count
#The unit of count is pixel and the value of count did not minus len(overStr)
#need to re-check because auth-code change


def genAuthCode(height,width,overStr):
    numAuth=height*width
    randonStr=""
    for i in range(numAuth):
        if len(overStr)!=0:
            randonStr+=overStr[0]
            overStr=overStr[1:]
        else:
            randonStr+=str(random.randint(0,1))
    return randonStr



"""
hisOfPeaksBlock: histogram of number of peaks in block
UnEmbImg: UnEmbeddedable block image(only 0 or 255). 0 means unEmbeddedable block.
peakCount:number of peaks in a block
"""
def embeddedShiftStego(peakZeroList,residualImg,blockSize,blocation,randonStr):
    hisOfPeaksBlock={i:0 for i in range(16)}
    UnEmbImg=[[255 for i in range(512)]for i in range(512)]
    ind=0

    for bRowOfImg in range(0,len(residualImg),blockSize):
        for bColOfImg in range(0,len(residualImg[0]),blockSize):
            bHighBound=bRowOfImg+blockSize
            bWidthBound=bColOfImg+blockSize
            basicPRow=bRowOfImg+blocation[1]
            basicPCol=bColOfImg+blocation[0]

            peakCount=0
            ran=int(randonStr[ind])
            ind+=1
            for rowOfBlock in range(bRowOfImg,bHighBound,1):
                for colOfBlock in range(bColOfImg,bWidthBound,1):
                    if (rowOfBlock==basicPRow) & (colOfBlock==basicPCol):
                        pass
                    else:
                        for dic in peakZeroList:
                            if residualImg[rowOfBlock][colOfBlock]==dic['p']:
                                residualImg[rowOfBlock][colOfBlock]+=ran*dic["sign"]
                                peakCount+=1
                            elif (dic["p"]<residualImg[rowOfBlock][colOfBlock]<dic["z"])or(dic["z"]<residualImg[rowOfBlock][colOfBlock]<dic["p"]):
                                residualImg[rowOfBlock][colOfBlock]+=dic["sign"]
                        residualImg[rowOfBlock][colOfBlock]+=residualImg[basicPRow][basicPCol]
            if peakCount==0:
                for rowOfBlock in range(bRowOfImg,bHighBound,1):
                    for colOfBlock in range(bColOfImg,bWidthBound,1):
                        UnEmbImg[rowOfBlock][colOfBlock]=0
            hisOfPeaksBlock[peakCount]+=1
    return residualImg,UnEmbImg,hisOfPeaksBlock


def PSNR(oriNumImg,stegoImg,imgSize):
    MSE=float(0)
    for row in range(len(oriNumImg)):
        for col in range(len(oriNumImg[0])):
            tem=oriNumImg[row][col]-stegoImg[row][col]
            MSE+=tem*tem
    MSE/=imgSize
    psnr=10*math.log((255*255)/MSE,10)
    return psnr

"""==============================for 2.3======================================"""

def diffImg(stegoImg,tamperImg,blockSize):
    difPImg=[[255 for i in range(512)]for i in range(512)]
    difBImg=[[255 for i in range(512)]for i in range(512)]

    difPCount=0
    difBCount=0
    for bRowOfImg in range(0,len(stegoImg),blockSize):
        for bColOfImg in range(0,len(stegoImg[0]),blockSize):
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


def extraRcvDetc(embResiImg,peakZeroList,randonStr,blockSize,blocation):
    ind=0
    UnBCount=0
    detectUnImg=[[255 for i in range(512)]for i in range(512)]
    for bRowOfImg in range(0,len(embResiImg),blockSize):
        for bColOfImg in range(0,len(embResiImg[0]),blockSize):
            bHighBound=bRowOfImg+blockSize
            bWidthBound=bColOfImg+blockSize
            basicPRow=bRowOfImg+blocation[1]
            basicPCol=bColOfImg+blocation[0]

            temStr=""
            for rowOfBlock in range(bRowOfImg,bHighBound,1):
                for colOfBlock in range(bColOfImg,bWidthBound,1):
                    if (rowOfBlock==basicPRow) & (colOfBlock==basicPCol):
                        pass
                    else:
                        for dic in peakZeroList:
                            if embResiImg[rowOfBlock][colOfBlock]==dic['p']:
                                temStr+="0"
                            elif ((dic["p"]+1)<=embResiImg[rowOfBlock][colOfBlock]<(dic["z"]+1))or((dic["z"]-1)<embResiImg[rowOfBlock][colOfBlock]<=(dic["p"]-1)):
                                if (embResiImg[rowOfBlock][colOfBlock]==(dic["p"]+1))or(embResiImg[rowOfBlock][colOfBlock]==(dic["p"]-1)):
                                    temStr+="1"
                                embResiImg[rowOfBlock][colOfBlock]-=dic["sign"]
                        embResiImg[rowOfBlock][colOfBlock]+=embResiImg[basicPRow][basicPCol]

            if len(temStr)!=0:
                diffFlag=0
                ran=randonStr[ind]
                for char in temStr:
                    if char!=ran:
                        diffFlag=1
                if diffFlag==1:
                    UnBCount+=1
                    for rowOfBlock in range(bRowOfImg,bHighBound,1):
                        for colOfBlock in range(bColOfImg,bWidthBound,1):
                            detectUnImg[rowOfBlock][colOfBlock]=0
            ind+=1
    return UnBCount,embResiImg,detectUnImg


def refine(detectUnImg,blockSize):
    mark=1
    
    while mark:
        mark=0
        ReBCount=0
        for bRowOfImg in range(0,len(detectUnImg),blockSize):
            for bColOfImg in range(0,len(detectUnImg[0]),blockSize):
                if detectUnImg[bRowOfImg][bColOfImg]==255:
                    #print bRowOfImg-blockSize,bColOfImg          ,bRowOfImg+blockSize,bColOfImg          
                    mark+=boundCheckPaint([bRowOfImg-blockSize,bColOfImg          ,bRowOfImg+blockSize,bColOfImg          ],detectUnImg,bRowOfImg,bColOfImg,blockSize)
                    
                    #print bRowOfImg          ,bColOfImg-blockSize,bRowOfImg          ,bColOfImg+blockSize
                    mark+=boundCheckPaint([bRowOfImg          ,bColOfImg-blockSize,bRowOfImg          ,bColOfImg+blockSize],detectUnImg,bRowOfImg,bColOfImg,blockSize)
                    
                    #print bRowOfImg-blockSize,bColOfImg-blockSize,bRowOfImg+blockSize,bColOfImg+blockSize
                    mark+=boundCheckPaint([bRowOfImg-blockSize,bColOfImg-blockSize,bRowOfImg+blockSize,bColOfImg+blockSize],detectUnImg,bRowOfImg,bColOfImg,blockSize)
                    
                    #print bRowOfImg+blockSize,bColOfImg-blockSize,bRowOfImg-blockSize,bColOfImg+blockSize
                    mark+=boundCheckPaint([bRowOfImg+blockSize,bColOfImg-blockSize,bRowOfImg-blockSize,bColOfImg+blockSize],detectUnImg,bRowOfImg,bColOfImg,blockSize)
                else:
                    ReBCount+=1
    return ReBCount,detectUnImg
                
def boundCheckPaint(indList,detectUnImg,bRowOfImg,bColOfImg,blockSize):
    flag=0
    for ind in indList:
        if 0<=ind<len(detectUnImg):
            flag+=1
    if flag<4:
        return 0
    else:
        #print indList[0],indList[1],indList[2],indList[3]
        if (detectUnImg[indList[0]][indList[1]]==0)&(detectUnImg[indList[2]][indList[3]]==0):
            bHighBound=bRowOfImg+blockSize
            bWidthBound=bColOfImg+blockSize
            for rowOfBlock in range(bRowOfImg,bHighBound,1):
                for colOfBlock in range(bColOfImg,bWidthBound,1):
                    detectUnImg[rowOfBlock][colOfBlock]=0
            return 1
        else:
            return 0


def falseDetect(difPImg,difBImg,refineImg,blockSize):
    falDetImgP=[[255 for i in range(512)]for i in range(512)]
    falDetImgB=[[255 for i in range(512)]for i in range(512)]
    unDetectB=0
    wrongDetectB=0
    unDetectP=0
    wrongDetectP=0
    for bRowOfImg in range(0,len(refineImg),blockSize):
        for bColOfImg in range(0,len(refineImg[0]),blockSize):
            bHighBound=bRowOfImg+blockSize
            bWidthBound=bColOfImg+blockSize
            flag=0
            
            if (refineImg[bRowOfImg][bColOfImg]==255)&(difBImg[bRowOfImg][bColOfImg]==0):
                flag=1  #undetected(should be detected)
                unDetectB+=1
            elif (refineImg[bRowOfImg][bColOfImg]==0)&(difBImg[bRowOfImg][bColOfImg]==255):
                flag=2 #wrong detection(should not be detected)
                wrongDetectB+=1
                
            for rowOfBlock in range(bRowOfImg,bHighBound,1):
                for colOfBlock in range(bColOfImg,bWidthBound,1):
                    if (refineImg[rowOfBlock][colOfBlock]==255)&(difPImg[rowOfBlock][colOfBlock]==0):
                        falDetImgP[rowOfBlock][colOfBlock]=0  #undetected(should be detected)
                        unDetectP+=1
                    elif (refineImg[rowOfBlock][colOfBlock]==0)&(difPImg[rowOfBlock][colOfBlock]==255):
                        falDetImgP[rowOfBlock][colOfBlock]=128 #wrong detection(should not be detected)
                        wrongDetectP+=1
                    
                    if flag==1:
                        falDetImgB[rowOfBlock][colOfBlock]=0
                    if flag==2:
                        falDetImgB[rowOfBlock][colOfBlock]=128
    return unDetectB,wrongDetectB,unDetectP,wrongDetectP,falDetImgP,falDetImgB


def overRecover(randonStr,RecoverImg):
    overCount=int(randonStr[0:10], 2)
    overPoint=[]
    for i in range(1,(2*overCount)+1):
        overPoint.append(int(randonStr[i*10:(i*10)+10],2))
    for ind in range(0,len(overPoint),2):
        if RecoverImg[overPoint[ind]][overPoint[ind+1]]==1:
            RecoverImg[overPoint[ind]][overPoint[ind+1]]-=1
        elif RecoverImg[overPoint[ind]][overPoint[ind+1]]==254:
            RecoverImg[overPoint[ind]][overPoint[ind+1]]+=1
    return RecoverImg
            
    









