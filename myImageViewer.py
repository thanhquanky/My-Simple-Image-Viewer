'''
Author: Thanh Ky Quan
Date: 05/20/2010
Filename: myImageViewer.py
Version: 0.1.4 beta

'''

"""
Copyright (c) <2010> <Thanh Ky Quan>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# What is new:
'''
Version 0.1.1 beta:

    + added convert to grayscale feature

Version 0.1.2 beta:

    + added convert to negative feature
    + added horizontal scrollbar and vertical scrollbar if necessary
    + set image's path on title instead of status bar like version 0.1.1
    + added menubbar for second frame instead of using buttons
    + set frame's size dynamically based on screen resolution

Version 0.1.3 beta:

    + added resize image feature
    + added shrink by scale feature
    + added progress bar
    
Version 0.1.4 beta
    
    + added drop image feature
    + load whatisnew by text editor dynamically with notepad on Windows and gedit on Linux
    + reduce the extra frame also the amount of code
    + monitor modification and show warning when user exit 
    + added save beside saveas 
    + remove default image
    + monitor mouse position
    + added several acceleration keys
'''

import wx
import os
import sys
import math

ID_CREDIT = 110
ID_CONVERT_TO_GREYSCALE = 111
ID_CONVERT_TO_NEGATIVE = 112
ID_RESIZE_IMAGE = 113
ID_SHRINK_IMAGE = 114
ID_WHATISNEW = 115
ID_CROP_IMAGE = 116
ID_EXPORT_GBA = 117
#DEF_IMAGE = 'hspt.jpg'


class MySimpleImageViewer(wx.App):
    def MakeMenubar(self):
        menubar = wx.MenuBar()
        menu_File = wx.Menu()
        menu_File.Append(wx.ID_OPEN, '&Open\tCtrl-O', 'Click here to load image')
        menu_File.Append(wx.ID_SAVE, '&Save\tCtrl-S', 'Click here to save image')
        menu_File.Append(wx.ID_SAVEAS, 'Save &As', 'Save image as')
        menu_File.Append(ID_EXPORT_GBA, '&Export GBA','Export to GBA');
        menu_File.AppendSeparator()
        menu_File.Append(wx.ID_EXIT, 'E&xit\tCtrl-X', 'Click here to terminate application')
        menu_Help = wx.Menu()
        menu_Help.Append(ID_WHATISNEW, 'What is &new', 'What is new')
        menu_Help.Append(wx.ID_ABOUT, '&About Simple image viewer\tCtrl-A', 'Click here to learn more about this application')
        menu_Help.Append(110, '&Credit\tCtrl-T', 'Creditation')
        menu_Tool = wx.Menu()
        menu_Tool.Append(ID_CONVERT_TO_GREYSCALE, 'Convert to &greyscale\tCtrl-G', 'Convert image to greyscale')
        menu_Tool.Append(ID_CONVERT_TO_NEGATIVE, 'Convert to &negative\tCtrl-N', 'Convert to negative')
        menu_Tool.Append(ID_RESIZE_IMAGE, '&Resize image\tCtrl-R', 'Resize image')
        menu_Tool.Append(ID_SHRINK_IMAGE, '&Shrink image\tCtrl-K', 'Shrink image')
        menu_Tool.Append(ID_CROP_IMAGE, '&Crop image\tCtrl-C', 'Crop image')
        menubar.Append(menu_File, '&File')
        menubar.Append(menu_Tool, '&Tools')
        menubar.Append(menu_Help, '&Help')
        self.frame.SetMenuBar(menubar)
        
        self.frame.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.frame.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.frame.Bind(wx.EVT_MENU, self.OnSaveAs, id=wx.ID_SAVEAS)
        self.frame.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id =wx.ID_ABOUT)
        self.frame.Bind(wx.EVT_MENU, self.OnCredit, id = ID_CREDIT)
        self.frame.Bind(wx.EVT_MENU, self.ConvertToGreyscale, id = ID_CONVERT_TO_GREYSCALE)
        self.frame.Bind(wx.EVT_MENU, self.ConvertToNegative, id = ID_CONVERT_TO_NEGATIVE)
        self.frame.Bind(wx.EVT_MENU, self.ResizeImage, id = ID_RESIZE_IMAGE)
        self.frame.Bind(wx.EVT_MENU, self.Shrink, id = ID_SHRINK_IMAGE)
        self.frame.Bind(wx.EVT_MENU, self.WhatIsNew, id = ID_WHATISNEW)
        self.frame.Bind(wx.EVT_CLOSE, self.OnClose, id = self.frame.GetId())
        self.frame.Bind(wx.EVT_MENU, self.CropImage, id = ID_CROP_IMAGE)
        self.frame.Bind(wx.EVT_MENU, self.ExportToGBA, id = ID_EXPORT_GBA)
        
    def configuration(self):
        self.clientMaxSize = wx.GetDisplaySize()
        self.clientMaxSize = (self.clientMaxSize[0] - 100, self.clientMaxSize[1] - 200)
        self.appname = "My Simple Image Viewer"
        self.version = "0.1.4 Beta"
        self.author = "Thanh Ky Quan"
        self.cursor = wx.StockCursor(wx.CURSOR_ARROW)    
        self.whatisnew = 'whatisnew.txt'
        self.image = ''
        self.frame2 = ''
        self.status = self.frame.CreateStatusBar()
        self.savePath = ''
        self.imagePath = ''
        self.imageBox = '' #wx.StaticBitmap(self.panel, -1, wx.EmptyBitmapRGBA(500, 500, 252, 252, 254, 0))
        self.frame.SetTitle(self.appname)
        self.is_modified = False
        self.click_point = (0,0)
        
    def CreatePanel(self):
        self.panel = wx.PyScrolledWindow(self.frame, pos = (0,0), style = wx.STAY_ON_TOP)
        
    def __init__(self, redirect = False, filename = None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, -1, title = 'Simple image viewer', size = (500, 500), pos = (0, 0))
        self.frame.SetBackgroundColour("#FCFCFE")
        self.CreatePanel()
        self.MakeMenubar()

        # Default parameters
        self.configuration()
        
        self.panel.Layout()
        self.frame.Show()
    


    # show credit
    def OnCredit(self, event):
        creditMessage = "Thanks to my computer science teachers at Florida Virtual School:\n\n"
        teachers = ['Mrs. Lisa Brock', 'Mrs. Amie Ross', 'Mr. William Jordan']
        for teacher in teachers:
            creditMessage += " - " + teacher + "\n"
        msgBox = wx.MessageDialog(None, message= creditMessage, caption = 'Credit', style = wx.OK | wx.STAY_ON_TOP)
        if (msgBox.ShowModal() == wx.ID_OK):
            msgBox.Destroy()

    # show what is new
    def WhatIsNew(self, event):
        operating_system = sys.platform
        if (operating_system.find('win')>=0):
            os.system("notepad.exe " + self.whatisnew)
        elif (operating_system.find('inux')>=0):
            os.system("gedit " + self.whatisnew)

    # show file dialog to load image
    def OnOpen(self, event):
        wc = 'All image file (*.jpg;*.png;*.bmp;*.gif)|*.jpg;*.png;*.bmp;*.gif|JPEG file (*.jpg)|*.jpg|GIF file (*.gif)|*.gif|BMP file (*.bmp)|*.bmp|PNG file (*.png)|*.png'
        dialog = wx.FileDialog(None, message = 'Select image to display', wildcard = wc, style = wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.imagePath = dialog.GetPath()
            self.loadImage()       
        dialog.Destroy()

    # close event
    def OnClose(self, event):
        if self.is_modified == True:
            msgbox = wx.MessageDialog(self.panel, message = 'File ' + os.path.basename(self.imagePath) + ' has been modified. Do you want to save?', caption = 'Warning', style = wx.STAY_ON_TOP | wx.YES | wx.NO | wx.CANCEL | wx.ICON_WARNING)
            value = msgbox.ShowModal()
            if value == wx.ID_YES:
                msgbox.Destroy()
                self.OnSaveAs(event)
            elif value == wx.ID_NO:
                msgbox.Destroy()
                self.frame.Destroy()
            else:
                msgbox.Destroy()
        else:
            self.frame.Destroy()
            

    # show about information
    def OnAbout(self, event):
        aboutMessage = "Simple Image Viewer version " + self.version + "\n\nCreated by " + self.author + "\n\nCopyright of Thanh Ky Quan, 2010"
        msgBox = wx.MessageDialog(None, message =  aboutMessage, caption = 'About', style = wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK)
        if (msgBox.ShowModal() == wx.ID_OK):
            msgBox.Destroy()
            
    # save event
    def OnSave(self, event):
        self.WriteNewImage(self.imagePath, self.image)

    # on left click
    def OnLeftClick(self, event):
        self.click_point = event.GetPosition()
    
    # on mouse motion
    def OnMouseMotion(self, event):
        self.status.SetStatusText(str(event.GetPosition()))

    #check image size and max size to add scrollbar if needed
    def IsEnableScrollbar(self, image_size):
        scroll = [False, False]
        if (image_size[0] > self.clientMaxSize[0]):
            scroll[0] = True
        if (image_size[1] > self.clientMaxSize[1]):
            scroll[1] = True
        return scroll

    #find possible ratio of scrollbar
    def GetScrollbarRatio(self, frame_size):
        HScroll_min = 20
        VScroll_min = 20
        HScroll_max = frame_size[0] / HScroll_min
        VScroll_max = frame_size[1] / VScroll_min

        ratio = [0,0,0,0]
        
        if (frame_size[0] > self.clientMaxSize[0]):
            ratio[0] = HScroll_min
            ratio[2] = HScroll_max
        if (frame_size[1] > self.clientMaxSize[1]):
            ratio[1] = VScroll_min
            ratio[3] = VScroll_max

        return ratio

    #find possible frame size
    def AdjustFrameSize(self, image_size):
        frame_size = image_size
        
        if (frame_size[0] > self.clientMaxSize[0]):
            frame_size[0] = self.clientMaxSize[0]
        if (frame_size[1] > self.clientMaxSize[1]):
            frame_size[1] = self.clientMaxSize[1]
            
        return frame_size

    #load image method    
    def loadImage(self):  
        self.image = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY)
        self.imageBox = wx.StaticBitmap(self.panel, wx.ID_ANY, self.image.ConvertToBitmap())
        self.imageBox.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.imageBox.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.status.SetStatusText(str(self.image.GetWidth()) + "x" + str(self.image.GetHeight()))
        self.UpdateTitle('')
        img_size = self.image.GetSize()
        frame_size = self.AdjustFrameSize(img_size)
        scrollbar = self.IsEnableScrollbar(self.image.GetSize())
        self.panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(self.image.GetSize())
        self.panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        self.panel.AdjustScrollbars()
        self.frame.SetClientSize(frame_size)
        self.panel.SetScale(0.1, 0.1)
        self.panel.Update()
        

    #convert image to grayscale
    def ConvertToGreyscale(self, event):
        img = self.image.ConvertToGreyscale()
        self.image = img
        self.imageBox.SetBitmap(wx.BitmapFromImage(img))
        self.is_modified = True
        self.UpdateTitle('Grayscale')
        self.panel.Update()
        
    #convert image to negative
    def ConvertToNegative(self, event):
        self.frame.ClearBackground()
        img = self.image
        wx.SetCursor(wx.StockCursor(wx.CURSOR_ARROWWAIT))
        progress = wx.ProgressDialog(title = "Converting to negative", message = "Processing", maximum = img.GetWidth(), parent = self.frame, style = wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME)
        for i in range(img.GetWidth()):
            progress.Update(i)
            for j in range(img.GetHeight()):
                r = img.GetRed(i,j)
                g = img.GetGreen(i,j)
                b = img.GetBlue(i,j)
                img.SetRGB(i, j, 255 - r, 255 - g, 255 - b)
        wx.SetCursor(self.cursor)
        progress.Destroy()
        self.image = img
        self.imageBox.SetBitmap(wx.BitmapFromImage(img))
        self.is_modified = True
        self.UpdateTitle('Negative')
        self.panel.Update()
        
    #export to GBA
    def ExportToGBA(self, event):
        img = self.image
        resizeDialog = wx.MessageDialog(parent = self.frame, caption= "Do you want to resize?", 
			message = "GBA image's resolution has only have maximum value of 240x160. If you select No, this image will be automatically scaled to 240x160", style=wx.YES_NO)

        if resizeDialog.ShowModal() == wx.ID_OK:
            self.ResizeImage(self)
        else:
            img = img.Scale(width = 240, height = 160, quality = wx.IMAGE_QUALITY_HIGH)
        colors = []
        for j in range(img.GetHeight()):
            for i in range(img.GetWidth()):
                r = int(round(img.GetRed(i,j) * 31.0 / 255.0))
                g = int(round(img.GetGreen(i,j) * 31.0 / 255.0))
                b = int(round(img.GetBlue(i,j) * 31.0 / 255.0))
                img.SetRGB(i, j, r, g, b)
                colors.append(r|g<<5|b<<10)
        self.image = img
        self.newImage = img
        self.imageBox.SetBitmap(wx.BitmapFromImage(self.image))
        frame_size = self.AdjustFrameSize(self.image.GetSize())
        scrollbar = self.IsEnableScrollbar(frame_size)
        self.panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(frame_size)
        self.panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        self.panel.AdjustScrollbars()
        self.frame.SetClientSize(frame_size)
        self.panel.SetScale(0.1, 0.1)
        self.panel.Update()
        getVarNameDialog = wx.TextEntryDialog(None, message = "Please enter variable name", caption = "Name", defaultValue = "image")
        if (getVarNameDialog.ShowModal() == wx.ID_OK):
            varName = getVarNameDialog.GetValue()
            size = img.GetWidth() * img.GetHeight()
            f = open(varName + ".c", 'w')   
            f.write("const unsigned short " + varName + "[" + str(size) + "] = {\n")
            i=0
            totalPixels = len(colors)
            for i in range(totalPixels-1):
                i = i + 1
                f.write(hex(colors[i]) + ",")
                if (i%9 == 8):
                    f.write("\n")
            f.write(hex(colors[totalPixels-1]) + "\n};")
            f.close()
            f = open(varName + ".h", 'w')
            defineName = varName.upper() + "_BITMAP_H"
            f.write("#ifndef " + defineName +"\n#define " + defineName + "\n\n")
            f.write("extern const unsigned short " + varName + " [" + str(size) + "];\n");
            f.write("#define " + varName.upper() + "_WIDTH " + str(img.GetWidth()) + "\n");
            f.write("#define " + varName.upper() + "_HEIGHT " + str(img.GetHeight()) + "\n");
            f.write("#endif")
            wx.MessageDialog(None, message = "Exported " + varName + ".h and " + varName + ".c", style=wx.ID_OK).ShowModal()
            
    #resize image
    def ResizeImage(self, event):
        self.UpdateTitle('resize image')
        w = self.image.GetWidth()
        h = self.image.GetHeight()
        getWidth = wx.TextEntryDialog(None, message = "Enter new width (current: " + str(w) + "): ", caption = "Resize Image", defaultValue = str(w))
        if getWidth.ShowModal() == wx.ID_OK:
            w = getWidth.GetValue()
            getHeight = wx.TextEntryDialog(None, message = "Enter new height (current: " + str(h) + "): ", caption = "Resize Image", defaultValue = str(h))
            if getHeight.ShowModal() == wx.ID_OK:
                h = getHeight.GetValue()
        self.newImage = self.image.Scale(width = int(w), height = int(h), quality =  wx.IMAGE_QUALITY_HIGH)
        self.image = self.newImage
        self.imageBox.SetBitmap(wx.BitmapFromImage(self.image))
        frame_size = self.AdjustFrameSize(self.image.GetSize())
        scrollbar = self.IsEnableScrollbar(frame_size)
        self.panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(frame_size)
        self.panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        self.panel.AdjustScrollbars()
        self.frame.SetClientSize(frame_size)
        self.panel.SetScale(0.1, 0.1)
        self.panel.Update()
                    
    # shrink image
    def Shrink(self, event):
        self.UpdateTitle('resize image')
        scaleX = 1
        scaleY = 1
        getScaleX = wx.TextEntryDialog(self.frame, message = "Enter x factor (current: " + str(1) + "): ", caption = "Shrink Image", defaultValue = str(2))
        if getScaleX.ShowModal() == wx.ID_OK:
            scaleX = getScaleX.GetValue()
            getScaleY = wx.TextEntryDialog(self.frame, message = "Enter y factor (current: " + str(1) + "): ", caption = "Shrink Image", defaultValue = str(2))
            if getScaleY.ShowModal() == wx.ID_OK:
                scaleY = getScaleY.GetValue()
        img = self.image.ShrinkBy((float) (scaleX), (float) (scaleY))
        self.image = img
        self.imageBox.SetBitmap(self.image.ConvertToBitmap())
        frame_size = self.AdjustFrameSize(img.GetSize())
        
        scrollbar = self.IsEnableScrollbar(frame_size)
        self.panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(frame_size)
        self.panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        self.panel.AdjustScrollbars()
        self.frame.SetClientSize(frame_size)
        self.panel.SetScale(0.1, 0.1)
    
    # crop image by x,y coordinates
    def CropImage(self, event):      
        def CloseWindow(self, event): 
            self.frame2.Destroy()
        wx.SetCursor(wx.StockCursor(wx.CURSOR_CROSS));    
        self.frame2 = wx.Frame(self.frame, -1, 'Select crop position', pos = (0,0), size = (300, 200))
        panel = wx.PyScrolledWindow(self.frame2)
        xA_label = wx.StaticText(panel, -1, 'xA', pos = (10, 20), size = (80, 40), style = wx.ALIGN_CENTER)
        self.xA = wx.SpinCtrl(panel, -1, '', pos = (100, 20), size = (80, 40), style = wx.SP_WRAP)
        self.xA.SetRange(0, self.image.GetHeight())
        yA_label = wx.StaticText(panel, -1, 'yA', pos = (10, 50), size = (80, 40), style = wx.ALIGN_CENTER)
        self.yA = wx.SpinCtrl(panel, -1, '', pos = (100, 50), size = (80, 40), style = wx.SP_WRAP)
        self.yA.SetRange(0, self.image.GetWidth())
        xB_label = wx.StaticText(panel, -1, 'xB', pos = (10, 80), size = (80, 40), style = wx.ALIGN_CENTER)
        self.xB = wx.SpinCtrl(panel, -1, '', pos = (100, 80), size = (80, 40), style = wx.SP_WRAP)
        self.xB.SetRange(0, self.image.GetHeight())
        yB_label = wx.StaticText(panel, -1, 'yB', pos = (10, 110), size = (80, 40), style = wx.ALIGN_CENTER)
        self.yB = wx.SpinCtrl(panel, -1, '', pos = (100, 110), size = (80, 40), style = wx.SP_WRAP)
        self.yB.SetRange(0, self.image.GetWidth())
        ok_btn = wx.Button(panel, wx.NewId(), label = 'OK', pos = (200, 30), size = (60, 40), style = wx.ID_OK)
        cancel_btn = wx.Button(panel, wx.NewId(), label = 'Cancel', pos = (200, 100), size = (60, 40), style = wx.ID_CANCEL)
        self.frame2.Bind(wx.EVT_BUTTON, self.CropImageSelection, id = ok_btn.GetId())
        self.frame2.Bind(wx.EVT_BUTTON, self.CloseExtraWindow, id = cancel_btn.GetId())
        self.frame2.Show()
                        
    # get selected points
    def CropImageSelection(self, event):        
        pA = wx.Point(self.xA.GetValue(), self.yA.GetValue())
        pB = wx.Point(self.xB.GetValue(), self.yB.GetValue())
        w = math.fabs(pB.x - pA.x)
        h = math.fabs(pB.y - pA.y)
        rect = wx.Rect(pA.x, pA.y, (int) (w), (int) (h))
        img = self.image.GetSubImage(rect)
        self.image = img
        self.imageBox.SetBitmap(img.ConvertToBitmap())
        frame_size = self.AdjustFrameSize(img.GetSize())
        
        scrollbar = self.IsEnableScrollbar(frame_size)
        self.panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(frame_size)
        self.panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        self.panel.AdjustScrollbars()
        self.frame.SetClientSize(frame_size)
        self.panel.SetScale(0.1, 0.1)
        self.UpdateTitle('crop')
        self.is_modified = True
        self.CloseExtraWindow(event)
        
    # close extra window
    def CloseExtraWindow(self, event):
        self.frame2.Destroy()
        
    # update title
    def UpdateTitle(self, newTitle):
        newTitle = self.appname + ' - ' + os.path.basename(self.imagePath) + ' - ' + newTitle
        if self.is_modified == True:
            newTitle = newTitle + ' - Modified'
        self.frame.SetTitle(newTitle)
        
        
    #save image
    def OnSaveAs(self, event):
        dialog = wx.FileDialog(self.frame, message = 'Save your image', wildcard = "JPEG file (*.jpg, *.jpeg), PNG file (*.png), BMP file (*.bmp)| *.jpg, *.png, *.jpeg, *.bmp", style = wx.SAVE)
        if (dialog.ShowModal() == 5100):
            path = dialog.GetPath()
            self.WriteNewImage(path, self.image)
        else:
            self.savePath = ""
        dialog.Destroy()
        
    # get file extension
    def getExtension(self, path):
        return os.path.splitext(path)[1]

    # write output
    def WriteNewImage(self, path, img):
        ext = self.getExtension(path)
        imgType = {
            '.jpg': wx.BITMAP_TYPE_JPEG,
            '.jpeg': wx.BITMAP_TYPE_JPEG,
            '.png': wx.BITMAP_TYPE_PNG,
            '.bmp': wx.BITMAP_TYPE_BMP
        }
        img.SaveFile(path, imgType.get(ext))
        self.UpdateTitle('saved')
        self.is_modified = False
                               
        
def main():
    app = MySimpleImageViewer()
    app.MainLoop()
    
main()
