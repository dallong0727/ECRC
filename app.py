#!/usr/bin/python3 
# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, Response
from apscheduler.schedulers.background import BackgroundScheduler

import json
import time
import atexit

from Server.utils.login_utils import login
# from Server.utils.read_data_utils import get_weather_data
from Server.utils.read_data_utils import get_weather_data, get_meta_data, fetch_mongo_data
from Server.utils.preprocessing_data_utils import preprocessing_analysis_data, preprocessing_user_data, preprocessing_day_count
from Server.utils.analyze_job_utils import analyze_recommend_job, analyze_activity_job
from Server.utils.callback_results_utils import callback_results
from Server.utils.utils_for_env.url import SERVER_URL_PORT

###Choose a port (Port for this agent)
AGENT_PORT = 4010

sched = BackgroundScheduler(timezone='Asia/Seoul')
sched.add_job(get_weather_data, 'interval', hours=6)
sched.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: sched.shutdown())

app = Flask(__name__)  

@app.route('/api/v1/analyze_data', methods=['POST'])
def analyze_data2():
    start = time.time()
    #0. Parse meta-data
    body = request.json
    print(body)

    URL_PORT = SERVER_URL_PORT()
    user_id = body['user_id']
    subscription_id = body['subscription_id']
    service_type = body['job']['service_type']

    if (body == None) : 
        response = make_response(json.dumps({"message": "Data None"}),  400, )
        return response

    else : 
        try :             
            #1. Login developer account
            access_token = login(URL_PORT)
            
            login_chk = time.time()
            
            #2. Read data(job_id)
            job_list, birth, gender, personal_survey, inserted_at = get_meta_data(URL_PORT, access_token, user_id, subscription_id)
            
            read_data1_chk = time.time()            
            
            data_list = fetch_mongo_data(URL_PORT, access_token, service_type, subscription_id, job_list)

            read_data2_chk = time.time()
            
            #3. Preprocess data
            age = preprocessing_user_data(birth)
            day_count = preprocessing_day_count(inserted_at)
            last_mission_id = data_list[0]['payload']['scene_id']
            
            mission5_data, mission6_data, mission7_data, mission8_data, mission9_data, mission10_data = preprocessing_analysis_data(data_list)
            
            preprocess_data_chk = time.time()
                                    
            #4. Analyze data
            scoring_result = analyze_activity_job(mission5_data, mission6_data, mission7_data, mission8_data, mission9_data, mission10_data, day_count)

            rec_results = analyze_recommend_job(age, gender, personal_survey, last_mission_id ,mission5_data, mission6_data, mission7_data, mission8_data, mission9_data, mission10_data)
            
            analyze_data_chk = time.time()
            
            # # #5. Upload data
            # callback_results(URL_PORT, body, access_token)
            callback_results(URL_PORT, body, scoring_result, rec_results, access_token) 
            
            end = time.time()

            print(f"{login_chk - start:.5f} sec")
            print(f"{read_data1_chk - login_chk:.5f} sec")
            print(f"{read_data2_chk - read_data1_chk:.5f} sec")
            print(f"{preprocess_data_chk - read_data2_chk:.5f} sec")   
            print(f"{analyze_data_chk - preprocess_data_chk:.5f} sec")   
            print(f"{end - analyze_data_chk:.5f} sec")
            print(f"{end - start:.5f} sec")
            
            return "callback success"

        # else:
        except Exception as e:
            print(e)
            return e

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=AGENT_PORT, threaded=True, use_reloader=True, use_debugger=True)

