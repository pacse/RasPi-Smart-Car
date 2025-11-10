# RasPi-Smart-Car
A customixed version of Freenove's base to add controller support and more eventually.

## How to configure a pi
```bash
cd /path/to/desired/directory

git clone https://github.com/pacse/RasPi-Smart-Car.git

cd RasPi-Smart-Car

pip install -r requirements.txt
```

## Connect to bluetooth controller
NOTE: Assume controller address: F4:6A:D7:E0:3E:BC

```bash
sudo bluetoothctl

# To find controller address
scan on
# Find Xbox Controller

pair F4:6A:D7:E0:3E:BC     # or correct address
trust F4:6A:D7:E0:3E:BC    # or correct address
connect F4:6A:D7:E0:3E:BC  # or correct address

exit # leave bluetooth ctl
```

## File Structure
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
```

# Original repo
https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi
