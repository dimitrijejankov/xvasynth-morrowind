import re as re

mw_lines = {}
with open("dialogue_dump/morroblivion.txt") as file:

    lines = file.readlines()
    for line in lines:
        i = line.split("\t")[0] + "_" + line.split("\t")[3]
        mw_lines[i] = line

ob_lines = {}
with open("dialogue_dump/oblivion.txt") as file:

    lines = file.readlines()
    for line in lines:
        i = line.split("\t")[0] + "_" + line.split("\t")[3]
        ob_lines[i] = line

not_sure = []
out = []
for k in mw_lines.keys():

    if k not in ob_lines.keys():
        out.append(mw_lines[k])

    if k in ob_lines.keys():
        not_sure.append(mw_lines[k])


with open("processed/mw_processed_lines.txt", "w") as file:
    for line in out:

        back = line
        line = line.replace(",&sUActnQuick1;", "")
        line = line.replace(",&sUActnQuick1", "")
        line = line.replace("&sUActnQuick1;", "")
        line = line.replace("&sUActnQuick1", "")
        line = line.replace("&sUActnQuick2;", "")
        line = line.replace("&", "")

        line = re.sub(r'\[.*]', '', line)
        line = re.sub(r'\[.*', '', line)

        line = line.replace('*hic*', '')
        line = line.replace('*burp*', '')
        line = line.replace('*this path to your destiny is blocked*', '')
        line = re.sub(r'\*[Hh]iccup.?\*', '', line)
        line = re.sub(r'\*(gulp ?)+\*', '', line)
        line = re.sub(r'\*[Ss]igh.?\*', '', line)
        line = re.sub(r'\*[Yy]awn.?\*', '', line)
        line = re.sub(r'\*[Bb]urp.?\*', '', line)
        line = re.sub(r'\*[Cc]ough.?\*', '', line)
        line = re.sub(r'\*[Ss]ob.?\*', '', line)
        line = re.sub(r'\*[Gg]asp.?\*', '', line)
        line = re.sub(r'\*[zZ]+.?\*', '', line)
        line = re.sub(r'\*', '', line)

        m = re.search(r'\t\d\t(.*])', line)
        if m is not None:
            line = line.replace(m.group(1), "")

        # remove extra space
        line = re.sub(r'  +', ' ', line)
        line = re.sub(r'\t ', '\t', line)
        split = line.split("\t")

        if split[4].strip() == "":
            continue

        file.write(line)
