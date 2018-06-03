# -*- coding: utf-8 -*- 

"""
Name: Yoav Rozner
Version: 1.16
Description: Subprocess of the Bpm Finder which opens a window
             to proceed the stopped song or metronome.
"""

import wx
import wx.xrc

ARIEL = "Arial"

###########################################################################
## Class BpmFinderProceed
###########################################################################


class BpmFinderProceed(wx.Frame):
    """
    Subprocess proceed gui.
    """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"BpmFinderProceed", pos=wx.DefaultPosition,
                          size=wx.Size(174, 135), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.panel.SetBackgroundColour(wx.Colour(128, 255, 0))

        grid_sizer = wx.GridSizer(0, 2, 0, 0)

        box_sizer1 = wx.BoxSizer(wx.VERTICAL)

        self.proceed_button = wx.Button(self.panel, wx.ID_ANY, u"PROCEED", wx.DefaultPosition, wx.Size(165, 105), 0)
        self.proceed_button.SetFont(wx.Font(22, 74, 90, 90, False, ARIEL))

        box_sizer1.Add(self.proceed_button, 0, wx.ALL, 5)

        self.panel.SetSizer(grid_sizer)
        self.panel.Layout()
        grid_sizer.Fit(self.panel)
        frame_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(frame_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.proceed_button.Bind(wx.EVT_BUTTON, self.proceed)

    # Virtual event handlers, override them in your derived class
    def proceed(self, event):
        """
        Closes the subprocess on button click.
        """
        raise SystemExit


def main():
    app = wx.App(False)
    f = BpmFinderProceed(None)
    f.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()