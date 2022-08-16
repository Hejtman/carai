class Config:
    """ Storage for an external environment configurations / dependencies. """
    RC_HTTP_SERVER = ('192.168.10.1', 81)

    BATTERIES = 3                        # using 3 LIFEPO4 batteries
    NORMAL_VOLTAGE = 3.2 * BATTERIES     # https://batteryfinds.com/whats-lifepo4-over-discharge-lifepo4-overcharge/
    LOW_VOLTAGE = 3 * BATTERIES
    VERY_LOW_VOLTAGE = 2.7 * BATTERIES

