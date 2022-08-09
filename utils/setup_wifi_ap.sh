#!/bin/sh

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install hostapd
sudo apt-get install dnsmasq
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

file="/etc/dhcpcd.conf"
echo "modifying ${file}"
sudo cat <<EOF >> "${file}"
interface wlan1
static ip_address=192.168.0.10/24
denyinterfaces eth0
denyinterfaces wlan1
EOF

file="/etc/dnsmasq.conf"
echo "modifying ${file}"
[[ -f ${file} ]] || sudo mv ${file} ${file}.orig
sudo cat <<EOF >> "${file}"
interface=wlan1
dhcp-range=192.168.0.11,192.168.0.30,255.255.255.0,240h
EOF

file="/etc/hostapd/hostapd.conf"
echo "modifying ${file}"
sudo cat <<EOF >> "${file}"
interface=wlan1
bridge=br0
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=NETWORK              # !!!
wpa_passphrase=PASSWORD   # !!!
EOF

file="/etc/default/hostapd"
echo "modifying ${file}"
sudo cat <<EOF >> "${file}"
DAEMON_CONF="/etc/hostapd/hostapd.conf"
EOF

file="/etc/sysctl.conf"
echo "modifying ${file}"
sudo cat <<EOF >> "${file}"
net.ipv4.ip_forward=1
EOF

sudo iptables -t nat -A POSTROUTING -o eth0 --dport 53 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o eth0 --dport 443 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
file="/etc/rc.local"
echo "modifying ${file}"
sudo cat <<EOF >> "${file}"
iptables-restore < /etc/iptables.ipv4.nat  # !!!above the line exit 0
EOF

sudo apt-get install bridge-utils
sudo brctl addbr br0
sudo brctl addif br0 eth0
file="/etc/network/interfaces"
echo "modifying ${file}"
sudo cat <<EOF >> "${file}"
auto br0
iface br0 inet manual
bridge_ports eth0 wlan1
EOF

echo "FIX! edited files above and reboot."
