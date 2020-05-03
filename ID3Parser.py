# Создание класса для более удобной работы с тегами
class ID3Parser:
    def __init__(self, song, artist, album):
        # Удаление ненужных символов и проверка на наличие мусора
        self._song = song.strip().rstrip('\x00') if song and len(song) != song.count(song[0]) else False
        self._artist = artist.strip().rstrip('\x00') if artist and len(artist) != artist.count(artist[0]) else False
        self._album = album.strip().rstrip('\x00') if album and len(album) != album.count(album[0]) else False

    def get_song(self):
        return self._song

    def get_artist(self):
        return self._artist

    def get_album(self):
        return self._album
