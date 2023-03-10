# painting_automower

To change lengths of lines:

1. Start local host by running the server.py.
2. Go to <http://localhost:8000/userInput/>
3. Input the dimensions of your soccer field
4. Click submit

To start control mower with asdw:
1. run this anywhere in terminal: source ~/450/devel/setup.bash 
2. run this anywhere in terminal: sudo chmod 666 /dev/ttyACM0 (if error, check if automower is on) 
3. Enter password: "kandidatarbete"
4. run this anywhere in terminal: roslaunch am_driver_safe automower_hrp.launch
5. Open a secound terminal and run this anywhere in terminal: source ~/450/devel/setup.bash
6. run this anywhere in terminal: rosrun am_driver hrp_teleop.py (If error, run this in 450/src/hrp/am_driver/scripts: chmod 777 hrp_teleop.py)

To get position run this in terminal at 450/src/hrp/am_driver_scripts: rostopic echo /pose 