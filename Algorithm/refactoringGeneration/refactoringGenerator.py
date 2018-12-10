import numpy as np

from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences

from refactoringGeneration.MoveMethodRefactoring import MoveMethodRefactoring
from refactoringGeneration.stringUtils import partition_name

METHOD_NAME_COLUMN = 'methodName'
SOURCE_CLASS_QUALIFIED_NAME_COLUMN = 'sourceClassQualifiedName'
TARGET_CLASS_QUALIFIED_NAME_COLUMN = 'targetClassQualifiedName'
SOURCE_CLASS_NAME_COLUMN = 'sourceClassName'
TARGET_CLASS_NAME_COLUMN = 'targetClassName'
SOURCE_CLASS_DISTANCE_COLUMN = 'sourceClassDistance'
TARGET_CLASS_DISTANCE_COLUMN = 'targetClassDistance'
METHOD_PARAMETERS_COLUMN = 'methodParameters'


def parameters_to_list(method_parameters):
    if method_parameters == "0":
        return []
    else:
        return str.split(method_parameters, ",")[:-1]


def load_model():
    MODELPATH = '../model-CNN/'
    fold_number = 1
    model = model_from_json(open(MODELPATH + 'my_model_' + str(fold_number) + '#Fold.json').read())
    model.load_weights(MODELPATH + 'my_model_weights_' + str(fold_number) + '#Fold.h5')
    return model


class RefactoringGenerator:
    MAX_SEQUENCE_LENGTH = 15
    model = load_model()

    @staticmethod
    def get_refactoring_for_each_opportunity(refactoring_opportunities):
        refactoring_to_suggest = None
        refactoring_accuracy = -1

        for opportunity in refactoring_opportunities:
            partitioned_method_name = partition_name(opportunity[METHOD_NAME_COLUMN])
            partiotioned_source_class_name = partition_name(opportunity[SOURCE_CLASS_NAME_COLUMN])
            partiotioned_target_class_name = partition_name(opportunity[TARGET_CLASS_NAME_COLUMN])
            model_string_data = [" ".join(partitioned_method_name +
                                          partiotioned_source_class_name + partiotioned_target_class_name)]

            test_distances = [[opportunity[SOURCE_CLASS_DISTANCE_COLUMN], opportunity[TARGET_CLASS_DISTANCE_COLUMN]]]

            tokenizer1 = Tokenizer(num_words=None)
            tokenizer1.fit_on_texts(model_string_data)
            test_sequences = tokenizer1.texts_to_sequences(model_string_data)
            test_data = pad_sequences(test_sequences, maxlen=RefactoringGenerator.MAX_SEQUENCE_LENGTH)
            test_distances = np.asarray(test_distances)

            x_val = []
            x_val_names = test_data
            x_val_dis = test_distances
            x_val_dis = np.expand_dims(x_val_dis, axis=2)
            x_val.append(x_val_names)
            x_val.append(np.array(x_val_dis))

            is_feature_envy = bool(RefactoringGenerator.model.predict_classes(x_val)[0][0])
            if is_feature_envy:
                accuracy = RefactoringGenerator.model.predict(x_val)[0][0]
                if accuracy > refactoring_accuracy:
                    refactoring_to_suggest = opportunity
                    refactoring_accuracy = accuracy

        return None if refactoring_to_suggest is None else \
            MoveMethodRefactoring(refactoring_to_suggest[TARGET_CLASS_QUALIFIED_NAME_COLUMN],
                                  refactoring_to_suggest[SOURCE_CLASS_QUALIFIED_NAME_COLUMN],
                                  refactoring_to_suggest[METHOD_NAME_COLUMN],
                                  parameters_to_list(refactoring_to_suggest[METHOD_PARAMETERS_COLUMN]),
                                  float(refactoring_accuracy))

    # More correctly to use this method instead of above method because researchers in DLB in test.py use the same
    # logic as below.
    @staticmethod
    def get_refactoring_for_opportunities_bucket(refactoring_opportunities):
        partitioned_method_name = partition_name(refactoring_opportunities[0][METHOD_NAME_COLUMN])
        partitioned_source_class_name = partition_name(refactoring_opportunities[0][SOURCE_CLASS_NAME_COLUMN])
        model_string_data = []
        test_distances = []
        for opportunity in refactoring_opportunities:
            assert partitioned_method_name == partition_name(opportunity[METHOD_NAME_COLUMN])
            assert partitioned_source_class_name == partition_name(opportunity[SOURCE_CLASS_NAME_COLUMN])
            partiotioned_target_class_name = partition_name(opportunity[TARGET_CLASS_NAME_COLUMN])
            model_string_data.append(" ".join(partitioned_method_name +
                                              partitioned_source_class_name + partiotioned_target_class_name))
            test_distances.append([opportunity[SOURCE_CLASS_DISTANCE_COLUMN],
                                   opportunity[TARGET_CLASS_DISTANCE_COLUMN]])

        tokenizer1 = Tokenizer(num_words=None)
        tokenizer1.fit_on_texts(model_string_data)
        test_sequences = tokenizer1.texts_to_sequences(model_string_data)
        test_data = pad_sequences(test_sequences, maxlen=RefactoringGenerator.MAX_SEQUENCE_LENGTH)
        test_distances = np.asarray(test_distances)

        x_val = []
        x_val_names = test_data
        x_val_dis = test_distances
        x_val_dis = np.expand_dims(x_val_dis, axis=2)
        x_val.append(x_val_names)
        x_val.append(np.array(x_val_dis))

        predictions = RefactoringGenerator.model.predict_classes(x_val)
        accuracy_predictions = RefactoringGenerator.model.predict(x_val)
        refactoring_to_suggest = None
        refactoring_accuracy = -1
        index_max = list(accuracy_predictions).index(max(accuracy_predictions))
        is_feature_envy = bool(predictions[index_max][0])
        if is_feature_envy:
            refactoring_to_suggest = refactoring_opportunities[index_max]
            refactoring_accuracy = accuracy_predictions[index_max][0]

        return None if refactoring_to_suggest is None else \
            MoveMethodRefactoring(refactoring_to_suggest[TARGET_CLASS_QUALIFIED_NAME_COLUMN],
                                  refactoring_to_suggest[SOURCE_CLASS_QUALIFIED_NAME_COLUMN],
                                  refactoring_to_suggest[METHOD_NAME_COLUMN],
                                  parameters_to_list(refactoring_to_suggest[METHOD_PARAMETERS_COLUMN]),
                                  float(refactoring_accuracy))

    @staticmethod
    def get_refactoring(refactoring_opportunities):
        return RefactoringGenerator.get_refactoring_for_opportunities_bucket(refactoring_opportunities)
