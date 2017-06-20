import requests
import simplejson as json
import pprintpp as pprint
import string
import getopt
import pandas as pd
import datetime
import numpy as np
import pickle
import sys
from abc import ABCMeta
import mysql.connector
import sqlalchemy
import MySQLdb
from sqlalchemy import create_engine
import time
from datetime import datetime, timedelta,date

class create_new_sensor(object):

        """


        This class aims to create a new indoor sensor configuration
	maximum 200 times requirememnts per day
        param type_sensor: the description of the smart sensor, corresponds to "devdesciption" in database
        param user: The email that used for registering
        param headers: includes the formate and the key to obtain the data from cloud
        param location: F stands for the floor number, R stands for the room number
        """
        def __init__(self,type_sensor,user,location,accept,api_token,start, end, averageBy):
                self.type_sensor = type_sensor
                self.user = user
                self.accept = accept
                self.api_token = api_token
                self.location = location
                self.header = {"Aceept": self.accept,"X-API-KEY-TOKEN": self.api_token}
                url1= "http://api.foobot.io/v2/owner/"+ Foobot.converse_name(self.user) + "/device/"
                identify_api = requests.get(url1,headers=self.header).json()[0]
                self.uuid = identify_api['uuid'] #get the Device unique identifier

        @staticmethod
        def converse_name(name):
                new_name=string.replace(name, ":", "%3A")
                return new_name

        @staticmethod
        def df_to_mysql(datapoints_df,table_name):
                """
                This function aims to save a data frame into MySQL
                """
                #dbServer = "http://138.100.82.183"
                #dbPass = "tian.2016"
                #dbSchema = "cmadrid"
                engine = create_engine('mysql+mysqlconnector://cmadrid:tian.2016@138.100.82.183:3306/madrid_pollution', echo=False)
                datapoints_df.to_sql(name=table_name, con=engine, if_exists = 'append', index=False)

        def is_new_sensor(self):
                """
                test if the device a new sensor
                """
                #db=mysql.connect()
                db = MySQLdb.connect(host="138.100.82.183",user="cmadrid",passwd="tian.2016",db="madrid_pollution")
                cur = db.cursor()
                cur.execute("select devid from SensorConfiguration where devid= %s", [self.uuid])
                data = cur.fetchall()
                if data is ():
                        print ("This is a new sensor")
                        return 1

                else :
                        print ("This device is found in database")
                        return 0
        def save_new_sensor(self):
                """
                save the configuration information of the new sensor
		types:  uuid, int(11)
			devdescrpition  varchar(250) 
			email  	varchar(50) 
			headers  varchar(250) 
			location varchar(255) 
                """
		col_list = ("devid","devdescription","email","headers","location")
                df_new_sensor = pd.DataFrame([self.uuid,self.type_sensor,self.user,self.api_token,self.location])
                df_new_sensor_t = df_new_sensor.transpose()
		df_new_sensor_t.columns=col_list
		
		time.ctime() #'Mon Oct 18 13:35:29 2010' 
		t = time.strftime("%Y-%m-%d %H:%M:%S") 
		df_new_sensor_t["timestamp"] = t

                table_name="SensorConfiguration"
                create_new_sensor.df_to_mysql(df_new_sensor_t,table_name)




#start = ""
#end = ""
#averageBy=""
#USER = "gongbing1112@gmail.com"
class Foobot(create_new_sensor):
	
        def __init__(self, type_sensor,user,location,accept,api_token,start, end, averageBy):
                """
                param start: start time
                param end : end time
                """
                super(Foobot,self).__init__(type_sensor,user,location,accept,api_token,start,end,averageBy)
		#Foobot.__init__(self)
                self.start  = start
                self.end = end
		self.type_sensor = type_sensor
                self.user = user
                self.accept = accept
                self.api_token = api_token
                self.location = location
		self.averageBy = averageBy
                self.header = {"Aceept": self.accept,"X-API-KEY-TOKEN": self.api_token}
                url1= "http://api.foobot.io/v2/owner/"+ Foobot.converse_name(self.user) + "/device/"
                identify_api = requests.get(url1,headers=self.header).json()[0]
                self.uuid = identify_api['uuid'] #get the Device unique identifier



        def generate_url(self):
                """
                generate the URL for the specific USER
                """
                url2= "http://api.foobot.io/v2/device/"
                start_url = create_new_sensor.converse_name(self.start)
                end_url = create_new_sensor.converse_name(self.end)
                url = url2 + str(self.uuid) + "/datapoint/" + start_url+"/"+end_url+"/" + str(self.averageBy)+"/"
                return url

        
        def get_datapoints(self,url):
                datapoints = requests.get(url=url,headers= self.header).json()
		if("datapoints" in datapoints.keys()):
			
                	colnames = datapoints[datapoints.keys()[5]]#get the name from list
                	dats_key = datapoints.keys()[3]#get the data points from the data list
                	datapoints_df=pd.DataFrame(datapoints[dats_key],columns=colnames) #data points in data frame type
			datapoints_df["devid"] = str(self.uuid)


                	if(datapoints_df.shape[1] > 0):
                        	# Change the time to "%Y-%m-%d %H:%M:%S" formate
                        	for i in range(datapoints_df.shape[0]):
                        	#check if the time formate is datetime.datetime
					if(isinstance(datapoints_df["time"][i], datetime)):										                     	 	pass
                                	else:
                                       	 	t = datetime.fromtimestamp((datapoints_df["time"][i]))
                                        	fmt = "%Y-%m-%d %H:%M:%S"
                                        	t.strftime(fmt)
                                        	datapoints_df["time"][i] = t

                        	#file_name_pik = str("start_" + str(start) + "_end_" + str(end) + "_averageBy_" + str(averageBy)+".pickle")
                        	#file_name_csv = str("start_" + str(start) + "_end_" + str(end) + "_averageBy_" + str(averageBy)+".csv")

#                       	 with open(file_name_pik, 'wb') as handle:#save file into .pickle file
#                              	 pickle.dump(datapoints_df, handle)
#                      	 	handle.close()
                       	 	#save file to csv format
#                        	datapoints_df.to_csv(file_name_csv, sep='\t', encoding='utf-8')
			else:
				print "There is no records in the requested period"
			return(datapoints_df)
		else:
	 		print ("URL is wrong")
			 

		
def main(argv):
        global accept
        global api_token 
        global user
        global type_sensor 
        global location 
	global start 
        global end 
        global averageBy 
	global yesterday
	accept = "application/json;charset=UTF-8"
	api_token = "eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiZ29uZ2JpbmcxMTEyQGdtYWlsLmNvbSIsImlhdCI6MTQ3OTgwNTA4MiwidmFsaWRpdHkiOi0xLCJqdGkiOiJlMmYyZjE1ZS00ODgxLTQxMDItYmFiNy04NjExOTgxNWE1NmMiLCJwZXJtaXNzaW9ucyI6WyJ1c2VyOnJlYWQiLCJkZXZpY2U6cmVhZCJdLCJxdW90YSI6MjAwLCJyYXRlTGltaXQiOjV9.MfNT6f-o7S2A_tvBFbQ1k3-61lDvconmVl7zdyjOP5k"
	user = "gongbing1112@gmail.com"
	type_sensor= "foobot"
	location = "F1_R1"
	yesterday =date.today() - timedelta(1)
	start = yesterday.strftime("%Y-%m-%d %H:%M:%S")
	end = date.today().strftime("%Y-%m-%d %H:%M:%S")
	#averageBy = 

        try:
                opts,args = getopt.getopt(sys.argv[1:],"u:t:l:p:k:s:e:b:h",["user=","type_sensor=","location=","accept=","api_token","start=","end=","averageBy=","help"])
        except getopt.GetoptError:
                print 'getdata_foobot.py -u <user> -t <type_sensor> -l <location> -p <accept> -k <api_token> -s <start> -e <end> -b <averageBy>'
                sys.exit(2)

        for opt,arg in opts:
                if opt in ('-h',"--help"):
                        print 'getdata_foobot.py -u <user> -t <type_sensor> -l <location> -p <accept> -k <api_token> -s <start> -e <end> -b <averageBy>'
                elif opt in("-u","--user"):
			user = arg
		elif opt in("-t", "--type_sensor"):
			type_sensor=arg
		elif opt in("-l","--location"):
			location=arg
		elif opt in("-p","--accept"):
			accept = arg
		elif opt in("-k","--api_token"):
			api_token=arg
		elif opt in ("-s", "--start"):
                        start = arg
                elif opt in ("-e", "--end"):
			end = arg
                elif opt in ("-b", "--averageBy"):
                        averageBy = arg
	sensor = create_new_sensor(type_sensor,user,location,accept,api_token,start,end,averageBy)

	if(sensor.is_new_sensor()):#add new sensor to sql
		sensor.save_new_sensor()
		print sensor.uuid
	else:
		pass
        myFootbot = Foobot(type_sensor,user,location,accept,api_token,start,end,averageBy)
        url =myFootbot.generate_url()
	print(url)
	print("start time is:%s" %( start))
        dat =myFootbot.get_datapoints(url)
        if(dat.shape[0]>0):
                
                #print(dat)
                #myFootbot.save_datapoints(dat)
                table_name="foobot_samples"
                create_new_sensor.df_to_mysql(dat,table_name)
        else:
                print "There is no records in the requested period"

        #print(start)
        #print(end)




if __name__=='__main__':
   main(sys.argv)
#	python getdata_foobot_v3.py -s 2016-11-27T18:50:02 -e 2016-11-12T18:50:02 -b 6^


