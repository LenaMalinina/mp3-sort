import argparse
from mp3_tagger import MP3File, VERSION_2
import os
from FSWrapper import FSWrapper
from ID3Parser import ID3Parser


parser = argparse.ArgumentParser(description='Sort mp3 files')
parser.add_argument('--src-dir', '-s', type=str, help='Source path', default='.')
parser.add_argument('--dst-dir', '-d', type=str, help='Destination path', default='.')
args = parser.parse_args()

# Удаление ненужных разделителей
if not os.path.isabs(args.src_dir) and args.src_dir != '.':
    args.src_dir = args.src_dir.strip('.\\/')
if not os.path.isabs(args.dst_dir) and args.dst_dir != '.':
    args.dst_dir = args.dst_dir.strip('.\\/')

args.src_dir = os.path.normpath(args.src_dir)
args.dst_dir = os.path.normpath(args.dst_dir)
# Проверка на наличие директории
if not os.path.exists(args.src_dir) or not os.path.isdir(args.src_dir):
    print('Входная директория не существует')
    exit()
# Проверка на наличие прав
if not os.access(args.src_dir, os.R_OK):
    print('Не хватает прав для чтения входной директории')
    exit()
# Проверка на существование выходной директории, ее создание и наличие прав
if not os.path.exists(args.dst_dir):
    try:
        os.makedirs(args.dst_dir)
    except OSError as e:
        print(e)
        exit()
    else:
        print('Выходная директория успешно создана')
elif not os.access(args.dst_dir, os.W_OK):
    print('Не хватает прав для записи в выходную директорию')
    exit()

files = FSWrapper.listdir(args.src_dir)
for file in files:
    src_file_name = os.path.join(args.src_dir, file)
    if os.access(src_file_name, os.R_OK):
        try:
            mp3file = MP3File(src_file_name)
        except(WindowsError, PermissionError):
            print(f'Недостаточно прав для чтения файла {file}')
            continue
    else:
        print(f'Недостаточно прав для чтения файла {file}')
        continue

    mp3file.set_version(VERSION_2)
    audio_file = ID3Parser(mp3file.song, mp3file.artist, mp3file.album)

    if not audio_file.get_artist() or not audio_file.get_album():
        print(f'Ошибка: {src_file_name} не содержит тегов')
        continue
    if audio_file.get_song():
        file_name = f'{audio_file.get_song()} - {audio_file.get_artist()} - {audio_file.get_album()}.mp3'
    else:
        file_name = file
    dst_file_name = os.path.join(args.dst_dir, audio_file.get_artist(), audio_file.get_album(), file_name)
    os.makedirs(os.path.join(args.dst_dir, audio_file.get_artist(), audio_file.get_album()), mode=0o777, exist_ok=True)
    if os.path.exists(dst_file_name):
        os.remove(dst_file_name)
    os.renames(src_file_name, dst_file_name)
    print(f'{src_file_name} -> {dst_file_name}')
print('Готово.')
