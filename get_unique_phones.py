lines = open("preprocessed_data/GlobalPhoneGerman/train.txt", "r").readlines()
phones = set()
for line in lines:
    t = line.split("{")[1].split("}")[0].split()
    phones.update(set(t))
print(phones)