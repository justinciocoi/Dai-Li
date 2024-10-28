import json

def calculate_task_averages(input):
    with open(input, "r") as file:
        data = json.load(file)

    # gather task data
        # 2 possible approaches
            #iterate through json each time (time consuming but easier to implement)
            #keep a counter for each task each time you log
