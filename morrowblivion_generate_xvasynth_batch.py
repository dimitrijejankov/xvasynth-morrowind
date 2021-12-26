import csv

# where should xvasynth store the wav files
out = "D:\\mw_data\\sound\\voice\\morrowind_ob.esm\\imperial\\%s\\%s.wav"

# maps race and gender to a xvasynth
mapping = {
    ("argonian", "female"): ("skyrim", "sk_femaleargonian"),  # hifi
    ("argonian", "male"): ("oblivion", "ob_maleargskhaj"),  # hifi
    ("breton", "female"): ("skyrim", "sk_femaleeventoned"),  # hifi
    ("breton", "male"): ("skyrim", "sk_malecommoner"),  # hifi
    ("darkelf", "female"): ("skyrim", "sk_femaledarkelf"),  # hifi
    ("darkelf", "male"): ("oblivion", "ob_malealtmer_bosmer_dunmer_gsaint"),  # hifi
    ("highelf", "female"): ("skyrim", "sk_femaledarkelf"),  # hifi
    ("highelf", "male"): ("oblivion", "ob_malealtmer_bosmer_dunmer_gsaint"),  # hifi
    ("imperial", "male"): ("skyrim", "sk_malecommoner"),  # hifi
    ("imperial", "female"): ("skyrim", "sk_femaleeventoned"),  # hifi
    ("khajiit", "female"): ("skyrim", "sk_femaleargonian"),  # hifi
    ("khajiit", "male"): ("oblivion", "ob_maleargskhaj"),  # hifi
    ("nord", "male"): ("oblivion", "ob_malenord"),  # hifi
    ("nord", "female"): ("skyrim", "sk_femalenord"),
    ("orc", "male"): ("skyrim", "sk_maleorc"),  # hifi
    ("orc", "female"): ("skyrim", "sk_femaleorc"),  # hifi
    ("redguard", "male"): ("oblivion", "ob_maleredguard"),  # hifi
    ("redguard", "female"): ("skyrim", "sk_femalecommoner"),  # hifi maybe bad choice
    ("woodelf", "female"): ("skyrim", "sk_femaledarkelf"),  # hifi
    ("woodelf", "male"): ("oblivion", "ob_malealtmer_bosmer_dunmer_gsaint"),  # hifi
}

# maps race and gender to a xvasynth to races I don't really have an good voice for
mapping_unsure = {

    # these are just silly assigments to have something...
    ("daedra", "female"): ("skyrim", "sk_femaledarkelf"),  # hifi
    ("daedra", "male"): ("oblivion", "ob_malealtmer_bosmer_dunmer_gsaint"),  # hifi
    ("riekling", "male"): ("skyrim", "sk_femaleargonian"),  # hifi
    ("draugr", "male"): ("oblivion", "ob_malenord"),  # hifi
    ("dwemer", "male"): ("skyrim", "sk_malecommoner"),  # hifi
    ("ghost", "male"): ("skyrim", "sk_malecommoner"),  # hifi
    ("god", "female"): ("skyrim", "sk_femaledarkelf"),  # hifi
    ("god", "male"): ("skyrim", "sk_maledarkelfcynical"),  # hifi
    ("dagoth", "male"): ("skyrim", "sk_maledarkelfcynical"),  # hifi
}

npc_unknown_dialogue = []
npc_dialogue_data = {}
duplicate_npc_lines = 0
with open("processed/mw_npc_dialogue.csv", encoding="UTF-16") as file:
    lines = file.readlines()

    for line in lines:
        try:
            split = line.split("|")
            identifier = (split[2].split("_")[2] + "_" + split[2].split("_")[3]).strip()
            if identifier in npc_dialogue_data.keys():
                duplicate_npc_lines += 1
            else:
                # race,   gender,   filename
                npc_dialogue_data[identifier] = (split[0], split[1], split[2].lower().strip())
        except:

            # these will be lines that do not have an identifier
            npc_unknown_dialogue.append(line)

# there should not be any duplicate line
assert (duplicate_npc_lines == 0)

npc_lines = []
generic_lines = []
with open("processed/mw_processed_lines.txt") as file:
    lines = file.readlines()
    for l in lines:
        splits = l.split("\t")
        text = splits[4]
        i = "00" + splits[0].split(":")[1].strip()[2:] + "_" + str(int(splits[3]) + 1)
        i = i.lower()

        if i not in npc_dialogue_data.keys():

            # this is most likely a generic line
            file_name = (splits[1] + "_" + splits[2] + "_" + i).lower()
            generic_lines.append((file_name, text))

        else:

            # since this is an npc line get info about race and gender
            race, gender, npc_data_file_name = npc_dialogue_data[i]
            exported_data_file_name = (splits[1] + "_" + splits[2] + "_" + i).lower()

            # this is a sanity check to make sure the data is consistent
            assert (npc_data_file_name == exported_data_file_name)

            # make sure that the race is known before adding it
            file_name = npc_data_file_name.strip()
            if race == "unknown":
                generic_lines.append((file_name, text))
            else:
                npc_lines.append((file_name, text, race, gender))

with open("output/mw_known_batch_gen.csv", "w", newline='\n') as file:
    csv_writer = csv.writer(file, delimiter=',', quotechar='"')
    csv_writer.writerow(["game_id", "voice_id", "text", "vocoder", "out_path", "pacing"])
    for line in npc_lines:

        file, text, race, gender = line
        if (race, gender) not in mapping.keys():
            continue

        game, voice = mapping[(race, gender)]
        gender = gender[0]

        csv_writer.writerow([game, voice, text.replace("\n", ""), "hifi", out % (gender, file.lower()), 1])

# for each generic line generate one for imperial male and female
with open("output/mw_unknown_batch_gen.csv", "w", newline='\n') as file:
    csv_writer = csv.writer(file, delimiter=',', quotechar='"')
    csv_writer.writerow(["game_id", "voice_id", "text", "vocoder", "out_path", "pacing"])

    for line in npc_lines:

        file, text, race, gender = line
        if (race, gender) not in mapping_unsure.keys():
            continue

        game, voice = mapping_unsure[(race, gender)]
        gender = gender[0]

        csv_writer.writerow([game, voice, text.replace("\n", ""), "hifi", out % (gender, file.lower()), 1])

    for line in generic_lines:
        file, text = line
        game_m, voice_m = mapping[("imperial", "male")]
        csv_writer.writerow([game_m, voice_m, text.replace("\n", ""), "hifi", out % ('m', file.lower()), 1])

        game_f, voice_f = mapping[("imperial", "female")]
        csv_writer.writerow([game_f, voice_f, text.replace("\n", ""), "hifi", out % ('f', file.lower()), 1])

print("unidentified npc lines %s" % len(npc_unknown_dialogue))
print("generic lines %s" % len(generic_lines))
print("npc lines %s" % len(npc_lines))
