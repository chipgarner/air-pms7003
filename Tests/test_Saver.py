import save.saver
import os
import time


def remove_file(saver_class):
    if os.path.exists(saver_class.abs_file_path):
        os.remove(saver_class.abs_file_path)


def test_saves():
    saver = save.saver.Saver()

    saver.save_line('wop')

    f = open(saver.abs_file_path, "r")
    lines = f.readlines()

    assert len(lines) == 1
    assert lines[0] == 'wop\n'

    remove_file(saver)


def test_creates_new_file():
    saver = save.saver.Saver()

    for i in range(5):
        saver.save_line('wop')

    f = open(saver.abs_file_path, "r")
    lines = f.readlines()

    assert len(lines) == 5
    assert lines[4] == 'wop\n'

    time.sleep(1)  # So the next file has a new name

    saver_two = save.saver.Saver()

    saver_two.save_line('pop')

    f = open(saver_two.abs_file_path, "r")
    lines = f.readlines()

    assert len(lines) == 1
    assert lines[0] == 'pop\n'

    remove_file(saver)
    remove_file(saver_two)

def test_creates_new_file_over_max():
    saver = save.saver.Saver()

    for i in range(6):
        saver.save_line('plop')

    assert saver.lines_in_file == 6

    save.saver.MAX_LINES_IN_FILE = 3
    for i in range(5):
        saver.save_line('scmop')

    f = open(saver.abs_file_path, "r")
    lines = f.readlines()

    assert len(lines) == 11  # This is too fast to create a new file name (< 1 second) but shows lines_in_files changed.
    assert lines[4] == 'plop\n'
    assert saver.lines_in_file == 1

    remove_file(saver)
