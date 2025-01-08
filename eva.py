from circuit import RPI
from speech import TTS
from time import sleep
import string


class EVA:

    ### THESE ARE MODIFIABLE FOR PROGRAM ADJUSTMENTS
    end_string = "step loading (sky method)"  # this string represents the last cell that isnt part of this workout
    time_modifier = 60 #regular value for this is 60 (1min), only shouldn't be 60 for testing
    time_to_perform_exercise = 10 # in seconds
    time_to_tell_next_exercise = 15 # says what the next exercise is at "x" seconds 
    max_cell_length = 28 # this is the max cell length in the print to console function

    # workout data
    sets = 0 
    reps = 0
    load = 0 # in lbs
    pause = 0 # in minutes, if blank 2 min will be set
    alap = 0.6 # in minutes 0.6 = 36 sec

    workout_data = []  # stores the google sheets data in an array
    workout_type = ""
    workout_selected = False
    workouts = []  # stores the names of the workouts (ex. push - strength)

    def __init__(self):
        self.tts = TTS()
        self.rpi = RPI()

    def wipe_workout_data(self):
        self.workout_data.clear()
        self.workouts.clear()

    def load_workout_types(self, google_data):
        for line in google_data:
            if line[0].strip().lower() == self.end_string:
                break 
            if line[0].strip().lower() != "":
                self.workouts.append(line[0].lower().strip())


    def read_workout_from_csv(self, google_data):  # reads only the required wokrouts data and stores it in the array
        #google_data is in the form of an 2d string array

        append_to_file = False

        for line in google_data:
            if line[0].strip().lower() == self.workout_type:
                append_to_file = True
            elif line[0].strip().lower() == self.end_string:
                append_to_file = False
            elif line[0].strip().lower() in self.workouts:
                append_to_file = False
            
            if append_to_file:
                self.workout_data.append(line)

    def print_to_console(self, gui):  # prints the workout data to console
        for line in self.workout_data:
            sum_string = ""
            for cell_num in range(len(line)):

                cols_to_print = {1,2,4,5}  #only print these coloumns 
                if cell_num in cols_to_print:

                    if line[cell_num] == "":
                        sum_string += "[" + (" "*(self.max_cell_length//2)) + "]" #spaces when no value
                    else:
                        sum_string += "[" + line[cell_num][:self.max_cell_length] + "]"

            gui.lbl_add(sum_string + "\n")

    def select_workout(self, gui):
        try:

            #CONSOLE get input from console:
            # workout_num = int(input("\nPlease enter a number: "))
            workout_num = gui.wait_for_input()
                
            #if button pressed wasnt a number raise error
            if not isinstance(workout_num, int):
                raise ValueError

            workout_num -= 1
            if workout_num < 0: # if number is too low throw error
                raise IndexError

            self.workout_type = (self.workouts[workout_num].strip().lower())  
            # gets rid of spaces before and after

            if (self.workout_type in self.workouts):  
                # if the workout_type is expected break
                gui.lbl_add(f"\n<{self.workout_type.lower()}> selected")
                self.tts.speak(f"{self.workout_type.lower()} workout selected")
            else:
                gui.lbl_print("Fatal Error: workout not in self.workouts")
                self.tts.speak("fatal error. failed to find workout in the list of workouts... exiting")
                exit()

            self.workout_selected = True # this causes the loop in the main func to not repeat

        except ValueError:
            gui.lbl_add("\n\nError: the input was not a number")
            self.tts.speak("sorry i didn't understand that. please enter a number")
        except IndexError:
            gui.lbl_add("\n\nError: the input number was too high or too low")
            self.tts.speak("sorry the number entered was too high or too low")


    def get_sets_reps(self, sets_reps, gui):
        try:
            sets_reps = sets_reps.lower().replace(" " ,"")

            if sets_reps == "":
                self.sets = 1
                self.reps = 1
            else:
                sets_reps = sets_reps.split('x')
                self.sets = 0
                self.reps = 0

                for halfline in sets_reps: #this loop loads the sets and reps variables
                    if "set" in halfline: # halfline exmaple: "4rep"
                        for c in halfline:
                            if c.isdigit(): 
                                self.sets = self.sets*10 + int(c)

                    if "rep" in halfline:
                        for c in halfline:
                            if c.isdigit():
                                self.reps = self.reps*10 + int(c)

            #some cells dont have sets/reps, this defaults to 1 if theres no data
            if self.reps == 0: self.reps = 1 
            if self.sets == 0: self.sets = 1
                
        except Exception as ex:
            gui.lbl_print(f"Fatal Error: could not load 'sets reps' data\n{ex}")
            self.tts.speak("fatal error. could not load sets and reps data... exiting")
            exit()

    def get_pause(self, pause_data, gui):
        #pause_data exmaple = " 3 "
        try:
            pause_data = pause_data.lower().replace(" ", "")
            if pause_data == "":
                self.pause = 2 # 2 min is the default value when its left blank
            elif pause_data == "alap": 
                self.pause = self.alap #change the alap value at the top of the code 0.5 = 30 sec
            else:
                self.pause = float(pause_data)

        except Exception as ex:
            gui.lbl_print(f"Fatal Error: could not load 'pause' data\n{ex}")
            self.tts.speak("fatal error. could not load pause data... exiting")
            exit()

    def get_load(self, load_data, gui):
        try:
            cleaned_data = ""
            for i in range(len(load_data)):
                if load_data[i].isdigit() or load_data[i] == '.':
                    cleaned_data += load_data[i]
        
            if cleaned_data == "":
                self.load = 0
            else:
                self.load = float(cleaned_data)

        except Exception as ex:
            gui.lbl_print(f"Fatal Error: could not load load data\n{ex}")
            self.tts.speak("fatal error. could not load load data... exiting")
            exit()

    def say_upcoming_exercise(self, line, gui):

        if len(self.workout_data) != line+1: # this line prevents this function from activating on the last exercise

            self.get_sets_reps(self.workout_data[line+1][4], gui) #momentarily loads the next exercises data
            self.get_load(self.workout_data[line+1][2], gui)

            if self.reps ==1 and self.load==0:
                self.tts.speak(f"Upcoming: {self.workout_data[line+1][1].strip()}. {self.reps} rep")
            elif self.reps !=1 and self.load==0:
                self.tts.speak(f"Upcoming: {self.workout_data[line+1][1].strip()}. {self.reps} reps")
            elif self.reps ==1 and self.load!=0:
                self.tts.speak(f"Upcoming: {self.workout_data[line+1][1].strip()}. {self.load} lbs. {self.reps} rep")
            else:
                self.tts.speak(f"Upcoming: {self.workout_data[line+1][1].strip()}. {self.load} lbs. {self.reps} reps")

            self.get_sets_reps(self.workout_data[line][4], gui) #reload the orignal data
            self.get_load(self.workout_data[line][2], gui)

    def test_pause_button(self, gui):
        if gui.btn_num == "pause": #hold button until beep to pause
            gui.lbl_add("          <PAUSED>")
            self.rpi.beep(0.2)
            gui.btn_num = -1 # reset btn since we need to check for another input
            
            while True:
                sleep(0.01)
                if gui.btn_num == "pause": #repress to unpause
                    gui.btn_num = -1 # reset btn
                    self.rpi.beep(0.2)
                    break

    def is_skip_button_pressed(self, line, current_set, gui):
        if gui.btn_num == "skip": #hold button until beep to skip
            gui.btn_num = -1 # reset btn
            self.rpi.beep(0.15)
            sleep(0.85)
            self.tts.speak("Set skipped")

            if current_set+1 == self.sets: #if the last set for this exercise than tell next exercise
                self.say_upcoming_exercise(line, gui)
                self.tts.speak("in 10 seconds")
            else:
                self.tts.speak("Next set in 10 seconds")

            total_time = 10 # begin a countdown to the skipped exercise
            for itime in range(total_time):
                gui.lbl_print(f"Timer: {int(total_time) - itime}")
                self.count_down(total_time, itime) #beep for the last few seconds of the countdown
                self.test_pause_button(gui) # pause the program if the pause button is pressed
            return True
        return False


    def count_down(self, total_time, itime):
        if total_time-itime == 3 or total_time-itime == 2 or total_time-itime == 1:
            self.rpi.beep(0.15) 
            sleep(0.85)
        else:
            sleep(1)

    def start_workout(self, gui):
        for line in range(len(self.workout_data)):

            if self.workout_data[line][1].lower().strip() != "exercise" or "": # skips the first line

                self.get_sets_reps(self.workout_data[line][4], gui) 
                self.get_pause(self.workout_data[line][5], gui)
                self.get_load(self.workout_data[line][2], gui)

                for current_set in range (self.sets): 

                    # lbl_output is the full string that is printed to the screen
                    lbl_output_p1 = f"Exercise: {self.workout_data[line][1].strip()}\nReps: {self.reps}, Sets: {current_set+1}/{self.sets}\nLoad: {self.load} lbs"
                    total_time = self.pause * self.time_modifier + self.time_to_perform_exercise

                    for itime in range(int(total_time)): #itime is the numbers of seconds between sets
                        lbl_output = lbl_output_p1 +  f"\n\nTimer: {int(total_time) - itime}"
                        gui.lbl_print(lbl_output)

                        #say what the upcoming exercise is when its the last set
                        if total_time-itime == self.time_to_tell_next_exercise and current_set+1==self.sets:
                            self.say_upcoming_exercise(line, gui)
            
                        self.count_down(total_time, itime) #beep for the last few seconds of a set       #TIME.SLEEP(1) is in count_down
                        self.test_pause_button(gui) # pause the program if the pause button is pressed

                        if self.is_skip_button_pressed(line, current_set, gui): #skips the current set when pressed
                            break
