import vlc
import vk
import requests
import json
import time 
import urllib
import tty
import sys
import termios
import turtle
import threading
import datetime

from tkinter import *

#internal files
from authorization import *
from player_states import *
from dbg import dbg


appWin = Tk();
appWin.title('VK pyplayer v0.0.1');

# disable resizing by user
appWin.resizable(width=False,height=False);
appWin.minsize(width=550, height=200);
appWin.maxsize(width=800, height=800);

save_input_user_password = IntVar();
owner_comp_list = IntVar();
repeat_current = IntVar();

search_str = StringVar();
user_str   = StringVar();
pwd_str    = StringVar();
playing_str = StringVar();

user     = '';
password = '';
curplay_idx = 0;

def get_credentials(in_user, in_pwd):
    #check default
    dbg('Default credentials are used');
    user, password = get_def_user_password_pair();

    if in_user == '' or in_pwd == '':
        return user, password;

    if user == '' or password == '':
        return in_user, in_pwd;

    if in_user != user and in_pwd != password:
        if save_input_user_password.get():  
            dbg('Store credentials option was entered');
            store_user_password_pair(in_user, in_pwd);

    return in_user, in_pwd;


def download_song(song_data):
    try:
        urllib.request.urlretrieve(song_data['url'],
                song_data['artist'] + '-' + song_data['title'] + '.mp3');
    except: pass;
    set_player_state(ACTIVE);
    

def play_song(song_data, player, vlc_inst):
    global playing_str;
    try:
        playing_str.set(song_data['artist'] + ' - ' + song_data['title']);
        media = vlc_inst.media_new(song_data['url']);
    except Exception as e:
        dbg('Exception : ', e);
        return -1;

    media.get_mrl();
    player.set_media(media);

    player.play();
    playing = set([1,2,3,4]); #some strange shit. Just copied :)

    time.sleep(1);
 
    return 0;

def process_playlist():
    global music_list;
    global curplay_idx;
    
    playlist = [ url['url'] for url in music_list]
    limit = len(music_list)

    vlc_inst = vlc.Instance();
    player = vlc_inst.media_player_new();

    while (curplay_idx < limit):
        set_player_state(ACTIVE);

        play_song(music_list[curplay_idx], player, vlc_inst);

        while True:
            player_state = get_player_state();
            if   player_state == PAUSE:
                player.pause();
                while (get_player_state() == PAUSE):
                    continue;
            elif player_state == DOWNLOAD:
                download_song(music_list[curplay_idx]);
            elif player_state == STOP:
                player.stop();
                return 0;
            elif player_state == PLAY:
                set_player_state(ACTIVE);
                player.play();
            elif player_state == NEXT:
                break;
            elif player_state == PREV:
                if not repeat_current.get():
                    curplay_idx -= 2;
                break;
            elif player_state == CHANGED:
                global PlayListBox;
                curplay_idx = PlayListBox.curselection()[0] - 1;
                break;
            continue;
        if not repeat_current.get():
            curplay_idx += 1;
    return 1;

PlayListBox = None;
music_list = None;

def vk_music_main(a=None):
    global PlayListBox;
    global music_list;
    global curplay_idx;
    curplay_idx = 0;

    if get_player_state() == ACTIVE:
        set_player_state(STOP);
        time.sleep(1);
    set_player_state(ACTIVE); 
    #get Credentials window
    user = user_str.get();
    password = pwd_str.get();

    user, password = get_credentials(user, password);
    if not user or not password:
        dbg("No credentials. Good buy!");
        return 0;

    #get access_token to use VK API
    access_token, my_id = get_token(user, password);
    if access_token == 0:
        return 0;


    session = vk.Session()
    api = vk.API(session, access_token=access_token)

    if owner_comp_list.get():
        music_response=api.audio.get(owner_id=my_id, count=1000, access_token=access_token);
    else:
        music_response = api.audio.search(count=1000, access_token=access_token, q=search_str.get());
     
    if not PlayListBox:
        PlayListBox = Listbox(appWin, selectmode=SINGLE, width=90, height=25);
        PlayListBox.grid(row=5, column=0,columnspan=5);
        yscroll = Scrollbar(command=PlayListBox.yview, orient=VERTICAL);
        yscroll.grid(row=5, column=5);
        PlayListBox.configure(yscrollcommand=yscroll.set);
        PlayListBox.bind('<Double-Button-1>', play_selected);
    PlayListBox.delete(0, PlayListBox.size());

    music_list = music_response[1:];

    for i in range(0, len(music_list)):
        PlayListBox.insert(i + 1, '[' + '{0: ^5}'.format(i) +'] ' + 
                music_list[i]['artist'] + ' - ' + music_list[i]['title'] + '  ' + 
                str(datetime.timedelta(seconds=music_list[i]['duration'])));


    Process = threading.Thread(target=process_playlist);
    Process.start();

###############################################################################
############ UI related data #########################
###############################################################################
 
def player_stop():
    set_player_state(STOP);

def player_next():
    set_player_state(NEXT);

def player_prev():
    set_player_state(PREV);

def player_download():
    set_player_state(DOWNLOAD);

def player_pause():
    set_player_state(PAUSE);

def player_play():
    set_player_state(PLAY);

def play_selected(event):
    set_player_state(CHANGED);

# set background picture
bg_pic = PhotoImage(file='pictures/music_wall_gif.gif');
bg_label = Label(appWin, image=bg_pic);
bg_label.place(x=0, y=0, relwidth=1, relheight=1);


# Check buttons for Repeat and Owner..
wrap_around = Checkbutton(appWin, text='Repeat current', 
                          variable=repeat_current,
                          onvalue=1, offvalue=0);
wrap_around.grid(row=4, column=1);

owner_compositions = Checkbutton(appWin, text='Owner compositions',
                                 variable=owner_comp_list,
                                 onvalue=1, offvalue=0);
owner_compositions.grid(row=4, column=2);

# login
login_label = Label(appWin, text='User ');
login_label.grid(row=0, column=0);
login_entry = Entry(appWin, bd=4, textvariable=user_str);
login_entry.grid(row=0, column=1);

# password
pwd_label = Label(appWin, text='Password ');
pwd_label.grid(row=1, column=0);
pwd_entry = Entry(appWin, bd=4, textvariable=pwd_str, show="*");
pwd_entry.grid(row=1, column=1);

# save login + password?
save_credentials = Checkbutton(appWin, text='Save credentials',
                               variable=save_input_user_password,
                               onvalue=1, offvalue=0);
save_credentials.grid(row=0, column=2 );


# Search
search_label = Label(appWin, text='Search ');
search_label.grid(row= 2, column=0);
search_entry = Entry(appWin, bd=4, textvariable=search_str);
search_entry.grid(row= 2, column=1);

# Now playing data
playing_label = Label(appWin, text='Now playing :');
playing_label.grid(row=6, column=0);
playing_entry = Entry(appWin, bd=4, textvariable=playing_str, width=80);
playing_entry.grid(row=6, column=1, columnspan=4);

# Buttons creation
start_button = Button(appWin, command=vk_music_main, text='Start'); 
stop_button  = Button(appWin, command=player_stop, text='Stop');
play_button = Button(appWin, command=player_play, text='Play');
pause_button = Button(appWin, command=player_pause, text='Pause');
next_button  = Button(appWin, command=player_next, text='Next');
prev_button  = Button(appWin, command=player_prev, text='Prev');
download_button = Button(appWin, command=player_download, text='Download'); 

# Buttons location
start_button.grid(row=3, column=0);
stop_button.grid(row=3, column=1);
play_button.grid(row=3, column=2);
pause_button.grid(row=3, column=3);
prev_button.grid(row=3, column=4);
next_button.grid(row=3, column=5);
download_button.grid(row=4, column=0);

# Tkinter mainloop :)
appWin.mainloop();


