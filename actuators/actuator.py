from typing import Type
from time import time
from threading import Condition
from queue import PriorityQueue

from actuators.action import Action, NoneAction, Result
from lib.threading2 import LoggingExceptionsThread
from lib.utils import who_long, who


# TODO: fix logging:
#  * +justification (in the put at least)

class Actuator(LoggingExceptionsThread):
    """
        Actuators job is to serialize given Actions and execute them in their priority order.
        Action instances are put to Actuator instance from various threads, but they are all executed exclusively in Actuator instance thread.
        That ensure only one Action instance execution per Actuator instance at the time.
    """
    def __init__(self, accepts: Type[Action]) -> None:
        super().__init__()
        self.action_queue = PriorityQueue()         # thread-safe shared task container
        self.lock = Condition()                     # for locking action execution + waiting to complete the action duration (wait() can be interrupted from outside by notify() to abort action sooner)
        self.current_action = None                  # cross-thread shard driving variable used in critical sections
        self.accepts = accepts

    def put(self, action: Action, abort_current: bool = False) -> bool:
        """
            This method is called from outer thread.
            All access of internal variables here is restricted to read only, except the thread-safe action_queue.put.
            :param action: Action instance to execute when time is right (action.priority helps with that decision)
            :param abort_current: abort currently executed action if it has lower priority
        """
        self.logger.debug(f'{who(self)}: Started putting: {who_long(action)} - {action.justification}')

        if not isinstance(action, self.accepts):
            self.logger.debug(f'{who(self)}: Refusing to put incompatible {action}')
            return False                                    # incompatible > try other actuator

        if action.same_actions_limit and self.count_same_actions(action) >= action.same_actions_limit:
            self.logger.debug(f'{who(self)}: Refusing to put another: {action} as actions_limit={action.same_actions_limit} level reached.')
            action.result = Result.DROPPED
            return True                                     # compatible but it does not meet its own condition to be queued for execution

        self.action_queue.put(action)                       # put() needs to be outside of self.lock as get() is inside of self.lock and blocking while empty (deadlock if both inside)
        action.event.queued = time()

        if abort_current:
            with self.lock:                                 # lock self.current_action to not abort just added (high priority) action as get runs on other thread and can happen any time
                if self.current_action and self.current_action.priority > action.priority:  # higher number means lower priority >>> surly different action >>> abort it
                    self.logger.debug(f'{who(self)} notified to abort current action: {who_long(self.current_action)} in favor of {who_long(action)}.')
                    self.lock.notify()
        self.logger.debug(f'{who(self)}: finished putting: {who_long(action)}')
        return True

    def iterate(self) -> None:
        """ This method gets repeatedly called (while Actuator's thread lives) for getting and executing actions (in action priority order) from the action_queue. """
        with self.lock:
            self.current_action = self.action_queue.get()
            self.logger.debug(f'{who(self)}: executing: {who_long(self.current_action)} - {self.current_action.justification}')
            self.current_action.execute_wrapper(self)       # actuator's lock needed for waiting given action.duration (also lock might get notify to abort the execution)
            self.current_action = None

    def stop(self, abort_current=False) -> None:
        """ Make the "Action execution thread" to finish. """
        super().stop()                                      # iterate() won't be called again. That will stop getting new actions from the queue.
        self.action_queue.put(NoneAction())                 # Stop waiting for an action to be put into the action queue (happens when queue is empty)
        if abort_current:
            with self.lock:
                self.lock.notify()                          # make "self.lock.wait(timeout)" to abort before timeout

    def count_same_actions(self, action: Action) -> int:
        """ This method is called from outer thread."""
        queued = len([same_action for same_action in self.action_queue.queue if same_action == action])
        return queued + 1 if action == self.current_action else queued

    @property
    def state(self) -> str:
        """ This method is called from outer thread. Variables might change asynchronously. """
        actions = f'{self.current_action.justification} [{", ".join(who(a) for a in self.action_queue.queue)}]' if self.current_action else ''
        return f'{super().state} {actions}'
