import getopt
import sys

from refactoringGeneration.databaseExtraction import get_possible_refactorings_for_project


def print_help():
    print('refactoringGeneration.py -u <database_user> -p <database_password>')


def main(argv):
    db_user = None
    db_password = None
    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["user=", "password="])
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
    if db_user is None or db_password is None:
        print("Param is missing, try again\n")
        print_help()
        sys.exit(2)
    possible_refactorings = get_possible_refactorings_for_project(db_user, db_password, "ant")


if __name__ == "__main__":
    main(sys.argv[1:])
