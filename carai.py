from controls.control import Control


# TODO: Is this abstraction/file needed?  Seems that this content can be moved to main()
class CarAI:
    """
        This class is the highest in abstraction hierarchy to wrap all the components.
        It is to initialise controls object which handles everything on main thread and leaves nothing to pass into main().

        HW = sensors + actuators
        SW = sensor >DATA> controls >ACTION> actuator

        Implemented as: Producer / Consumer design pattern:
        * Producer - produces actions based on sensory read (sensor + decision making)
        * Consumer - performs actions from the priority queue (actuator)
    """
    def __init__(self):
        super().__init__()
        self.control = Control()

    def main_loop(self) -> None:
        self.control.main_loop()


if __name__ == '__main__':
    c = CarAI()
    c.main_loop()
