from typing import List


class MoveMethodRefactoring:
    def __init__(self, target_class_qualified_name: str, source_class_qualified_name: str,
                 method_name: str, params_classes: List[str], accuracy: float) -> None:
        super().__init__()
        self.target_class_qualified_name = target_class_qualified_name
        self.source_class_qualified_name = source_class_qualified_name
        self.method_name = method_name
        self.params_classes = params_classes
        self.accuracy = accuracy

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.target_class_qualified_name, self.source_class_qualified_name,
                     self.method_name, tuple(self.params_classes)))
