import requests
from dbg import dbg
from os import path

#PWD_FILE='~/projects/pyplayer/paad.tmp';
PWD_FILE='paad.tmp'

def get_token(user=None, pwd=None):
    if user == None or pwd == None:
        dbg("User and/or password are None");
        return (0, 0);

    response = requests.get('https://oauth.vk.com/token?grant_type=password&' +
        'client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&' +
        'username=' + user + '&' +
        'password=' + pwd
        );
    rsp_json = response.json();
   
    try:
        return (response.json()["access_token"], 
                response.json()["user_id"]);
    except:
        pass 

    try:
        dbg("rsp: " + str(response));
        dbg("rsp: " + str(response.content));
        dbg("Error: " + response.content.json()["error"]);
    except: pass

    return (0, 0);

def store_user_password_pair(user, password):
    pw_file = open(PWD_FILE, 'w');
    if pw_file:
        pw_file.write(user+'\n');
        pw_file.write(password+'\n');
        pw_file.close();
    return 0;


def get_def_user_password_pair():
    if path.exists(PWD_FILE):
        pw_file = open(PWD_FILE, 'r');
        up_pair = (pw_file.readline()[:-1], pw_file.readline()[:-1]);
        pw_file.close();
        return up_pair;
    else:
        dbg("User data was not entered yet");
        return (0, 0);
