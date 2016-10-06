from threading import Lock

ACTIVE   = 0;     #player is active
PLAY     = 1;     #player switched from PUASE
PAUSE    = 2;     #playing is stopped
STOP     = 3;     #player is deactivated
DOWNLOAD = 4;     #download curent song in bg
NEXT     = 5;     #switch to the next song
PREV     = 6;     #switch to the prev song
CHANGED  = 7;     #switch to selected song  

ACTIVE_STATES = (ACTIVE, PLAY, DOWNLOAD);

player_state = ACTIVE;
state_lock = Lock();

def get_player_state():
    global player_state;
    global state_lock;
    state = None;

    state_lock.acquire();
    state = player_state;
    state_lock.release();
    return state

def set_player_state(state):
    global player_state;
    global state_lock;

    state_lock.acquire();
    player_state = state;
    state_lock.release();
