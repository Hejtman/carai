import time
import unittest
from pathlib import Path
from actuators.actuator import Actuator
from actuators.action import Action, Result, Priority
from lib.cli import TerminalLogger
from lib.utils import wait_for_callable


class CustomAction(Action):
    def __init__(self):
        super().__init__(0, 0)
        self.was_executed = False

    def execute(self):
        self.was_executed = True


class ExecutionOrderTestingAction(Action):
    execution_counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execution_order = -1

    def execute(self):
        ExecutionOrderTestingAction.execution_counter += 1
        self.execution_order = self.execution_counter


class ActuatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        TerminalLogger(file_path=f'{Path.home()}/{Path.cwd().stem}/{Path(__file__).stem}.log')

    def setUp(self) -> None:
        self.actuator = Actuator()

    def tearDown(self) -> None:
        if self.actuator.is_alive():
            self.actuator.stop()
            self.actuator.join()

    def test_01_that_actuator_executes_given_action(self) -> None:
        action = CustomAction()
        self.actuator.put_action(action)

        self.actuator.start()
        time.sleep(0.001)
        assert action.was_executed

    def test_02_that_action_is_not_executed_when_actuator_not_started(self) -> None:
        action = CustomAction()
        self.actuator.put_action(action)

        time.sleep(0.002)
        assert not action.was_executed

    def test_03_that_action_status_is_finished_after_execution(self) -> None:
        action = CustomAction()
        self.actuator.put_action(action)
        assert action.result is Result.NOT_SET

        self.actuator.start()
        time.sleep(0.001)
        assert action.result is Result.FINISHED

    def test_04_that_actuator_queue_is_empty_before_and_after_execution(self) -> None:
        assert self.actuator.action_queue.empty()
        self.actuator.put_action(CustomAction())
        assert not self.actuator.action_queue.empty()

        self.actuator.start()
        time.sleep(0.001)
        assert self.actuator.action_queue.empty()

    def test_05_that_actuator_executes_actions_sequentially(self) -> None:
        ExecutionOrderTestingAction.execution_counter = 0
        duration = 0.1
        actions = [ExecutionOrderTestingAction(priority=0, duration=duration),
                   ExecutionOrderTestingAction(priority=1, duration=duration),
                   ExecutionOrderTestingAction(priority=2, duration=duration)]
        for action in actions:
            self.actuator.put_action(action)

        self.actuator.start()

        for i in [0, 1, 2]:
            assert wait_for_callable(lambda: actions[i].result,  # passing result as lambda (and not as immutable variable) makes it to reflect changes from other thread within wait method context.
                                     expected_value=Result.FINISHED,  period=duration/10,
                                     timeout=2*duration)         # Expected duration + overhead
            for ii in range(i+1, len(actions)):                  # make sure the rest is not FINISHED yet
                assert actions[ii].result is Result.NOT_SET

    def test_06_that_actuator_performs_high_priority_action_first(self) -> None:
        ExecutionOrderTestingAction.execution_counter = 0
        actions = [ExecutionOrderTestingAction(priority=Priority.LOW+1, duration=0),  # 3. (higher number means lower priority)
                   ExecutionOrderTestingAction(priority=Priority.HIGH, duration=0),   # 1.
                   ExecutionOrderTestingAction(priority=Priority.LOW, duration=0)]    # 2.
        for action in actions:
            self.actuator.put_action(action)

        self.actuator.start()
        time.sleep(0.001)

        expected_order = (3, 1, 2)
        assert all(action.execution_order == order for action, order in zip(actions, expected_order))
        assert all(action.result is Result.FINISHED for action in actions)

    def test_07_that_actuator_performs_high_priority_action_first_different_order(self) -> None:
        ExecutionOrderTestingAction.execution_counter = 0
        actions = [ExecutionOrderTestingAction(priority=Priority.LOW-1, duration=0),  # 2. (lower number means higher priority)
                   ExecutionOrderTestingAction(priority=Priority.LOW, duration=0),    # 3.
                   ExecutionOrderTestingAction(priority=Priority.HIGH, duration=0)]   # 1.

        for action in actions:
            self.actuator.put_action(action)

        self.actuator.start()
        time.sleep(0.001)

        expected_order = (2, 3, 1)
        assert all(action.execution_order == order for action, order in zip(actions, expected_order))
        assert all(action.result is Result.FINISHED for action in actions)

    def test_08_that_actuator_performs_high_priority_action_immediately_after_finishing_currently_executed(self) -> None:
        ExecutionOrderTestingAction.execution_counter = 0
        duration = 0.01
        actions = [ExecutionOrderTestingAction(priority=Priority.LOW-1, duration=duration),  # 1. (lower number means higher priority)
                   ExecutionOrderTestingAction(priority=Priority.LOW, duration=duration)]    # 3.
        for action in actions:
            self.actuator.put_action(action)

        self.actuator.start()

        assert wait_for_callable(lambda: actions[0].execution_order, 1, period=duration/10, timeout=2*duration)                     # wait for first low priority action to be executed
        high_priority_action = ExecutionOrderTestingAction(priority=Priority.HIGH, duration=duration)
        self.actuator.put_action(high_priority_action)
        assert all(action.result is Result.NOT_SET for action in actions)  # no action finished yet (duration period)

        assert wait_for_callable(lambda: actions[0].result, Result.FINISHED, period=duration/10, timeout=2*duration)                # wait for first low priority action to be finished
        assert actions[0].time_spent >= duration
        assert wait_for_callable(lambda: high_priority_action.result, Result.FINISHED, period=duration / 10, timeout=2 * duration)  # wait for high priority action to be finished
        assert actions[1].result is not Result.FINISHED

    def test_09_that_actuator_aborts_lower_priority_action(self) -> None:
        ExecutionOrderTestingAction.execution_counter = 0
        duration = 0.01
        actions = [ExecutionOrderTestingAction(priority=Priority.LOW-1, duration=1),  # 1. (lower number means higher priority)
                   ExecutionOrderTestingAction(priority=Priority.LOW, duration=duration)]    # 3.
        for action in actions:
            self.actuator.put_action(action)

        self.actuator.start()

        assert wait_for_callable(lambda: actions[0].execution_order, 1, period=duration/10, timeout=2*duration)                     # wait for first low priority action to be executed
        high_priority_action = ExecutionOrderTestingAction(priority=Priority.HIGH, duration=duration)
        self.actuator.put_action(high_priority_action, abort_current=True)
        assert all(action.result is not Result.FINISHED for action in actions)                                                      # no action finished yet (duration period)

        assert wait_for_callable(lambda: actions[0].result, Result.ABORTED, period=duration/10, timeout=duration/2)                 # should be aborted (sooner than action duration)
        assert actions[0].time_spent < duration
        assert wait_for_callable(lambda: high_priority_action.result, Result.FINISHED, period=duration / 10, timeout=2 * duration)  # wait for high priority action to be finished
        assert actions[1].result is not Result.FINISHED
