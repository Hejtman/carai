class Config:
    """ Storage for an external environment configurations / dependencies. """
    RC_HTTP_SERVER = ('192.168.10.1', 81)           # main wlan0
    LOCAL_RC_HTTP_SERVER = ('127.0.0.1', 81)        # fake for development outside PI
    ETH0_RC_HTTP_SERVER = ('192.168.1.238', 81)     # eth0 for development via wire

    BATTERIES = 3                        # using 3 LIFEPO4 batteries
    NORMAL_VOLTAGE = 3.2 * BATTERIES     # https://batteryfinds.com/whats-lifepo4-over-discharge-lifepo4-overcharge/
    LOW_VOLTAGE = 3 * BATTERIES
    VERY_LOW_VOLTAGE = 2.7 * BATTERIES
