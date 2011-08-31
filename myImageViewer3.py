'''
Author: Thanh Ky Quan
Date: 05/19/2010
Filename: myImageViewer.py
Version: 0.1.2 beta
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

'''
What's new:

Version 0.1.1 beta:

    + add convert to grayscale feature

Version 0.1.2 beta:

    + add convert to negative feature
    + add horizontal scrollbar and vertical scrollbar if necessary
    + set image's path on title instead of status bar like version 0.1.1 beta
    + add menubbar for second frame instead of using buttons
    + set frame's size dynamically based on screen resolution
    
'''

import wx
import copy

ID_CREDIT = 110
ID_CONVERT_TO_GREYSCALE = 111
ID_CONVERT_TO_NEGATIVE = 112
ID_RESIZE_IMAGE = 113
DEF_IMAGE = 'hspt.jpg'


class MySimpleImageViewer(wx.App):
    def MakeMenubar(self):
        menubar = wx.MenuBar()
        menu_File = wx.Menu()
        menu_File.Append(wx.ID_OPEN, '&Open', 'Click here to load image')
        menu_File.Append(wx.ID_SAVE, '&Save As', 'Click here to save image')
        menu_File.Append(wx.ID_EXIT, 'E&xit', 'Click here to terminate application')
        menu_Help = wx.Menu()
        menu_Help.Append(wx.ID_ABOUT, '&About Simple image viewer', 'Click here to learn more about this application')
        menu_Help.Append(110, '&Credit', 'Creditation')
        menu_Tool = wx.Menu()
        menu_Tool.Append(ID_CONVERT_TO_GREYSCALE, 'Convert to &greyscale', 'Convert image to greyscale')
        menu_Tool.Append(ID_CONVERT_TO_NEGATIVE, 'Convert to &negative', 'Convert to negative')
        menu_Tool.Append(ID_RESIZE_IMAGE, '&Resize image', 'Resize image')
        menubar.Append(menu_File, '&File')
        menubar.Append(menu_Tool, '&Tool')
        menubar.Append(menu_Help, '&Help')

        return menubar
    
    def configuration(self):
        self.clientMaxSize = wx.GetDisplaySize()
        self.clientMaxSize = (self.clientMaxSize[0] - 100, self.clientMaxSize[1] - 200)
        self.appname = "My Simple Image Viewer"
        self.version = "0.1.2 Beta"
        self.author = "Thanh Ky Quan"
        self.cursor = wx.StockCursor(wx.CURSOR_ARROW)    

        
    def __init__(self, redirect = False, filename = None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, -1, title = 'Simple image viewer', size = (500, 500), pos = (0, 0))
        self.panel = wx.PyScrolledWindow(self.frame, pos = (0,0))
      
        self.configuration()

        self.frame.SetMenuBar(self.MakeMenubar())
        self.frame.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.frame.Bind(wx.EVT_MENU, self.OnClickExit, id=wx.ID_EXIT)
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id =wx.ID_ABOUT)
        self.frame.Bind(wx.EVT_MENU, self.OnCredit, id = ID_CREDIT)
        self.frame.Bind(wx.EVT_MENU, self.ConvertToGreyscale, id = ID_CONVERT_TO_GREYSCALE)
        self.frame.Bind(wx.EVT_MENU, self.ConvertToNegative, id = ID_CONVERT_TO_NEGATIVE)
        self.frame.Bind(wx.EVT_MENU, self.ResizeImage, id = ID_RESIZE_IMAGE)
        
        self.hBox = wx.BoxSizer()
        self.vBox = wx.BoxSizer(wx.VERTICAL)
        self.vBox.Add(self.hBox, proportion = 1, flag = wx.EXPAND, border = 0)
        self.imagePath = DEF_IMAGE        
        tmpImg = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY)

        self.frame.SetClientSize(tmpImg.GetSize())
        self.imageBox = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(tmpImg))
        self.hBox.Add(self.imageBox, proportion = 1, flag = wx.EXPAND, border = 0)

        # Default parameters
        self.image = tmpImg
        self.frame2 = ''
        self.status = self.frame.CreateStatusBar()
        self.savePath = ""
        self.newImage = ""
        self.status.SetStatusText(str(tmpImg.GetWidth()) + "x" + str(tmpImg.GetHeight()))
        self.frame.SetTitle(self.appname + " - " + self.imagePath)
        
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

    # show file dialog to load image
    def OnOpen(self, event):
        wc = 'All image file (*.jpg;*.png;*.bmp;*.gif)|*.jpg;*.png;*.bmp;*.gif|JPEG file (*.jpg)|*.jpg|GIF file (*.gif)|*.gif|BMP file (*.bmp)|*.bmp|PNG file (*.png)|*.png'
        dialog = wx.FileDialog(None, message = 'Select image to display', wildcard = wc, style = wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.imagePath = dialog.GetPath()
            self.loadImage()       
        dialog.Destroy()

    # show about information
    def OnAbout(self, event):
        aboutMessage = "Simple Image Viewer version " + self.version + "\n\nCreated by " + self.author
        msgBox = wx.MessageDialog(None, message =  aboutMessage, caption = 'About', style = wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK)
        if (msgBox.ShowModal() == wx.ID_OK):
            msgBox.Destroy()

    #check image size and max size to add scrollbar if needed
    def IsEnableScrollbar(self, frame_size):
        scroll = [False, False]
        
        if (frame_size[0] > self.clientMaxSize[0]):
            scroll[0] = True
        if (frame_size[1] > self.clientMaxSize[1]):
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
        self.imageBox.SetBitmap(wx.BitmapFromImage(self.image))
        self.status.SetStatusText(str(self.image.GetWidth()) + "x" + str(self.image.GetHeight()))
        self.frame.SetTitle(self.appname + " - " + self.imagePath)
        frame_size = self.AdjustFrameSize(self.image.GetSize())
        scrollbar = self.IsEnableScrollbar(self.image.GetSize())
        self.panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(self.image.GetSize())
        self.panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        self.panel.AdjustScrollbars()
        self.frame.SetClientSize(frame_size)
        self.panel.SetScale(0.1, 0.1)
        self.panel.Refresh()

    #convert image to grayscale
    def ConvertToGreyscale(self, event):
        frame = wx.Frame(None, -1, 'Convert To Greyscale', pos = (0,0))
        self.frame2 = frame
        panel = wx.PyScrolledWindow(frame, style = wx.STAY_ON_TOP)
        img = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY).ConvertToGreyscale()
        self.newImage = img
        imageBox = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(img))
        frame_size = self.AdjustFrameSize(img.GetSize())
        
        scrollbar = self.IsEnableScrollbar(self.image.GetSize())
        panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(self.image.GetSize())
        panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        panel.AdjustScrollbars()
        frame.SetClientSize(frame_size)
        panel.SetScale(0.1, 0.1)

        
        frame.SetMenuBar(self.MakeMenubar())
        frame.Bind(wx.EVT_MENU, self.SaveImage, id = wx.ID_SAVE)
        frame.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        frame.Bind(wx.EVT_MENU, self.OnClickExit, id=wx.ID_EXIT)
        frame.Bind(wx.EVT_MENU, self.OnAbout, id =wx.ID_ABOUT)
        frame.Bind(wx.EVT_MENU, self.OnCredit, id = ID_CREDIT)
        frame.Bind(wx.EVT_MENU, self.ConvertToGreyscale, id = ID_CONVERT_TO_GREYSCALE)
        frame.Bind(wx.EVT_MENU, self.ConvertToNegative, id = ID_CONVERT_TO_NEGATIVE)
        frame.SetClientSize(frame_size)        
        frame.Show()

    #convert image to negative
    def ConvertToNegative(self, event):
        frame = wx.Frame(None, -1, 'Convert To Negative', pos = (0,0))
        self.frame2 = frame
        panel = wx.PyScrolledWindow(frame, style = wx.STAY_ON_TOP)
        img = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY)
        wx.SetCursor(wx.StockCursor(wx.CURSOR_ARROWWAIT))
        progress = wx.ProgressDialog(title = "Converting to negative", message = "Processing", maximum = img.GetWidth(), parent = frame, style = wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME)
        for i in range(img.GetWidth()):
            progress.Update(i)
            for j in range(img.GetHeight()):
                img.SetRGB(i,j,255-img.GetRed(i,j), 255-img.GetGreen(i,j), 255 - img.GetRed(i,j))
        wx.SetCursor(self.cursor)
        progress.Destroy()
        self.newImage = img
        imageBox = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(img))
        frame_size = self.AdjustFrameSize(img.GetSize())
        
        scrollbar = self.IsEnableScrollbar(frame_size)
        panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(frame_size)
        panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        panel.AdjustScrollbars()
        frame.SetClientSize(frame_size)
        panel.SetScale(0.1, 0.1)

        frame.SetMenuBar(self.MakeMenubar())
        frame.SetMenuBar(self.MakeMenubar())
        frame.Bind(wx.EVT_MENU, self.SaveImage, id = wx.ID_SAVE)
        frame.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        frame.Bind(wx.EVT_MENU, self.OnClickExit, id=wx.ID_EXIT)
        frame.Bind(wx.EVT_MENU, self.OnAbout, id =wx.ID_ABOUT)
        frame.Bind(wx.EVT_MENU, self.OnCredit, id = ID_CREDIT)
        frame.Bind(wx.EVT_MENU, self.ConvertToGreyscale, id = ID_CONVERT_TO_GREYSCALE)
        frame.Bind(wx.EVT_MENU, self.ConvertToNegative, id = ID_CONVERT_TO_NEGATIVE)        
        frame.SetClientSize(frame_size)        
        frame.Show()

    #resize image
    def ResizeImage(self, event):
        frame = wx.Frame(None, -1, 'Resize Image', pos = (0,0))
        self.frame2 = frame
        panel = wx.PyScrolledWindow(frame, style = wx.STAY_ON_TOP)
        w = self.image.GetWidth()
        h = self.image.GetHeight()
        getWidth = wx.TextEntryDialog(None, message = "Enter new width (current: " + str(w) + "): ", caption = "Resize Image", defaultValue = str(w))
        if getWidth.ShowModal() == wx.ID_OK:
            w = getWidth.GetValue()
            getHeight = wx.TextEntryDialog(None, message = "Enter new width (current: " + str(h) + "): ", caption = "Resize Image", defaultValue = str(h))
            if getHeight.ShowModal() == wx.ID_OK:
                h = getHeight.GetValue()
        self.newImage = self.image.Scale((int) (w), (int) (h))
        img = self.newImage
        imageBox = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(img))
        frame_size = self.AdjustFrameSize(img.GetSize())
        
        scrollbar = self.IsEnableScrollbar(frame_size)
        panel.EnableScrolling(scrollbar[0], scrollbar[1])
        ratio = self.GetScrollbarRatio(frame_size)
        panel.SetScrollbars(ratio[0], ratio[1], ratio[2], ratio[3])
        panel.AdjustScrollbars()
        frame.SetClientSize(frame_size)
        panel.SetScale(0.1, 0.1)

        frame.SetMenuBar(self.MakeMenubar())
        frame.SetMenuBar(self.MakeMenubar())
        frame.Bind(wx.EVT_MENU, self.SaveImage, id = wx.ID_SAVE)
        frame.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        frame.Bind(wx.EVT_MENU, self.OnClickExit, id=wx.ID_EXIT)
        frame.Bind(wx.EVT_MENU, self.OnAbout, id =wx.ID_ABOUT)
        frame.Bind(wx.EVT_MENU, self.OnCredit, id = ID_CREDIT)
        frame.Bind(wx.EVT_MENU, self.ConvertToGreyscale, id = ID_CONVERT_TO_GREYSCALE)
        frame.Bind(wx.EVT_MENU, self.ConvertToNegative, id = ID_CONVERT_TO_NEGATIVE)        
        frame.SetClientSize(frame_size)        
        frame.Show()
                    
                
        
    #clear frame
    def ClearFrame(self, event):
        self.newImage = ""
        self.frame2.Destroy()
    
    #close window
    def CloseWindow(self, event):
        self.frame2.Destroy()

    #save image
    def SaveImage(self, event):
        dialog = wx.FileDialog(self.frame2, message = 'Save your image', wildcard = 'JPEG file (*.jpg) | *.jpg', style = wx.SAVE)
        if (dialog.ShowModal() == 5100):
            self.WriteNewImage(dialog.GetPath(), self.newImage)
            self.frame2.SetTitle(self.appname + " - " + dialog.GetPath())
        else:
            self.savePath = ""
        dialog.Destroy()

    # write output
    def WriteNewImage(self, path, img):
        img.SaveFile(path, wx.BITMAP_TYPE_JPEG)
        self.savePath = ""
                               

    # exit event
    def OnClickExit(self, event):
        self.frame.Destroy()
        
def main():
    app = MySimpleImageViewer()
    app.MainLoop()
    
main()
