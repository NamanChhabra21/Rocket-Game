import platform
import requests
import json
import datetime
import uuid

DATABASE_URL = "YOUR FIREBASE DATABASE URL"
"""

Question : How do I get this Database URl ?

Step-1 : Goto https://console.firebase.google.com/ --> Console
Step-2 : Login/Create Account
Step-3 : Find Realtime Database --> Create Database --> Choose test mode and select any region
step-4 : Done and copy the link ( Example: https://mygame-default-rtdb.firebaseio.com/ )

Question : What if I dont want to collect data of User ?

Answer: You can leave the `DATABASE_URL` variable unchanged, it will not effect your main code
as try/except is used in `main.py` file last line.

FOR FURTHER QUESTIONS , visit discussions tab on Github.

"""

# Creating Unique I'd for each computer
class Uid:
    def __init__(self,username="Guest"):
        try:
            self.node = platform.uname()[1]
            self.username = username
            self.random_id = uuid.uuid4()
            self.current_time = datetime.datetime.now().strftime("%D_%H:%M:%S")
            self.os = platform.platform()
            self.success = True
        except Exception as e:
            # Sometimes there are network issues
            add_error(e)
            self.success = False
    def make(self):
        if self.success:
            UserId = self.username+"-"+self.os+"-"+self.node+"-"+str(self.current_time)+"-"+str(self.random_id)
            with open("UserData.json","r") as datafile:
                df = json.load(datafile)
                df["UserId"] = UserId
                df["Username"] = self.username
                df["OS type"] = self.os
            with open("UserData.json", "w") as writedf:
                json.dump(df,writedf)
            return UserId
        else:
            return False

    @staticmethod
    def is_created():
        # Checks if the user id is created or not
        with open("UserData.json") as datafile:
            df = json.load(datafile)
            uid = df["UserId"]
            if uid:
                return True
            else:
                return False


# GAME DATA STORING

def save_high_score(high_score):
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            df["HighestScore"] = high_score
    with open("UserData.json", "w") as writedf:
        json.dump(df,writedf)

def get_high_score():
    with open("UserData.json","r") as datafile:
        df = json.load(datafile)
        score = df["HighestScore"]
    return score

def update_rating(rating):
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            df["Rated"] = rating
    with open("UserData.json", "w") as writedf:
        json.dump(df,writedf)
def is_rated():
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            rate = df["Rated"]
    if rate:
        return True
    else:
        return False

def update_playtime(add_seconds):
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            df["PlayTimeSeconds"] += add_seconds # Adds played time in minutes
    with open("UserData.json", "w") as writedf:
        json.dump(df,writedf)

def update_last_played():
    now = datetime.datetime.now()
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            df["LastPlayed"] = str(now)
    with open("UserData.json", "w") as writedf:
        json.dump(df,writedf)

def add_error(error):
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            df["Errors"].append(str(error))
    with open("UserData.json", "w") as writedf:
        json.dump(df,writedf)

def add_feedback(feedback):
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
            df["Feedback"].append(feedback)
    with open("UserData.json", "w") as writedf:
        json.dump(df,writedf)


# SAVING DATA IN ` firebasedatabase `
def save_database():
    with open("UserData.json","r") as datafile:
            df = json.load(datafile)
    try:
        requests.post(
            f"{DATABASE_URL}/feedback.json",
            json=df
        )
    except Exception as e:
        add_error(e) # Store what was the error


# I forgot to make seprate function for opening and wrting UserData.json file
# Your Task : Fork this repo and add this function :)
