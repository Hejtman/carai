# CarAI
AI powered RC for SunFounder PiCar-X

Quick Links:
- [PiCar-X AI powered RC](#picar-x-ai-powered-rc)
  - [SW](#sw)
  - [HW](#hw)
  - [setup](#setup)
  - [Usage](#usage)
  - [Contribute](#contribute)
  - [Contact me](#contact-us)

## SW
Python3.10+, multi-thread, HTML, CSS, JSCRIPT hobby project on PI OS.
* Sensor > Control > Actuator
* RC > Control2 > Actuator
* Sensor < Control1,2 > Actuator


## HW
[PiCar-X](https://www.sunfounder.com/collections/main-products/products/picar-x) is [SunFounder's](https://www.sunfounder.com) car that is build around the [Raspberry Pi](https://www.raspberrypi.org).

## Setup
FIXME
* PI OS
* WiFi AP+STA
  * alien/ap_sta_config.sh --ap <ap_ssid> <ap_password> --client <client_password> <client_password> --country <iso_3166_country_code>
* setup.sh
    * python3.10
    * requirements.txt
    * /etc/rc.local

## Usage
FIXME: Before running the car, stop ezblock service

```python
sudo service ezblock stop
cd carai
sudo python3 main.py
```

Stop running the CarAI by using <kbd>Ctrl</kbd>+<kbd>C</kbd>

## Contribute
Branch, improve, pull request.
Feel free to be apart.

## Contact me
E-mail:
    hejtman2@@centrum..cz
