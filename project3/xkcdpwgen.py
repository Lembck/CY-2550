import sys
import random

# CONSTANTS

PARAMETERS = sys.argv[1:]
default_parameters = {"WORDS": 4, "CAPS": 0, "NUMBERS": 0, "SYMBOLS": 0}
OVERRIDES = ["-w", "-c", "-n", "-s", "--words", "--caps", "--numbers", "--symbols"]
NUMBERS = "0123456789"
SYMBOLS = "~!@#$%^&*():;.,<>?+="
HELP_MESSAGE = '''
usage: xkcdpwgen [-h] [-w WORDS] [-c CAPS] [-n NUMBERS] [-s SYMBOLS]
                
Generate a secure, memorable password using the XKCD method
                
optional arguments:
    -h, --help            show this help message and exit
    -w WORDS, --words WORDS
                          include WORDS words in the password (default=4)
    -c CAPS, --caps CAPS  capitalize the first letter of CAPS random words
                          (default=0)
    -n NUMBERS, --numbers NUMBERS
                          insert NUMBERS random numbers in the password
                          (default=0)
    -s SYMBOLS, --symbols SYMBOLS
                          insert SYMBOLS random symbols in the password
                          (default=0)'''

#retrieve words from words.txt
def retrieve_words():
    with open("words.txt", "r") as f:
        return f.readlines()

WORDS = retrieve_words()

#parse parameters according to XKCD specifications
def parse_parameters():
    final_parameters = default_parameters

    if "-h" in PARAMETERS or "--help" in PARAMETERS:
        print(HELP_MESSAGE)
        return False
    
    while len(PARAMETERS) >= 2:
        p1 = PARAMETERS.pop(0)
        p2 = PARAMETERS.pop(0)

        if p1 not in OVERRIDES:
            continue

        if not p2.isnumeric() or int(p2) < 0:
            continue
        
        if p1 == "-w" or p1 == "--words":
            final_parameters["WORDS"] = p2
        elif p1 == "-c" or p1 == "--caps":
            final_parameters["CAPS"] = p2
        elif p1 == "-n" or p1 == "--numbers":
            final_parameters["NUMBERS"] = p2
        elif p1 == "-s" or p1 == "--symbols":
            final_parameters["SYMBOLS"] = p2

    return final_parameters
            

#pick a random word
def pick_random_word():
    random_word_index = random.randrange(0, len(WORDS))
    return WORDS[random_word_index][:-1]

#insert a given character into a random spot in a given string
def insert_randomly(string, char):
    index = random.randrange(0, len(string)+1)
    return string[:index] + char + string[index:]

#main function
def main():
    parsed_parameters = parse_parameters()
    if not parsed_parameters:
        return False
    
    word_count, caps_count, nums_count, syms_count = map(int, parsed_parameters.values())

    #Get words
    my_words = []
    for word in range(int(word_count)):
        my_words.append(pick_random_word())

    #Handle caps
    if caps_count != 0:
        if caps_count > word_count:
            caps_count = word_count

        while caps_count > 0:
            my_random_word_index = random.randrange(0, len(my_words))
            my_random_word = my_words[my_random_word_index]
            if my_random_word[0] != my_random_word[0].upper():
                my_words[my_random_word_index] = my_random_word[0].upper() + my_random_word[1:]
                caps_count -= 1

    #Handle Numbers & Symbols
    spots = [""] * (len(my_words) + 1)
    
    while nums_count > 0:
        my_num = str(random.choice(NUMBERS))
        spot = random.randrange(0, len(spots))
        spots[spot] = insert_randomly(spots[spot], my_num)
        nums_count -= 1

    while syms_count > 0:
        my_sym = str(random.choice(SYMBOLS))
        spot = random.randrange(0, len(spots))
        spots[spot] = insert_randomly(spots[spot], my_sym)
        syms_count -= 1
    
    my_words.append("") #making spots and my_words equal length for zip
    
    final_password = "".join([item for pair in zip(spots, my_words) for item in pair])


    return final_password
    
if __name__ == "__main__":
    print(main())
