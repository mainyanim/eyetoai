import json
import random

def get_dic_from_two_lists(keys, values):
    return { keys[i] : values[i] for i in range(len(keys)) }

def report(items,infile):
    data_list = []
    for i in range(items):
        with open(infile) as f:
            contents_of_file = f.read()
            lines = contents_of_file.splitlines()
            line_number = random.randrange(0, len(lines))
            person_name = lines[line_number]
        dict_keys = ['name', 'age', 'person name']
        dict_values = ['n', 'a', person_name]
        data = get_dic_from_two_lists(dict_keys, dict_values)
        data_list.append(data)

    reports = json.dumps(data_list)
    print(reports)

def main():
    report(5, "first-names.txt")

main()
