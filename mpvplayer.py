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

    def add_video(self, video: dict):
        self.playlist.append(video)

    def play(self, index=None):
        if index is not None:
            self.index = index
        if self.index < len(self.playlist):
            self.current_vid = pafy.new(self.playlist[self.index]['url'])
            self.player.play(self.playlist[self.index]['url'])
            self.index += 1
        else:
            print('playlist at end - add songs')

    def disconnect(self):
        self.player.terminate()read xml python

    def goto(self, index: int):

    def __str__(self):
        string = ""
        for i, video in enumerate(self.playlist):
            if self.index - 1 == i:
                string += f"\n--> {i}: {video['title']}"
            else:
                string += f"\n{i}: {video['title']}"
        return string


class Searcher:

    def __init__(self):
        self.results = []

    def __str__(self):
        string = ""
        for i, result in enumerate(self.results):
            string += f"\n{i} -> {result['title']}"
        return string + "\n"

    def search(self, args: str):
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


class CommandManager:

    def __init__(self, player: Player, searcher: Searcher):
        self.map = {
                "play": self.play_cmd,
                "skip": None,
                "list": self.list_cmd,
                "find": self.find_cmd,
                "addall": None,
                "add": self.add_cmd}
        self.player = player
        self.searcher = searcher

    def execute_command(self, basename: str, args: list):
        if self.map[basename] is not None:
            self.map[basename](args)
        else:
            print('command not defined')

    def play_cmd(self, args: list):
        pass

    def add_cmd(self, args: list):
        pass

    def find_cmd(self, args: list):
        pass

    def list_cmd(self, args: list):

player = Player()
searcher = Searcher()
commandManager = CommandManager(player, searcher)

# main loop
command = input("> ")
while command != "quit":
    command = command.split(' ')
    basename = command[0]
    if len(command) >= 2:
        args = command[1:]
    else
        args = None
    commandManager.execute_command(basename, args)
    command = input("> ")

#    if command.startswith("find "):
#        command = command.split(" ")[1:]
#        searcher.search(command)
#        print(searcher)
#    elif command.startswith("add "):
#        video = searcher.get_video(int(command.split(' ')[1]))
#        player.add_video(video)
#    elif command.startswith("play"):
#        if len(command.split(' ')) == 2 and command.split(' ')[1].isnumeric():
#            player.play(int(command.split(' ')[1])) # play specific song
#        else:
#            player.play() # play next song
#    elif command.startswith("skip"):
#        
#    elif command == "list":
#        print(player)
#    elif command == "addall":
#        for video in searcher.get_all_videos():
#            player.add_video(video)
#        print('all video\'s added to playlist')
#    else:
#        print('Unkown command')
#    command = input("> ")

player.disconnect()
