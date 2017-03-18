# print-google-events

## Installation:

1. Clone this repository
2. Create a google-calendar api:  
[see the quickstart tutorial step 1](https://developers.google.com/google-apps/calendar/quickstart/python) 
save the credentials.json in the projects root directory

3. Print your next 4-days schedule and Google Keep reminders:

in the 'main.py'

replace the strings 'YOUR_MAIL', 'YOURPASSWORD' in line 15 with your user credentials
replace the string 'PRINTER' with your printers name (find it via lpstat -a) 
run main.py

## Run the software every 4 days:

use e.g. [Cron](https://help.ubuntu.com/community/CronHowto) with the 
line 0 0 */4 \* \*  /path/to/the/main.py  -> runs at 00:00 every four days.

