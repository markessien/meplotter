

debug_file = "/home/mark/.chia/mainnet/log/debug.log"
file = open(debug_file, "r") 


def get_file_name(str):
    plotpos = str.find(".plot")
    return str[:plotpos+5]

files_not_found = []
files_no_pk = []

for line in file:
    err = -1
    pos = line.find(" Failed to open file ") 
    if pos > -1:
        err = 1
        file_name = get_file_name(line[pos+21:])

    pos = line.find("Looking up qualities on ") 
    if pos > -1:
        err = 2
        file_name = get_file_name(line[pos+24:])

        time_pos = line.find(file_name + " took:") + len(file_name + " took:") + 1
        time_required = float(line[time_pos:time_pos+4])


    pos1 = line.find("WARNING  Plot ") 
    pos2 = line.find("has a farmer public key that is not")
    if pos1 > -1 and pos2 > -1:
        err = 3
        file_name = get_file_name(line[pos1+14:])

    if err == 1:
        print("File not found on " + file_name)
        files_not_found.append(file_name)

    if err == 2:
        print("Slow lookup on " + file_name + " Time: " + str(time_required) + "s")
    
    if err == 3:
        print("PK not found for " + file_name)
        files_no_pk.append(file_name)


print("Files not found")
for file_name in files_not_found:
    print("rm " + file_name)

print("\n\nFiles without pk")
for file_name in files_no_pk:
    print("rm " + file_name)
