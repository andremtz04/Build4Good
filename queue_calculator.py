import time

# from human_detection import persons_detected

# persons_detected_prev = persons_detected # variable to compare new number of persons detected

class Queue_Calculator:
    # run_timer = False            # turns the analyzer on
    # timer = 0                    # keeps track of time in seconds
    # refreshes_per_second = 0      # frequency of refreshes

    def __init__(self, refreshes, time_per_person):
        self.refreshes_per_second = refreshes
        self.run_timer = False
        self.time_per_person = time_per_person # idk minutes

        # calculates estimated queue time #
    def estimated_queue_time(self, persons_detected): 
        # needs to calculate average time per person to estimate queue time

        return self.time_per_person * persons_detected.value

        # starts tracking per refresh how many people are in queue #
    def start_tracking(self, persons_detected): # takes in refresh rate of calculator
        self.run_timer = True
        time_per_refresh = 1 / self.refreshes_per_second
        
        while self.run_timer:
            queue_time = self.estimated_queue_time(persons_detected) # runs estimater with timer
            print("Estimated queue time:", queue_time)
            time.sleep(time_per_refresh)

        # stops tracking people in line #
    def stop_tracking(self):          
        self.run_timer = False