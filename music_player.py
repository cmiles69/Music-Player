#!/usr/bin/env python3
# coding = utf-8

# Craig Miles

import tkinter
from tkinter import font
import tkinter.filedialog
import os
import pickle
import pygame

# From PyGuru -> Music player with python pygame _ #pyGuru-zMrr2E3heDM.mp4
# 11:43, 12:37, 13:04, 16:17, 16:51, 17:22, 19:00, 19:55
# 22:59, 23:11, 24:24, 24:49, 26:27, 28:13, 30:03, 30:26
# 32:01, 48:57, 106:58, 1:11:53, 1:13:43, 1:14:52, 1:15:30
# 1:16:46

class Player( object ):

    def __init__( self, root ):
        self.root = root
        pygame.init()
        #pygame.mixer.init()
        self.initUI()

        if os.path.exists( 'songs.pickle' ):
            #print( 'found pickle' )
            f = open( 'songs.pickle', 'rb' )
            self.playlist = pickle.load( f )
            f.close()
            self.enumerate_songs()
            self.frm_tracklist['text'] = f'Playlist - {str( len( self.playlist ))}'
        else:
            self.playlist.clear()

    def initUI( self ):
        self.root.wm_title( 'Music Player' )
        self.geometry = self.screen_size( size = 0.50 )
        # print( self.geometry )
        self.root.geometry( self.geometry )
        self.center_root()
        self.root.configure( background = 'deep sky blue' )
        self.create_variables()
        self.create_fonts()
        self.create_frames()
        self.create_widgets()

    def screen_size( self, size ):
        # Obtain desired screen size
        width = self.root.winfo_screenwidth() * size
        height = self.root.winfo_screenheight() * size
        return( '{}x{}+{}+{}'
        .format( int( width ), int( height ), 0, 0 ))

    def center_root( self ):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        pos_right = \
        int( self.root.winfo_screenwidth() // 2 - window_width // 2 )
        pos_down = \
        int( self.root.winfo_screenheight() // 2 - window_height // 2 )
        self.root.geometry( '{}x{}+{}+{}'
        .format( window_width, window_height, pos_right, pos_down ))

#================================= Variables ===================================

    def create_variables( self ):
        self.playlist = []
        self.current_song = 0
        self.paused = True
        self.played = False
        self.volume = tkinter.DoubleVar()
        self.img_background = tkinter.PhotoImage( file = 'images/music.gif' )
        self.img_next_ = tkinter.PhotoImage( file = 'images/next.gif' )
        self.img_prev = tkinter.PhotoImage( file = 'images/previous.gif' )
        self.img_play = tkinter.PhotoImage( file = 'images/play.gif' )
        self.img_pause = tkinter.PhotoImage( file = 'images/pause.gif' )



#================================= Fonts =======================================

    def create_fonts( self ):
        self.track_font = font.Font( family = 'LuxiSerif',
                                     size = 15,
                                     weight = 'bold' )

        self.label_font = font.Font( family = 'LuxiSerif',
                                     size = 15,
                                     weight = 'normal' )

        self.btn_font = font.Font( family = 'Bitstream Charter',
                                   size = 13,
                                   weight = 'bold' )

                                   # 'Fira Sans Light'

        self.lbox_font = font.Font( family = 'Lato Semibold',
                                   size = 15,
                                   weight = 'normal' )

#================================ Frames =======================================

    def create_frames( self ):
        self.frm_track = tkinter.LabelFrame( self.root,
                                             font = self.track_font,
                                             text = 'Song Track',
                                             borderwidth = 5,
                                             background = 'grey',
                                             foreground = 'white',
                                             relief = tkinter.GROOVE )
        self.frm_track.place( relx = 0.01,
                              rely = 0.02,
                              relwidth = 0.46,
                              relheight = 0.66 )

        self.frm_controls = tkinter.LabelFrame( self.root,
                                             font = self.track_font,
                                             text = 'Controls',
                                             borderwidth = 5,
                                             background = 'grey',
                                             foreground = 'white',
                                             relief = tkinter.GROOVE )
        self.frm_controls.place( relx = 0.01,
                                 rely = 0.69,
                                 relwidth = 0.46,
                                 relheight = 0.295 )

        self.frm_tracklist = tkinter.LabelFrame( self.root,
                                    font = self.track_font,
                                    text = f'Playlist - {len( self.playlist )}',   # {}.format( len( self.playlist ))
                                    borderwidth = 5,
                                    background = 'grey',
                                    foreground = 'white',
                                    relief = tkinter.GROOVE )
        self.frm_tracklist.place( relx = 0.475,
                                  rely = 0.02,
                                  relwidth = 0.518,
                                  relheight = 0.965 )

#============================== Widgets ========================================

    def create_widgets( self ):

        #=================== Track Widgets ==========================#

        self.img_label = tkinter.Label( self.frm_track,
                                        image = self.img_background )
        self.img_label.place( relx = 0,
                              rely = 0,
                              relwidth = 1,
                              relheight = 0.75 )

        self.txt_label = tkinter.Label( self.frm_track,
                                        font = self.label_font,
                                        text = 'Music player Mp3' )
        self.txt_label.place( relx = 0,
                              rely = 0.76,
                              relwidth = 1,
                              relheight = 0.25 )

        #=================== Control Widgets =========================#

        self.btn_load = tkinter.Button( self.frm_controls,
                                        font = self.btn_font,
                                        text = 'Load Songs',
                                        foreground = 'white',
                                        background = 'green',
                                        command = self.retrieve_songs )
        self.btn_load.place( relx = 0.04,
                             rely = 0.10,
                             relwidth = 0.25,
                             relheight = 0.33 )

        self.btn_previous = tkinter.Button( self.frm_controls,
                                            image = self.img_prev,
                                            command = self.previous_song )
        self.btn_previous.place( relx = 0.31,
                                 rely = 0.10,
                                 relwidth = 0.12,
                                 relheight = 0.33 )

        self.btn_pause = tkinter.Button( self.frm_controls,
                                         image = self.img_pause,
                                         command = self.pause_song  )
        self.btn_pause.place( relx = 0.45,
                              rely = 0.10,
                              relwidth = 0.12,
                              relheight = 0.33 )

        self.btn_next_ = tkinter.Button( self.frm_controls,
                                         image = self.img_next_,
                                         command = self.next_song )
        self.btn_next_.place( relx = 0.59,
                              rely = 0.10,
                              relwidth = 0.12,
                              relheight = 0.33 )

        self.slider = tkinter.Scale( self.frm_controls,
                                     from_ = 0,
                                     to = 10,
                                     variable = self.volume,
                                     orient = tkinter.HORIZONTAL,
                                     command = self.change_volume )
        self.slider.place( relx = 0.04,
                           rely = 0.49,
                           relwidth = 0.67,
                           relheight = 0.33 )
        self.slider.set( 8 )
        pygame.mixer.music.set_volume( 0.8 )

    #=================== Tracklist Widgets =========================#

        self.scrollbar = tkinter.Scrollbar( self.frm_tracklist,
                                            orient = tkinter.VERTICAL )
        self.scrollbar.pack( side = tkinter.RIGHT,
                             fill = tkinter.Y,
                             anchor = tkinter.E )

        self.list = tkinter.Listbox( self.frm_tracklist,
                                     font = self.lbox_font,
                                     yscrollcommand = self.scrollbar.set,
                                     selectmode = tkinter.SINGLE,
                                     selectbackground = 'sky blue' )

        self.list.bind( '<Double-1>', self.play_song )
        self.scrollbar.configure( command = self.list.yview )

        self.list.pack( side = tkinter.TOP,
                        expand = tkinter.TRUE,
                        fill = tkinter.BOTH )


        self.enumerate_songs()


#========================== Button Callbacks ===================================

    def retrieve_songs( self ):
        self.songlist = []
        directory = tkinter.filedialog.askdirectory()
        for root_, dirs, files in os.walk( directory ):
            for file in files:
                if os.path.splitext( file )[1] == '*.mp3' or '*.ogg':
                    path = ( root_ + '/' + file ).replace( '\\', '/' )
                    self.songlist.append( path )

        f = open( 'songs.pickle', 'wb' )
        pickle.dump( self.songlist, f )
        f.close()

        self.playlist = self.songlist
        self.frm_tracklist['text'] = f'Playlist - {str( len( self.playlist ))}'
        self.list.delete( 0, tkinter.END )
        self.enumerate_songs()

    def pause_song( self ):    # 1:09:37
        if not self.paused:
            self.paused = True
            pygame.mixer.music.pause()
            self.btn_pause['image'] = self.img_pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            pygame.mixer.music.unpause()
            self.btn_pause['image'] = self.img_play


    def play_song( self, event = None ):
        if event is not None:
            self.current_song = self.list.curselection()[0]
            for i in range( len( self.playlist )):
                self.list.itemconfigure( i, background = 'white' )

        pygame.mixer.music.load( self.playlist[self.current_song] )
        self.btn_pause['image'] = self.img_play
        self.paused = False
        self.played = True
        self.txt_label['anchor'] = tkinter.W
        self.txt_label['text'] = os.path.basename( self.playlist[self.current_song] )
        self.list.activate( self.current_song )
        self.list.itemconfigure( self.current_song, background = 'sky blue' )
        pygame.mixer.music.play()


    def previous_song( self ):  # 1:13:57
        if self.current_song > 0:
            self.current_song -= 1
        else:
            self.current_song = 0
        #self.list.itemconfigure( self.current_song + 1, background = 'white' )
        self.list.selection_clear( self.current_song + 1 )
        self.list.itemconfigure( self.current_song , background = 'sky blue' )
        for i in range( len( self.playlist )):
                self.list.itemconfigure( i, background = 'white' )
        #self.list.activate( self.current_song + 1 )
        #self.list.itemconfigure( self.current_song , background = 'sky blue' )
        self.play_song()


    def next_song( self ):   # 1:15:32
        if self.current_song < len( self.playlist ) - 1:
            self.current_song += 1
        else:
            self.current_song = 0
        self.list.itemconfigure( self.current_song - 1, background = 'white' )
        self.play_song()


    def change_volume( self, event = None ):
        self.v = self.volume.get()
        #print( self.v )
        pygame.mixer.music.set_volume( self.v / 10 )

    def enumerate_songs( self ):
        for index, song in enumerate( self.playlist ):
            self.list.insert( index, os.path.basename( song ))





#================================= Main ========================================

if __name__ == '__main__':
    root = tkinter.Tk()
    application = Player( root )
    root.mainloop()
