# -*- coding: utf-8 -*-

"""
Name: Yoav Rozner
Version: 1.16
Description: Subprocess of the Bpm Finder which prints a gif on the screen.
"""

from Tkinter import *
from PIL import Image, ImageTk

GIF_FILE_NAME = 'loading.gif'
RGBA = 'RGBA'
DURATION = 'duration'

###########################################################################
## Class BpmFinderGif
###########################################################################


class BpmFinderGif(Label):
    """
    Subprocess which creates a gif gui.
    """
    def __init__(self, master, filename):
        """
        @param master: the Tk main window.
        @param filename: the file name of the gif.
        """
        im = Image.open(filename)
        seq = []
        try:
            while 1:
                seq.append(im.copy())
                # skip to next frame
                im.seek(len(seq))
        except EOFError:
            pass

        try:
            self.delay = im.info[DURATION]
        except KeyError:
            self.delay = 100

        first = seq[0].convert(RGBA)
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert(RGBA)
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        """
        Passes frame by frame to play the animation.
        """
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)


def main():
    root = Tk()
    root.overrideredirect(1)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(
        root.winfo_id()))
    animation = BpmFinderGif(root, GIF_FILE_NAME)
    animation.pack()
    root.mainloop()


if __name__ == '__main__':
    main()