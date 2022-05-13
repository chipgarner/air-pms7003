import save.saver
import os


def remove_file():
    saver = save.saver.Saver()
    if os.path.exists(saver.abs_file_path):
        os.remove(saver.abs_file_path)


def test_saves():
    remove_file()
    saver = save.saver.Saver()

    saver.save_line('wop')

    f = open(saver.abs_file_path, "r")
    lines = f.readlines()

    assert len(lines) == 1
    assert lines[0] == 'wop\n'
