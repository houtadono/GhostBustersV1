import datetime
import pickle

class User:
    def __init__(self, name, player,score, time, die) -> None:
        self.name, self.player, self.score, self.time, self.die = name, player, score, datetime.timedelta(seconds= time), die
        pass
    def __lt__(self, other):
        if isinstance(other, User):
            if self.score == other.score:
                if self.time == other.time:
                    return self.die < other.die
                return self.time < other.time
            return self.score < other.score
        return False
    def __str__(self) -> str:
        return f"{self.name}|{self.player}|{self.time}|{self.die}|{self.score}"

class Scoreboard:
    lst = []
    @staticmethod
    def read_file():
        with open("./Data/scoreboard", "rb") as f:
            try:
                Scoreboard.lst = pickle.load(f)
            except:
                Scoreboard.lst = [User('NoName','Hacker',1000,200,2)]*5

    @staticmethod
    def add_user(user):
        Scoreboard.lst.append(user)
        Scoreboard.lst.sort(reverse=True)
        while len(Scoreboard.lst) > 5: Scoreboard.lst.pop()
        if user in Scoreboard.lst:
            return Scoreboard.lst.index(user)
        return None
    
    @staticmethod
    def save_file():
        with open("./Data/scoreboard", "wb") as f:
            pickle.dump(Scoreboard.lst, f)
    
        
