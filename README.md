# fbk_glasses_bot

Reddit bot for automatic Fubuki copypasta.


## Setup

Following instructions are for RaspberryPi, but they should be very similar for any other Debian/Ubuntu based OS.

### Manually install Python3.9 (Optional)

If you want to run this bot on RaspberryPi (stretch), you will have to manually install Python. The newest version in repos is Python3.5, but this bot is made for Python 3.9+.

```shell
sudo apt install build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev libnss3-dev libdb5.3-dev libncursesw5-dev wget
wget https://www.python.org/ftp/python/3.9.17/Python-3.9.17.tgz
tar -xzvf Python-3.9.17.tgz
cd Python-3.9.17/
# ignore the unsupported platform warning
./configure --enable-optimizations
# this can take a few hours
sudo make altinstall
```

Test that it works:

```shell
python3.9 -c 'print("works")'
```

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
