e = 0
for i in range(4):
    for j in range(4):
        e += 1
        print("i", i, "j", j)
        if j >= 2:
            break
        print("e", e)
