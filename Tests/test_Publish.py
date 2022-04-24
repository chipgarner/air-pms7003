import publish.publish
import os


class CheckInternet:
    def __init__(self, return_value=True):
        self.connected = return_value

    def check_internet_connection(self):
        return self.connected

class FakePublisher:
    def __init__(self):
        self.last_message = ''

    def send_message(self, message):
        self.last_message = message
        return None  # Not using this


class FakePublisherTrue:
    def __init__(self):
        self.last_message = ''

    def send_message(self, message):
        self.last_message = message
        return True  # True to pretend internet is working


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def test_publish_averaged_data_format():
    fp = FakePublisher()
    pub = publish.publish.Publish(fp, CheckInternet().check_internet_connection)

    pub.publish_averaged_data({'Big': 2, 'fat': 11, 'fake': 9}, 7)

    assert 'ts' in fp.last_message
    assert "{'Big': 2, 'fat': 11, 'fake': 9}" in fp.last_message

    delete_file(pub.MISSED_CONN_FILE_NAME)


def test_starts_saving_when_internet_off():
    fp = FakePublisher()
    pub = publish.publish.Publish(fp, CheckInternet(False).check_internet_connection)
    delete_file(pub.MISSED_CONN_FILE_NAME)

    pub.publish_averaged_data({'Big': 2, 'fat': 11, 'fake': 9}, 7)

    assert os.path.exists(pub.MISSED_CONN_FILE_NAME)

    pub.publish_averaged_data({'Big': 3, 'fat': 13, 'fake': 10}, 7)

    with open(pub.MISSED_CONN_FILE_NAME) as f:
        lines = f.readlines()

    assert "{'Big': 2, 'fat': 11, 'fake': 9}" in lines[0]
    assert "{'Big': 3, 'fat': 13, 'fake': 10}" in lines[1]

    delete_file(pub.MISSED_CONN_FILE_NAME)


def test_no_file_save_with_internet():
    fp = FakePublisher()
    pub = publish.publish.Publish(fp, CheckInternet(False).check_internet_connection)

    pub.publish_averaged_data({'Big': 2, 'fat': 11, 'fake': 9}, 7)

    file_size = os.path.getsize(pub.MISSED_CONN_FILE_NAME)

    assert file_size == 66  # A file was created and is this size

    fp = FakePublisher()
    pub = publish.publish.Publish(fp, CheckInternet().check_internet_connection)

    pub.publish_averaged_data({'Big': 2, 'fat': 17, 'fake': 9}, 7)

    file_size = os.path.getsize(pub.MISSED_CONN_FILE_NAME)

    assert file_size == 66  # File size is unchanged
    assert "{'Big': 2, 'fat': 17, 'fake': 9}" in fp.last_message  # Making sure the message was sent
    with open(pub.MISSED_CONN_FILE_NAME) as f:
        lines = f.readlines()
    assert "{'Big': 2, 'fat': 11, 'fake': 9}" in lines[0]  # FIle content unchanged

    delete_file(pub.MISSED_CONN_FILE_NAME)


def test_sends_saved_file():
    fp = FakePublisher()
    ci = CheckInternet(False)
    pub = publish.publish.Publish(fp, ci.check_internet_connection)

    # Save a file with two lines
    pub.publish_averaged_data({'Big': 2, 'fat': 11, 'fake': 9}, 7)
    pub.publish_averaged_data({'Big': 2, 'fat': 17, 'fake': 9}, 7)

    ci.connected = True # Next attempt finds internet
    pub.publish_averaged_data({'Big': 3, 'fat': 27, 'fake': 19}, 77)

    assert "{'Big': 2, 'fat': 17, 'fake': 9}" in fp.last_message  # Making sure a saved message was sent

    delete_file(pub.MISSED_CONN_FILE_NAME)
