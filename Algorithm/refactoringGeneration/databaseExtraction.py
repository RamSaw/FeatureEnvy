from collections import defaultdict

import pymysql.cursors

from refactoringGeneration.refactoringGenerator import RefactoringGenerator

METHOD_NAME_COLUMN = 'methodName'
SOURCE_CLASS_QUALIFIED_NAME_COLUMN = 'sourceClassQualifiedName'
TARGET_CLASS_QUALIFIED_NAME_COLUMN = 'targetClassQualifiedName'
SOURCE_CLASS_NAME_COLUMN = 'sourceClassName'
TARGET_CLASS_NAME_COLUMN = 'targetClassName'
SOURCE_CLASS_DISTANCE_COLUMN = 'sourceClassDistance'
TARGET_CLASS_DISTANCE_COLUMN = 'targetClassDistance'
METHOD_PARAMETERS_COLUMN = 'methodParameters'


def get_possible_refactorings_for_project(db_user, db_password, project):
    path_to_sql_command_file = "../../Data/DataBase/query_to_get_evaluation_data.sql"
    connection = pymysql.connect(host='localhost',
                                 user=db_user,
                                 password=db_password,
                                 db=project,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor, open(path_to_sql_command_file, 'r') as sql_command_file:
            sql = sql_command_file.read()
            cursor.execute(sql)
            method_refactoring_opportunities = defaultdict(list)
            for refactoring_opportunity in cursor.fetchall():
                method_name = refactoring_opportunity[METHOD_NAME_COLUMN]
                source_class_qualified_name = refactoring_opportunity[SOURCE_CLASS_NAME_COLUMN]
                method_refactoring_opportunities[(method_name, source_class_qualified_name)]\
                    .append(refactoring_opportunity)
            possible_refactorings = []
            for _, refactoring_opportunities in method_refactoring_opportunities.items():
                refactoring = RefactoringGenerator.get_refactoring(refactoring_opportunities)
                if refactoring is not None:
                    possible_refactorings.append(refactoring)
            return possible_refactorings
    finally:
        connection.close()
