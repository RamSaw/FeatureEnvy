import getopt
import json
import os
import sys

from refactoringGeneration.databaseExtraction import get_possible_refactorings_for_project


def print_help():
    print('refactoringGeneration.py -u <database_user> -p <database_password>')


def encode_b(obj):
    if isinstance(obj, float):
        return str(obj)
    return obj.__dict__


def generate_possible_refactorings_for_dataset(db_user, db_password, dataset_path):
    dataset_root_path = os.path.join(dataset_path, "projects")
    for project in os.listdir(dataset_root_path):
        try:
            print("Started: " + project)
            json_file_name = "DLB_" + project
            project_path = os.path.join(dataset_root_path, project)
            possible_refactorings = get_possible_refactorings_for_project(db_user, db_password, project)
            with open(os.path.join(project_path, json_file_name), 'w') as refactorings_file:
                refactorings_file.write(json.dumps([ob.__dict__ for ob in possible_refactorings], indent=2))
            print("Ended: " + project)
        except Exception as err:
            print("Error on project: " + project)
            print(err)


def main(argv):
    db_user = None
    db_password = None
    dataset_path = None
    try:
        opts, args = getopt.getopt(argv, "hu:p:d:", ["user=", "password=", "dataset="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-u", "--user"):
            db_user = arg
        elif opt in ("-p", "--password"):
            db_password = arg
        elif opt in ("-d", "--dataset"):
            dataset_path = arg
    if db_user is None or db_password is None or dataset_path is None:
        print("Param is missing, try again\n")
        print_help()
        sys.exit(2)
    generate_possible_refactorings_for_dataset(db_user, db_password, dataset_path)


if __name__ == "__main__":
    main(sys.argv[1:])
