# painting automower

To change lengths of lines:

1. Start local host by running the server.py.
2. Go to <http://localhost:8000/userInput/>
3. Input the dimensions of your soccer field
4. Click submit

To start control mower:

1. run this anywhere in terminal: "source ~/450/devel/setup.bash"
2. run this anywhere in terminal: "sudo chmod 666 /dev/ttyACM0" (if error, check if automower is on)
3. Enter password: "kandidatarbete"
4. run this anywhere in terminal: "roslaunch am_driver_safe automower_hrp.launch"
5. Open a second terminal, run "cd ~/450/src/calculations"
6. run "source ~/450/devel/setup.bash"
7. run "rosrun am_driver main.py" (If error, run this in 450/src/hrp/am_driver/scripts: "chmod 777 main.py")

To run simulation:

1. Change trip to paint or comb

- Paint:
  - 1 Change paint_order in paint.py to desierd trip
  - 2 Change self.order = paint_order in simulate.py
- Comb and cut
  - 1 Change comb_order in comb_cut.py to desierd trip
  - 2 Change self.order = comb_cut_order in simulate.py

2. Run "cd calculations", then run "python3 simulate.py"
3. Check you simulated result in calculations/plots/plot-latest.png

To get position run this in terminal "cd 450/src/hrp/am_driver/scripts", then: "rostopic echo /pose"
To get GPS run this in termrminal: "cd 450/src/hrp/am_driver/scripts", then: "rostopic echo /GPSfix"
To see all rostopics run this in termrminal: "cd 450/src/hrp/am_driver/scripts", then: "rostopic echo /GPSfix"



SSH

1. Install vscode and the plugin ssh to vscode
2. Connect to the same wifi as the jetson nano (SSID: CASELAB, Password:CaseLocalNet)
3. Open ssh extention (bottom left green), connect to host, "ssh kandidatarbete@192.168.1.110"
4. Open 450/src

To change wifi

1. sudo nano /etc/netplan/01-network-manager-all.yaml
2. change to correct wifi, copy one of these:

network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: no
      addresses:
        - 192.168.1.110/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
      access-points:
        "CASELAB":
          password: "CaseLocalNet"

network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: no
      addresses:
        - 192.168.1.110/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
      access-points:
        "GalaxyS20":
          password: "12345678"

3. sudo netplan apply

