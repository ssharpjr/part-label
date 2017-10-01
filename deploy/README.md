# Raspberry Pi 3 SBC Setup


## Raspberry Pi Initial Configuration
##### Raspi-Config *(Option 1)*
Using a Raspberry Pi3 running Raspian.
```shell
sudo raspi-config
```

Perform the following steps:
1. Expand Filesystem
2. Change User Password
3. International Options
  a. Change locale to en_US.UTF-8 UTF-8.
  b. Change Timezone to US/Eastern.
  c. Change Keyboard Layout to 104-Key US Generic
4. Advanced Options
  a. Set Hostname
  b. Enable SSH
  c. Enable I2C
5. Reboot


##### Console Only *(Option 2)*
__Set Locale to US__
```shell
sudo locale-gen en_US.UTF-8
sudo update-locale
```

__Set Keyboard Map__
```shell
sudo echo XKBMODEL="pc104" > /etc/default/keyboard
sudo echo XKBLAYOUT="us" > /etc/default/keyboard
```
__Set Time Zone__
```shell
sudo echo US\Eastern > /etc/timezone
```

__Change Pi User Password__
```shell
echo "pi:PASSWORD" | sudo chpasswd
```

__Set Hostname__

*Whatever hostname is needed*
```shell
NEWHOSTNAME="NEWHOSTNAME"
sudo sed -i 's/127\.0\.1\.1\traspberrypi/127\.0\.1\.1\t'"$NEWHOSTNAME"'/g' \
/etc/hosts
echo $NEWHOSTNAME | sudo tee /etc/hostname > /dev/null
HOSTNAME=$NEWHOSTNAME
sudo /etc/init.d/hostname.sh
```

__Set AutoLogin__
```shell
sudo sed -i 's/ExecStart=-\/sbin\/agetty --noclear \%I \$TERM/ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM/g' \
/etc/systemd/system/autologin@.service
```



##### Setup Wireless Networking
Edit wpa_supplicant.conf.
```shell
sudo nano /etc/wpa_supplicant_wpa_supplicant.conf
```

Add the following to the end of this file:
```shell
network={
ssid="TPINET"
psk="SUPERSECRETKEY"
}
```
Reboot


## Software Removal
##### Uninstall unnecessary packages and update all packages
```shell
sudo apt-get remove --purge wolfram-engine libreoffice* scratch minecraft-pi sonic-pi dillo gpicview \
oracle-java8-jdk openjdk-7-jre oracle-java7-jdk openjdk-8-jre vim-tiny -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y
sudo apt-get autoclean
sync
```

## Software Installation
##### Install the necessary packages
```shell
sudo apt-get update
sudo apt-get install -y vim build-essential python3-dev python3-smbus \
python3-pip git rpi-update python3-rpi.gpio i2c-tools virtualenv cups
```

##### Setup VIM
Setup Dot File *(optional)*
```shell
git clone https://github.com/ssharpjr/dotfiles.git
cd dotfiles
cp vimrc.rpi /home/pi/.vimrc
./install_vundle.sh
```

##### Clone Repositories
Clone the Part-Label Repo
```shell
git clone https://github.com/ssharpjr/part-label.git
```

##### Create Virtual Environment
```shell
cd part-label
virtualenv env
source env/bin/activate
```

##### Install pip software
```shell
sudo pip3 install -r requirements.txt
```

##### Create Maintenance User Account
```shell
sudo adduser USERNAME
sudo usermod -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,\
     netdev,spi,i2c,gpio -a USERNAME
```

##### Setup Autologin
Create a systemd startup file
```shell
sudo vi /etc/systemd/system/getty@tty1.service.d/autologin.conf
```

Enter the following:
```shell
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pi --noclear %I 38400 linux
```

Start the service
```shell
sudo systemctl enable getty@tty1.service
```

##### Setup AutoStart Script
Edit the .bashrc for pi
```shell
vi /home/pi/.bashrc
```

Enter the following at the end of the file:
```shell
# Run Part Labeler
cd part-label
python3 print_label.py
```

##### Create place holder files
```shell
touch /tmp/date_file.txt
touch /tmp/sn_file.txt
touch /home/pi/part-label/log/serial_numbers.log
```


##### Setup ZLP Printer
__TODO:__
```shell

```


##### Docker?
*Looking into this  :)*