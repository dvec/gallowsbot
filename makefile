WGET=/usr/bin/wget
DB_URL=https://raw.githubusercontent.com/matveyvarg/Name-Generator/master/word_rus.txt

run:
        PYTHONPATH=$(shell pwd) python3 gallowsbot/main.py

load:
	$(WGET) $(DB_URL)
