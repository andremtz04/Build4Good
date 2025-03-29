import time
from back_end.human_detection import persons_detected, FRAMERATE

run_timer = False            # turns the analyzer on
timer = 0                    # keeps track of time in seconds

    # starts tracking per refresh how many people are in queue #
def start_timer(): # takes in refresh rate of calculator
    run_timer = True
    time_per_refresh = 1 / FRAMERATE
    
    while run_timer:
        estimated_queue_time(persons_detected) # runs estimater with timer
        time.sleep(time_per_refresh)

    # stops tracking people in line #
def stop_timer():          
    run_timer = False

    # calculates estimated queue time #
def estimated_queue_time(persons): 
    queue_time = persons
    
    return queue_time
    
    # needs to calculate average time per person to estimate queue time
    
def get_queue_time(): # allows the server to get the queue time
    return estimated_queue_time(persons_detected)