###########################################################
#    _____              _ _             _ _    /\ ___    #
#   / ____|            | (_)           | (_)  |/\|__ \   #
#  | |     __ _ _ __ __| |_ _ __   __ _| |_ ___     ) |  #
#  | |    / _` | '__/ _` | | '_ \ / _` | | / __|   / /   #
#  | |___| (_| | | | (_| | | | | | (_| | | \__ \  / /_   #
#   \_____\__,_|_|  \__,_|_|_| |_|\__,_|_|_|___/ |____|  #
#                                                        #
##########################################################                                                      
# beerware license - do whatever you want with this crap #
##########################################################

# import stuff
import twitter
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# setup pins
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)
GPIO.setup(24, GPIO.IN) #, pull_up_down = GPIO.PUD_DOWN)

#init into admin mode and set some other mode stuff
dirs = ["forward", "stop", "left", "right"]
modes = ["monarchy", "democracy", "anarchy"]
mode = "monarchy"
prev_admin = ""
prev_demo = ""

# init twitter API with key
api = twitter.Api(consumer_key="REDACTED", consumer_secret="REDACTED", access_token_key="REDACTED", access_token_secret="REDACTED")

def set_pins(pin1, pin2):
    '''simple function to set direction pins.
       directions are
       Stop | 00
       Forw | 11
       Right| 01
       Left | 10'''

    GPIO.output(18, pin1)
    GPIO.output(23, pin2)

def set_mode(admin_tweet):
    for mode in modes:
        if mode in admin_tweet:
            return mode

def get_admin_tweet():
    return api.GetUserTimeline("EDL_2015")[0].text

def set_dir(command):
    print "setting direction: " + command
    if command is "forward":
        set_pins(True, True)
    elif command is "stop":
        set_pins(False, False)
    elif command is "left":
        set_pins(True, False)
    elif command is "right":
        set_pins(False, True)
    return

# loop... FOREVER ever
# ever
while True:
    # testmode
    if (GPIO.input(4) == 1):
        print "Arduino Ready: "
        if mode is "monarchy":
            print "Starting mode: monarchy"

            # get the admin tweet text
            admin_tweet = get_admin_tweet()

            # if it's a new tweet, execute it
            if admin_tweet != prev_admin:
                print "new tweet found."
                for direction in dirs:
                    if direction in admin_tweet:
                        print "direction found: " + direction
                        set_dir(direction)

            # save the previous admin tweet object
            prev_admin = admin_tweet

            # give arduino time to get command
            time.sleep(1)

            # reset
            set_dir("stop")
        elif mode is "anarchy":
            print "Starting mode: anarchy"

            # search the hashtag
            commands = api.GetSearch(term = "#EDL_2015")

            # break var. You can't break outer loops with
            # python, which makes this difficult.
            brk = False

            # set the dir with the most recent valid
            # tweet.
            for command in commands:
                command = command.text
                print "parsing: " + command
                if brk = False:
                    for item in dirs:
                        if item in command:
                            print "Found dir: " + item
                            set_dir(item)
                            brk = True
                            break
                else:
                    break

            # give arduino time to get command
            time.sleep(1)
        
            # reset
            set_dir("stop")

        elif mode is "democracy":
            tweets = api.GetSearch(term = "#EDL_2015")
            right = 0;
            left = 0;
            forw = 0;

            # set a reasonable limit for parsable tweets,
            # starting with the top few
            if len(tweets) > 50:
                tweets = tweets[0:49]

            # just increment counts
            for tweet in tweets:
                text = tweet.text
                if prev_demo == text:
                    break
                print "parsing tweet: " + text
                if "right" in text:
                    right = right + 1
                if "left" in text:
                    left = left + 1
                if "forward" in text:
                    forward = forward + 1
            if forw > right and forw > left:
                set_dir("forward")
            elif right > forw and right > left:
                set_dir("right")
            elif left > forw and left > right:
                set_dir("left")
            else:
                set_dir("stop")

            # don't want to count duplicates
            prev_demo = tweets[0].text

            # give arduino time to get command
            time.sleep(1)

            # reset
            set_dir("stop")

        mode = set_mode(get_admin_tweet())

# ever
