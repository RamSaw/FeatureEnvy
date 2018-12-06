DROP TABLE IF EXISTS distancevalue1 CASCADE;
DROP TABLE IF EXISTS relations CASCADE;
DROP TABLE IF EXISTS methodinfo CASCADE;
DROP TABLE IF EXISTS classinfo CASCADE;

CREATE TABLE classinfo ( -- here are inserted all classes in the system, but probably
ClassId INT PRIMARY KEY, -- max table row
ClassQualifiedName VARCHAR(3000) NOT NULL UNIQUE, -- qualified name
ClassName VARCHAR(3000) NOT NULL -- simple name
);

CREATE TABLE methodinfo (-- all methods except (constructors and methods in nested classes)
MethodID INT PRIMARY KEY, -- max table row
MethodName VARCHAR(3000) NOT NULL, -- simple method name without package
MethodParameters VARCHAR(5000), -- method parameters with qualified names, if no params then value is "0"
MethodOfClass VARCHAR(3000) NOT NULL -- qualified class name where method is located
);

CREATE TABLE relations ( -- here are all methods except constructors with classes where it can be moved (based on params variables and used fields) or with method's original class
KeyNum INT PRIMARY KEY, -- max table row
ClassID INT NOT NULL REFERENCES classinfo, -- class id
MethodID INT NOT NULL REFERENCES methodinfo, -- method id
MethodInThisClassOrNot INT NOT NULL CHECK(MethodInThisClassOrNot = 0 OR MethodInThisClassOrNot = 1), -- actually 1 if not in this class, 0 if it is in this class
UNIQUE(ClassID, MethodID)
);

CREATE TABLE distanceValue1 ( -- stores distances that are less than 1 between all classes and all methods, so intersection with relations is needed
methodId INT NOT NULL, -- max table row, it is not methodId, it is just id or row
methodName VARCHAR(3000) NOT NULL, -- simple method name
methodParameters VARCHAR(5000), -- method params classes qualified names listed by ',' or "0" if it is void
methodOfClass VARCHAR(3000) NOT NULL, -- qualified name of method's source class
className VARCHAR(3000) NOT NULL, -- target class qualified name
distance DOUBLE NOT NULL -- distance between method and target class
);

-- distanceValue1 JOIN methodinfo is smaller than |distanceValue1| because methods that are located in nested classes considered in distancevalue1 table but did not in methodinfo
-- distanceValue1 JOIN classinfo is smaller than |distanceValue1| because not all classes exists in classinfo (probably there is no interfaces in classinfo or something else)
