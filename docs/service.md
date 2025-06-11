# Service

This file describes how to make MuddyBot a systemd service.

## User

So we will have to have a dedicated user for muddybot or you can use the default it is up to you.

```bash
useradd muddybot # Add muddybot user
passwd muddybot # Add password for muddybot
```

You will need the user and group for the user you want to use whether that be a dedicated user or the default user.

```bash
id muddybot # Could also be a dedicated user
```

Take a note of one of the names under the group field, you will need that for later

## Installing MuddyBot

You will need muddybot installed for whatever user you use for MuddyBot. So if the user is ***abc123*** MuddyBut will have to be installed using that user.

To install download the one of the `.whl` files from the github repository.

```bash
curl -o muddybot.whl https://github.com/TheCrunching/MuddyBot/raw/refs/tags/v1.0.0/dist/muddybot-1.0.0-py3-none-any.whl # Download the whl file
pip install .muddybot.whl # Install with pip
```

The first command downloads the wheel file in this case version 1.0.0. The second command installs MuddyBot using the downloaded wheel file.

## Service file creation

In order to make MuddyBot a service we first have to make a service file for it. We can do this by running these commands.

```bash
sudo touch /etc/systemd/system/muddybot.service # Create the service file
sudo chmod 664 /etc/systemd/system/muddybot.service # Set the appropriate permissions
```

The first command makes our config file and the second command sets the right permissions on it.

Next we have to edit it so systemd knows how to run our service.

```bash
sudo nano /etc/systemd/system/muddybot.service # Open the file with nano
```

Once the file is open we will put the following config in it.

For ExecStart you will have to put the location of your MuddyBot executable which can be found with `which muddybot`.

```ini
[Unit]
Description=A twitch bot.

[Service]
ExecStart=/usr/bin/python3 # Put your muddybot location here
User=# The user muddybot is installed as
Group=# The group the user is a part of

[Install]
WantedBy=multi-user.target
```

My system file looked like this.

```ini
[Unit]
Description=A twitch bot.

[Service]
ExecStart=/usr/bin/python3 /home/muddybot/.local/bin/muddybot
User=muddybot
Group=muddybot

[Install]
WantedBy=multi-user.target
```

## Service creation

After we have completed editing the file we need to reload systemd's configuration.

```bash
sudo systemctl daemon-reload # Reload the config
```

You can start it with `sudo systemctl start muddybot.service` and you can have it start on boot with `sudo systemctl enable muddybot.service`. You can also check the services status and logs with `sudo systemctl status muddybot.service`.
