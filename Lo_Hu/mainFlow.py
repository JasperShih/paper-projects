import hindingFunct as hfun,scipy.misc as pnimg,cPickle as pickle,wx,wx.lib.filebrowsebutton,os,sys
from os.path import basename
from wx.lib.anchors import LayoutAnchors

def create(parent):
    return Frame2(parent)

[wxID_FRAME2, wxID_FRAME2BUTTON1, wxID_FRAME2BUTTON2, wxID_FRAME2CHECKBOX1,
 wxID_FRAME2FILEBROWSEBUTTONWITHHISTORY1,
 wxID_FRAME2FILEBROWSEBUTTONWITHHISTORY2,
 wxID_FRAME2FILEBROWSEBUTTONWITHHISTORY3, wxID_FRAME2NOTEBOOK1,
 wxID_FRAME2PANEL1, wxID_FRAME2PANEL2, wxID_FRAME2STATICTEXT1,
 wxID_FRAME2TEXTCTRL1,
] = [wx.NewId() for _init_ctrls in range(12)]

class Frame2(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=True, text=u'Embed')
        parent.AddPage(imageId=-1, page=self.panel2, select=False,
              text=u'Recover or Detect')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME2, name='', parent=prnt,
              pos=wx.Point(587, 342), size=wx.Size(549, 333),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame2')
        self.SetClientSize(wx.Size(533, 295))

        self.notebook1 = wx.Notebook(id=wxID_FRAME2NOTEBOOK1, name='notebook1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(533, 295), style=0)

        self.panel1 = wx.Panel(id=wxID_FRAME2PANEL1, name='panel1',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(525, 268),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME2PANEL2, name='panel2',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(525, 268),
              style=wx.TAB_TRAVERSAL)

        self.fileBrowseButtonWithHistory1 = wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME2FILEBROWSEBUTTONWITHHISTORY1, initialValue='',
              labelText='File Entry:', parent=self.panel1, pos=wx.Point(32, 32),
              size=wx.Size(408, 48), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.staticText1 = wx.StaticText(id=wxID_FRAME2STATICTEXT1,
              label=u'peak pairs:', name='staticText1', parent=self.panel1,
              pos=wx.Point(32, 128), size=wx.Size(58, 14), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME2TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(104, 128), size=wx.Size(40, 24),
              style=0, value=u'2')

        self.button1 = wx.Button(id=wxID_FRAME2BUTTON1, label=u'Embed!',
              name='button1', parent=self.panel1, pos=wx.Point(32, 184),
              size=wx.Size(120, 48), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME2BUTTON1)

        self.fileBrowseButtonWithHistory2 = wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME2FILEBROWSEBUTTONWITHHISTORY2, initialValue='',
              labelText=u'Stego or Tampered image:', parent=self.panel2,
              pos=wx.Point(24, 24), size=wx.Size(464, 48), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.fileBrowseButtonWithHistory3 = wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME2FILEBROWSEBUTTONWITHHISTORY3, initialValue='',
              labelText=u'Stego image', parent=self.panel2, pos=wx.Point(104,
              128), size=wx.Size(384, 40), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

        self.button2 = wx.Button(id=wxID_FRAME2BUTTON2,
              label=u'Recover or Detect!', name='button2', parent=self.panel2,
              pos=wx.Point(24, 200), size=wx.Size(152, 48), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME2BUTTON2)

        self.checkBox1 = wx.CheckBox(id=wxID_FRAME2CHECKBOX1,
              label=u'To generate difference images and false detection images',
              name='checkBox1', parent=self.panel2, pos=wx.Point(32, 104),
              size=wx.Size(352, 32), style=0)
        self.checkBox1.SetValue(True)
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox1Checkbox,
              id=wxID_FRAME2CHECKBOX1)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnCheckBox1Checkbox(self, event):
        if self.checkBox1.GetValue()==True:
            self.fileBrowseButtonWithHistory3.Enable()
        else:
            self.fileBrowseButtonWithHistory3.Disable()

    def OnButton1Button(self, event):
        blockSize=4
        blocation=(2,2)
        peakPair=int(self.textCtrl1.GetValue())

        filePath=self.fileBrowseButtonWithHistory1.GetValue()

        print filePath,"    peak pair:",peakPair
        print "Processing......"

        imgNum=pnimg.imread(filePath)
        img=imgNum.tolist()
        """
        Turn Numpy array to normal array. img is a normal array.
        Numpy array would not ref same obj with array
        but it will ref same obj between array
        """

        img,overStr=hfun.overProcessing(img)
        residualImg=img
        histogram=hfun.prediction(residualImg,blockSize,blocation)
        zeroList=hfun.pickZero(histogram,peakPair)
        peakList=hfun.pickPeak(histogram,zeroList)
        peakZeroList=hfun.mergePZ(peakList,zeroList)
        count=hfun.capacityCheckOver(peakZeroList,histogram,overStr)
        randonStr=hfun.genAuthCode(len(imgNum)/blockSize,len(imgNum[0])/blockSize,overStr)
        stegoImg,UnEmbImg,hisOfPeaksBlock=hfun.embeddedShiftStego(peakZeroList,residualImg,blockSize,blocation,randonStr)
        psnr=hfun.PSNR(imgNum,stegoImg,512*512)

        FileList=[peakZeroList,randonStr]
        f = file("PzRanList.data",'w')
        pickle.dump(FileList, f)
        f.close()

        for row in range(len(imgNum)):
            for col in range(len(imgNum[0])):
                imgNum[row][col]=stegoImg[row][col]
        pnimg.imsave( os.path.abspath('..')+"\\output\\Stego"+basename(filePath)[0:-4]+"P"+str(peakPair)+".bmp",imgNum )
        for row in range(len(UnEmbImg)):
            for col in range(len(UnEmbImg[0])):
                imgNum[row][col]=UnEmbImg[row][col]
        pnimg.imsave( os.path.abspath('..')+"\\output\\unembeddableBlock"+basename(filePath)[0:-4]+"P"+str(peakPair)+".bmp",imgNum )
        print "capacity=",count,"    PSNR=",psnr
        print "Total number of image blocks with different embeddable bits"
        print hisOfPeaksBlock
        print "Done."
        print ""

        __console__=sys.stdout
        f_handler=open(os.path.abspath('..')+"\\output\\embeddedRecord.txt", 'a')
        sys.stdout=f_handler
        print filePath,"    peak pair:",peakPair
        print "Processing......"
        print "capacity=",count,"    PSNR=",psnr
        print "Total number of image blocks with different embeddable bits"
        print hisOfPeaksBlock
        print "Done."
        print ""
        sys.stdout=__console__

    def OnButton2Button(self, event):
        blockSize=4
        blocation=(2,2)
        tamper=self.checkBox1.GetValue()

        filePath=self.fileBrowseButtonWithHistory2.GetValue()
        stegoNum=pnimg.imread(filePath)
        stegoImg=stegoNum.tolist()
        print filePath
        print "Processing......"

        __console__=sys.stdout
        f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
        sys.stdout=f_handler
        print filePath
        print "Processing......"
        sys.stdout=__console__

        f = file("PzRanList.data")
        FileList= pickle.load(f)
        f.close()
        peakZeroList=FileList[0]
        randonStr=FileList[1]


        if tamper==True:
            filePath2=self.fileBrowseButtonWithHistory3.GetValue()
            tamperNum=pnimg.imread(filePath2)
            tamperImg=tamperNum.tolist()

            difPCount,difBCount,difPImg,difBImg=hfun.diffImg(stegoImg,tamperImg,blockSize)
            for row in range(len(difPImg)):
                for col in range(len(difPImg[0])):
                    tamperNum[row][col]=difPImg[row][col]
                    stegoNum[row][col]=difBImg[row][col]
            pnimg.imsave( os.path.abspath('..')+"\\output\\diffPixel"+basename(filePath)[0:-4]+".bmp",tamperNum )
            pnimg.imsave( os.path.abspath('..')+"\\output\\diffBlock"+basename(filePath)[0:-4]+".bmp",stegoNum )
            print "difference pixel:",difPCount,"    difference block:",difBCount
            __console__=sys.stdout
            f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
            sys.stdout=f_handler
            print "difference pixel:",difPCount,"    difference block:",difBCount
            sys.stdout=__console__

        embResiImg=stegoImg
        hfun.prediction(embResiImg,blockSize,blocation)
        UnBCount,RecoverImg,detectUnImg=hfun.extraRcvDetc(embResiImg,peakZeroList,randonStr,blockSize,blocation)
        print "Black blocks in un-refine detected image:",UnBCount
        __console__=sys.stdout
        f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
        sys.stdout=f_handler
        print "Black blocks in un-refine detected image:",UnBCount
        sys.stdout=__console__

        if UnBCount>0:
            for row in range(len(detectUnImg)):
                for col in range(len(detectUnImg[0])):
                    stegoNum[row][col]=detectUnImg[row][col]
            pnimg.imsave( os.path.abspath('..')+"\\output\\detect"+basename(filePath)[0:-4]+".bmp",stegoNum )

            ReBCount,refineImg=hfun.refine(detectUnImg,blockSize)
            for row in range(len(refineImg)):
                for col in range(len(refineImg[0])):
                    stegoNum[row][col]=refineImg[row][col]
            pnimg.imsave( os.path.abspath('..')+"\\output\\refine"+basename(filePath)[0:-4]+".bmp",stegoNum )
            print "Black blocks in refine detected image:",ReBCount
            __console__=sys.stdout
            f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
            sys.stdout=f_handler
            print "Black blocks in refine detected image:",ReBCount
            sys.stdout=__console__


            if tamper==True:
                unDetectB,wrongDetectB,unDetectP,wrongDetectP,falDetImgP,falDetImgB=hfun.falseDetect(difPImg,difBImg,refineImg,blockSize)
                for row in range(len(falDetImgP)):
                    for col in range(len(falDetImgP[0])):
                        stegoNum[row][col]=falDetImgP[row][col]
                pnimg.imsave( os.path.abspath('..')+"\\output\\falseDetectPixel"+basename(filePath)[0:-4]+".bmp",stegoNum )
                for row in range(len(falDetImgB)):
                    for col in range(len(falDetImgB[0])):
                        stegoNum[row][col]=falDetImgB[row][col]
                pnimg.imsave( os.path.abspath('..')+"\\output\\falseDetectBlock"+basename(filePath)[0:-4]+".bmp",stegoNum )
                print "We compared refine detected image with difference block image"
                print "Blocks which should be black but it is white(Undetected):",unDetectB
                print "Blocks which should be white but it is black(Wrong detected):",wrongDetectB
                print "We compared refine detected image with difference pixel image"
                print "Pixels which should be black but it is white(Undetected):",unDetectP
                print "Pixels which should be white but it is black(Wrong detected):",wrongDetectP
                __console__=sys.stdout
                f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
                sys.stdout=f_handler
                print "We compared refine detected image with difference block image"
                print "Blocks which should be black but it is white(Undetected):",unDetectB
                print "Blocks which should be white but it is black(Wrong detected):",wrongDetectB
                print "We compared refine detected image with difference pixel image"
                print "Pixels which should be black but it is white(Undetected):",unDetectP
                print "Pixels which should be white but it is black(Wrong detected):",wrongDetectP
                sys.stdout=__console__

        else:
            recOverImg=hfun.overRecover(randonStr,RecoverImg)
            for row in range(len(recOverImg)):
                for col in range(len(recOverImg[0])):
                    stegoNum[row][col]=recOverImg[row][col]
            pnimg.imsave(os.path.abspath('..')+"\\output\\recover"+basename(filePath)[0:-4]+".bmp",stegoNum )
            print "Recover successfully"
            __console__=sys.stdout
            f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
            sys.stdout=f_handler
            print "Recover successfully"
            sys.stdout=__console__
        print "Done."
        print ""
        __console__=sys.stdout
        f_handler=open(os.path.abspath('..')+"\\output\\recoverDetectRecord.txt", 'a')
        sys.stdout=f_handler
        print "Done."
        print ""
        sys.stdout=__console__


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()

