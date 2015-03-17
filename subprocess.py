import wx
import os
import subprocess


class MyFrame(wx.Frame):
    """make a frame, inherits wx.Frame"""
    def __init__(self):
        # create a frame, no parent, default to wxID_ANY
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Niggua',
            pos=(300, 150), size=(320, 250))
        self.SetBackgroundColour("black")
        
        self.button1 = wx.Button(self, id=-1, label='liveUpdatePy',
            pos=(0, 0), size=(10, 20))
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)
        
        # show the frame
        self.Show(True)
    def button1Click(self,event):
    	subprocess.Popen(['python', 'trialGraph.py'])

if __name__ == '__main__':
	app = wx.PySimpleApp()
	window = MyFrame()
	app.MainLoop()