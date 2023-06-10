# fbk_glasses_bot

Reddit bot for automatic Fubuki copypasta.


## Setup

### Install dependencies

```shell
python3.11 -m pip install -U -r requirements.txt
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
python3.11 fbk_glasses_bot.py
```


## Development

Configure pre-commit.

```shell
python3.11 -m pip --no-cache-dir install pre-commit
pre-commit install
```
