import random

class user_agent_tool():
    def __init__(self):
        self.user_agent_list = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN'
        ]

    def get_user_agent(self):
        user_agent_list = self.user_agent_list
        random.shuffle(user_agent_list)
        return user_agent_list[0]