# userActivity
Back-end API  to get activity_periods of a user on multiple pages on an application.

INTRODUCTION:
	
	1. An application having three pages namely: 'home', 'catalouge', 'shop' is considered.
	
	2. Users are divided into three categories: 'platinum', 'gold', 'silver'.
	
	3. The database is populated with the help of 'user_config' file. 
	
	4. Method 'store_user_details_in_database' is written to store user details in database.
	
	5. Method 'store_user_activity_in_database' is written to store users activity in database.
	
	6. Method 'calculate_response_for_user' gives response to a get request with key arguments 'setion'. (section are the pages on the application).
	
	7. All the above methods are at 'userActivity/project1_full_throttle/userActivity/views.py' .
	
	
OBJECTIVE:
	
	1. To calculate the users activity on a web page and send the response in the required json.
	
	
DATABASE USED:
	
	1. Mongodb
	
WEB - FRAMEWORK:

	1. Django
	
	
API END-POINTS:

	1. http://3.7.213.105:8000/user_details?section=home
	
	2. http://3.7.213.105:8000/user_details?section=catalouge
	
	3. http://3.7.213.105:8000/user_details?section=shop
	