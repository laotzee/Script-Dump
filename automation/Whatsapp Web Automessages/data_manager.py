import csv

COUNTER_NAME = "counter.csv"
DATA_NAME = "data.csv"

def read_counter(file_name=COUNTER_NAME):
    """Returns the counter contained in file_name. Returns None is file is not properly formatted"""

    with open(file_name) as read_file:

        counter: int
        data = csv.reader(read_file)
        for row in data:
            if row[0].isdecimal():
                return int(row[0])
        return None

def increase_counter(file_name=COUNTER_NAME):
    """Increase count inside of file_name by 1"""

    counter = read_counter(file_name)
    counter += 1

    with open(file_name, "w") as write_file:

        writer = csv.writer(write_file)
        writer.writerow(["count"])
        writer.writerow([str(counter)])

def get_data(counter, file_name=DATA_NAME):
    """Grabs data from file_name at a given counter number ID. Returns None is file_name is not properly formatted"""

    with open(file_name) as read_file:

        data = csv.reader(read_file)
        for row in data:
            if row[0].isdecimal() and int(row[0]) == counter:
                return row[1]
        return None

if __name__ == "__main__":

    pass
