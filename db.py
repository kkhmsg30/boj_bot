from pymongo import MongoClient

class DB(MongoClient):
    
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        super().__init__(host=uri)

        self.__db = self["boj"]

    def user_exist(self, discord_id:str) -> bool:
        users = self.__db['users']
        user = users.find_one({"discord_id":discord_id})
        return user is not None

    def get_boj_handle(self, discord_id:str) -> None|str:
        users = self.__db['users']
        user = users.find_one({"discord_id":discord_id})
        if user is None:
            return None
        return user['boj_handle']
    
    def get_problems(self, discord_id:str):
        problems = self.__db['problems']
        if 
        

if __name__=="__main__":
    db = DB()
    print(db.get_boj_id("kkhmsg30"))