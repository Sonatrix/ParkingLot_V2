#!/usr/bin/python3.6
import os, sys
import parking

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

class ParkingCommands(object):

    def __init__(self):
        self.parking = parking.Connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.conn = self.parking.get_conn()

    def process_file(self, given_file):
        if not os.path.exists(given_file):
            print("Given file {} does not exist".format(given_file))

        file_obj = open(given_file)
        try:
            line = file_obj.readline()
            while line:
                if line.endswith('\n'): line = line[:-1]
                if line == '': continue
                self.process_command(line)
                line = file_obj.readline()
        except StopIteration:
            file_obj.close()
            self.parking.close_connection()
        except Exception as ex:
            print(f"Error occured while processing file {repr(ex)}")

    def process_input(self):
        try:
            while True:
                stdin_input = input("Enter command: ")
                self.process_command(stdin_input)
        except (KeyboardInterrupt, SystemExit):
            return
        except Exception as ex:
            print("Error occured while processing input {}".format(ex))


    def process_command(self, stdin_input):
        inputs = stdin_input.split()
        command = inputs[0]
        params = inputs[1:]
        if hasattr(self.parking, command):
            command_function = getattr(self.parking, command)
            command_function(*params)
        else:
            print("Got wrong command.")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        pk_command = ParkingCommands()
        pk_command.process_input()
    elif len(args) == 2:
        pk_command = ParkingCommands()
        pk_command.process_file(args[1])
    else:
        print("Wrong number of arguments.\n" \
                "Usage:\n" \
                "./parking_lot.py <filename> OR \n" \
                "./parking_lot.py")
