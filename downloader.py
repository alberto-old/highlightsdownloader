import datetime
import os
import ConfigParser
import progressbar

from instapaper import Instapaper, Folder

# Init instapaper with key, secret, login and password
def init():
    # Read credentials from Credentials.ini file
    configParser = ConfigParser.RawConfigParser()
    configParser.read('Credentials.ini')

    key = configParser.get('Instapaper', 'INSTAPAPER_KEY')
    secret = configParser.get('Instapaper', 'INSTAPAPER_SECRET')
    login = configParser.get('Login', 'INSTAPAPER_LOGIN')
    password = configParser.get('Login', 'INSTAPAPER_PASSWORD')

    # Create instance of Instapaper using the OAth credentials
    instapaper = Instapaper(key, secret)

    # Login with user and password
    instapaper.login(login, password)

    return instapaper

# Function to change to highlights folder
def change_to_highlights_folder():
    # If there is no folder in the system with highlights then create it
    if not os.path.exists('highlights'):
        os.makedirs('highlights')

    # Change to the folder
    os.chdir('highlights')

# Change to folder using the folder_id
def change_to_folder(folder_id):
    # Folder name = its folder_id
    folder = str(folder_id)

    # If there is no folder in the system for this folder_id then create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Change to the folder
    os.chdir(folder)

def get_list_of_existing_highlights():
    existing = []

    # Get all .md files in current directory
    for file in os.listdir('.'):
        if file.endswith('.md'):
            existing.append(int(os.path.splitext(file)[0]))

    return existing

# Process bookmarks in one folder
def process_folder(folder):
    # Show id and title of the folder
    print "Processing folder", folder.title, "(id:", folder.folder_id, ")"

    change_to_folder(folder.folder_id)

    existing = get_list_of_existing_highlights()

    # Get bookmarks from the current folder using its folder_id
    # TODO: identify which bookmarks have been processed and pass their ids
    # as parameter to this function as 'have'. Current library does not allow
    # this functionality, needs to be updated
    bookmarks = instapaper.get_bookmarks(folder=folder.folder_id, have=existing, limit=500)

    process_bookmarks(bookmarks)

# Process list of bookmarks
def process_bookmarks(bookmarks):
    progress = progressbar.ProgressBar(max_value=len(bookmarks))
    i = 1
    for bookmark in bookmarks:
        process_bookmark(bookmark)
        progress.update(i)
        i = i + 1

# Process the highlights of one bookmark
def process_bookmark(bookmark):
    # Get the highlights
    highlights = bookmark.get_highlights()

    # If there is any highlight
    if len(highlights) > 0:
        # Check if the bookmark has been already processed
        # TODO: we would not need this if the 'have' parameter is used
        # in the call to get_bookmarks
        if not os.path.exists(str(bookmark.bookmark_id) + ".md"):
            # Show that we have found a new bookmark with highlights
            print "New highlight file: " + str(bookmark.bookmark_id) + ".md"

            # Create the file
            new_file = open(str(bookmark.bookmark_id) + ".md", "w")

            # Add the title and reference url
            new_file.write('# ' + bookmark.title.encode('utf-8') + '\n')
            new_file.write('[Reference]' + '(' + bookmark.url.encode('utf-8') + ')\n\n')

            # Write each highlight to the file, adding a line between them
            for highlight in highlights:
                new_file.write(highlight.text.encode('utf-8') + '\n\n')
            new_file.close()

# ----------------------------------
# Init Instapaper
instapaper = init()

# Change to highlights folder
change_to_highlights_folder()

# Get all folders
folders = instapaper.get_folders()

# Process each folder
for folder in folders:

    process_folder(folder)

    # Change to the root folder
    os.chdir('..')
