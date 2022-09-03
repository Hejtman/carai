from threading import Thread, Event
import unittest
import time

from controls.base import ComponentPeriod
from lib.threading2 import LoggingExceptionsThread

PERIOD = 0.1


class CustomThread(Thread):
    def __init__(self):
        super().__init__()
        self.event_stop = Event()
        self.iteration_times = []

    def run(self):
        while not self.event_stop.is_set():
            self.iteration_times.append(time.time())
            self.event_stop.wait(PERIOD)

    def stop(self):
        self.event_stop.set()


class IterationThreadTest(unittest.TestCase):
    def setUp(self) -> None:
        self.thread = CustomThread()

    def test_1_that_it_does_not_iterate_before_start(self) -> None:
        assert self.thread.iteration_times == []

    def test_2_that_it_starts(self) -> None:
        self.thread.start()
        self.thread.stop()
        assert len(self.thread.iteration_times) == 1

    def test_3_that_it_stops(self) -> None:
        self.thread.start()
        self.thread.stop()
        time.sleep(PERIOD)
        assert len(self.thread.iteration_times) == 1

    def test_4_that_it_waits_period_between_iterations(self) -> None:
        self.thread.start()
        time.sleep(10 * PERIOD)
        self.thread.stop()
        assert len(self.thread.iteration_times) == 10
        for i in range(0, 8):
            assert round(self.thread.iteration_times[i+1] - self.thread.iteration_times[i], 1) == PERIOD


class CustomComponentPeriod(ComponentPeriod, LoggingExceptionsThread):
    def __init__(self, period):
        super().__init__(period)
        LoggingExceptionsThread.__init__(self)
        self.iteration_times = []

    def iterate(self):
        self.iteration_times.append(time.time())


class ComponentPeriodTest(IterationThreadTest):
    def setUp(self) -> None:
        self.thread = CustomComponentPeriod(PERIOD)

    def test_5_that_it_pause_and_resume_iterations(self) -> None:
        self.thread.start()
        time.sleep(5 * PERIOD)
        self.thread.reverse_activity()
        assert len(self.thread.iteration_times) == 5
        time.sleep(5 * PERIOD)
        assert len(self.thread.iteration_times) == 5
        self.thread.reverse_activity()
        time.sleep(5 * PERIOD)
        assert len(self.thread.iteration_times) == 10
        self.thread.stop()
