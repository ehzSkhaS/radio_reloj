# Radio Reloj

## Linux requirements:
**`sudo pip3 install ntplib`**<br>
**`sudo pip3 install --upgrade --force-reinstall pygame`**<br>
**`sudo apt-get update`**<br>
**`sudo apt-get install libsdl2-mixer-2.0-0`**<br>
**`sudo apt-get install python-rpi.gpio python3-rpi.gpio`**

**`sudo mkdir /opt/radio_reloj`**

*copy:*
  >>**clock_ticks.py**<br>
  >>**time_sync_ntp.py**<br>
  >>**telegraphic.py**

*to:* 
  >>**/opt/radio_reloj**

**`sudo chmod -R 777 /opt/radio_reloj`**

**`python`** *(press tab twise)* **note:** check avaliable python envs 

*open* **clock_ticks.service:**
  >>*line 10, change: python3.6*<br> 
  >>*to: your_python_env*

*open* **time_sync_ntp.service:**
  >>*line 8, change: python3.6*<br>
  >>*to: your_python_env*

*open* **telegraphic.py:**
  >>*line 10, change: python3.6*<br>
  >>*to: your_python_env*

*copy:*
  >>**clock_ticks.service**<br>
  >>**time_sync_ntp.service**<br>
  >>**telegraphic.service**

*to:*
  >>**/etc/systemd/system**

**`sudo chmod 775 /etc/systemd/system/clock_tick.service`**<br>
**`sudo chmod 775 /etc/systemd/system/time_sync_ntp.service`**<br>
**`sudo chmod 775 /etc/systemd/system/telegraphic.service`**

**`sudo systemctl daemon-reload`**<br>
**`sudo systemctl enable clock_ticks.service`**<br>
**`sudo systemctl enable time_sync_ntp.service`**<br>
**`sudo systemctl enable telegraphic.service`**

**`sudo systemctl start clock_ticks.service`**<br>
**`sudo systemctl start time_sync_ntp.service`**<br>
**`sudo systemctl start telegraphic.service`**

**`sudo systemctl status clock_ticks.service`**<br>
**`sudo systemctl status time_sync_ntp.service`**<br>
**`sudo systemctl status telegraphic.service`**

**`sudo shutdown -h 0`**

*hardwire connect: (Button)*
  >>**pin number 1**<br>  
  >>**pin number 10**
  >>![rpi3gpio](https://github.com/ehzSkhaS/radio_reloj/blob/optimized/docs/rpi3gio.png)
  >>![schematic](https://github.com/ehzSkhaS/radio_reloj/blob/optimized/docs/schematic.png)

**DONE**

  
