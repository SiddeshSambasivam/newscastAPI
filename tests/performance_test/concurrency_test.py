import requests
import threading
import queue
import sys
import time
import logging
import statistics

from tqdm import tqdm
logging.basicConfig(level="INFO")

response_time = None


def test_mock_service():

    url = "https://newscast-api.herokuapp.com/api"
    resp = requests.get(url)

    if resp.status_code != 200:
        if resp.status_code == 422:
            logging.info("Test passed")
            return 'pass', resp.elapsed.total_seconds()

        logging.error('Test failed with response status code %s.' %
                      resp.status_code)
        return 'fail', resp.elapsed.total_seconds()

    elif resp.status_code == 200:
        # print()
        assert len(resp.json()["results"]) == 10
        logging.info('Test passed.')
        return 'pass', resp.elapsed.total_seconds()

    else:
        logging.error('Test failed with code.')
        return 'fail', resp.elapsed.total_seconds()


# Global variables
queue_results = queue.Queue()
start_time = 0


def loop_test(loop_wait=0, loop_times=sys.maxsize):
    global response_time
    looped_times = 0
    while looped_times < loop_times:
        # run an API test
        test_result, elapsed_time = test_mock_service()
        response_time.append(elapsed_time)
        # put results into a queue for statistics
        queue_results.put(['test_mock_service', test_result, elapsed_time])

        # You can add more API tests in a loop here.
        looped_times += 1
        time.sleep(loop_wait)


if __name__ == '__main__':
    response_time = []
    ### Test Settings ###
    concurrent_users = 3
    loop_times = 2

    workers = []
    start_time = time.time()

    # start concurrent user threads
    for i in tqdm(range(concurrent_users)):
        thread = threading.Thread(target=loop_test, kwargs={
                                  'loop_times': loop_times}, daemon=True)
        thread.start()
        workers.append(thread)

    # Block until all threads finish.
    for w in workers:
        w.join()

    end_time = time.time()
    print()
    logging.error('Total test time: %s seconds.' % (end_time - start_time))
    try:
        avg = statistics.mean(response_time)
        logging.error(f"Avg Time: {avg}")
    except ZeroDivisionError:
        logging.error(f"response time is not updated")
    print()
