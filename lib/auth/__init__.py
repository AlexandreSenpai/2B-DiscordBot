###[BUILT-IN MODULES]###

########################
###[PERSONAL MODULES]###

########################
###[EXTERNAL MODULES]###
import dotenv
########################

class Auth(object):
    def __init__(self):
        self.__ENV_PATH = './lib/auth/.env'
        self.DISCORD_BOT_TOKEN = dotenv.get_key(self.__ENV_PATH, 'DISCORD_BOT_TOKEN')

if __name__ == '__main__':
    auth = Auth()
    print(auth.DISCORD_BOT_TOKEN)