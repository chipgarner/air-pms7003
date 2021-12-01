import pms7003.publisher


def test_publish():
    pub = pms7003.publisher.Publisher()

    message = '{"Test": 799, "Publishing": 99}'
    pub.send_message(message)

    pub.stop()