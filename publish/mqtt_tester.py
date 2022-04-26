import logging
import publisher
import time
from Secrets import TEST_SECRET

if __name__ == '__main__':
    log_format = '%(asctime)s %(name)s %(message)s'
    logging.basicConfig(format=log_format,
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
    logger = logging.getLogger()

    logger.debug('Test logger')

    pub = publisher.Publisher(TEST_SECRET)

    big = 2

    for i in range(100):
        delta = 3
        if i % 2 == 0:
            delta = -1
        big = big + delta

        message = {'Big': big, 'fat': 28, 'fake': 20}
        pub.send_message(str(message))
        time.sleep(5)

    pub.stop()


    # For testing the mqtt library
    # from Secrets import TEST_SECRET
    # if __name__ == '__main__':
    #     pub = Publisher(TEST_SECRET)
    #
    #     def send_missed_file():
    #         with open('data_not_sent_test.txt') as f:
    #             lines = f.readlines()
    #
    #         for line in lines:
    #             pub.send_message(line)
    #             time.sleep(1)
    #
    #     send_missed_file()
    #     pub.stop()
