# -*- coding: utf-8 -*- 

"""
Name: Yoav Rozner
Version: 1.16
Description: Subprocess of the Bpm Finder which opens a window
             to exit the song or the metronome.
"""

import wx
import wx.xrc

###########################################################################
## Class BpmFinderExit
###########################################################################


class BpmFinderExit(wx.Frame):
    """
    Subprocess exit gui.
    """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(169, 113),
                          style=wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.Colour(128, 255, 0))

        box_sizer1 = wx.BoxSizer(wx.VERTICAL)

        self.exit = wx.Button(self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.Size(200, 400), 0)
        box_sizer1.Add(self.exit, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(box_sizer1)
        self.Layout()

        # Connect Events
        self.exit.Bind(wx.EVT_BUTTON, self.exit_song)

    # Virtual event handlers, override them in your derived class
    def exit_song(self, event):
        """
        Closes the subprocess on button click.
        """
        raise SystemExit


def main():
    app = wx.App(False)
    f = BpmFinderExit(None)
    f.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()