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
## Class BpmFinderExit
###########################################################################


class BpmFinderStop(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"BpmFinderStop", pos=wx.DefaultPosition,
                          size=wx.Size(174, 135), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.panel.SetBackgroundColour(wx.Colour(128, 255, 0))

        gridsizer = wx.GridSizer(0, 2, 0, 0)

        boxsizer1 = wx.BoxSizer(wx.VERTICAL)

        self.stopbutton = wx.Button(self.panel, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.Size(165, 105), 0)
        self.stopbutton.SetFont(wx.Font(36, 74, 90, 90, False, "Arial"))

        boxsizer1.Add(self.stopbutton, 0, wx.ALL, 5)

        self.panel.SetSizer(gridsizer)
        self.panel.Layout()
        gridsizer.Fit(self.panel)
        frame_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(frame_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.stopbutton.Bind(wx.EVT_BUTTON, self.stop)


    # Virtual event handlers, overide them in your derived class
    def stop(self, event):
        raise SystemExit


def main():
    app = wx.App(False)
    f = BpmFinderStop(None)
    f.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()