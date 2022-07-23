import logging
from threading import Thread, Condition, current_thread
from queue import Queue, PriorityQueue


class EngineActionThread(Thread):
    """
        * Performs drive / stop actions on the motors.
        * All motor actions are performed exclusively on this thread to ensure right prioritisation / serialisation.
    """
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.action_queue = PriorityQueue()         # thread-safe shared task container
        self.lock = Condition()                     # for abortion of running task from other threads
        self.current_action = None                  # cross-thread shard driving variable used in critical sections

    def put_action(self, priority: int, time2finish: float, id_: int, action=None, abort_current=False) -> None:
        """
        This method is called from outer thread.
        All access of internal variables here is restricted to read only, except the thread-safe action_queue.put.
        :param priority: the lower int number the sooner execution
        :param time2finish: time to spend in action to consider it as completed
        :param id_:
        :param action: mainly the method which should be executed
        :param abort_current: abort current action with lower priority (higher int number) if True
        :return:
        """
        self.logger.debug(f'started putting: {priority} / {time2finish} / {id_}')
        self.action_queue.put(item=(priority, time2finish, id_))                # put() needs to be outside of self.lock as get() is inside of self.lock and blocking while empty
        if abort_current:
            with self.lock:                                                     # lock self.current_action to not abort just added (high priority) action
                if self.current_action and self.current_action[0] > priority:   # abort only lower priority (higher number) than newly added
                    self.logger.debug(f'engine notified to abort current action: {self.current_action} with priority {self.current_action[0]} in favor of {action} with priority {priority}')
                    self.lock.notify()
        self.logger.debug(f'ended putting: {priority} / {time2finish} / {id_}')

    def run(self):
        """ Engine action execution/abortion thread. """
        self.logger.info(f'Engine running {current_thread()}')

        while True:
            with self.lock:
                self.current_action = self.action_queue.get()                   # if queue empty > thread blocked (until something to get)
                start = time()
                self.logger.debug(f'engine started {self.current_action}')
                self.lock.wait(timeout=self.current_action[1])                  # wait given time (to complete the action) or abort it (in favour of action with higher priority)
                duration = time() - start
                if duration < self.current_action[1]:
                    self.logger.info(f'action dropped after {duration}s')
                else:
                    self.logger.debug(f'action finished after {duration}s')
