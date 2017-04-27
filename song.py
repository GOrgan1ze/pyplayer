#
# Song class
#

import urllib

ARTIST = 'artist';
TITLE  = 'title';
URL    = 'url';

class song(object):
    
    def __init__(self, song_data, vlc_instance, player):
        self.player = player;
        self.song = song_data;
        self.vlc  = vlc_instance;

    @property
    def artist(self):
        return self.song[ARTIST];

    @property
    def title(self):
        return self.song[TITLE];

    @property
    def url(self):
        return self.song(URL);

    def play(self):
        try:
            media = self.vlc.media_new(song.url);
            playing_str.set(self.song.artist + ' - ' + self.song.title);

        except Exception as e:
            dbg('Exception : ', e);
            return -1;
        
        media.get_mrl();
        self.player.set_media(media);
        self.player.play();

        time.sleep(1); # TODO : test
        return 0;

    def download(self):
        destination = self.song.artist.replace("/","\\") + '-' + \
                      self.song.title.replace("/","\\")  + '.mp3';

        try:
            urllib.request.urlretrieve(self.song.url, destination);
        except: pass; #cant download, do nothing

        return 0;

### debug stuff
    def info(self):
        print('SONG values:');
        print(vars(self));



