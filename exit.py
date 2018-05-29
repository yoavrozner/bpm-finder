# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyPanel1
###########################################################################


class BpmFinderExit(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(169, 113),
                          style=wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.Colour(128, 255, 0))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.exit = wx.Button(self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.Size(200, 400), 0)
        bSizer1.Add(self.exit, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.exit.Bind(wx.EVT_BUTTON, self.exit_song)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def exit_song(self, event):
        raise SystemExit


def main():
    app = wx.App(False)
    f = BpmFinderExit(None)
    f.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()