DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ticks="clock_ticks.py"
sync="time_sync_ntp.py"
tele="telegraphic.py"
ticks_s="clock_ticks.service"
sync_s="time_sync_ntp.service"
tele_s="telegraphic.service"
rr="/opt/radio_reloj"
boot_services="/etc/systemd/system"

sudo systemctl stop $ticks_s
sudo systemctl stop $sync_s
sudo systemctl stop $tele_s

sudo systemctl disable $ticks_s
sudo systemctl disable $sync_s
sudo systemctl disable $tele_s
sudo systemctl daemon-reload

sudo rm "$boot_services/$ticks_s"
sudo rm "$boot_services/$sync_s"
sudo rm "$boot_services/$tele_s"

sudo rm -dR $rr

sudo apt-get update
sudo apt-get --purge --reinstall install pulseaudio
sudo sec -i -e 's/; nice-level = -11/; nice-level = -1/g' /etc/pulse/daemon.conf
sudo sec -i -e 's/; flat-volumes = yes/; flat-volumes = no/g' /etc/pulse/daemon.conf
echo 'export SDL_AUDIODRIVER=pulseaudio' >> ~/.bashrc
source ~/.bashrc
sudo apt-get install python3.7 libsdl2-mixer-2.0-0 python-rpi.gpio python3-rpi.gpio

pip3 install ntplib pygame
pip3 install --upgrade --force-reinstall pygame

sudo mkdir $rr
sudo cp "$DIR/$ticks" $rr
sudo cp "$DIR/$sync" $rr
sudo cp "$DIR/$tele" $rr
sudo cp -R "$DIR/sounds" $rr
sudo chmod -R 775 $rr

sudo cp "$DIR/services/$ticks_s" $boot_services
sudo cp "$DIR/services/$sync_s" $boot_services
sudo cp "$DIR/services/$tele_s" $boot_services
sudo chmod 775 "$boot_services/$tick_s"
sudo chmod 775 "$boot_services/$sync_s"
sudo chmod 775 "$boot_services/$tele_s"

sudo systemctl daemon-reload
sudo systemctl enable $ticks_s
sudo systemctl enable $sync_s
sudo systemctl enable $tele_s

sudo systemctl start $ticks_s
sudo systemctl start $sync_s
sudo systemctl start $tele_s

echo "DONE"
