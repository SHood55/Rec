# separator used by search.py, categories.py, ...
SEPARATOR = ";"

LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = "36fd27f08b5615d4" # "xxxxxxxxxxxxxxxx"
GOOGLE_LOGIN    = "wilhelmws@gmail.com" # "username@gmail.com"
GOOGLE_PASSWORD = "1.9.Alpha"
AUTH_TOKEN      = None # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

