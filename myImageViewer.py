'''
Author: Thanh Ky Quan
Date: 05/19/2010
Filename: myImageViewer.py
Version: 0.1.1 beta
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
import wx

ID_CREDIT = 110
ID_CONVERT_TO_GRAYSCALE = 111
DEF_IMAGE = 'hspt.jpg'

class MySimpleImageViewer(wx.App):
    def __init__(self, redirect = False, filename = None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, -1, title = 'Simple image viewer', size = (500, 500))
        self.panel = wx.Panel(self.frame)
      
        menubar = wx.MenuBar()
        menu_File = wx.Menu()
        menu_File.Append(wx.ID_OPEN, '&Open', 'Click here to load image')
        menu_File.Append(wx.ID_EXIT, 'E&xit', 'Click here to terminate application')
        menu_Help = wx.Menu()
        menu_Help.Append(wx.ID_ABOUT, '&About Simple image viewer', 'Click here to learn more about this application')
        menu_Help.Append(110, '&Credit', 'Creditation')
        menu_Tool = wx.Menu()
        menu_Tool.Append(ID_CONVERT_TO_GRAYSCALE, 'Convert to &grayscale', 'Convert image to grayscale')
        menubar.Append(menu_File, '&File')
        menubar.Append(menu_Tool, '&Tool')
        menubar.Append(menu_Help, '&Help')
        self.frame.SetMenuBar(menubar)
        
        self.frame.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.frame.Bind(wx.EVT_MENU, self.OnClickExit, id=wx.ID_EXIT)
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id =wx.ID_ABOUT)
        self.frame.Bind(wx.EVT_MENU, self.OnCredit, id = ID_CREDIT)
        self.frame.Bind(wx.EVT_MENU, self.ConvertToGreyscale, id = ID_CONVERT_TO_GRAYSCALE)
        
        self.hBox = wx.BoxSizer()
        self.vBox = wx.BoxSizer(wx.VERTICAL)
        self.vBox.Add(self.hBox, proportion = 1, flag = wx.EXPAND, border = 0)
        self.imagePath = DEF_IMAGE        
        tmpImg = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY)
        self.frame.SetClientSize(tmpImg.GetSize())
        self.imageBox = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(tmpImg))
        self.hBox.Add(self.imageBox, proportion = 1, flag = wx.EXPAND, border = 0)


        # Default parameters
        self.frame2 = ""
        self.status = self.frame.CreateStatusBar()
        self.savePath = ""
        self.newImage = ""
        self.status.SetStatusText(self.imagePath + " " + str(tmpImg.GetWidth()) + "x" + str(tmpImg.GetHeight()))
        self.version = "0.1.1 Beta"
        self.author = "Thanh Ky Quan"
        
        self.panel.Layout()
        self.frame.Show()



    # show credit
    def OnCredit(self, event):
        creditMessage = "Thanks to my computer science teachers at Florida Virtual School:\n\n"
        teachers = ['Mrs. Lisa Brock', 'Mrs. Amie Ross', 'Mr. William Jordan']
        for teacher in teachers:
            creditMessage += " - " + teacher + "\n"
        msgBox = wx.MessageDialog(self.frame, message= creditMessage, caption = 'Credit', style = wx.OK | wx.STAY_ON_TOP)
        if (msgBox.ShowModal() == wx.ID_OK):
            msgBox.Destroy()

    # show file dialog to load image
    def OnOpen(self, event):
        dialog = wx.FileDialog(None, message = 'Select image to display', wildcard = 'JPEG file (*.jpg)|*.jpg', style = wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.imagePath = dialog.GetPath()
            self.loadImage()
        dialog.Destroy()

    # show about information
    def OnAbout(self, event):
        aboutMessage = "Simple Image Viewer version " + self.version + "\n\nCreated by " + self.author
        msgBox = wx.MessageDialog(self.frame, message =  aboutMessage, caption = 'About', style = wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK)
        if (msgBox.ShowModal() == wx.ID_OK):
            msgBox.Destroy()
            
    #load image method    
    def loadImage(self):
        img = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY)
        self.status.SetStatusText(self.imagePath + " " + str(img.GetWidth()) + "x" + str(img.GetHeight()))
        img_size = img.GetSize()
        self.frame.SetClientSize(img_size)
        self.imageBox.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()

    #convert image to grayscale
    def ConvertToGreyscale(self, event):
        frame = wx.Frame(None, -1, 'Convert To Greyscale', size=(300, 150))
        self.frame2 = frame
        panel = wx.Panel(frame)
        img = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY).ConvertToGreyscale()
        self.newImage = img
        imageBox = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(img))
        img_size = img.GetSize()
        frame_size = (img_size[0], img_size[1]+ 50)
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, '&Cancel', pos = (20, img_size[1] + 10))        
        save_btn = wx.Button(panel, wx.ID_SAVE, '&Save', pos = (100, img_size[1] + 10))

        frame.Bind(wx.EVT_BUTTON, self.SaveImage, id = wx.ID_SAVE)
        frame.Bind(wx.EVT_BUTTON, self.CloseWindow, id = wx.ID_CANCEL)
        
        frame.SetClientSize(frame_size)        
        frame.Show()

    #close window
    def CloseWindow(self, event):
        self.frame2.Destroy()

    #save image
    def SaveImage(self, event):
        dialog = wx.FileDialog(None, message = 'Save your image', wildcard = 'JPEG file (*.jpg) | *.jpg', style = wx.SAVE)
        if (dialog.ShowModal() == 5100):
            self.WriteNewImage(dialog.GetPath(), self.newImage)
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
