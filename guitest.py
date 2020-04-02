<<<<<<< HEAD
import wx
from PIL import Image

SIZE = (640, 480)

def get_image():
    # Put your code here to return a PIL image_tools from the camera.
    return Image.open('IDS_cam_accuracy1.png')


def pil_to_wx(image):
    width, height = image.size
    buffer = image.convert('RGB').tobytes()
    bitmap = wx.Bitmap.FromBuffer(width, height, buffer)
    return bitmap


class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)
        self.SetSize(SIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.update()

    def update(self):
        self.Refresh()
        self.Update()
        wx.CallLater(15, self.update)

    def create_bitmap(self):
        image = get_image()
        bitmap = pil_to_wx(image)
        return bitmap

    def on_paint(self, event):
        bitmap = self.create_bitmap()
        dc = wx.AutoBufferedPaintDC(self)
        dc.DrawBitmap(bitmap, 0, 0)


class Frame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX
        super(Frame, self).__init__(None, -1, 'Camera Viewer', style=style)
        panel = Panel(self)
        self.Fit()


def main():
    app = wx.App()
    frame = Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
=======
import wx
from PIL import Image

SIZE = (640, 480)

def get_image():
    # Put your code here to return a PIL image from the camera.
    return Image.open('IDS_cam_accuracy1.png')

def pil_to_wx(image):
    width, height = image.size
    buffer = image.convert('RGB').tobytes()
    bitmap = wx.Bitmap.FromBuffer(width, height, buffer)
    return bitmap

class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)
        self.SetSize(SIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.update()
    def update(self):
        self.Refresh()
        self.Update()
        wx.CallLater(15, self.update)
    def create_bitmap(self):
        image = get_image()
        bitmap = pil_to_wx(image)
        return bitmap
    def on_paint(self, event):
        bitmap = self.create_bitmap()
        dc = wx.AutoBufferedPaintDC(self)
        dc.DrawBitmap(bitmap, 0, 0)

class Frame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX
        super(Frame, self).__init__(None, -1, 'Camera Viewer', style=style)
        panel = Panel(self)
        self.Fit()

def main():
    app = wx.App()
    frame = Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
>>>>>>> b2f87d2e2efd67bde85ee950538ba845082b1690
    main()