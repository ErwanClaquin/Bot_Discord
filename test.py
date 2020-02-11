voteCount = {"Seb": -10, "Max": 0, "Francky": -51146461, "Pierre": 455}

playerOrder = sorted(voteCount.items(), key=lambda x: x[1], reverse=True)

print(playerOrder)