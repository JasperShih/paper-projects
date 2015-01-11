#Boa:Frame:Frame1

import wx
import wx.lib.filebrowsebutton
from wx.lib.anchors import LayoutAnchors
import improveFunc as imF, scipy.misc as pnimg,random,cPickle as pickle
from os.path import basename
import os,sys

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1BUTTON3, 
 wxID_FRAME1CHECKBOX1, wxID_FRAME1FILEBROWSEBUTTON1, 
 wxID_FRAME1FILEBROWSEBUTTON2, wxID_FRAME1FILEBROWSEBUTTON3, 
 wxID_FRAME1FILEBROWSEBUTTON4, wxID_FRAME1FILEBROWSEBUTTON5, 
 wxID_FRAME1FILEBROWSEBUTTON6, wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1PANEL3, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, 
 wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT6, wxID_FRAME1STATICTEXT7, 
 wxID_FRAME1STATICTEXT8, wxID_FRAME1TEXTCTRL1, wxID_FRAME1TEXTCTRL2, 
 wxID_FRAME1TEXTCTRL3, wxID_FRAME1TEXTCTRL4, wxID_FRAME1TEXTCTRL5, 
] = [wx.NewId() for _init_ctrls in range(28)]

class Frame1(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=True,
              text=u'Embeding')
        parent.AddPage(imageId=-1, page=self.panel2, select=False,
              text=u'Extracting')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text=u'Picture anchor')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(811, 235), size=wx.Size(630, 368),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(614, 330))

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(614, 330), style=0)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(606, 303),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(606, 303),
              style=wx.TAB_TRAVERSAL)
        self.panel2.SetConstraints(LayoutAnchors(self.panel2, True, True, False,
              False))

        self.fileBrowseButton1 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON1, initialValue='',
              labelText=u'Original Image', parent=self.panel1, pos=wx.Point(32,
              24), size=wx.Size(544, 48), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'T*=', name='staticText1', parent=self.panel1,
              pos=wx.Point(40, 104), size=wx.Size(24, 14), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(72, 104), size=wx.Size(24, 24),
              style=0, value=u'')

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'max Th list', name='staticText2', parent=self.panel1,
              pos=wx.Point(40, 176), size=wx.Size(59, 14), style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
              parent=self.panel1, pos=wx.Point(120, 176), size=wx.Size(100, 22),
              style=0, value=u'')

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'range Th list', name='staticText3', parent=self.panel1,
              pos=wx.Point(40, 232), size=wx.Size(68, 14), style=0)

        self.textCtrl3 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL3, name='textCtrl3',
              parent=self.panel1, pos=wx.Point(120, 232), size=wx.Size(100, 22),
              style=0, value=u'')

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'Embed!',
              name='button1', parent=self.panel1, pos=wx.Point(496, 232),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.fileBrowseButton2 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON2, initialValue='',
              labelText=u'Stego/Tampered image', parent=self.panel2,
              pos=wx.Point(8, 24), size=wx.Size(576, 48), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'Extract!',
              name='button2', parent=self.panel2, pos=wx.Point(512, 248),
              size=wx.Size(75, 24), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME1BUTTON2)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'(Split list by comma)', name='staticText4',
              parent=self.panel1, pos=wx.Point(224, 184), size=wx.Size(111, 14),
              style=0)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'(Split list by comma)', name='staticText5',
              parent=self.panel1, pos=wx.Point(224, 240), size=wx.Size(111, 14),
              style=0)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(606, 303),
              style=wx.TAB_TRAVERSAL)

        self.checkBox1 = wx.CheckBox(id=wxID_FRAME1CHECKBOX1,
              label=u'Generating different image', name='checkBox1',
              parent=self.panel2, pos=wx.Point(16, 112), size=wx.Size(240, 24),
              style=0)
        self.checkBox1.SetValue(True)
        self.checkBox1.SetThemeEnabled(True)
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox1Checkbox,
              id=wxID_FRAME1CHECKBOX1)

        self.fileBrowseButton3 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON3, initialValue='',
              labelText=u'Stego:', parent=self.panel2, pos=wx.Point(104, 144),
              size=wx.Size(480, 40), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')
        self.fileBrowseButton3.SetThemeEnabled(True)

        self.fileBrowseButton4 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON4, initialValue='',
              labelText=u'Transparent:', parent=self.panel3, pos=wx.Point(32,
              24), size=wx.Size(512, 48), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.fileBrowseButton5 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON5, initialValue='',
              labelText=u'Gray', parent=self.panel3, pos=wx.Point(32, 104),
              size=wx.Size(512, 40), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.fileBrowseButton6 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON6, initialValue='',
              labelText=u'Stego:', parent=self.panel3, pos=wx.Point(32, 176),
              size=wx.Size(512, 40), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.button3 = wx.Button(id=wxID_FRAME1BUTTON3, label=u'Anchor!',
              name='button3', parent=self.panel3, pos=wx.Point(472, 256),
              size=wx.Size(75, 24), style=0)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button,
              id=wxID_FRAME1BUTTON3)

        self.textCtrl4 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL4, name='textCtrl4',
              parent=self.panel3, pos=wx.Point(152, 256), size=wx.Size(32, 22),
              style=0, value=u'')

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'start position:', name='staticText6', parent=self.panel3,
              pos=wx.Point(32, 256), size=wx.Size(75, 14), style=0)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label=u'row=', name='staticText7', parent=self.panel3,
              pos=wx.Point(120, 256), size=wx.Size(30, 14), style=0)

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8,
              label=u', colume=', name='staticText8', parent=self.panel3,
              pos=wx.Point(192, 256), size=wx.Size(56, 14), style=0)

        self.textCtrl5 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL5, name='textCtrl5',
              parent=self.panel3, pos=wx.Point(256, 256), size=wx.Size(32, 22),
              style=0, value=u'')

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        stdoutFd=sys.stdout
        writeFd=open(os.path.abspath('..')+"\\output\\tem.txt",'w')
        sys.stdout=writeFd
        
        inPath=self.fileBrowseButton1.GetValue()
        #inPath="C:\\Users\\Jasper\\Desktop\\lena.bmp"#v
        picName=basename(inPath).strip().split('.')
        print picName[0]
        saveNum=pnimg.imread(inPath)
        oriNum=pnimg.imread(inPath)
        oriImg=oriNum.tolist()
        Ori=oriNum.tolist()
        imF.hiImg=Ori
        blockSize=3
        centerBias=(1,1)
        imF.Block.imgSize=len(oriImg)
        imF.Block.blockSize=blockSize
        imF.Block.centerBias=centerBias
        #Blocking
        BofImg=[]
        for bRowOfImg in range(0,len(oriImg)-blockSize+1,blockSize):
            for bColOfImg in range(0,len(oriImg[0])-blockSize+1,blockSize):
                BofImg.append(imF.Block((bRowOfImg,bColOfImg)))
                
        
        TStar=int(self.textCtrl1.GetValue())
        imF.Block.TStar=TStar
        print "T*="+self.textCtrl1.GetValue()
        
        maxTh=[]
        tem=self.textCtrl2.GetValue().strip().split(',')
        if tem==[u'']:
            pass
        else:
            for Th in tem:
                maxTh.append(int(Th))
        print "maxTh list="+self.textCtrl2.GetValue()
        print "rangeTh list="+self.textCtrl3.GetValue()
        print ""
            

        #Max then Embed
        for Th in maxTh:
            print "max    Th="+str(Th)
            oriImg=oriNum.tolist() #each Th needs a new oriImg
            blockUnEableImg=[[255 for i in range(len(oriImg))]for i in range(len(oriImg[0]))]
            imF.Block.overUnderFlow=[]
            rSeed=random.random()
            random.seed(rSeed)
            imF.Block.embedBitCapacity=0
            imF.Block.embedBlockCapacity=0
            
            for block in BofImg:
                imF.embed(imF.maxS(oriImg,block,Th),block,oriImg)
                if imF.Block.blockEmbeddable==0:
                    for row in range(block.start[0],block.start[0]+block.blockSize):
                        for col in range(block.start[1],block.start[1]+block.blockSize):
                            blockUnEableImg[row][col]=0


            print "PSNR:"+str(imF.PSNR(Ori,oriImg))
            for row in range(len(oriImg)):
                for col in range(len(oriImg[0])):
                    saveNum[row][col]=oriImg[row][col]
            #LenaStego,max,Th,Tstar
            idName=picName[0]+"Stego,max,"+str(Th)+","+str(TStar)+","
            outName=idName+".bmp"
            outName=os.path.abspath('..')+"\\output\\"+outName
            pnimg.imsave(outName,saveNum )
            
            for row in range(len(blockUnEableImg)):
                for col in range(len(blockUnEableImg[0])):
                    saveNum[row][col]=blockUnEableImg[row][col]
            outName="UnembeddableBlock"+idName+".bmp"
            outName=os.path.abspath('..')+"\\output\\"+outName
            pnimg.imsave(outName,saveNum )
            
            
            dataName=idName+".data"
            dataName=os.path.abspath('..')+"\\output\\"+dataName
            f = file(dataName,'w')
            pickle.dump([rSeed,imF.Block.overUnderFlow], f)
            f.close()
            print "embedding bits:"+str(imF.Block.embedBitCapacity)
            print "embeddable blocks:"+str(imF.Block.embedBlockCapacity)
            print ""
        
             
        
        
        
        rangeTh=[]
        tem=self.textCtrl3.GetValue().strip().split(',')
        if tem==[u'']:
            pass
        else:
            for Th in tem:
                rangeTh.append(int(Th))
            

        for Th in rangeTh:
            print "range    Th="+str(Th)
            oriImg=oriNum.tolist() #each Th needs a new oriImg
            blockUnEableImg=[[255 for i in range(len(oriImg))]for i in range(len(oriImg[0]))]
            imF.Block.overUnderFlow=[]
            rSeed=random.random()
            random.seed(rSeed)
            imF.Block.embedBitCapacity=0
            imF.Block.embedBlockCapacity=0
            
            for block in BofImg:
                imF.embed(imF.rangeS(oriImg,block,Th),block,oriImg)
                if imF.Block.blockEmbeddable==0:
                    for row in range(block.start[0],block.start[0]+block.blockSize):
                        for col in range(block.start[1],block.start[1]+block.blockSize):
                            blockUnEableImg[row][col]=0
            print "PSNR:"+str(imF.PSNR(Ori,oriImg))
            for row in range(len(oriImg)):
                for col in range(len(oriImg[0])):
                    saveNum[row][col]=oriImg[row][col]
                    
            #LenaStego,range,Th,Tstar
            idName=picName[0]+"Stego,range,"+str(Th)+","+str(TStar)+","
            outName=idName+".bmp"
            outName=os.path.abspath('..')+"\\output\\"+outName
            pnimg.imsave(outName,saveNum )
            
            for row in range(len(blockUnEableImg)):
                for col in range(len(blockUnEableImg[0])):
                    saveNum[row][col]=blockUnEableImg[row][col]
            outName="UnembeddableBlock"+idName+".bmp"
            outName=os.path.abspath('..')+"\\output\\"+outName
            pnimg.imsave(outName,saveNum )
            
            dataName=idName+".data"
            dataName=os.path.abspath('..')+"\\output\\"+dataName
            f = file(dataName,'w')
            pickle.dump([rSeed,imF.Block.overUnderFlow], f)
            f.close()
            print "embedding bits:"+str(imF.Block.embedBitCapacity)
            print "embeddable blocks:"+str(imF.Block.embedBlockCapacity)
            print ""
        print "==============================================================="
        
        sys.stdout=stdoutFd
        writeFd.close()
        
        readFd=file(os.path.abspath('..')+"\\output\\tem.txt",'r')
        outStr=readFd.read()
        readFd.close()
        print outStr
        writeFd=file(os.path.abspath('..')+"\\output\\embedRecord.txt",'a')
        writeFd.write(outStr)
        writeFd.close()

    def OnButton2Button(self, event):
        stegoPath=self.fileBrowseButton2.GetValue()
        #stegoPath="C:\\Users\\Jasper\\Desktop\\lenaStego,range,1,1,.bmp"#v
        
        
        fNameParse=stegoPath.strip().split(',')
        stegoName=basename(stegoPath)#
        if stegoName[0:8]=="tampered":
            basePath=stegoName[8:]
        else:
            basePath=stegoName
        basePath=basePath.strip().split('.')
        saveNum=pnimg.imread(stegoPath)
        stegoNum=pnimg.imread(stegoPath)
        stegoImg=stegoNum.tolist()
        blockSize=3
        centerBias=(1,1)
        imF.Block.imgSize=len(stegoImg)
        imF.Block.blockSize=blockSize
        imF.Block.centerBias=centerBias
        BofImg=[]
        for bRowOfImg in range(0,len(stegoImg)-blockSize+1,blockSize):
            for bColOfImg in range(0,len(stegoImg[0])-blockSize+1,blockSize):
                BofImg.append(imF.Block((bRowOfImg,bColOfImg)))
        TStar=int(fNameParse[3])
        imF.Block.TStar=TStar
        f = file(os.path.abspath('..')+"\\output\\"+basePath[0]+".data")
        rSeed,imF.Block.overUnderFlow= pickle.load(f)
        f.close()
        random.seed(rSeed)
        
        
        if(self.checkBox1.GetValue()==True):
            realStego=pnimg.imread(self.fileBrowseButton3.GetValue())
            realStegoImg=realStego.tolist()
            difPCount,difBCount,difPImg,difBImg=imF.diffImg(realStegoImg, stegoImg, blockSize)
            for row in range(len(difPImg)):
                for col in range(len(difPImg[0])):
                    saveNum[row][col]=difPImg[row][col]
            pnimg.imsave(os.path.abspath('..')+"\\output\\"+"pixelDiff"+stegoName,saveNum )
            for row in range(len(difBImg)):
                for col in range(len(difBImg[0])):
                    saveNum[row][col]=difBImg[row][col]
            pnimg.imsave(os.path.abspath('..')+"\\output\\"+"blockDiff"+stegoName,saveNum )
            
        
        if fNameParse[1]=="max":
            maxTh=int(fNameParse[2])
            W=""
            for block in BofImg:
                W+=imF.extract(imF.maxS(stegoImg,block,maxTh),block,stegoImg)
            #print W
        
        elif fNameParse[1]=="range":
            rangeTh=int(fNameParse[2])
            W=""
            for block in BofImg:
                W+=imF.extract(imF.rangeS(stegoImg,block,rangeTh),block,stegoImg)
            #print W
        
        
        
        dtcImg=[[255 for i in range(len(stegoImg))]for j in range(len(stegoImg))]
        Wind=0
        tamper=0
        for bRowOfImg in range(0,len(dtcImg)-blockSize+1,blockSize):
            for bColOfImg in range(0,len(dtcImg[0])-blockSize+1,blockSize):
                paintFg=0
                embStr=str(random.randint(0,1))
                if W[Wind]=='*' or W[Wind]==embStr:
                    pass
                else:
                    paintFg=1
                    tamper=1
                Wind+=1
        
                embStr=str(random.randint(0,1))
                if W[Wind]=='*' or W[Wind]==embStr:
                    pass
                else:
                    paintFg=1
                    tamper=1
                Wind+=1
                if(paintFg):
                    for Row in range(bRowOfImg,bRowOfImg+blockSize):
                        for Col in range(bColOfImg,bColOfImg+blockSize):
                            dtcImg[Row][Col]=0
        
        
        if(tamper):
            for row in range(len(dtcImg)):
                for col in range(len(dtcImg[0])):
                    saveNum[row][col]=dtcImg[row][col]
            pnimg.imsave(os.path.abspath('..')+"\\output\\"+"DetecImg"+stegoName,saveNum )
            
            ReBCount,refineImg=imF.refine(dtcImg, blockSize)
            for row in range(len(refineImg)):
                for col in range(len(refineImg[0])):
                    saveNum[row][col]=refineImg[row][col]
            pnimg.imsave(os.path.abspath('..')+"\\output\\"+"refineDetecImg"+stegoName,saveNum )
            print "Detecting image generated"
        elif tamper==0:
            for row in range(len(stegoImg)):
                for col in range(len(stegoImg[0])):
                    saveNum[row][col]=stegoImg[row][col]
            pnimg.imsave(os.path.abspath('..')+"\\output\\"+"RecoverImg"+stegoName,saveNum )
            #pnimg.imsave("C:\\Users\\Jasper\\Desktop\\recoverImg.bmp",saveNum )
            print "Recover successfully"

    def OnButton3Button(self, event):
        temPath=self.fileBrowseButton4.GetValue()      
        TrNum=pnimg.imread(temPath)
        TrImg=TrNum.tolist()
        temPath=self.fileBrowseButton5.GetValue()
        grayNum=pnimg.imread(temPath)
        grayImg=grayNum.tolist()  
        temPath=self.fileBrowseButton6.GetValue()
        stegoNum=pnimg.imread(temPath)
        stegoImg=stegoNum.tolist()    
        stegoName=basename(temPath)#
        
        
        Scol=int(self.textCtrl4.GetValue())
        Srow=int(self.textCtrl5.GetValue())
        
        imF.picAnchor(TrImg, grayImg, stegoImg, (Scol,Srow))   
        for row in range(len(stegoImg)):
                for col in range(len(stegoImg[0])):
                    stegoNum[row][col]=stegoImg[row][col]
        pnimg.imsave(os.path.abspath('..')+"\\output\\"+"tampered"+stegoName,stegoNum )

    def OnCheckBox1Checkbox(self, event):
        if self.checkBox1.GetValue()==True:
            self.fileBrowseButton3.Enable()
        else:
            self.fileBrowseButton3.Disable()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
