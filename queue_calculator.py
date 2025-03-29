import time

from human_detection import persons_detected

run_timer = False            # turns the analyzer on
timer = 0                    # keeps track of time in seconds
refreshes_per_second = 0     # frequency of refreshes

    # starts tracking per refresh how many people are in queue #
def start_timer(refreshes_per_second): # takes in refresh rate of calculator
    run_timer = True
    time_per_refresh = 1 / refreshes_per_second
    
    while run_timer:
        estimated_queue_time(persons_detected) # runs estimater with timer
        time.sleep(time_per_refresh)

    # stops tracking people in line #
def stop_timer():          
    run_timer = False

    # calculates estimated queue time #
def estimated_queue_time(persons): 
    p = persons
    
    # needs to calculate average time per person to estimate queue time