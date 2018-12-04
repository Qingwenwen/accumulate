
import os
import gc

import datetime

from pympler import muppy
from pympler import summary


DIRECTORY = '/home/qws/MemoryLeaks/'
TYPE_FILES = [
    'dict.txt', 'list.txt', 'tuple.txt',
]
TRACK_TYPE_LIST = [
    dict, list, tuple,
]
EXTRA_FILES = [
    '10000.txt', '20000.txt', '50000.txt', '100000.txt', '1000.txt'
]
# EXTRA_TRACK_LIST = []


def create_file():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    if os.path.isdir(DIRECTORY):
        exist_files = os.listdir(DIRECTORY)
        files = TYPE_FILES + EXTRA_FILES
        files.append('uncollectable.txt')

        for file in files:
            if file not in exist_files:
                os.mknod(DIRECTORY + file)


def object_track_record(filename, Type=None, min=-1, max=-1):
    filter_objects = muppy.filter(
        muppy.get_objects(include_frames=True),
        Type,
        min,
        max)
    objects_size = summary.summarize(filter_objects)
    date_time = datetime.datetime.utcnow()

    with open(filename, 'a') as f:
        f.write('%s: %s+\n' % (str(date_time), str(objects_size)))


def write_uncollectable():
    gc.collect()
    uncollectable = gc.garbage
    filename = DIRECTORY + 'uncollectable.txt'
    date_time = datetime.datetime.utcnow()
    with open(filename, 'a') as f:
        f.write('%s: %s+\n' % (str(date_time), str(uncollectable)))


def make_tasks():
    tasks = []
    default_min = -1
    default_max = 10000

    for i in range(len(TRACK_TYPE_LIST)):
        file_path = DIRECTORY + TYPE_FILES[i]
        Type = TRACK_TYPE_LIST[i]
        tasks.append((file_path, Type, default_min, default_max))

    for filename in EXTRA_FILES:
        max = int(filename.split('.')[0])
        tasks.append((DIRECTORY + filename, object, default_min, max))

    return tasks


def exec_track():
    tasks = make_tasks()

    for task in tasks:
        object_track_record(task[0], task[1], task[2], task[3])

    write_uncollectable()


def init():
    create_file()


def main():
    init()
    exec_track()
