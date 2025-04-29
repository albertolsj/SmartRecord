Complete Procedure to Set Up the OPC UA Server on Raspberry Pi

This guide will install, configure, and run the OPC UA server on your Raspberry Pi,
ensuring automatic startup and daily reboot at 12:00 PM.

Step 1: Place the Script in the Documents Folder

Run the following command to move the script to the correct location:

mv ~/Downloads/main.py ~/Documents/

Or, if the script is already in another location, adjust the command accordingly.

Step 2: Install Required Libraries (Without Virtual Environment)

Since we are not using a virtual environment, install the required libraries globally:

sudo pip install opcua psutil RPi.GPIO

If pip gives a "externally managed environment" error, run:

sudo pip install opcua psutil RPi.GPIO sdnotify --break-system-packages

Verify that the libraries are installed correctly:

python3 -c "import opcua, psutil, RPi.GPIO; print('Libraries installed successfully!')"

Step 3: Create a Systemd Service to Auto-Start the Script

We need to register the script as a systemd service so that it runs automatically on
boot.

1️⃣ Create the service file:

sudo nano /etc/systemd/system/opcua_server.service

2️⃣ Add the following content:

[Unit]
Description=OPC UA Server for Raspberry Pi
After=network.target

[Service]
Type=notify
ExecStart=/usr/bin/python3 /home/bicmes/Documents/main.py
WorkingDirectory=/home/bicmes/Documents
Restart=always
RestartSec=5s
User=bicmes
WatchdogSec=10s
NotifyAccess=all
StandardOutput=append:/var/log/opcua_server.log
StandardError=append:/var/log/opcua_server.log

[Install]
WantedBy=multi-user.target

3️⃣ Save and exit:

•Press CTRL + X
•Press Y (Yes)
•Press Enter

4️⃣ Reload systemd to apply the changes:

sudo systemctl daemon-reload

5️⃣ Enable the service to start automatically on boot:

sudo systemctl enable opcua_server.service

6️⃣ Start the service manually (for testing):

sudo systemctl start opcua_server.service

7️⃣ Check if the service is running correctly:

sudo systemctl status opcua_server.service

If you see "Active (running)", everything is working fine.

Step 4: Implement Auto-Restart Every Day at 12:00 PM

To restart the Raspberry Pi daily at 12:00 PM, we will use a cron job.

1️⃣ Open the crontab editor:

sudo crontab -e

2️⃣ Go to the bottom and add the following line:

0 12 * * * /sbin/shutdown -r now

Explanation:

•0 12 * * * → Runs at 12:00 PM every day.

•/sbin/shutdown -r now → Reboots the Raspberry Pi.

3️⃣ Save and exit:

•
Press CTRL + X•Press Y (Yes)
•Press Enter

4️⃣ Verify if the cron job was added:

sudo crontab -l

You should see:

0 12 * * * /sbin/shutdown -r now

Step 5: Verify Everything is Working

Run these final checks:

Check if the service is running:

sudo systemctl status opcua_server.service

Check if the cron job is correctly scheduled:

sudo crontab -l

Test manual reboot:

sudo shutdown -r now

After the reboot, check if the OPC UA server starts automatically:

sudo systemctl status opcua_server.service

Final Result

OPC UA server script installed and running on boot

Libraries installed globally

Service registered in systemd for automatic execution

Daily Raspberry Pi reboot scheduled at 12:00 PM

Everything is now running smoothly!

If you need any adjustments, let me know!


