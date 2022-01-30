from os.path import exists


path_to_file = input()

if not exists(path_to_file):
    exit()

with open(path_to_file, "r") as file:
    code = [x.strip("\n") for x in file.readlines()]


for line in range(len(code)):
    if len(code[line]) > 49:
        print(f"Line {line + 1}: S001 Too long. Please make sure that each line is no longer than 49 characters")
