
import sys 

STOP_PATTERN = "---\n"
try:
    file_name = sys.argv[1]
except IndexError:
    print("No file was given. Aborting")
    exit()

data = ""
with open(file_name, "r") as read_file:

    stop_reached = False
    for line in read_file:

        if line == STOP_PATTERN:
            stop_reached = True

        if not stop_reached:
            data += line.replace("[x]", "[ ]")
        else:
            data += line

with open(file_name, "w") as write_file:

    write_file.write(data)




