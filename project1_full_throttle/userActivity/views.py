from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

import random
import string
from datetime import datetime, timedelta

from pandas import DataFrame

from userActivity.configs import ravi_db as mongo_db
from userActivity.user_config import user_details

"""
server check method
"""
def home(request):
	result = {'status':'running'}
	return JsonResponse(result)


"""
1. method to store user details in database.
"""
def store_user_details_in_database():
    records = []
    try:
        for _ in user_details:
            records.append({
                'user_id': ''.join([random.choice(string.ascii_letters
                                                  + string.digits) for n in range(6)]),
                'real_name': _,
                'tz': user_details[_]['timezone'],
                'membership': user_details[_]['membership']})
        print(records)
        mongo_db['user_details'].insert(records)
    except Exception as ex:
        print('Exception in store_user_details_in_database:', str(ex))


"""
1. Method to store users activity in database.
"""
def store_user_activity_in_database():
    try:
        user_data = list(mongo_db['user_details'].find({}, {'_id': 0, 'user_id': 1}))
        user_data_df = DataFrame(user_data)
        for i in range(3):
            date = (datetime.utcnow() - timedelta(days=random.randrange(20, 50, 3))).replace(hour=0, minute=30,
                                                                                             second=0, microsecond=0)

            for _ in user_data_df['user_id']:
                start_time = datetime.utcnow() - timedelta(days=random.randrange(20, 50, 3))
                data_to_database = {
                    'user_id': _,
                    'section': random.choice(['home', 'catalouge', 'shop']),
                    'date': date,
                    'start_time': start_time,
                    'end_time': start_time + timedelta(hours=random.randrange(3, 10))
                }
                mongo_db['user_activity'].update_many({'date': date, 'user_id': _}, {'$set': data_to_database},
                                                      upsert=True)
    except Exception as ex:
        print('Exception in store_user_activity_in_database:', str(ex))



"""
1. Method to return user activity_periods in the required format.
"""
def get_user_activity_period(user_id, section):
    try:
        activity_records = []
        user_activity_data = list(mongo_db['user_activity'].find({'section': section}, {'_id': 0}))
        user_activity_data_df = DataFrame(user_activity_data)
        records = user_activity_data_df.loc[user_activity_data_df['user_id'] == user_id]
        records.reset_index(inplace=True, drop = True)
        for i in range(len(records['user_id'])):
            activity_records.append({'start_time': (records['start_time'][i]).strftime('%b %d %Y %I%p'), 'end_time': (records['end_time'][i]).strftime('%b %d %Y %I%p')})
        return activity_records
    except Exception as ex:
        print('Exception in get_user_activity_period:', str(ex))



"""
1. Method to return the response to a get request with key arguments as section(section is the pages 
   on th application) in the required format.
"""
def calculate_response_for_user(request):
    try:
        members_records = []
        section = request.GET['section']
        user_activity_data = list(mongo_db['user_activity'].find({'section': section}, {'_id': 0}))
        user_activity_data_df = DataFrame(user_activity_data)
        user_details_data = list(mongo_db['user_details'].find({}, {'_id': 0}))
        user_details_data_df = DataFrame(user_details_data)
        for _ in user_activity_data_df['user_id'].unique():
            members_records.append({
                "id": user_details_data_df.loc[user_details_data_df['user_id'] == _, 'user_id'].iloc[0],
                "real_name":
                    user_details_data_df.loc[user_details_data_df['user_id'] == _, 'real_name'].iloc[0],
                "tz": user_details_data_df.loc[user_details_data_df['user_id'] == _, 'tz'].iloc[0],
                "activity_periods": get_user_activity_period(user_id= _, section=section)
            })
        final_json = {"ok": True, "members": members_records}
        return JsonResponse(final_json)
    except Exception as ex:
        print('Exception in calculate_response_for_user:', str(ex))



