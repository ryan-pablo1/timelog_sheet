import mysql.connector


#Creating the database
def create_db():
	try:
	    test_db = mysql.connector.connect(
		host = "db",
		user = "root",
		password = "root",
	    )

	    test_cursor = test_db.cursor()
	    print("Creating the database, if it does not exists...", end="")
	    test_cursor.execute("create database if not exists timesheetlog")
	    print("success")
	    test_cursor.close()


	except mysql.connector.Error as err:
		print(f"Error: {err}")

#Creating the tables
def create_tables():
	try:
	    test_db = mysql.connector.connect(
		host = "db",
		user = "root",
		password = "root",
		database = "timesheetlog"
	    )

	    test_cursor = test_db.cursor()
	    print("Creating Table, 'users'...", end = '')
	    test_cursor.execute("create table users (user_id int primary key auto_increment, email varchar(100) unique not null, username varchar(100) unique not null, password_hashed varchar(100) not null, hours_worked int default 0, active json default '{\"active\": false, \"time_id\": null}')")
	    print("success")
	    test_cursor.close()
	except mysql.connector.Error as err:
		#Error code parse
		code = str(err).split()[0]
		
		#Table exists error code
		if code == '1050':
		    print("table already exists")
		else:
		    print(f"Error: {err}")


	#Creating the tables
	try:
	    test_db = mysql.connector.connect(
		host = "db",
		user = "root",
		password = "root",
		database = "timesheetlog"
	    )

	    test_cursor = test_db.cursor()
	    print("Creating Table, 'timelogs'...", end = '')
	    test_cursor.execute("create table timelogs (time_id int primary key auto_increment, user_id int not null references users(user_id), time_start datetime, time_stop datetime, hours_shift double(10,2))")
	    print("success")
	    test_cursor.close()
	except mysql.connector.Error as err:
		#Error code parse
		code = str(err).split()[0]
		
		#Table exists error code
		if code == '1050':
		    print("table already exists")
		else:
		    print(f"Error: {err}")
