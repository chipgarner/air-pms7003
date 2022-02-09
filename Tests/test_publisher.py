import publisher


def test_publish():
    pub = publisher.Publisher()

    message = '{"Test": 799, "Publishing": 99}'
    pub.send_message(message)

    pub.stop()