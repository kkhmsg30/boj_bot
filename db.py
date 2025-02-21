from pymongo import MongoClient

class DB(MongoClient):
    
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        super().__init__(host=uri)

        self.__db = self["boj"]

    def user_exist(self, discord_id:str):
        users = self.__db['users']
        user = users.find_one({"discord_id":discord_id})
        print(user)
        return user is not None

    def get_boj_id(self, discord_id:str):
        users = self.__db['users']

if __name__=="__main__":
    db = DB()
    db.user_exist("kkhmsg30")