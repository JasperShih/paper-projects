'''
Created on 2014/4/19

@author: Jasper
'''
import math,scipy.misc as pnimg,random

#hiNum=pnimg.imread("C:\\Users\\Jasper\\Desktop\\Lena.bmp")#################################################
#hiImg=hiNum.tolist()
hiImg=None


class Block:
    imgSize=None    #512
    blockSize=None  #3
    centerBias=None #(1,1) Left-top is (0,0), more right-Bot value more larger
    TStar=0
    overUnderFlow=[]
    embedBitCapacity=0
    embedBlockCapacity=0
    blockEmbeddable=0
    
    def __init__(self, start):
        self.start=start
        self.center=(start[0]+Block.centerBias[0],start[1]+Block.centerBias[1])
        self.adjB={}
        self.adj2B={}
        self.adjSearch(self.start)


    def adjSearch(self,start):
        if (start[1]-Block.blockSize)>=0:
            self.adjB["L"]=(self.center[0],self.center[1]-self.blockSize)
        if (start[1]+Block.blockSize)<=(Block.imgSize-Block.blockSize):
            self.adjB["R"]=(self.center[0],self.center[1]+self.blockSize)
        if (start[0]-Block.blockSize)>=0:
            self.adjB["U"]=(self.center[0]-self.blockSize,self.center[1])
        if (start[0]+Block.blockSize)<=(Block.imgSize-Block.blockSize):
            self.adjB["B"]=(self.center[0]+self.blockSize,self.center[1])

        if ("L" in self.adjB)&("R" in self.adjB):
            self.adj2B["L"]=self.adjB["L"]
            self.adj2B["R"]=self.adjB["R"]
        elif ("U" in self.adjB)&("B" in self.adjB):
            self.adj2B["U"]=self.adjB["U"]
            self.adj2B["B"]=self.adjB["B"]
        else:
            self.adj2B=self.adjB.copy()


def maxS(oriImg,block,Th):
    #max(abs(oriImg[satl[0]][satl[1]]-oriImg[block.center[0]][block.center[1]]) for satl in block.adjB.values())
    maxCandidate=[]
    for satl in block.adjB.values():
        maxCandidate.append(abs(oriImg[satl[0]][satl[1]]-oriImg[block.center[0]][block.center[1]]))
    if max(maxCandidate)<Th:
        return "smooth"
    else:
        return "complex"

def rangeS(oriImg,block,Th):
    satlList=[]
    for satl in block.adjB.values():
        satlList.append(oriImg[satl[0]][satl[1]])
    dif=max(satlList)-min(satlList)
    if dif<Th:
        return "smooth"
    else:
        return "complex"
    

def embed(similarity,block,Img):
    w=str(random.randint(0,1))
    w+=str(random.randint(0,1))
    #print similarity
    if similarity=="smooth":
        smoothEmbed(block,Img,w)
    elif similarity=="complex":
        complexEmbed(block,Img,w)

        
def extract(similarity,block,Img):
    if similarity=="smooth":
        return unSmooth(block,Img)
    elif similarity=="complex":
        return unComplex(block,Img)
    

def smoothEmbed(block,Img,w):
    dL=Img[block.center[0]][block.center[1]-1]-Img[block.center[0]][block.center[1]]
    dR=Img[block.center[0]][block.center[1]+1]-Img[block.center[0]][block.center[1]]
    
    Block.blockEmbeddable=0
    if -Block.TStar<=dL<=Block.TStar:
        dLPrime=dL*2+int(w[0])
        Block.embedBitCapacity+=1
        Block.blockEmbeddable=1
    elif -Block.TStar>dL:
        dLPrime=dL-Block.TStar
    elif Block.TStar<dL:
        dLPrime=dL+Block.TStar+1
    
    if -Block.TStar<=dR<=Block.TStar:
        dRPrime=dR*2+int(w[1])
        Block.embedBitCapacity+=1
        Block.blockEmbeddable=1
    elif -Block.TStar>dR:
        dRPrime=dR-Block.TStar
    elif Block.TStar<dR:
        dRPrime=dR+Block.TStar+1
    
    if Block.blockEmbeddable==1:
        Block.embedBlockCapacity+=1
        
    
    Img[block.center[0]][block.center[1]-1]=dLPrime+Img[block.center[0]][block.center[1]]
    if (Img[block.center[0]][block.center[1]-1]>255)or(Img[block.center[0]][block.center[1]-1]<0):
        print "overflow/underflow! 1"
        Img[block.center[0]][block.center[1]-1]=hiImg[block.center[0]][block.center[1]-1]
        Block.overUnderFlow.append((block.center[0],block.center[1]-1))
    Img[block.center[0]][block.center[1]+1]=dRPrime+Img[block.center[0]][block.center[1]]
    if (Img[block.center[0]][block.center[1]+1]>255)or(Img[block.center[0]][block.center[1]+1]<0):
        print "overflow/underflow! 2"
        Img[block.center[0]][block.center[1]+1]=hiImg[block.center[0]][block.center[1]+1]
        Block.overUnderFlow.append((block.center[0],block.center[1]+1))
        
def unSmooth(block,Img):
    twoTStar=Block.TStar*2
    Lfg=1
    Rfg=1
    
    
    for overUnder in Block.overUnderFlow:
        if (overUnder[0]==block.center[0]) and (overUnder[1]==block.center[1]-1):
            w='*'
            Lfg=0
            break
    if Lfg==1:
        dLPrime=Img[block.center[0]][block.center[1]-1]-Img[block.center[0]][block.center[1]]
        if -twoTStar<=dLPrime<=(twoTStar+1):
            w=str(dLPrime%2)
            dL=dLPrime/2
        elif dLPrime<=-(twoTStar+1):#dL-T*
            w='*'
            dL=dLPrime+Block.TStar
        elif (twoTStar+2)<=dLPrime:#T*<dL
            w='*'
            dL=dLPrime-Block.TStar-1
        Img[block.center[0]][block.center[1]-1]=dL+Img[block.center[0]][block.center[1]]
    
    
    
    for overUnder in Block.overUnderFlow:
        if (overUnder[0]==block.center[0]) and (overUnder[1]==block.center[1]+1):
            w+='*'
            Rfg=0
            break
    if Rfg==1:
        dRPrime=Img[block.center[0]][block.center[1]+1]-Img[block.center[0]][block.center[1]]
        if -twoTStar<=dRPrime<=(twoTStar+1):
            w+=str(dRPrime%2)
            dR=dRPrime/2
        elif dRPrime<=-(twoTStar+1):#dR-T*
            w+='*'
            dR=dRPrime+Block.TStar
        elif (twoTStar+2)<=dRPrime:#T*<dR
            w+='*'
            dR=dRPrime-Block.TStar-1
        Img[block.center[0]][block.center[1]+1]=dR+Img[block.center[0]][block.center[1]]
        
    
    return w
    

#can more improve psnr by hiding w in U/B pixel near Center!!!!!!!!!!!
def complexEmbed(block,Img,w):  
    adj2BV=block.adj2B.values()
    
    #In fact, L is not real in L location. It just is a presentation in adj2BV's location.
    LStar=int(math.floor((Img[block.center[0]][block.center[1]]*2 + Img[adj2BV[0][0]][adj2BV[0][1]])/3))
    RStar=int(math.floor((Img[block.center[0]][block.center[1]]*2 + Img[adj2BV[1][0]][adj2BV[1][1]])/3))
    minStar=min(abs(LStar-Img[block.center[0]][block.center[1]]),abs(RStar-Img[block.center[0]][block.center[1]]))
    
    Llocat=(block.center[0]+toOne(adj2BV[0][0]-block.center[0]),block.center[1]+toOne(adj2BV[0][1]-block.center[1]))
    Rlocat=(block.center[0]+toOne(adj2BV[1][0]-block.center[0]),block.center[1]+toOne(adj2BV[1][1]-block.center[1]))
    
    dL=Img[Llocat[0]][Llocat[1]]-Img[block.center[0]][block.center[1]]
    dR=Img[Rlocat[0]][Rlocat[1]]-Img[block.center[0]][block.center[1]]
    
    dLStar=dL-minStar
    dRStar=dR-minStar
    
    
    Block.blockEmbeddable=0
    if -Block.TStar<=dLStar<=Block.TStar:
        dLPrime=dLStar*2+int(w[0])
        Block.embedBitCapacity+=1
        Block.blockEmbeddable=1
    elif -Block.TStar>dLStar:
        dLPrime=dLStar-Block.TStar
    elif Block.TStar<dLStar:
        dLPrime=dLStar+Block.TStar+1
        
    if -Block.TStar<=dRStar<=Block.TStar:
        dRPrime=dRStar*2+int(w[1])
        Block.embedBitCapacity+=1
        Block.blockEmbeddable=1
    elif -Block.TStar>dRStar:
        dRPrime=dRStar-Block.TStar
    elif Block.TStar<dRStar:
        dRPrime=dRStar+Block.TStar+1
        
    if Block.blockEmbeddable==1:
        Block.embedBlockCapacity+=1
    
    Img[Llocat[0]][Llocat[1]]=dLPrime+Img[block.center[0]][block.center[1]]
    if (Img[Llocat[0]][Llocat[1]]>255)or(Img[Llocat[0]][Llocat[1]]<0):
        print "overflow/underflow! 3"
        Img[Llocat[0]][Llocat[1]]=hiImg[Llocat[0]][Llocat[1]]
        Block.overUnderFlow.append((Llocat[0],Llocat[1]))
    Img[Rlocat[0]][Rlocat[1]]=dRPrime+Img[block.center[0]][block.center[1]]
    if (Img[Rlocat[0]][Rlocat[1]]>255)or(Img[Rlocat[0]][Rlocat[1]]<0):
        print "overflow/underflow! 4"
        Img[Rlocat[0]][Rlocat[1]]=hiImg[Rlocat[0]][Rlocat[1]]
        Block.overUnderFlow.append((Rlocat[0],Rlocat[1]))
        
def unComplex(block,Img):
    adj2BV=block.adj2B.values()
    LStar=int(math.floor((Img[block.center[0]][block.center[1]]*2 + Img[adj2BV[0][0]][adj2BV[0][1]])/3))
    RStar=int(math.floor((Img[block.center[0]][block.center[1]]*2 + Img[adj2BV[1][0]][adj2BV[1][1]])/3))
    minStar=min(abs(LStar-Img[block.center[0]][block.center[1]]),abs(RStar-Img[block.center[0]][block.center[1]]))
    twoTStar=Block.TStar*2
    Lfg=1
    Rfg=1


    Llocat=(block.center[0]+toOne(adj2BV[0][0]-block.center[0]),block.center[1]+toOne(adj2BV[0][1]-block.center[1]))
    for overUnder in Block.overUnderFlow:
        if (overUnder[0]==Llocat[0]) and (overUnder[1]==Llocat[1]):
            w='*'
            Lfg=0
            break
    if Lfg==1:
        dLPrime=Img[Llocat[0]][Llocat[1]]-Img[block.center[0]][block.center[1]]
        if -twoTStar<=dLPrime<=(twoTStar+1):
            w=str(dLPrime%2)
            dLStar=dLPrime/2
        elif dLPrime<=-(twoTStar+1):#dL-T*
            w='*'
            dLStar=dLPrime+Block.TStar
        elif (twoTStar+2)<=dLPrime:#T*<dL
            w='*'
            dLStar=dLPrime-Block.TStar-1
        dL=dLStar+minStar
        Img[Llocat[0]][Llocat[1]]=dL+Img[block.center[0]][block.center[1]]
    
    
    
    Rlocat=(block.center[0]+toOne(adj2BV[1][0]-block.center[0]),block.center[1]+toOne(adj2BV[1][1]-block.center[1]))
    for overUnder in Block.overUnderFlow:
        if (overUnder[0]==Rlocat[0]) and (overUnder[1]==Rlocat[1]):
            w+='*'
            Rfg=0
            break
    if Rfg==1:
        dRPrime=Img[Rlocat[0]][Rlocat[1]]-Img[block.center[0]][block.center[1]]    
        if -twoTStar<=dRPrime<=(twoTStar+1):
            w+=str(dRPrime%2)
            dRStar=dRPrime/2
        elif dRPrime<=-(twoTStar+1):#dR-T*
            w+='*'
            dRStar=dRPrime+Block.TStar
        elif (twoTStar+2)<=dRPrime:#T*<dR
            w+='*'
            dRStar=dRPrime-Block.TStar-1
        dR=dRStar+minStar
        Img[Rlocat[0]][Rlocat[1]]=dR+Img[block.center[0]][block.center[1]]
    
    return w
    
    
def sign(num):
    if num==0:
        return 1
    return num/abs(num)

def toOne(num):
    if num>0:
        return 1
    elif num==0:
        return 0
    else:#num<0
        return -1
        
def PSNR(oriNumImg,stegoImg):
    imgSize=len(oriNumImg)*len(oriNumImg)
    MSE=float(0)
    for row in range(len(oriNumImg)):
        for col in range(len(oriNumImg[0])):
            tem=oriNumImg[row][col]-stegoImg[row][col]
            MSE+=tem*tem
    MSE/=imgSize
    psnr=10*math.log((255*255)/MSE,10)
    return psnr


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

def picAnchor(Transparent,gray,baseImg,start,toBlack=0):
    Srow=start[0]
    Scol=start[1]
    for row in range(len(Transparent)):
        for col in range(len(Transparent[0])):
            if Transparent[row][col]==[0, 0, 0, 0]:
                pass
            elif toBlack==0:
                baseImg[row+Srow][col+Scol]=gray[row][col]
            elif toBlack==1:
                baseImg[row+Srow][col+Scol]=0
    #list is called by ref, so we can directly use baseImg in caller rather return baseImg

"""
print oriImg[adjBCenAt[0][0]][adjBCenAt[0][1]]
    print oriImg[block.center[0]][block.center[1]]
    """



