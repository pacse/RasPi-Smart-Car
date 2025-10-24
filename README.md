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

# Original repo
https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi
