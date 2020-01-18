import re
import json
import ctypes, os
import logging

#sanitize the code for saving to a file on the OS
def get_valid_filename(s):

    """
    Stolen from Django, me thinks?
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """

    s = str(s).strip().replace(' ', '_')

    return re.sub(r'(?u)[^-\w.]', '', s)


def json_write(location, filename, dictio, sanitation=True):
    
    location = location.strip()

    if sanitation == True:
        filename = get_valid_filename(filename)
    
    location_filename = location + "/" + filename
    logging.debug(f"Saving to: {location_filename}")

    with open(f'{location_filename}', 'w') as outfile:
        json.dump(dictio, outfile)

def json_read(location, filename):
    
    location_filename = location + "/" + filename
    logging.debug(f"Reading from: {location_filename}")

    with open(f'{location_filename}') as json_file:
        data = json.load(json_file)
        
        return data

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def check_file_exists(filenameLocation):
    try:
        with open(filenameLocation) as f:
            return True
    except IOError:
        return False

if __name__ == "__main__":
    pass
    #print(isAdmin())
