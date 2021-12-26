import csv
from glob import glob

npc_meta = glob('npc_data/*')

npc_race_gender = {}
for f in npc_meta:

    tmp = str(f).split("\\")[-1][0:-4]
    race, gender = tmp.split("_")

    with open(f) as file:

        lines = file.readlines()
        for line in lines:
            name = line.strip()
            npc_race_gender[name] = (race, gender)

out = open("processed/mw_npc_dialogue.csv", 'w', encoding="UTF-16")

npcs = glob('npc_dialogue_dump/*')
num_npcs = 0
num_lines = 0
for f in npcs:
    npc_name = str(f).split("\\")[-1][0:-4]

    race = ""
    genders = []
    if npc_name in npc_race_gender.keys():
        race, gender = npc_race_gender[npc_name]
        genders = [gender]
    elif npc_name == "Guard":
        genders = ["male"]
        race = "darkelf"
    elif npc_name == "Redoran Guard":
        genders = ["male"]
        race = "darkelf"
    elif npc_name == "Imperial Guard":
        genders = ["male"]
        race = "imperial"
    elif npc_name not in npc_race_gender.keys():
        num_npcs += 1
        print(npc_name)
        continue

    for gender in genders:
        with open(f, encoding="UTF-16") as file:
            _ = file.readline()
            spamreader = csv.reader(file, delimiter=',', quotechar='"')
            for row in spamreader:
                out.write("%s|%s|%s\n" % (race, gender, row[-1]))

print("num_npcs : %s, num_npcs_missing : %s" % (len(npcs), num_npcs))
print("num_lines : %s" % num_lines)

out.close()
