import pickle

status = {
	'character': 'Warrior',
	'level' : 3,
	'score': 11000,
	'time_play': 0,
	'die' : 0,
	'grenades': 7,
	'health': 100000
}

# Ghi dict vào file byte
with open("./Data/save_game", "wb") as f:
    pickle.dump(status, f)

