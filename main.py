from eva import EVA
from google_sheets_data import GoogleData
from circuit import RPI
from speech import TTS
from time import sleep
from gui import GUI
import threading

# this is the auto launch file/directory on the rpi3a+
# @python3 /home/eva/rpi/EVA/main.py 

def main():

    # instantiate text to speech, gui, and eva objects
    tts = TTS()
    eva = EVA()
    gui = GUI()

    #start the GUI with psuedo hyperthreading so it can run simultaneously
    threading.Thread(target=gui.start_window).start()

    #this waits for lbl object to be initialized because it is needed for lbl_print()
    #FIX FOR:if its not initialized because too slow then next line will crash program
    while gui.lbl_initialized == False: 
        sleep(0.1) 

    # intro
    gui.lbl_print("Welcome to EVA: \n\nE xercise\nV irtual\nA ssistant\n")
    tts.speak("welcome to Eyva... your virtual exercise assistant")

    # loads workouts array
    tts.speak("fetching/reading google data")
    gui.lbl_print("fetching file from google sheets api...")
    gd = GoogleData() #fetch data from google sheets and pass it to read wokrout
    gd_array = gd.get_google_data()
    gui.lbl_add("\nfile succesfully received")
    
    gui.lbl_add("\n\nloading available workouts...")
    eva.load_workout_types(gd_array); # load workouts from spreadsheet
    gui.lbl_add("\nworkouts loaded")
    tts.speak("workouts loaded")


    # workout selection
    tts.speak("please select a workout")
    # loop until the workout is correctly selected by the user
    while eva.workout_selected == False: 
        gui.lbl_print("Your Options:\n\n")
        for i in range(len(eva.workouts)):
            gui.lbl_add(f'{i+1}. {eva.workouts[i]}\n')

        eva.select_workout(gui)
    #CONSOLE:
    # eva.select_workout()

    # loads the chosen workouts data in workout_data
    gui.lbl_print("reading workout data...")
    eva.read_workout_from_csv(gd_array)
    gui.lbl_add("\nfile successfully read")
    gui.lbl_add("\nworkout data successfully loaded")


    # loop for asking user if they want to begin this workout
    gui.lbl_print("") # needs to be reset for this function
    eva.print_to_console(gui) #display loaded data

    while True:
        tts.speak("would you like to begin this workout?")
        gui.lbl_add("\nwould you like to begin this workout? (YES/NO)")
        string_in = gui.wait_for_input()
        if string_in == "y":
            break
        elif string_in == "n": #restarts the program if "n" #TODO not working correctly#TODO
            eva.wipe_workout_data()
            del gui # destroys the current window for the restart
            main()
            exit()
        else:
            gui.lbl_add("\nError: invalid entry. not y or n")
            tts.speak("sorry i didn't understand that. please respond with y or n")
            

    gui.lbl_print("\n\nStarting Workout...\n") #this time before the first set starts

    #tells what the first exercise is
    eva.say_upcoming_exercise(0, gui)

    tts.speak("starting workout in 10 seconds...")
    rpi = RPI()
    for i in range(10,0,-1):
        gui.lbl_print(f"First set in: {i} ")
        
        if i == 3 or i == 2 or i == 1:
            rpi.beep(0.15) 
            sleep(0.85)
        else:
            sleep(1)

    gui.lbl_print("GO!!!")
    tts.speak("GO!")
    eva.start_workout(gui)

    gui.lbl_print("\nWorkout complete! Great job!")
    tts.speak("Workout complete! Great job!")

main()
