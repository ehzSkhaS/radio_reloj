DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ticks="clock_ticks.py"
sync="time_sync_ntp.py"
tele="telegraphic.py"
ticks_s="clock_ticks.service"
sync_s="time_sync_ntp.service"
tele_s="telegraphic.service"
rr="/opt/radio_reloj"
boot_services="/etc/systemd/system"
reload=0

echo "********************************"
echo "*    Radio Reloj Installing    *"
echo "********************************"

if [[ -e "$boot_services/$ticks_s" ]]
then
    let reload=1
    sudo systemctl stop $ticks_s
    sudo systemctl disable $ticks_s
    sudo rm "$boot_services/$ticks_s"
    echo "********************************"
    echo "* Clock Ticks Service Removed  *"
    echo "********************************"
fi

if [[ -e "$boot_services/$sync_s" ]]
then
    let reload=1
    sudo systemctl stop $sync_s
    sudo systemctl disable $sync_s
    sudo rm "$boot_services/$sync_s"
    echo "********************************"
    echo "*  Sync Time Service Removed   *"
    echo "********************************"
fi

if [[ -e "$boot_services/$tele_s" ]]
then
    let reload=1
    sudo systemctl stop $tele_s
    sudo systemctl disable $tele_s
    sudo rm "$boot_services/$tele_s"
    echo "********************************"
    echo "* Telegraphic Service Removed  *"
    echo "********************************"
fi

if [[ $reload==1 ]]
then
    sudo systemctl daemon-reload
fi

if [[ -d "$rr" ]]
then
    sudo rm -dR $rr
    echo "********************************"
    echo "*  Old Source Folder Removed   *"
    echo "********************************"
fi

sudo apt-get update

echo "********************************"
echo "* Installing Necesary Packages *"
echo "********************************"
sudo apt-get --purge --reinstall install alsa-base alsa-utils pulseaudio
sudo apt-get install pavumeter pavucontrol paman paprefs
sudo apt-get install python3.7 libsdl2-mixer-2.0-0 python-rpi.gpio python3-rpi.gpio

echo "********************************"
echo "*          Part I End          *"
echo "*          Now Reboot          *"
echo "********************************"
