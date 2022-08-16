import pzt_config as c

'''
some abbreviations
RELW/RELH  -  relative width/relative height
RELX/RELY  -  relative X/relative Y
FOOT/FB  -  footer/footer button
LB  -  logobox
DD  -  dropdown section
BG/FG  -  backg/foreg
ABG/AFG  -  active backg/active foreg
HLT/HLBG  -  highlightthickness/highlightbackg
BD  -  border
'''

# path to letter and number database/dictionary files (binary)
letterdictionary = "reference/aldict.pkl"
digitdictionary = "reference/digitdict.pkl"
dictnote = (f"Dictionary from "
            f"github.com/dwyl/english-words")
# minimum length of words to flag in Caesar rotations
MINCAESARWORDLENGTH = c.MINIMUM_WORD_LENGTH
# general display and formatting
WIDTH = c.WIDTH
HEIGHT = c.HEIGHT
MINSIZE_FACTOR = 0.8
MAXSIZE_FACTOR = 1.4
BG1 = c.BACKGROUND1
BG2 = c.BACKGROUND2
FG1 = "black"
ABG_SPECIAL = "white"
AFG_SPECIAL = "purple"
AFG1 = "black"
AFG2 = "white"
HLBG = "black"
HLT = 2
BD = 0
ENTRYBOXTEXTCOLOR = FG1
ENTRYBOXBACKGROUND = ABG_SPECIAL
# font builder  -  all preceded with F
# currently based on starting width of window
FXXLARGE = (WIDTH // 30)
FXLARGE = (WIDTH // 40)
FLARGE = (WIDTH // 50)
FMEDIUM = (WIDTH // 60)
FSMALL = (WIDTH // 70)
FSMALLER = (WIDTH // 80)
FTINY = (WIDTH // 90)
FXTINY = (WIDTH // 100)
FTITLE = "Helvetica"
FPLAIN = "Arial"
FDATA = "Courier"
# logobox frame
LBRELW = .15
LBRELH = .1
LBX = 0
LBY = 0
LBLRELSIZE = 1
LBHLT = 0
# footer frame
FOOTRELW = 1
FOOTRELH = .04
FOOTRELX = 0
FOOTRELY = .96
# footer  -  quit button
FBRELW = .15
FBRELH = 1
FBRELX = 0
FBRELY = 0
FBBD = 0
FBHLT = 0
# dropdown menu section
DDRELH = .1
DDRELW = 1 - LBRELW
DDRELX = LBRELW
DDRELY = 0
DDMTOPBG = "silver"
DDMDROPABG = "white"
DDMABG = "dark gray"
DDMDROPAFG = AFG_SPECIAL
DDMRELW = .2
DDMRELH = .5
DDMRELX = .10
DDMRELY = .25
DDMHLT = 0
# sidebar section
SBRELW = LBRELW
SBRELH = 1 - LBRELH - FOOTRELH
SBRELY = LBRELH
SBRELX = 0
SBPLACERELH = 0.96
SBPLACERELW = 1
SBPLACERELY = .05
# main window frame
MWRELW = 1 - LBRELW
MWRELH = 1 - LBRELH - FOOTRELH
MWRELY = LBRELH
MWRELX = LBRELW
# entry box frame
ENTRYBOXWIDTH = 25
ENTRYBOXYPAD = 10
# tables
TABLEYPAD = 25
TABLEYPADNARROW = 10
# maximum allowed input num to avoid long processing time
# (may be adjustable in the future)
MAXNUMBER = 10000000

# MENUS / LISTS / DICTS
WORDSMENU = ["Anagram Comparison",
             "Caesar Shift",
             "Letter Representations",
             "Word Value Calculator",
             ]

NUMBERSMENU = ["Fun Facts",
               "# Representations",
               "Sequences"
               ]

EXTRASMENU = ["Links",
              "Reference Tables",
              ]

IMAGE_TITLE_MENU = ["ASCII",
                    "Dancing Man",
                    "Pentomino",
                    "Periodic Table",
                    "Semaphore",
                    "Sign Language",
                    "Braille Alphabet",
                    "Pigpen",
                    "Phone Pad",
                    "Morse Code",
                    "Solfa Cipher",
                    "Billiards & Darts",
                    "Maritime Flags"
                    ]

IMAGE_SOURCE_INFO = """∙ www.wikipedia.com (various)
∙ www.freepik.com (various)
∙ www.lookuptables.com/text/ascii-table
∙ cryptological.wordpress.com/2018/01/06/sherlock-holmes-the-dancing-men/
∙ flagsexpress.com/nautical-flags/code-of-signals/
∙ the-daily-dabble.com/morse-code-alphabet/
∙ www.wmich.edu/mus-theo/solfa-cipher/secrets/"""

LETTER_REPRESENTATION_MENU = ["Letter",
                              "Decimal",
                              "Binary",
                              "Ternary",
                              "Octal",
                              "Hex",
                              "Morse",
                              "ASCII cap",
                              "ASCII sm",
                              "NATO Phonetic",
                              "Scrb Val",
                              "Scrb Freq"]

# these start checked  - can be unchecked by user
LETTER_REPRESENTATION_DEFAULT_MENU = c.LETTER_REPRESENTATION_DEFAULT_MENU

NUMBER_REPRESENTATION_MENU = ["Number",
                              "Binary",
                              "Ternary",
                              "Octal",
                              "Hex",
                              "Morse",
                              "ASCII",
                              "Keyboard",
                              "Roman",
                              "Roman x10"]

# these start checked  - can be unchecked by user
NUMBER_REPRESENTATION_DEFAULT_MENU = c.NUMBER_REPRESENTATION_DEFAULT_MENU

NUMBER_SEQUENCES_MENU = ["Primes",
                         "Squares",
                         "Cubes",
                         "Fibonacci"]

# these start checked  - can be unchecked by user
NUMBER_SEQUENCES_DEFAULT_MENU = c.NUMBER_SEQUENCES_DEFAULT_MENU

LINKSDICT = {
    "Nutrimatic": "https://nutrimatic.org/",
    "Anagram Solver": "https://anagram - solver.net/",
    "Boxentriq": "https://www.boxentriq.com/",
    "Cyberchef": "https://cyberchef.org/",
    "Integer Sequences": "https://oeis.org/",
    "Dcode": "https://www.dcode.fr/",
    "Math calculators +": "https://www.toolmenow.com/",
    "MIT Puzzle Tool List": "https://puzzles.mit.edu/tools.html",
    "Crossword Parser": "https://www.npinsker.me/puzzles/crossword/",
    "Pokemon Pokedex": "https://www.pokemon.com/us/pokedex/",
    "Qat": "https://www.quinapalus.com/cgi - bin/qat?pat=&ent=Search&dict=0",
    "OneLook Dictionary": "https://onelook.com/",
    "Quinaplus": "https://www.quinapalus.com/cgi - bin/match?pat=*&ent=Search",
    "Regex Dictionary": "https://visca.com/regexdict/",
    "Unicode Search": "https://babelstone.co.uk/Unicode/whatisit.html",
    "Unicode Converter": "https://www.branah.com/unicode - converter",
    "What3Words": "https://what3words.com/adventuresome.orthodontic.moves",
    "Online Math Tools": "https://onlinemathtools.com/",
    "Online Photo Editor": "https://www.photopea.com/",
    "OneLook Thesaurus": "https://www.onelook.com/thesaurus/"
    }

SCRABBLE_POINT_DICTIONARY = {'A': 1, 'B': 3, 'C': 3,
                             'D': 2, 'E': 1,
                             'F': 4, 'G': 2, 'H': 4,
                             'I': 1, 'J': 8,
                             'K': 5, 'L': 1, 'M': 3,
                             'N': 1, 'O': 1,
                             'P': 3, 'Q': 10, 'R': 1,
                             'S': 1, 'T': 1,
                             'U': 1, 'V': 4, 'W': 4,
                             'X': 8, 'Y': 4, 'Z': 10}
