import logging
from enum import Enum
from time import time
from threading import Thread, Condition, Event
from queue import Queue, PriorityQueue

from actuators.action import Action, Result, NoneAction


class Actuator(Thread):
    """
        Actuators job is to serialize given Actions and execute them in their priority order.
        Action instances are put to Actuator instance from various threads, but they are all executed exclusively in Actuator instance thread.
        That ensure only one Action instance execution per Actuator instance at the time.
    """

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.action_queue = PriorityQueue()         # thread-safe shared task container
        self.lock = Condition()                     # for locking action execution + waiting to complete the action duration (wait() can be interrupted from outside by notify() to abort action sooner)
        self.current_action = None                  # cross-thread shard driving variable used in critical sections
        self.event_stop = Event()                   # to terminate the thread eventually

    def put_action(self, action: Action, abort_current=False) -> None:
        """
        This method is called from outer thread.
        All access of internal variables here is restricted to read only, except the thread-safe action_queue.put.
        :param action: an Action instance to execute when time is right (action.priority helps with that decision)
        :param abort_current: abort currently executed action if it has lower priority
        :return:
        """
        self.logger.debug(f'started putting: {action}')

        self.action_queue.put(action)                                   # put() needs to be outside of self.lock as get() is inside of self.lock and blocking while empty (deadlock if both inside)
        action.event.queued = time()

        if abort_current:
            with self.lock:                                             # lock self.current_action to not abort just added (high priority) action as get runs on other thread and can happened any time
                if self.current_action and self.current_action.priority > action.priority:  # higher number means lower priority >>> surly different action >>> abort it
                    self.logger.debug(f'{self.__class__.__name__} notified to abort current action: {self.current_action.__dict__} in favor of {action.__dict__}.')
                    self.lock.notify()
        self.logger.debug(f'finished putting: {action}')

    def run(self):
        """ Action execution thread. Getting and executing actions in action.priority from the queue until..."""
        self.logger.info(f'{self.__class__.__name__} thread running.')

        while not self.event_stop.is_set():
            with self.lock:
                self.current_action = self.action_queue.get()
                with self.current_action:                                                           # action execution happens in action context __enter__
                    execution_duration = self.current_action.event.execution - self.current_action.event.start
                    timeout = self.current_action.duration - execution_duration
                    self.logger.debug(f'{self.current_action.__class__.__name__} {hex(id(self.current_action))} execution took {execution_duration}s waiting {timeout}s to finish it.')

                    aborted = self.lock.wait(timeout)                                               # wait until action duration reached (or action aborted prematurely from outer thread)
                    self.current_action.result = Result.ABORTED if aborted else Result.FINISHED

        self.logger.info(f'{self.__class__.__name__} actuator thread ended.')

    def stop(self, abort_current=False):
        """ Make the "Action execution thread" to finish. """
        self.event_stop.set()                               # Stop getting actions from the queue.
        self.action_queue.put(NoneAction())                 # Stop waiting for an action to be put into the action queue (happens when queue is empty)
        if abort_current:
            with self.lock:
                self.lock.notify()                          # make "self.lock.wait(timeout)" to abort before timeout
