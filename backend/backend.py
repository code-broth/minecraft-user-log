#!/usr/bin/env python3

from mcstatus import MinecraftServer
from time import sleep
import atexit

def players():
    server = MinecraftServer.lookup("localhost")
    status = server.status()
    players = status.players
    if players.sample is None:
        return set()
    else:
        return {p.name for p in players.sample}

def save_event(username, logged_on):
    print(username, "logged", "on" if logged_on else "off")


users = players()

for p in users:
    save_event(p, True)
atexit.register(lambda: [save_event(u, False) for u in users])

while True:
    users_new = players()
    just_logged_in = users_new - users
    just_logged_off = users - users_new
    for p in just_logged_in:
        save_event(p, True)
    for p in just_logged_off:
        save_event(p, False)
    users = users_new
    sleep(10)
