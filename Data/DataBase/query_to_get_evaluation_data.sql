SELECT *
FROM (SELECT moveMethodRefactoringWithoutSourceDistance.methodName,
       moveMethodRefactoringWithoutSourceDistance.methodParameters,
       moveMethodRefactoringWithoutSourceDistance.sourceClassId,
       moveMethodRefactoringWithoutSourceDistance.sourceClassQualifiedName,
       moveMethodRefactoringWithoutSourceDistance.sourceClassName,
       moveMethodRefactoringWithoutSourceDistance.targetClassId,
       moveMethodRefactoringWithoutSourceDistance.targetClassQualifiedName,
       moveMethodRefactoringWithoutSourceDistance.targetClassName,
       COALESCE(distancevalue1.distance, 1) as sourceClassDistance,
       moveMethodRefactoringWithoutSourceDistance.distance as targetClassDistance,
       moveMethodRefactoringWithoutSourceDistance.IsMethodNotInThisClass
       FROM (SELECT distance_method_both_classes.methodId,
       distance_method_both_classes.methodName,
       distance_method_both_classes.methodParameters,
       distance_method_both_classes.sourceClassId,
       distance_method_both_classes.sourceClassQualifiedName,
       distance_method_both_classes.sourceClassName,
       distance_method_both_classes.targetClassId,
       distance_method_both_classes.targetClassQualifiedName,
       distance_method_both_classes.targetClassName,
       distance_method_both_classes.distance,
       relations.MethodInThisClassOrNot as IsMethodNotInThisClass
       FROM (SELECT distance_method_taget_class.methodId,
                      distance_method_taget_class.methodName,
                      distance_method_taget_class.methodParameters,
                      classinfo.ClassId as sourceClassId,
                      classinfo.ClassQualifiedName as sourceClassQualifiedName,
                      classinfo.ClassName as sourceClassName,
                      distance_method_taget_class.targetClassId,
                      distance_method_taget_class.targetClassQualifiedName,
                      distance_method_taget_class.targetClassName,
                      distance_method_taget_class.distance
               FROM
              (SELECT distance_method.MethodID as methodId, distance_method.methodName, distance_method.methodParameters,
                      distance_method.methodOfClass as sourceClassQualifiedName,
                      classinfo.ClassId as targetClassId,
                      classinfo.ClassQualifiedName as targetClassQualifiedName,
                      classinfo.ClassName as targetClassName,
                      distance_method.distance
               FROM
               (SELECT methodinfo.MethodID, distancevalue1.methodName,
                      distancevalue1.methodParameters, distancevalue1.methodOfClass,
                      distancevalue1.className, distancevalue1.distance
               FROM distancevalue1 JOIN methodinfo
                        ON distancevalue1.methodName = methodinfo.MethodName
                             AND distancevalue1.methodParameters = methodinfo.MethodParameters
                             AND distancevalue1.methodOfClass = methodinfo.MethodOfClass) as distance_method
               JOIN classinfo ON classinfo.ClassQualifiedName = distance_method.className) as distance_method_taget_class
               JOIN classinfo ON distance_method_taget_class.sourceClassQualifiedName = classinfo.ClassQualifiedName)
                  as distance_method_both_classes
               JOIN relations ON distance_method_both_classes.targetClassId = relations.ClassID AND distance_method_both_classes.methodId = relations.MethodID) as moveMethodRefactoringWithoutSourceDistance
               LEFT OUTER JOIN distancevalue1 ON moveMethodRefactoringWithoutSourceDistance.methodName = distancevalue1.methodName AND
               moveMethodRefactoringWithoutSourceDistance.methodParameters = distancevalue1.methodParameters AND
               moveMethodRefactoringWithoutSourceDistance.sourceClassQualifiedName = distancevalue1.methodOfClass AND
               moveMethodRefactoringWithoutSourceDistance.sourceClassQualifiedName = distancevalue1.className) as moveMethodRefactoring
WHERE moveMethodRefactoring.IsMethodNotInThisClass = 1;
