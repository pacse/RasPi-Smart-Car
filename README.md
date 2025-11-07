# RasPi-Smart-Car
A customixed version built of Freenove's base to add controller support and etc

## How to configure a pi
```bash
git clone https://github.com/pacse/RasPi-Smart-Car.git

sudo raspi-config # enable i2c in interface options

sudo apt-get install i2c-tools
sudo apt-get install python3-smbus

i2cdetect -y 1 # ensure you see 40 & 48

```

## Connect to bluetooth controller
NOTE: Assume controller address: F4:6A:D7:E0:3E:BC

```bash
sudo bluetoothctl

connect F4:6A:D7:E0:3E:BC
```

Code
├── __init__.py
├── config.py          # Config & variables
├── joytick_handler.py # Interface with Xbox joystick
├── motors
│   ├── __init__.py
│   ├── core.py        # Core Motor control
│   ├── car.py         # Expand Motor control
│   └── controller.py  # Add controller support
└── tests
    ├── __init__.py
    └── motors.py      # Test motor control
test.py                # Run tests
main.py                # Bring it all together


# Original repo
https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi
