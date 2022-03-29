# headsetcontrol_notify
Simple python script wrapper for checking the battery level using headsetcontrol and sending a notification when low

## Instructions

* Make sure to install [HeadsetControl](https://github.com/Sapd/HeadsetControl) and make sure it can be run without root access
* Change the LOW_BATTERY_THRESHOLD variable to set the battery percentage after which the script sends a notification(default is 20)
* Call the script
* Optionally schedule a task and call the script at a given interval
