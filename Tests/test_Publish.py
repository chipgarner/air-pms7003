import publish.publish


class FakePublisher:
    def __init__(self):
        self.last_message = ''

    def send_message(self, message):
        self.last_message = message


def test_publish_averaged_data():
    fp = FakePublisher()
    pub = publish.publish.Publish(fp)

    pub.publish_averaged_data({'Big': 2, 'fat': 11, 'fake': 9}, 7)

    assert 'ts' in fp.last_message
    assert "{'Big': 2, 'fat': 11, 'fake': 9}" in fp.last_message


