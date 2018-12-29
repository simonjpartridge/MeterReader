import os
import unittest
import time
import json
from datetime import datetime, timedelta

TEST_DB = ':memory'
os.environ["METER_DATABASE_PATH"] = TEST_DB

from server import app, db, constants
from server.models import Pip, Minute, Hour

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        #reset database
        self.reset_db()
        
        

        # Disable sending emails during unit testing
        # self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def reset_db(self):
        db.drop_tables([Pip, Minute, Hour])
        db.create_tables([Pip, Minute, Hour])
        db.close()

    def get_json(self, url):
        return json.loads(self.app.get(url).data)



        


###############
#### tests ####
###############


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_pips(self):
        #check pip without time doesn't work
        response = self.app.get('/api/pip/')
        self.assertEqual(response.status_code, 404)

        response = self.app.get('/api/pip')
        self.assertEqual(response.status_code, 404)

        response = self.app.get('/api/pip/abcd')
        self.assertIn('error',response.data.decode())

        #now add some pips
        now = time.time()

        response = self.app.get('/api/pip/' + str(now))
        self.assertIn('true',response.data.decode())

        response = self.app.get('/api/get_all_pips')
        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 1)



    def test_minutes(self):
        #test none returned before any added
        response = self.app.get('/api/get_all_minutes')
        data = json.loads(response.data)
        self.assertEquals(len(data), 0)

        #test adding one pip
        now = time.time()
        self.app.get('/api/pip/' +  str(now))

        response = self.app.get('/api/get_all_minutes')
        data = json.loads(response.data)
        self.assertEquals(data['1']['pips'], 1)

        #test adding 2 pips
        now = time.time()
        self.app.get('/api/pip/' +  str(now))

        response = self.app.get('/api/get_all_minutes')
        data = json.loads(response.data)
        self.assertEquals(data['1']['pips'], 2)

        #test adding pips in 2 different minutes
        day_ago = datetime.now() - timedelta(days=1)
        self.app.get('/api/pip/' + str(day_ago.timestamp()))

        response = self.app.get('/api/get_all_minutes')
        data = json.loads(response.data)
        self.assertEquals(len(data), 2)

    def test_hours(self):
        #test none returned befor any added
        response = self.app.get('/api/get_all_hours')
        data = json.loads(response.data)
        self.assertEquals(len(data), 0)

        #test adding one pip
        now = time.time()
        self.app.get('/api/pip/' +  str(now))

        response = self.app.get('/api/get_all_hours')
        data = json.loads(response.data)
        self.assertEquals(data['1']['pips'], 1)

        #test adding 2 pips
        now = time.time()
        self.app.get('/api/pip/' +  str(now))

        response = self.app.get('/api/get_all_hours')
        data = json.loads(response.data)
        self.assertEquals(data['1']['pips'], 2)

        #test adding pips in 2 different hours
        day_ago = datetime.now() - timedelta(days=1)
        self.app.get('/api/pip/' + str(day_ago.timestamp()))

        response = self.app.get('/api/get_all_hours')
        data = json.loads(response.data)
        self.assertEquals(len(data), 2)




    


    def test_instantaneous(self):
        #test error for no pops in database
        response = self.app.get('/api/instantaneous')
        self.assertIn('error',response.data.decode())


        #now add some pips
        now = time.time()
        second_ago = now - 1
        self.app.get('/api/pip/' + str(second_ago))
        self.app.get('/api/pip/' + str(now))

        data = self.get_json('/api/instantaneous')

        expected_power = 60*60 / constants.PIP_WH 
        self.assertEqual(expected_power, data['power'])

        #check timing works
        self.assertLessEqual(data['seconds_since_update'], 0.2)
        self.assertGreaterEqual(data['seconds_since_update'], 0)

    def test_pips_today(self):
        #test no pips present
        data = self.get_json("/api/total/today")
        self.assertEqual(data['energy'],0)

        self.app.get('/api/pip/' + str(time.time()))
        self.app.get('/api/pip/' + str(time.time()))

        data = self.get_json("/api/total/today")
        self.assertEqual(data['energy'],2)

        #test yesterdays pips don't show up
        yesterday = datetime.now().replace(hour=0, minute=0, second=0,microsecond=0)
        yesterday = yesterday.timestamp() - 1
        self.app.get('/api/pip/' + str(yesterday))

        data = self.get_json("/api/total/today")
        self.assertEqual(data['energy'],2)


    def test_hourly_today(self):
        #test no pips
        data = self.get_json("/api/historical/hourly/today")

        values = data['values']
        self.assertGreater(len(values), 0)
        self.assertTrue(all([x == 0 for x in values]))

        #check pip shows up in correct hour
        now = datetime.now()
        self.app.get('/api/pip/' + str(now.timestamp()))

        data = self.get_json("/api/historical/hourly/today")
        # print(data)
        times = data['times']
        values = data['values']

        hour = now.replace(minute=0, second=0, microsecond=0)

        value = values[times.index(str(hour))]
        self.assertEqual(value, 1)
        # self.assertEqual(len(values), hour+1) #all hours should be listed, even if empty

    def test_hours_custom(self):
        start = "2018-12-28:10"
        end = "2018-12-28:20"
        data = self.get_json("/api/historical/hourly?start=" + start + "&end=" + end)


        start = "2018-12-27:10"
        end = "2018-12-28:20"
        data = self.get_json("/api/historical/hourly?start=" + start + "&end=" + end)



        # print(data)




# def test_daily_this_month(self):
#      data = self.get_json("/api/historical/daily/this_year")



        





        




if __name__ == "__main__":
    unittest.main()
