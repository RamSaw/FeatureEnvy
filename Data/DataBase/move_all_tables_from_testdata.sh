username="root"
password="12345"
mysqladmin -u $username -p$password create $1
mysqldump -u $username -v testdata -p$password | mysql -u $username -p$password -D $1
mysql -u $username -p$password testdata < "./create_schema.sql"
