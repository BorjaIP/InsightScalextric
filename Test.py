from Insight import *
from arduinoCom import *
from datetime import datetime

# -------------------------------------------------------------------------
# Make dictionary for logEmoState

header = ['Time', 'UserID', 'wirelessSigStatus', 'Blink', 'leftWink',
          'rightWink', 'Surprise', 'Frown',
          'Smile', 'Clench',
          'MentalCommand Action', 'MentalCommand Power']
emoStateDict = {}
for emoState in header:
    emoStateDict.setdefault(emoState, None)

def send_emo_state_to_arduino():

    action = "Action - Push"
    power = insight.get_mental_command_current_action_power(insight.eState)
    power = power * 255

    #print power
    valToArduinoSimple(power,action)

# # -------------------------------------------------------------------------
#
# # connect to Arduino

setupSerial()

# -------------------------------------------------------------------------
# start EmoEngine or ControlPanel

print "==================================================================="
print "Example to show how to log EmoState from EmoEngine/ControlPanel."
print "==================================================================="
print "Press '1' to start and connect to the EmoEngine                    "
print "Press '2' to connect to the ControlPanel                            "
print ">> "

log_from_emo = int(raw_input())
# -------------------------------------------------------------------------

# instantiate Insight class
if log_from_emo == 1:
    insight = Insight()
elif log_from_emo == 2:
    insight = Insight(composerConnect=True)
else:
    print "option = ?"

# connect insight instance to Xavier composer or EmoEngine
insight.connect()
last_command = None

# event loop to update Insight state
while (1):
    # set of operations to get state from Insight
    # returns 0 if successful
    state = insight.get_state(insight.eEvent)
    if state== 0:
        # event types IEE_Event_t returns 64 if EmoStateUpdated
        eventType = insight.get_event_type(insight.eEvent)
        user_ID = insight.get_userID(insight.eEvent, insight.user)
        if eventType == 64:
            insight.get_engine_event_emo_state(insight.eEvent, insight.eState)
            timestamp = insight.get_time_from_start(insight.eState)
            print "Time:%10.3f User: %d \r" % (timestamp, user_ID)
            print
                
            # Limit the command rate so that we won't overflow the buffer
            if not last_command:
                last_command = datetime.now()
                send_emo_state_to_arduino()
            else:
                diff = datetime.now()-last_command
                #if (diff.microseconds/100.0 > 50.0):
                last_command = datetime.now()
                send_emo_state_to_arduino()

    elif state != 0x0600:
        print "Internal error in Emotiv Engine ! "