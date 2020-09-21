import csv


def parse_dataset(filename):
    # init
    maven_github = {}

    # open
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        i = 0
        for row in csv_reader:
            if i == 0:
                i += 1
                pass
            else:
                # d
                name = row[1].split("/")

                # type check
                if len(name) > 1:
                    maven_github[name[-1]] = (row[2], row[3])
                else:
                    maven_github[name[0]] = (row[2], row[3])

    # return
    return maven_github


if __name__ == "__main__":
    d = parse_dataset("dataset.csv")
    for item in d:
        print(item, d[item])
