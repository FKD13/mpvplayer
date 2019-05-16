#!/bin/python3

import json

class PlaylistManager:

    def __init__(self):
        self.path = 'playlists.json'
        self.playlists = dict()
        self.load()

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.playlists = json.load(f)
        except FileNotFoundError:
            print("No existing playlist file, will be made when saving first playlist")

    def save(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.playlists))

    def get_playlist(self, name: str):
        if name in self.playlists:
            return self.playlists[name]
        return None

    def get_all_playlist(self):
        return list(self.playlists.keys())

    def add_playlist(self, name: str, items: list):
        if name not in self.playlists:
            self.playlists[name] = items
            self.save()
            return True
        return False

    def playlist_add_item(self, name: str, item: list):
        if name in self.playlists:
            self.playlists[name].append(item)
            return True
        return False

    def playlist_delete_item(self, name: str, index: int):
        if name in self.playlists:
            if 0 <= index < len(self.playlists[name]):
                del self.playlists[name][index]
                return True
        return False

    def remove_playlist(self, name: str):
        if name in self.playlists:
            del self.playlists[name]
            self.save()
