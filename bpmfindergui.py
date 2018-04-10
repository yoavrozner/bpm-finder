# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import requests
import json
import youtube_dl
import os
import wave
import threading
import struct
import sys
import pyaudio
import numpy as np
from pydub import AudioSegment


ACCESS_TOKEN = 'access_token=UOmQ5JLigMe6w1hJbxuMr3Y6QaCaeNzk3GC2r5M3rMoigl14X87h5RacUdhGUiPy'
BASE_SEARCH_BY_NAME = 'https://api.genius.com/search?q='
SAMPLE_LEN = 230000
CHUNK = 1024
TRY = "try"
FAST = "fast"
STANDARD = "standard"
SLOW = "slow"
WAV = "wav"
DOT = "."
DOT_WAV = DOT + WAV
NEW_SONG = "newSong"
ARIAL = "Arial"
RESPONSE = "response"
METRONOME = "metronome"
RB = "rb"
SONG = "song"
MEDIA = "media"
URL = "url"


###########################################################################
## Class BpmFinder
###########################################################################


class BpmFinder(wx.Frame):
    def __init__(self, parent):
        self.counter = 1
        self.stop_metronome_variable = True
        self.stop_song_variable = False

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"BpmFinder", pos=wx.DefaultPosition,
                          size=wx.Size(997, 604), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 234))

        gridsizer = wx.GridSizer(0, 2, 0, 0)

        boxsizer1 = wx.BoxSizer(wx.VERTICAL)

        self.step_1 = wx.StaticText(self.panel, wx.ID_ANY, u"Step 1 - Enter the name of the song:", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.step_1.Wrap(-1)
        self.step_1.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        boxsizer1.Add(self.step_1, 0, wx.ALL, 5)

        self.song_name = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, -1), 0)
        boxsizer1.Add(self.song_name, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.step_2 = wx.StaticText(self.panel, wx.ID_ANY, u"Step 2 - Click on the relevant button", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.step_2.Wrap(-1)
        self.step_2.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        boxsizer1.Add(self.step_2, 0, wx.ALL, 5)

        self.fast = wx.RadioButton(self.panel, wx.ID_ANY, u"Fast (150+ bpm)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.fast.SetFont(wx.Font(20, 74, 90, 90, False, ARIAL))

        boxsizer1.Add(self.fast, 0, wx.ALL, 5)

        self.standard = wx.RadioButton(self.panel, wx.ID_ANY, u"Standard (70 - 150 bpm)", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.standard.SetFont(wx.Font(20, 74, 90, 90, False, ARIAL))

        boxsizer1.Add(self.standard, 0, wx.ALL, 5)

        self.slow = wx.RadioButton(self.panel, wx.ID_ANY, u"Slow (1 - 70 bpm)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.slow.SetFont(wx.Font(20, 74, 90, 90, False, ARIAL))

        boxsizer1.Add(self.slow, 0, wx.ALL, 5)

        self.step_3 = wx.StaticText(self.panel, wx.ID_ANY, u"Step 3 - press ENTER", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        self.step_3.Wrap(-1)
        self.step_3.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        boxsizer1.Add(self.step_3, 0, wx.ALL, 5)

        self.enter = wx.Button(self.panel, wx.ID_ANY, u"ENTER", wx.DefaultPosition, wx.Size(100, 50), 0)
        boxsizer1.Add(self.enter, 0, wx.ALL, 5)

        gridsizer.Add(boxsizer1, 1, wx.EXPAND, 5)

        boxsizer2 = wx.BoxSizer(wx.VERTICAL)

        self.answer = wx.StaticText(self.panel, wx.ID_ANY, u"This song's BPM is:", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        self.answer.Wrap(-1)
        self.answer.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        boxsizer2.Add(self.answer, 0, wx.ALL, 5)

        self.answer_bpm = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        boxsizer2.Add(self.answer_bpm, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.play_the_song = wx.Button(self.panel, wx.ID_ANY, u"Click to play the song", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        boxsizer2.Add(self.play_the_song, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.stop_the_song = wx.Button(self.panel, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0)
        boxsizer2.Add(self.stop_the_song, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.proceed_the_song = wx.Button(self.panel, wx.ID_ANY, u"PROCEED", wx.DefaultPosition, wx.DefaultSize, 0)
        boxsizer2.Add(self.proceed_the_song, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.metronome_introducer = wx.StaticText(self.panel, wx.ID_ANY, u"Metronome", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.metronome_introducer.Wrap(-1)
        self.metronome_introducer.SetFont(wx.Font(18, 74, 90, 90, False, ARIAL))

        boxsizer2.Add(self.metronome_introducer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.metronome_instruction = wx.StaticText(self.panel, wx.ID_ANY, u"Write the bpm:", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.metronome_instruction.Wrap(-1)
        self.metronome_instruction.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        boxsizer2.Add(self.metronome_instruction, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.metronome_text = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        boxsizer2.Add(self.metronome_text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.start = wx.Button(self.panel, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0)
        boxsizer2.Add(self.start, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.stop = wx.Button(self.panel, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0)
        boxsizer2.Add(self.stop, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gridsizer.Add(boxsizer2, 1, wx.EXPAND, 5)

        self.panel.SetSizer(gridsizer)
        self.panel.Layout()
        gridsizer.Fit(self.panel)
        frame_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(frame_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.enter.Bind(wx.EVT_BUTTON, self.calculate_bpm)
        self.play_the_song.Bind(wx.EVT_BUTTON, self.play_song)
        self.stop_the_song.Bind(wx.EVT_BUTTON, self.stop_song)
        self.proceed_the_song.Bind(wx.EVT_BUTTON, self.proceed_song)
        self.start.Bind(wx.EVT_BUTTON, self.start_metronome)
        self.stop.Bind(wx.EVT_BUTTON, self.stop_metronome)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def calculate_bpm(self, event):
        #Call to url finder main
        name_of_the_song = self.song_name.GetValue()
        url = url_finder(name_of_the_song)
        download_wav(url)
        rename(TRY + DOT_WAV)

        #Call to bmp finder main
        bpm = 0
        start_time = 0
        tempo = self.fast_standard_slow()
        bpm_tempo = False
        while tempo != bpm_tempo:
            slice_wav_file(start_time)
            spf = wave.open(NEW_SONG + DOT_WAV, 'r')

            #Extract Raw Audio from Wav File
            signal = spf.readframes(-1)
            signal = np.fromstring(signal, 'Int16')

            bpm = find_max(signal)
            bpm_tempo = bpm_check_speed(bpm)
            start_time += 10
            spf.close()
        self.answer_bpm.SetValue(str(bpm))
        os.rename(TRY + DOT_WAV, TRY + str(self.counter) + DOT_WAV)
        os.remove(NEW_SONG + DOT_WAV)
        self.counter += 1

    def play_song(self, event):
        # changed
        wf = wave.open(TRY + str(self.counter - 1) + DOT_WAV, RB)

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()

        # open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(CHUNK)

        # play stream (3)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)
            # Stops the song
            while not self.stop_song_variable:
                pass
        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()

    def stop_song(self, event):
        self.stop_song_variable = True

    def proceed_song(self, event):
        self.stop_song_variable = False

    def start_metronome(self, event):
        metronome_tempo = int(self.metronome_text.GetValue())
        if not os.path.isfile(METRONOME + str(metronome_tempo) + DOT_WAV):
            url = url_finder(METRONOME + " " + str(metronome_tempo))
            download_wav(url)
            os.rename(str(metronome_tempo), METRONOME + str(metronome_tempo))
        self.metronome(event, metronome_tempo)

    def stop_metronome(self, event):
        self.stop_metronome_variable = True

    def fast_standard_slow(self):
        # changed
        if self.fast.GetValue():
            return FAST
        elif self.standard.GetValue():
            return STANDARD
        return SLOW

    def metronome(self, event, metronome_tempo):
        self.stop_metronome_variable = False
        while not self.stop_metronome_variable:
            wf = wave.open(METRONOME + str(metronome_tempo) + DOT_WAV, RB)
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(CHUNK)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(CHUNK)
                if self.stop_metronome_variable:
                    break

            # stop stream (4)
            stream.stop_stream()
            stream.close()

            # close PyAudio (5)
            p.terminate()


###########################################################################
## Url finder functions
###########################################################################

def url_finder(name_of_the_song):
    try:
        response = requests.get(BASE_SEARCH_BY_NAME + str(name_of_the_song) + "&" + ACCESS_TOKEN)
        response = response.json()
        index = 0
        result = response
        id_item = (result[RESPONSE]['hits'][index]['result']['id'])
        id_item = requests.get('https://api.genius.com/songs/' + str(id_item) + '?' + ACCESS_TOKEN)
        id_item = id_item.json()
        place = 0
        my_url = str(unicode(id_item[RESPONSE][SONG][MEDIA][place][URL]))
        while "youtube" not in my_url:
            if place > 4:
                break
            place += 1
            my_url = str(unicode(id_item[RESPONSE][SONG][MEDIA][place][URL]))
        return my_url
    except IndexError:
        return False


def download_wav(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': WAV,
                'preferredquality': '192',
            }
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def rename(destination_name):
    files = [f for f in os.listdir(DOT) if os.path.isfile(f)]
    for f in files:
        # or METRONOME
        if DOT_WAV in f and not TRY  in f:
            os.rename(f, destination_name)


###########################################################################
## Bpm finder functions
###########################################################################


def slice_wav_file(start_time):
    t1 = start_time
    t2 = t1 + 10
    t1 *= 1000  # Works in milliseconds
    t2 *= 1000
    new_audio = AudioSegment.from_wav(TRY + DOT_WAV)
    new_audio = new_audio[t1:t2]
    new_audio.export(NEW_SONG + DOT_WAV, format=WAV)  # Exports to a wav file in the current path.


def find_max(signal):
    max_signal = max(signal)
    arr_max = []
    place = []
    i = 0
    while i < len(signal):
        if signal[i] + 5000 >= max_signal:
            if place:
                if i - 30000 >= place[len(place) - 1]:
                    arr_max.append(signal[i])
                    place.append(i)
            else:
                arr_max.append(signal[i])
                place.append(i)
        i += 1
    return len(arr_max) * 6


def bpm_check_speed(bpm):
    if bpm <= 70:
        return SLOW
    elif bpm <= 150:
        return STANDARD
    return FAST


def main():
    app = wx.App(False)
    f = BpmFinder(None)
    f.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()