from dotenv import load_dotenv
import pymemcache as customMemcache
from phpserialize import *
import os

#pip install pymemcache
#pip install python-dotenv
#pip install phpserialize

env_path = '.env'
load_dotenv(dotenv_path=env_path)

class SessionManager:
    def __init__(self,user_id,token):
        self.user_id = user_id
        self.token = token
        self.memcache_host = os.getenv('MEMCACHE_HOST')
        self.memcache_port = os.getenv('MEMCACHE_PORT')
        self.app_env =  os.getenv('APP_ENV')

    def validate_session(self):
        try:
            if self.app_env == "development":
                return True
            return self.__authenticate_user()
        except:
            return False

    def __authenticate_user(self):
        if self.token == '' or self.user_id == '':
            return False

        user_data = self.__get_user_data()
        
        if((user_data != False) and str(user_data['user_id']) == str(self.user_id)):
            return True    
        return False

    def __get_user_data(self):
        memcache_data = self.__get_memcache_data()
        
        if memcache_data == False:
            return False
        else:
            if 'Auth|' not in str(memcache_data):
                return False
            split_data = memcache_data.split('Auth|')
            user_data = unserialize(bytes(split_data[1].replace('\\', ''), 'utf-8'))
            return self.utf_decoder(user_data)

    def __get_memcache_data(self):
        try:
            client = customMemcache.Client((self.memcache_host, self.memcache_port))
            result = client.get(str(self.token))
            
            if (result is None) or (result is False):
                return False
            else:
                return str(result)
        except Exception as e:
            return False

    def utf_decoder(self,obj, enc_format = 'utf-8'):    
        newobj = {}
        for key,value in obj.items():
            if(type(value) == dict):
                value = self.utf_decoder(value)
            else:
                try:
                    value = value.decode(enc_format)
                except:
                    continue
            newobj[key.decode(enc_format)] = value
        return newobj
    

#How to Use
# session_manager = SessionManager('47007593','gkqjdkfm287snvuu25tfg9d5t1')
# session = session_manager.validate_session()
# print (session)
