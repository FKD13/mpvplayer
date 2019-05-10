#!/bin/python3.7

import mpv
from urllib import request
from pafy import pafy


class Player:

    def __init__(self):
        self.player = mpv.MPV(ytdl=True)
        self.player.observe_property('time-pos', self.time_update)
        self.current_vid = None
        self.playlist = []
        self.index = 0

    def time_update(self, name, new_value):
        if self.current_vid is not None and new_value is not None and self.current_vid.length <= new_value + 1: # 1 is for security, for some video's this is required
            self.play()

    def add_video(self, video):
        self.playlist.append(video)

    def play(self):
        if self.index < len(self.playlist):
            self.current_vid = pafy.new(self.playlist[self.index]['url'])
            self.player.play(self.playlist[self.index]['url'])
            self.index += 1
        else:
            print('playlist at end - add songs')

    def disconnect(self):
        self.player.terminate()

    def __str__(self):
        string = ""
        for i, video in enumerate(self.playlist):
            string += f"\n{i} "
            if self.index - 1 == i:
                string += "---> " 
            else:
                string += "-> " 
            string += video['title']
        return string


class Searcher:

    def __init__(self):
        self.results = []

    def __str__(self):
        string = ""
        for i, result in enumerate(self.results):
            string += f"\n{i} -> {result['title']}"
        return string + "\n"

    def search(self, args: [str]):
        # remove previous search results
        self.results = []
        # do new search
        html = request.urlopen('https://youtube.com/results?search_query=' + '+'.join(args))
        line = html.readline().decode()
        while line:
            if line.startswith('</div><div class="yt-lockup-content"><h3 class="yt-lockup-title ">'):
                video = {'url': 'https://youtube.com' + line.split('"')[5], 'title': line.split('"')[11]}
                self.results.append(video)
            line = html.readline().decode()

    def get_video(self, index: int):
        if len(self.results) > index:
            return self.results[index]
        return None

    def get_all_videos(self):
        return self.results

def display_help():
    print("")
    print("find|search <search item>: returns a list of youtube's matching the search term")
    print("add <search item id>: add the video with selected id to playlist.")
    print("addall: add all search items to the playlist.")
    print("skip|play: play the next song in the playlist.")
    print("list: returns the playlist.")
    print("quit: close the program and video.")
    print("help: print this help")
    print("")

player = Player()
searcher = Searcher()

# main loop
command = input("> ")
while command != "quit" and command != "exit":
    if command.startswith("find ") or command.startswith("search "):
        command = command.split(" ")[1:]
        searcher.search(command)
        print(searcher)
    elif command.startswith("add "):  
        indexstr = command.split(' ')[1]
        if indexstr.isdigit():
            video = searcher.get_video(int(indexstr))
            player.add_video(video)
    elif command == "play" or command == "skip":
        player.play()
    elif command == "list":
        print(player)
    elif command == "addall":
        for video in searcher.get_all_videos():
            player.add_video(video)
        print('all video\'s added to playlist')
    elif command.startswith("help"):
        display_help()
    else:
        print('Unkown command')
    command = input("> ")

player.disconnect()
