# -*- coding: utf-8 -*-

"""
Name: Yoav Rozner
Version: 1.16
Description: Finds the speed of the song's rhythm in Beats Per Minute (BPM).
             Moreover, Bpm Finder allows the user to hear the song and the song's
             speed of rhythm by allowing fast and accessible metronome.
"""

import wx
import wx.xrc
import requests
import json
import youtube_dl
import os
import wave
import subprocess
import pyaudio
import numpy as np
from pydub import AudioSegment
from time import sleep

ACCESS_TOKEN = 'access_token=UOmQ5JLigMe6w1hJbxuMr3Y6QaCaeNzk3GC2r5M3rMoigl14X87h5RacUdhGUiPy'
BASE_SEARCH_BY_NAME = 'https://api.genius.com/search?q='
GENIUS_API_SONGS = 'https://api.genius.com/songs/'
SAMPLE_LEN = 230000
CHUNK = 1024
TRY = "try"
FAST = "fast"
STANDARD = "standard"
STANDARD_BPM = 150
SLOW_BPM = 70
SLOW = "slow"
WAV = "wav"
DOT = "."
DOT_WAV = DOT + WAV
NEW_SONG = "newSong"
ARIAL = "Arial"
RESPONSE = "response"
METRONOME = "metronome"
RB = "rb"
INT16 = 'Int16'
SONG = "song"
MEDIA = "media"
YOUTUBE = "youtube"
HITS = 'hits'
RESULT = 'result'
ID = 'id'
URL = "url"
CONVERT_TO_MILLISECONDS = 1000
LOADING_SCREEN = 'loading_screen.py'
PYTHON = 'python'
EXIT = 'exit.py'
STOP = 'stop.py'
PROCEED = 'proceed.py'
UNIDENTIFIED_SONG = "Error: unidentified song."
NO_CONNECTION = "Error: there is no connection."
UNMATCHED_SPEED = "Error: the speed doesn't match the song's speed."
DOWNLOAD_FAIL = "Error: there was a download error please try again."
UNIDENTIFIED_CHARACTERS = "Error: unidentified characters."
UNKNOWN_SONG = "Error: no existing song."
VALUE_ERROR = "Error: metronome doesn't get the right values."
ZERO_DIVISION = "Error: we can't divide with zero yet."

###########################################################################
## Class BpmFinder
###########################################################################


class BpmFinder(wx.Frame):
    """
    Main gui of the program.
    """
    def __init__(self, parent):
        self.counter = 1
        self.stop_metronome_variable = True
        self.stop_song_variable = False

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"BpmFinder", pos=wx.DefaultPosition,
                          size=wx.Size(997, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 234))

        grid_sizer = wx.GridSizer(0, 2, 0, 0)

        box_sizer1 = wx.BoxSizer(wx.VERTICAL)

        self.step_1 = wx.StaticText(self.panel, wx.ID_ANY, u"Step 1 - Enter the name of the song:", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.step_1.Wrap(-1)
        self.step_1.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        box_sizer1.Add(self.step_1, 0, wx.ALL, 5)

        self.song_name = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, -1), 0)
        # Limits the maximum capacity of the text control to 100 characters.
        self.song_name.SetMaxLength(100)
        box_sizer1.Add(self.song_name, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.step_2 = wx.StaticText(self.panel, wx.ID_ANY, u"Step 2 - Click on the relevant button", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.step_2.Wrap(-1)
        self.step_2.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        box_sizer1.Add(self.step_2, 0, wx.ALL, 5)

        self.fast = wx.RadioButton(self.panel, wx.ID_ANY, u"Fast (150+ bpm)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.fast.SetFont(wx.Font(20, 74, 90, 90, False, ARIAL))

        box_sizer1.Add(self.fast, 0, wx.ALL, 5)

        self.standard = wx.RadioButton(self.panel, wx.ID_ANY, u"Standard (70 - 150 bpm)", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.standard.SetFont(wx.Font(20, 74, 90, 90, False, ARIAL))

        box_sizer1.Add(self.standard, 0, wx.ALL, 5)

        self.slow = wx.RadioButton(self.panel, wx.ID_ANY, u"Slow (1 - 70 bpm)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.slow.SetFont(wx.Font(20, 74, 90, 90, False, ARIAL))

        box_sizer1.Add(self.slow, 0, wx.ALL, 5)

        self.step_3 = wx.StaticText(self.panel, wx.ID_ANY, u"Step 3 - press ENTER", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        self.step_3.Wrap(-1)
        self.step_3.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        box_sizer1.Add(self.step_3, 0, wx.ALL, 5)

        self.enter = wx.Button(self.panel, wx.ID_ANY, u"ENTER", wx.DefaultPosition, wx.Size(100, 50), 0)
        box_sizer1.Add(self.enter, 0, wx.ALL, 5)

        grid_sizer.Add(box_sizer1, 1, wx.EXPAND, 5)

        box_sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.answer = wx.StaticText(self.panel, wx.ID_ANY, u"This song's BPM is:", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        self.answer.Wrap(-1)
        self.answer.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        box_sizer2.Add(self.answer, 0, wx.ALL, 5)

        self.answer_bpm = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.answer_bpm.SetMaxLength(100)
        box_sizer2.Add(self.answer_bpm, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.play_the_song = wx.Button(self.panel, wx.ID_ANY, u"Click to play the song", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        box_sizer2.Add(self.play_the_song, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.metronome_introduce = wx.StaticText(self.panel, wx.ID_ANY, u"Metronome", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.metronome_introduce.Wrap(-1)
        self.metronome_introduce.SetFont(wx.Font(18, 74, 90, 90, False, ARIAL))

        box_sizer2.Add(self.metronome_introduce, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.metronome_instruction = wx.StaticText(self.panel, wx.ID_ANY, u"Write the bpm:", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.metronome_instruction.Wrap(-1)
        self.metronome_instruction.SetFont(wx.Font(12, 74, 90, 90, False, ARIAL))

        box_sizer2.Add(self.metronome_instruction, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.metronome_text = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.metronome_text.SetMaxLength(100)
        box_sizer2.Add(self.metronome_text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.start = wx.Button(self.panel, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0)
        box_sizer2.Add(self.start, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        grid_sizer.Add(box_sizer2, 1, wx.EXPAND, 5)

        self.panel.SetSizer(grid_sizer)
        self.panel.Layout()
        grid_sizer.Fit(self.panel)
        frame_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(frame_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.enter.Bind(wx.EVT_BUTTON, self.calculate_bpm)
        self.play_the_song.Bind(wx.EVT_BUTTON, self.play_song)
        self.start.Bind(wx.EVT_BUTTON, self.start_metronome)

    # Virtual event handlers, override them in your derived class
    def calculate_bpm(self, event):
        """
        Binds all the BPM calculation functions and uses them.
        """
        loading_screen = subprocess.Popen([PYTHON, LOADING_SCREEN])
        try:
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
                signal = np.fromstring(signal, INT16)

                bpm = find_max(signal)
                bpm_tempo = bpm_check_speed(bpm)
                start_time += 10
                spf.close()
            loading_screen.terminate()

            self.Refresh()
            self.answer_bpm.SetValue(str(bpm))
            self.metronome_text.SetValue(str(bpm))
            os.rename(TRY + DOT_WAV, TRY + str(self.counter) + DOT_WAV)
            os.remove(NEW_SONG + DOT_WAV)
            self.counter += 1
        except TypeError:
            self.song_name.SetValue(UNIDENTIFIED_SONG)
            loading_screen.terminate()
        except requests.ConnectionError:
            self.song_name.SetValue(NO_CONNECTION)
            loading_screen.terminate()
        except ValueError:
            self.song_name.SetValue(UNMATCHED_SPEED)
            loading_screen.terminate()
        except youtube_dl.DownloadError:
            self.song_name.SetValue(DOWNLOAD_FAIL)
            loading_screen.terminate()
        except KeyError:
            self.song_name.SetValue(UNIDENTIFIED_CHARACTERS)
            loading_screen.terminate()

    def play_song(self, event):
        """
        Plays the last song that the user handled with.
        """
        loading_screen = subprocess.Popen([PYTHON, LOADING_SCREEN])

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()
        try:

            wf = wave.open(TRY + str(self.counter - 1) + DOT_WAV, RB)
            # open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # read data
            data = wf.readframes(CHUNK)

            exit_process = subprocess.Popen([PYTHON, EXIT])
            stop_process = subprocess.Popen([PYTHON, STOP])
            poll_exit = None
            poll_stop = None
            proceed_process = None
            # play stream (3)
            while len(data) > 0 and poll_exit is None:
                stream.write(data)
                data = wf.readframes(CHUNK)
                poll_exit = exit_process.poll()
                poll_stop = stop_process.poll()
                if poll_stop is not None:
                    proceed_process = subprocess.Popen([PYTHON, PROCEED])
                    poll_proceed = None
                    while poll_proceed is None and poll_exit is None:
                        poll_proceed = proceed_process.poll()
                        poll_exit = exit_process.poll()
                    if poll_exit is None:
                        stop_process = subprocess.Popen([PYTHON, STOP])
            if poll_stop is None:
                stop_process.terminate()
            else:
                proceed_process.terminate()
            # stop stream (4)
            stream.stop_stream()
            stream.close()

            # close PyAudio (5)
            p.terminate()
            loading_screen.terminate()
        except IOError:
            self.song_name.SetValue(UNKNOWN_SONG)
            p.terminate()
            loading_screen.terminate()

    def start_metronome(self, event):
        """
        Display a metronome with the wanted BPM.
        """
        try:
            metronome_tempo = int(self.metronome_text.GetValue())
            hold = 60 / metronome_tempo
            exit_process = subprocess.Popen([PYTHON, EXIT])
            stop_process = subprocess.Popen([PYTHON, STOP])
            poll_exit = None
            poll_stop = None
            proceed_process = None
            while poll_exit is None:
                metronome()
                sleep(hold)
                poll_exit = exit_process.poll()
                poll_stop = stop_process.poll()
                if poll_stop is not None:
                    proceed_process = subprocess.Popen([PYTHON, PROCEED])
                    poll_proceed = None
                    while poll_proceed is None and poll_exit is None:
                        poll_proceed = proceed_process.poll()
                        poll_exit = exit_process.poll()
                    if poll_exit is None:
                        stop_process = subprocess.Popen([PYTHON, STOP])
            if poll_stop is None:
                stop_process.terminate()
            else:
                proceed_process.terminate()
        except ValueError:
            self.song_name.SetValue(VALUE_ERROR)
        except ZeroDivisionError:
            self.song_name.SetValue(ZERO_DIVISION)

    def fast_standard_slow(self):
        if self.fast.GetValue():
            return FAST
        elif self.standard.GetValue():
            return STANDARD
        return SLOW


def metronome():
    """
    Plays one tick of metronome.
    """
    wf = wave.open(METRONOME + "1" + DOT_WAV, RB)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


###########################################################################
## Url finder functions
###########################################################################


def url_finder(name_of_the_song):
    """
    Finds the url of the song by its name.
    @param name_of_the_song: the name of the song.
    """
    try:
        response = requests.get(BASE_SEARCH_BY_NAME + str(name_of_the_song) + "&" + ACCESS_TOKEN)
        response = response.json()
        index = 0
        result = response
        id_item = (result[RESPONSE][HITS][index][RESULT][ID])
        id_item = requests.get(GENIUS_API_SONGS + str(id_item) + '?' + ACCESS_TOKEN)
        id_item = id_item.json()
        place = 0
        my_url = str(unicode(id_item[RESPONSE][SONG][MEDIA][place][URL]))
        while YOUTUBE not in my_url:
            if place > 4:
                break
            place += 1
            my_url = str(unicode(id_item[RESPONSE][SONG][MEDIA][place][URL]))
        return my_url
    except IndexError:
        return False


def download_wav(url):
    """
    Downloads the song from You Tube by the url that was given.
    @param url: the url of the song that is going to be downloaded.
    """
    # Settings changes which will allow the program to download the song as a wav file.
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
    """
    Changes the name of the recent downloaded song to try.wav.
    This function was built because the name of the song that was downloaded
    is unknown and changes so this function detects this file and changes its name.
    @param destination_name: the destination name for the wav file.
    """
    files = [f for f in os.listdir(DOT) if os.path.isfile(f)]
    for f in files:
        if DOT_WAV in f and not TRY in f and not METRONOME in f:
            os.rename(f, destination_name)


def delete_files():
    """
    Deletes every wav file in the current directory except the metronome
    file so they will not interrupt the rename function.
    """
    files = [f for f in os.listdir(DOT) if os.path.isfile(f)]
    for f in files:
        if DOT_WAV in f and not METRONOME + str(1) in f:
            os.remove(f)


###########################################################################
## Bpm finder functions
###########################################################################


def slice_wav_file(start_time):
    """
    Slices the wave file to a 10 seconds wave file,
    so all the modules will be able to support and allow
    the code to use them.
    @param start_time: time since the start of the song in seconds.
    """
    t1 = start_time
    t2 = t1 + 10
    # Works in milliseconds
    t1 *= CONVERT_TO_MILLISECONDS
    t2 *= CONVERT_TO_MILLISECONDS
    new_audio = AudioSegment.from_wav(TRY + DOT_WAV)
    new_audio = new_audio[t1:t2]
    new_audio.export(NEW_SONG + DOT_WAV, format=WAV)
    # Exports to a wav file in the current path.


def find_max(signal):
    """
    Finds the closest places in the signal to the
    maximum place in the signal between the average best working
    frequency range that is the most precised.
    @param signal: the song's wave that was transformed into numbers.
    """
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
    """
    Checks the speed of the song by it's bpm
    and by that decides if the song is slow,
    standard or fast and that is from the
    common convention about song speed.
    @param bpm: the speed of the rhythm of the song in beats per minute.
    """
    if bpm <= SLOW_BPM:
        return SLOW
    elif bpm <= STANDARD_BPM:
        return STANDARD
    return FAST


def main():
    delete_files()
    app = wx.App(False)
    f = BpmFinder(None)
    f.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()