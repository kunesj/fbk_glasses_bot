# fbk_glasses_bot

Reddit bot for automatic Fubuki copypasta.


## Setup

Following instructions are for `Raspbian GNU/Linux 10 (buster)`, but they should be very similar for any other Debian/Ubuntu based OS.

### Install dependencies

```shell
python3.9 -m pip install -U -r requirements.txt
```

### Create config file

Create `config.json` file with your API credentials and other configuration.

```json
{
    "author": "YOUR_USER_NAME",
    "subreddits": ["hololive", "hololewd", "test"],
    "client_id": "***********",
    "client_secret": "***********",
    "username": "fbk_glasses_bot",
    "password": "***********"
}
```

### Check if the bot works

```shell
python3.9 fbk_glasses_bot.py
```

### Create service (Optional)

To automatically start the bot as a system service, create a new file `/etc/systemd/system/fbk_glasses_bot.service`. Replace `YOUR_USER_NAME` with your username, and check that the working directory is correct.

```text
[Service]
WorkingDirectory=/home/YOUR_USER_NAME/fbk_glasses_bot
ExecStart=/usr/local/bin/python3.9 fbk_glasses_bot.py
Restart=always
User=YOUR_USER_NAME
Group=YOUR_USER_NAME

[Install]
WantedBy=multi-user.target
```

Start the service and make it automatically start at boot.

```shell
sudo systemctl daemon-reload
sudo systemctl start fbk_glasses_bot
sudo systemctl enable fbk_glasses_bot
```

You can check status and logs with these commands.

```shell
sudo systemctl status fbk_glasses_bot
sudo journalctl -u fbk_glasses_bot
```


## Development

Configure pre-commit.

```shell
python3.9 -m pip --no-cache-dir install pre-commit
pre-commit install
```
