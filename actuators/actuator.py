import logging
from threading import Thread, Condition, current_thread
from queue import Queue, PriorityQueue

from actuators.action import Action


class Actuator(Thread):
    """
        * Performs given actions on given actuator.
        * Actions performed exclusively on its thread to ensure actions prioritisation / serialisation on single actuator.
    """

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.action_queue = PriorityQueue()         # thread-safe shared task container
        self.lock = Condition()                     # for abortion of running task from other threads
        self.current_action = None                  # cross-thread shard driving variable used in critical sections

    def put_action(self, action: Action, abort_current=False) -> None:
        """
        This method is called from outer thread.
        All access of internal variables here is restricted to read only, except the thread-safe action_queue.put.
        :param action: an Action instance to execute when time is right (action.priority helps with that decision)
        :param abort_current: abort currently executed action if it has lower priority
        :return:
        """
        self.logger.debug(f'started putting: {priority} / {time2finish} / {id_}')
        assert self is action.actuator, f'Actuator {self.__class__.__name__} given incompatible action: {action.actuator.__class__.__name__}'

        self.action_queue.put(item=(action.priority, action))           # put() needs to be outside of self.lock as get() is inside of self.lock and blocking while empty (deadlock if both inside)
        if abort_current:
            with self.lock:                                             # lock self.current_action to not abort just added (high priority) action as get runs on other thread and can happened any time
                if self.current_action and self.current_action.priority < action.priority:  # lower priority > different action > abort it
                    self.logger.debug(f'{self.__class__.__name__} notified to abort current action: {self.current_action} with priority {self.current_action[0]} in favor of {action} with priority {priority}')
                    self.lock.notify()
        self.logger.debug(f'ended putting: {priority} / {time2finish} / {id_}')

    def run(self):
        """ Action execution/abortion thread. """
        self.logger.info(f'{self.__class__.__name__} actuator thread running.')

        while True:
            with self.lock:
                _, self.current_action = self.action_queue.get()        # item=(priority, action) ; queue empty > execution thread blocked (until put called from another thread)
                self.current_action.execute_wrapper()

    def create_action(self, cls: type[Action]) -> Action:
        """ Create action instance for this actuator instance. It can be put into execution queue to this actuator whenever. """
        return cls(self)
