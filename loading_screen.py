# -*- coding: utf-8 -*-
"""
Description:    Opens the loading animation

name:           Elad Hayek
date:           22.3.18
file name:      loading_screen.py
"""

from Tkinter import *
from PIL import Image, ImageTk

GIF_FILE_NAME = 'loading.gif'


class MyLabel(Label):
    def __init__(self, master, filename):
        """
        creates the animation

        :arg master = the Tk main window
        :type master = tk window

        :arg filename = the gif file name
        :type filename = string
        """
        im = Image.open(filename)
        seq = []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq))  # skip to next frame
        except EOFError:
            pass  # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        """
        passes frame by frame to run the animation
        """
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)


def main():
    """
    calls MyLabel class and runs the animation
    """
    root = Tk()
    root.overrideredirect(1)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(
        root.winfo_id()))
    anim = MyLabel(root, GIF_FILE_NAME)
    anim.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
