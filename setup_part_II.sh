DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ticks="clock_ticks.py"
sync="time_sync_ntp.py"
tele="telegraphic.py"
ticks_s="clock_ticks.service"
sync_s="time_sync_ntp.service"
tele_s="telegraphic.service"
rr="/opt/radio_reloj"
boot_services="/etc/systemd/system"
pulse_daemon="/etc/pulse/daemon.conf"
pulse_default="/etc/pulse/default.pa"

echo "********************************"
echo "*       PulseAudio Config      *"
echo "********************************"
if [[ -e "$pulse_daemon" ]]
then
    sudo sed -i -e 's/; high-priority = yes/ high-priority = yes/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; nice-level = -11/ nice-level = -20/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; realtime-scheduling = yes/ realtime-scheduling = yes/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; realtime-priority = 5/ realtime-priority = 9/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; flat-volumes = yes/ flat-volumes = no/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; default-sample-format = s16le/ default-sample-format = s16le/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; default-sample-rate = 44100/ default-sample-rate = 44100/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; default-sample-channels = 2/ default-sample-channels = 1/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/ default-fragment-size-msec = 15/; default-fragment-size-msec = 15/g' /etc/pulse/daemon.conf
    
    # WARNING: The fragments number and size mili seconds, depends on deactivating
    # the time scheduler, try this if you ear static in the audio, this depends on your
    # system architecture and hardware (recommended: study a lot first, know your system)
    # buffer_size: bs
    # fragment_size: fs
    # sample rate: sr
    # bit depth: bp
    # number channels: nc
    # bits per sec: bps
    # default-fragments: df
    # default-fragments-size-msec: fsm
    
    # On this example tested for Rpi 3B: sr= 44100 bp= 16 nc= 1(mono)
    # bps= sr*bp*nc
    # df= bs/fs
    # fsm= fs/bps
    # Use the next two commands to get the values of buffer_size and fragment_size:
    #     pulseaudio -k
    #     LANG=C timeout --foreground -k 10 -s kill 10 pulseaudio -vvvv 2>&1 | grep device.buffering -B 10
    # The presents are calculated for a Rpi 3B
    sudo sed -i -e 's/; default-fragments = 4/ default-fragments = 2/g' /etc/pulse/daemon.conf
    sudo sed -i -e 's/; default-fragment-size-msec = 15/ default-fragment-size-msec = 5/g' /etc/pulse/daemon.conf
else
    echo "File Not Found: $pulse_daemon"
fi

if [[ -e "$pulse_default" ]]
then    
    # Activate Glitch Free "Developers Mode" by setting tsched=1 or delete it
    # sudo sed -i -e 's/load-module module-udev-detect tsched=0/load-module module-udev-detect/g' /etc/pulse/default.pa
    sudo sed -i -e 's/load-module module-suspend-on-idle/#load-module module-suspend-on-idle/g' /etc/pulse/default.pa
    sudo sed -i -e 's/load-module module-suspend-on-idle/#load-module module-suspend-on-idle/g' /etc/pulse/system.pa
else
    echo "File Not Found: $pulse_default"
fi

echo "********************************"
echo "*       ALSA Group Users       *"
echo "********************************"
sudo adduser pulse audio
sudo adduser pi audio
sudo adduser root audio

echo "********************************"
echo "*       SDL2 Env Var Set       *"
echo "********************************"
echo 'export SDL_AUDIODRIVER=pulseaudio' >> ~/.bashrc
source ~/.bashrc

echo "********************************"
echo "*      Python3.7 Modules       *"
echo "********************************"
sudo pip3 install ntplib 
pip3 install pygame
pip3 install --upgrade --force-reinstall pygame

echo "********************************"
echo "*       Dirs and Sources       *"
echo "********************************"
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

echo "****************************************************************************"
echo "*                          Services are Waking-Up                          *"
echo "*  Warning: Remember change Raspberry Boot/Autologin to Console Autologin  *"
echo "****************************************************************************"
sudo systemctl daemon-reload
sudo systemctl enable $ticks_s
sudo systemctl enable $sync_s
sudo systemctl enable $tele_s

sudo systemctl start $ticks_s
sudo systemctl start $sync_s
sudo systemctl start $tele_s

echo "********************************"
echo "*           JOB DONE           *"
echo "********************************"
