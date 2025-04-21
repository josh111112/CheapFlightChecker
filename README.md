# CheapFlightChecker

## Description

Flights can be expensive, not to worry! This program will let you know when the cheapest flights are available according to your needs.

Some basic info:
    flights are typically cheapest when arriving on a tuesday and leaving on a thursday

### Requirements
- python
- serpAPI (free 100 calls per month)

If you want to automate use
- launchd (mac) use cron or anacron as alternatives



### Build
1. enter the data into the config file
2. in terminal go to ~/Library/LaunchAgents/ 
3. create .plist file example: touch flightcheckerauto.plist
4. add this and save
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string></string> <!-- to check logs make it similar to filename example: flightchecker-->
        <key>ProgramArguments</key>
        <array>
            <string>/usr/bin/python3</string> <!-- where python3 in terminal will show -->
            <string>path/oneForAll.py</string> <!-- path to python file -->
        </array>
        <key>StartInterval</key>
        <integer>190080</integer> <!-- Roughly every 2.2 days -->
        <key>RunAtLoad</key>
        <true/>
    </dict>
    </plist>
    ```
5. in terminal: launchctl load ~/Library/LaunchAgents/flightcheckerauto.plist

You're done! Now you will get automated emails on cheap flights.
Be careful with how many airport ID's you put in your config file, I am using 5 and have my automation set to run roughly every 2 days so I stay within my 100 calls per month free quota.