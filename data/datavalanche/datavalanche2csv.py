with open("datavalanche.csv") as input_file:
    i  = 0
    for line in input_file:
        if i == 0:
            print(line)
        i += 1