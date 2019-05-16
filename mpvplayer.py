#!/bin/python3.7

import mpv
from urllib import request
from pafy import pafy

from playListManager import *


class Player:

    def __init__(self):
        self.player = mpv.MPV(ytdl=True)
        self.player.observe_property('time-pos', self.time_update)
        self.current_vid = None
        self.playlist = []
        self.index = 0
        self.playing = False

    def time_update(self, name, new_value):
        if self.playing and self.current_vid is not None and new_value is not None and self.current_vid.length <= new_value + 1: # 1 is for security, for some video's this is required
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
            self.playing = True
        else:
            print('playlist at end - add songs')
            self.playing = False

    def skip(self, amounth: int):
        if 0 <= self.index + amounth - 1 < len(self.playlist):
            self.index += amounth - 1
            self.play()
        else:
            print(f'Could not skip {amounth} songs, song {self.index + amounth} does not exist')

    def disconnect(self):
        self.player.terminate()

    def goto(self, index: int):
        pass

    def __str__(self):
        string = ""
        for i, video in enumerate(self.playlist):
            # string += f"\n{i} "
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


class CommandManager:

    def __init__(self, player: Player, searcher: Searcher, playListManager: PlaylistManager):
        self.map = {
                "play": self.play_cmd,
                "skip": self.skip_cmd,
                "list": self.list_cmd,
                "find": self.find_cmd,
                "search": self.find_cmd,
                "addall": self.addall_cmd,
                "help": self.help_cmd,
                "add": self.add_cmd,
                "save": self.save_cmd,
                "showplaylist": self.show_playlist_cmd,
                "clear": self.clear_cmd,
                "load": self.load_cmd,
                "delete": self.delete_cmd}
        self.player = player
        self.searcher = searcher
        self.playListManager = playListManager

    def execute_command(self, basename: str, args: list):
        if basename in self.map:
            self.map[basename](args)
        else:
            print('command not defined')

    def play_cmd(self, args: list):
        if args is None:
            self.player.play()
        elif len(args) == 1:
            self.player.play(int(args[0]))
        else:
            print('Too many args: usage: play [nr]')

    def skip_cmd(self, args: list):
        if args is None:
            self.player.play()
        elif len(args) == 1:
            self.player.skip(int(args[0]))
        else:
            print('Too many args: usage: skip [nr]')

    def add_cmd(self, args: list):
        self.player.add_video(searcher.get_video(int(args[0])))

    def addall_cmd(self, args: list):
        for video in self.searcher.get_all_videos():
            self.player.add_video(video)

    def find_cmd(self, args: list):
        self.searcher.search(args)
        print(searcher)

    def clear_cmd(self, args: list):
        self.player.playlist = []

    def list_cmd(self, args: list):
        print(self.player)

    def save_cmd(self, args: list):
        if not self.playListManager.add_playlist(args[0], player.playlist):
            print('something went wrong')

    def delete_cmd(self, args: list):
        if args is not None and len(args) == 1:
            playListManager.remove_playlist(args[0])
        else:
            print('Too many args: usage: delete <name_playlist>')

    def load_cmd(self, args: list):
        if args is not None and len(args) == 1:
            player.playlist = playListManager.get_playlist(args[0])
            player.index = 0
        else:
            print('Too many args: usage: load <name_playlist>')

    def show_playlist_cmd(self, args: list):
        if args is None:
            for line in playListManager.get_all_playlist():
                print(line)
        elif len(args) == 1:
            for movie in playListManager.get_playlist(args[0]):
                print(movie['title'])
        else:
            print('Too Many args: Usage: > showplaylist [name]')

    def help_cmd(self, args: list):
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
playListManager = PlaylistManager()
commandManager = CommandManager(player, searcher, playListManager)

# main loop
command = input("> ")
while command != "quit" and command != "exit":
    command = command.split(' ')
    basename = command[0]
    if len(command) >= 2:
        args = command[1:]
    else:
        args = None
    commandManager.execute_command(basename, args)
    command = input("> ")

player.disconnect()
