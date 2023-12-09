import json

##########################
### Database Functions ###
##########################

# Function to save bookmarks
def save_bookmarks_to_file(brwsr, filename='db/bookmarks.json'):
    with open(filename, 'w') as file:
        json.dump(brwsr.bookmarks, file)

# Function to load bookmarks
def load_bookmarks_from_file(brwsr, filename='db/bookmarks.json'):
    try:
        with open(filename, 'r') as file:
            brwsr.bookmarks = json.load(file)
    except FileNotFoundError:
        pass

# Function to save the history
def save_history_to_file(brwsr, filename='db/history.json'):
    with open(filename, 'w') as file:
        json.dump(brwsr.history, file)

# Function to save the visit counts
def save_visits_to_file(brwsr, filename='db/visits.json'):
    with open(filename, 'w') as file:
        json.dump(brwsr.visits, file)
