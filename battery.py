""" Initializes and resets global variables for a simulation """
def initialize():
    global cur_temp 
    global cur_charge 
    global cur_time
    global good_battery_health 

# "default settings", as provided in the handout
    cur_temp = 20 
    cur_charge = 50
    cur_time = 0
    good_battery_health = True

# required for our implementation of battery health 
    global charge_history
    charge_history = [-360, -360, -360]

""" Simulates an 'activity' (str) for 'duration' (int) minutes """
def simulate_activity(activity, duration):
# all of these variables may need to be accessed / modified
    global cur_temp 
    global cur_charge 
    global cur_time 
    global good_battery_health

# code to simulate charging the battery
    if activity == "charge": 

    # useful for later, when we deal with bad battery health
        start_charge = cur_charge
        was_healthy = good_battery_health

    # charge the battery
        fast_minutes = duration_fast_charge_possible()
        if fast_minutes >= duration:
            cur_charge += 3 * duration
            cur_temp += 0.5 * duration
        else: 
            slow_minutes = duration - fast_minutes
            cur_charge += 3 * fast_minutes + slow_minutes
            cur_temp += 0.5 * fast_minutes + 0.25 * slow_minutes

    # update time
        cur_time += duration 

    # now we check if the battery health changed...
        if cur_charge >= 90:
        # cycles the charge history. alternatively you could expand the list
            charge_history[2] = charge_history[1]
            charge_history[1] = charge_history[0]
            charge_history[0] = cur_time - (cur_charge - 90) # (...) is time passed AFTER reaching 90
            if charge_history[0] - charge_history[2] < 360: # 3 times in 6 hours!
                good_battery_health = False

    # fix overflow battery health values
        if good_battery_health: # good battery health
            cur_charge = min(cur_charge, 100) # can't go over 100
        elif was_healthy: # turned bad during this session
            cur_charge = min(cur_charge, max(start_charge, 90)) # can't go over 90
        else: # already bad 
            cur_charge = min(cur_charge, max(start_charge, 80)) # can't go over 80
    # basically if start_charge is above the cap it stays there

# code to simulate using the battery
    elif activity == "use":

    # update time
        cur_time += duration 

    # minutes alive, using 2% charge per minute
        minutes_alive = cur_charge / 2

    # use the battery
        if duration > minutes_alive: # battery will die during usage
            cur_temp += minutes_alive - (duration - minutes_alive) # (...) is time since battery death
            cur_charge = 0 # battery is dead
        else:
            cur_charge -= 2 * duration 
            cur_temp += duration 

# code to simulate idling the battery 
    elif activity == "idle":

    # update time
        cur_time += duration 

    # idle the battery
        cur_temp -= duration # idling & dead lose temperature at the same rate
        cur_charge -= 0.5 * duration 

    # temperature & battery cannot drop below 0
        cur_temp = max(0, cur_temp)
        cur_charge = max(0, cur_charge)

""" Returns the duration of fast charge possible before switching to slow """
def duration_fast_charge_possible():
    if good_battery_health and cur_temp <= 40 and cur_charge < 80:
        return min((80 - cur_charge) / 3, 2 * (40 - cur_temp)) # gets durations for both slow charge conditions
    return 0 # cannot undergo fast charging

""" Returns the current temperature, cur_temp """
def get_cur_temp():
    return cur_temp 

""" Returns the current charge, cur_charge """
def get_cur_charge():
    return cur_charge 

""" Returns the state of the battery health, good_battery_health, as a Boolean """
def get_cur_battery_health():
    return good_battery_health 

""" Returns the amount of charge time needed to use the battery for 'minutes' minutes """
def charge_time_needed(minutes):

# no longer need to type 2 * minutes everywhere 
    needed_charge = 2 * minutes

# obvious cases
    if needed_charge <= cur_charge: # already have enough charge
        return 0
    if needed_charge > 100 or (not good_battery_health and needed_charge > 80): # impossible
        return None

# useful values to have, easier to read code
    fast_minutes = duration_fast_charge_possible() 
    charge_gap = needed_charge - cur_charge # amount we need to charge

# logic here
    if charge_gap <= 3 * fast_minutes: # ONLY fast charging
        return charge_gap / 3
    return fast_minutes + (charge_gap - 3 * fast_minutes) # fast charging + remaining amount of slow charging

""" Runs test cases """
if __name__ == '__main__':
    initialize()

    print(duration_fast_charge_possible()) # 10
    print(charge_time_needed(50)) # 30

    simulate_activity("charge", 30)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 30

    simulate_activity("use", 50)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 80

    simulate_activity("use", 10)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 70

    simulate_activity("charge", 100)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 95

    simulate_activity("idle", 100)
    print(get_cur_charge()) # 50
    print(get_cur_temp()) # 0
    print(get_cur_battery_health()) # True
    print(duration_fast_charge_possible()) # 10

    simulate_activity("charge", 80)
    print(get_cur_charge()) # 90
    print(get_cur_temp()) # 22.5
    print(get_cur_battery_health()) # False

    simulate_activity("use", 40)
    print(get_cur_charge()) # 10
    print(get_cur_temp()) # 62.5

    simulate_activity("charge", 80)
    print(get_cur_charge()) # 80
    print(get_cur_temp()) # 82.5

    initialize()
    # add your tests here