#!/bin/bash
set -ef

DOCKER_SRC="/opt/fbk_glasses_bot"

cd "$DOCKER_SRC" && python fbk_glasses_bot.py
