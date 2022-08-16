from functools import partial
import tkinter as tk
import inflect
import pickle
from PIL import ImageTk, Image
from tktooltip import ToolTip
import pzt_ancillary as a
from pzt_helper import *   # MISCELLANEOUS, NUMBER, AND WORD FUNCTIONS


class PuzzleTools:
    '''main class for the puzzle tools application'''
    def __init__(self):
        self.root = tk.Tk()
        self.set_up()

    def run(self):
        '''initiate collection of user input from display'''
        self.root.mainloop()

    def set_up(self):
        '''opening display of root window'''
        iconimage = 'images/toolboxFavicon-16x16.png'
        self.root.title("PuzTools")
        self.root.iconphoto(True,
                            tk.PhotoImage(file=iconimage))
        self.root.geometry(f'{a.WIDTH}x{a.HEIGHT}')
        # vertical dimension is adjustable within limits; width is fixed
        self.root.minsize(round(a.WIDTH),
                          round(a.HEIGHT * a.MINSIZE_FACTOR))
        self.root.maxsize(round(a.WIDTH),
                          round(a.HEIGHT * a.MAXSIZE_FACTOR))
        self.logobox_update()
        self.quit_button()
        self.drop_down_menus()
        self.firstmessage("Welcome to PuzTools by Tam")
        self.place_borderless_sidebar()
        self.place_footer("CS50p Final Project 2022")

    # DO WORDS SECTION
    def do_words(self, *args):
        todo = args[0]
        self.logobox_update(f'WORDS\n{todo}')
        self.drop_down_menus()
        if "Value" in todo:
            self.do_word_value()
        if "Caesar" in todo:
            self.do_Caesar_rotations()
        if "Anagram" in todo:
            self.do_anagram_compare()
        if "Represent" in todo:
            self.do_letter_representations()

    # Word Value Functions
    def do_word_value(self, *args):
        '''
        draws screen for wv entry, collects input, sends to wvcalc
        '''
        l1 = "Enter a word"
        l2 = "(Non-alphabetic characters will be ignored)"
        sb, wvmain, wvinput = self.make_top_area_with_entry_box(l1, l2)
        wvinput.bind('<Return>', lambda event: (wvcalc(event, wvinput.get()),
                                                wvinput.delete(0, 'end')))
        self.place_footer('')

        def wvcalc(self, word):
            '''
            subfunction for collection and display of results
            '''
            finalword, results = triple_word_value_calc(word)
            outputframe = MainWindow(wvmain)
            outputframe.place(relwidth=1,
                              relheight=1,
                              relx=0,
                              rely=.18)
            if not finalword:
                l3 = RegLabel(outputframe, text="Please enter a word.",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()

            else:
                finalwordlabel = RegLabel(outputframe,
                                          text=finalword,
                                          font=f'{a.FTITLE} {a.FMEDIUM} bold')
                finalwordlabel.pack()
                # tabular results for 3 word value calculations
                rows = 1
                columns = 2
                header = ("Scale", "Value")
                width = {0: 14, 1: 6}
                h = TableHeader(outputframe, width=width,
                                rows=rows, columns=columns)
                h.pack(pady=(a.TABLEYPADNARROW, 0), padx=(0, 30), fill='y')
                for i in range(len(header)):
                    h.set(0, i, header[i])
                rows = 3
                t = RegularTable(outputframe, width=width,
                                 rows=rows, columns=columns)
                t.pack(pady=(a.TABLEYPADNARROW//2,
                             a.TABLEYPADNARROW),
                       padx=(0, 30))
                for i in range(rows):
                    for j in range(columns):
                        t.set(i, j, results[i][j])
                do_dict_options(results)

        def do_dict_options(results):
            '''
            fills sidebar with WV sidebar widget
            buttons for view or download of lists of words for each scale
            button to submit an alternate word value
            '''
            sb = SideBar(self.root)
            sb.place(relwidth=a.SBRELW,
                     relheight=a.SBRELH,
                     rely=a.SBRELY,
                     relx=a.SBRELX)
            sbheaderl = RegLabel(sb,
                                 text=f"View or download\nlist of words\n"
                                 f"with indicated\nword value:",
                                 pady=15)
            sbheaderl.pack()
            d1 = SBWVWidget(sb, results[0][0], results[0][1])
            d1.pack()
            d2 = SBWVWidget(sb, results[1][0], results[1][1])
            d2.pack()
            d3 = SBWVWidget(sb, results[2][0], results[2][1])
            d3.pack()
            redirectl = RegLabel(sb,
                                 text=f"-OR-\nSubmit a new\nword value"
                                 f"\n for view/download\noptions")
            redirectl.pack()
            changewv = EntryBox(sb)
            changewv.config(width=8)
            changewv.pack()
            wvb = SBButton(sb,
                           text="Submit",
                           command=lambda results=results:
                           nwv_results(results, changewv.get()))
            wvb.pack()
            self.place_footer(' ')

        def nwv_results(results, nwv):
            '''update sidebar with new word value for view or download lists'''
            if not nwv:
                pass
            elif not nwv.isdigit():
                pass
            else:
                results = [('A1-Z26', nwv), ('Z1-A26', nwv), ('Scrabble', nwv)]
            self.do_word_value(self, *args)
            do_dict_options(results)

    # Anagram Comparison Functions
    def do_anagram_compare(self, *args):
        '''
        prepare screen with 2 entry boxes
        collect and process user input,
        display results
        '''

        l1 = "Enter two strings for comparison"
        l2 = "Common and unique letters will be returned"
        sb, anamain, a1in, a2in = self.make_top_area_with_entry_box(l1, l2, 2)
        footerInstruction = "Tab forward, Shift-Tab back, Return to submit"
        self.place_footer(footerInstruction)
        a1in.bind('<Tab>', a2in.focus_force())
        a2in.bind('<Tab>', a1in.focus_force())
        a1in.bind('<Return>',
                  lambda event: anagramfigure(a1in.get(), a2in.get(),
                                              a1in.delete(0, 'end'),
                                              a2in.delete(0, 'end')))
        a2in.bind('<Return>',
                  lambda event: anagramfigure(a1in.get(), a2in.get(),
                                              a1in.delete(0, 'end'),
                                              a2in.delete(0, 'end'),
                                              a1in.focus_force()))

        def anagramfigure(*args):
            '''
            subfunction for display of results
            '''
            a1, a2 = args[0], args[1]
            results = (a1, a2)
            outputframe = MainWindow(anamain)
            outputframe.place(relwidth=1,
                              relheight=1,
                              relx=0,
                              rely=.25)
            if not results[0] or not results[1]:
                msg = "Please enter 2 strings for comparison."
                l3 = RegLabel(outputframe, text=msg,
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
            else:
                s1, s2, incommon, s1only, s2only = check_for_anagram(a1, a2)
                s1label = RegLabel(outputframe,
                                   text=s1,
                                   font=f'{a.FTITLE} {a.FMEDIUM} bold')
                s1label.pack(anchor="center")
                s2label = RegLabel(outputframe,
                                   text=s2,
                                   font=f'{a.FTITLE} {a.FMEDIUM} bold')
                s2label.pack(anchor="center")
                if not s1only and not s2only:
                    analbl = RegLabel(outputframe,
                                      text=f"ANAGRAMS!! All letters in common"
                                      f"\n\nLetter list: {incommon}",
                                      font=f'{a.FTITLE} {a.FMEDIUM} bold',
                                      pady=15)
                    analbl.pack()
                else:
                    if not incommon:
                        incommon = None
                    if not s1only:
                        s1only = None
                    if not s2only:
                        s2only = None
                    incommonlbl = RegLabel(outputframe,
                                           text=f'Letters in common: '
                                           f'{incommon}',
                                           font=f'{a.FTITLE} {a.FMEDIUM} bold',
                                           pady=15)
                    incommonlbl.pack(anchor="center")
                    s1onlylbl = RegLabel(outputframe,
                                         text=f'Letters in {s1} '
                                         f'only: {s1only}',
                                         font=f'{a.FTITLE} {a.FMEDIUM} bold')
                    s1onlylbl.pack(anchor="center")
                    s2onlylbl = RegLabel(outputframe,
                                         text=f'Letters in {s2} '
                                         f'only: {s2only}',
                                         font=f'{a.FTITLE} {a.FMEDIUM} bold')
                    s2onlylbl.pack(anchor="center")

    # Caesar Rotation Functions
    def do_Caesar_rotations(self, *args):
        '''
        prepare screen, collect user input, process, display results
        '''

        l1 = "Enter a string"
        l2 = "All Caesar rotations will be returned"
        sb, csrmain, csrinput = self.make_top_area_with_entry_box(l1, l2)
        ft = FooterWidget(self.root, '')
        ft.place(relw=1-a.FBRELW,
                 relheight=a.FOOTRELH+.01,
                 relx=a.FBRELW,
                 rely=a.FOOTRELY-.01)
        csrinput.bind('<Return>',
                      lambda event: (caesarcalc(event, csrinput.get()),
                                     csrinput.delete(0, 'end')))

        def caesarcalc(self, text):
            '''
            subfunction for display of results
            sends results for assessment of matching words
            '''
            results = caesar_all(text)
            outputframe = MainWindow(csrmain)
            outputframe.place(relwidth=1,
                              relheight=1,
                              relx=0,
                              rely=.15)
            if not text:
                l3 = RegLabel(outputframe, text="Please enter a string.",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
                newsb = MainWindow(sb)
                newsb.place(relwidth=1, relheight=1, rely=0, relx=0)
                newft = FooterWidget(ft)
                newft.place(relwidth=1, relheight=1, rely=0, relx=0)
            else:
                rot = "-ROT-"
                rotated = "-Rotated String-"
                ctextbox = tk.Text(outputframe,
                                   bg=a.BG1,
                                   width=max(len(results[0][1]) + len(rot),
                                             len(rotated) + len(rotated)),
                                   height=60, bd=0,
                                   highlightcolor=a.BG1,
                                   highlightbackground=a.BG1,
                                   highlightthickness=0,
                                   font=f'{a.FDATA} {a.FSMALL+1}',
                                   pady=5, state='normal')
                ctextbox.tag_configure('center', justify='center')
                ctextbox.pack()
                col1width = len(rot)
                col2width = max([len(results[0][1]), len(rotated)])
                outputlist = []
                outputlist.append(f'{rot.rjust(col1width,"-")}'
                                  f' {rotated.center(col2width,"-")}\n')
                for i in range(26):
                    if len(str(results[i][0])) == 1:
                        numstring = ' ' + str(results[i][0])
                    else:
                        numstring = str(results[i][0])
                    outputlist.append(f'{numstring.center(col1width)} '
                                      f'{results[i][1].center(col2width)}\n')
                output = ''.join(outputlist)
                ctextbox.insert(tk.END, output, 'center')
                ctextbox['state'] = 'disabled'
                show_real_words(results, text)

        def show_real_words(results, text):
            '''
            split list of Caesar rotations into a list individual words
            compare each word to external dictionary
            display matching words if word length > a minimum length
            '''
            newsb = MainWindow(sb)
            newsb.place(relwidth=1, relheight=1, rely=0, relx=0)
            newft = FooterWidget(ft,
                                 message=f"{a.dictnote}")
            newft.place(relwidth=1, relheight=1, rely=0, relx=0)
            wordcount = 1
            if len(text) < a.MINCAESARWORDLENGTH:
                wordlist = []
            else:
                wordlist = [result[1].lower() for result in results]
                if ' ' in wordlist[0]:
                    wordcount = len(wordlist[0].split())
                    wordcompositelist = []
                    for entry in wordlist:
                        words = entry.split()
                        for word in words:
                            if len(word) >= a.MINCAESARWORDLENGTH:
                                wordcompositelist.append(word)
                    wordlist = wordcompositelist
            results = sorted(list(set(check_english(wordlist[wordcount:]))))
            l1 = RegLabel(newsb,
                          text=f"Possible\n English words \n"
                          f" in your results\n"
                          f"(>= word length {a.MINCAESARWORDLENGTH}):",
                          font=f'{a.FPLAIN} {a.FTINY}')
            l1.pack(pady=2)
            factor = a.MINSIZE_FACTOR
            t = RegularTable(newsb,
                             width={0: round(a.WIDTH * a.LBRELW * factor)},
                             rows=len(results), columns=1)
            t.pack(pady=(a.TABLEYPAD//4, 0), fill='y')
            if not results:
                l2 = RegLabel(newsb,
                              text="None",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l2.pack()
            else:
                for i in range(len(results)):
                    t.set(i, 0, results[i].upper())

    # Letter Representation Functions
    def do_letter_representations(self, *args):
        '''get a table of selected letter representations'''

        def modify_selected(num, name):
            '''continuous updating of checkbox on/off status'''
            if on_off_list[num].get() == 0:
                if (num, name) in selected:
                    selected.remove((num, name))
            if on_off_list[num].get() == 1:
                if num not in selected:
                    selected.append((num, name))

        def show_reps(*args):
            '''display of selected representations'''
            s = args[0]
            categories = [item[1] for item in s]
            lrmain = MainWindow(self.root)
            lrmain.place(relwidth=a.MWRELW,
                         relheight=a.MWRELH,
                         rely=a.MWRELY,
                         relx=a.MWRELX)
            self.place_footer(f"cap = capital, sm = small, Scrb = Scrabble, "
                              f"Val = Value, Freq = Frequency")
            if not categories:
                msg = "Select options from the menu to the left."
                lrmessage = RegLabel(lrmain,
                                     text=msg,
                                     font=f'{a.FTITLE} {a.FMEDIUM} bold')
                lrmessage.pack(expand=True, anchor='center')
            # tabular results -- header and contents
            # column width is determined by length of header string
            else:
                holdingframe = MainWindow(lrmain)
                holdingframe.place(relwidth=1,
                                   relheight=1,
                                   relx=0,
                                   rely=.02)
                with open(a.letterdictionary, 'rb') as f:
                    aldict = pickle.load(f)
                rows = 1
                columns = len(categories)
                if columns < 8:
                    size = a.FMEDIUM
                elif columns < 10:
                    size = a.FSMALL
                elif columns < 12:
                    size = a.FSMALLER
                else:
                    size = a.FTINY
                headerf = f'{a.FTITLE} {size} bold underline'
                bodyf = f'{a.FTITLE} {size}'
                header = []
                width = {}
                for i in range(columns):
                    header.append(categories[i])
                    width[i] = width.get(i, len(categories[i])+1)
                h = TableHeader(holdingframe, width=width,
                                rows=rows, columns=columns)
                h.pack(pady=(a.TABLEYPADNARROW, 0), fill='y')
                for i in range(columns):
                    h.set(0, i, header[i], headerf)
                rows = len(aldict.keys())
                t = RegularTable(holdingframe, width=width,
                                 rows=rows, columns=columns)
                t.pack(pady=(a.TABLEYPADNARROW, 0), fill='y')
                for i in range(rows):
                    for j in range(columns):
                        t.set(i, j, aldict[chr(i+97)][categories[j]], bodyf)

        # collect user request for which data to display
        # default values set in ancillary file
        # num in selected list determines order of placement
        selected = []  # list of tuples (num, name)
        on_off_list = []  # list of 1 or 0 representing selected or not
        counter = 0
        # draw a new sidebar
        sb = SideBar(self.root)
        sb.place(relwidth=a.SBRELW,
                 relheight=a.SBRELH,
                 rely=a.SBRELY,
                 relx=a.SBRELX)
        for num, name in enumerate(a.LETTER_REPRESENTATION_MENU, start=0):
            # default items appear as checked/on
            if name in a.LETTER_REPRESENTATION_DEFAULT_MENU:
                on_off_list.append(tk.IntVar(value=1))
                selected.append((num, name))
            # remainder items appear as unchecked/off
            else:
                on_off_list.append(tk.IntVar(value=0))
            # put the individual checkbox widget in the sidebar
            picker = SBCheckButton(sb,
                                   text=name,
                                   variable=on_off_list[num],
                                   command=partial(modify_selected, num, name))
            picker.grid(column=0, row=counter, pady=2, padx=6, sticky="w")
            counter += 1
        # place a submit button for collecting new values
        submit = SBButton(sb,
                          f=f'{a.FTITLE} {a.FSMALLER} bold underline',
                          fg="black",
                          text="GET VALUES",
                          command=lambda selected=selected:
                              show_reps(sorted(selected)))
        submit.grid(column=0, row=counter+1, pady=10, padx=0, sticky='w')
        # draw a new main window
        lrmain = MainWindow(self.root)
        lrmain.place(relwidth=a.MWRELW,
                     relheight=a.MWRELH,
                     rely=a.MWRELY,
                     relx=a.MWRELX)
        # call sub-function for display of the selected items
        show_reps(sorted(selected))

    # DO NUMBERS SECTION
    def do_numbers(self, *args):
        todo = args[0]
        self.logobox_update(f'NUMBERS\n{todo}')
        self.drop_down_menus()
        if "Rep" in todo:
            self.do_number_representations()
        if "Fun" in todo:
            self.do_num_fun_facts()
        if "Sequences" in todo:
            self.do_num_sequences()

    # Number Representation Functions
    def do_number_representations(self, *args):
        '''
        get a table of selected number representations
        '''

        def modify_selected(num, name):
            '''continuous updating of on/off status of checkboxes
            in selected list
            '''
            if on_off_list[num].get() == 0:
                if (num, name) in selected:
                    selected.remove((num, name))
            if on_off_list[num].get() == 1:
                if num not in selected:
                    selected.append((num, name))

        def show_reps(*args):
            s = args[0]
            categories = [item[1] for item in s]
            lrmain = MainWindow(self.root)
            lrmain.place(relwidth=a.MWRELW,
                         relheight=a.MWRELH,
                         rely=a.MWRELY,
                         relx=a.MWRELX)
            if not categories:
                msg = "Select options from the menu to the left."
                lrmessage = RegLabel(lrmain,
                                     text=msg,
                                     font=f'{a.FTITLE} {a.FMEDIUM} bold')
                lrmessage.pack(expand=True, anchor='center')
            # tabular results
            else:
                with open(a.digitdictionary, 'rb') as f:
                    digitdict = pickle.load(f)
                rows = 1
                columns = len(categories)
                if columns < 9:
                    size = a.FMEDIUM
                elif columns < 12:
                    size = a.FSMALL
                else:
                    size = a.FSMALLER
                headerf = f'{a.FTITLE} {size} bold underline'
                bodyf = f'{a.FTITLE} {size}'
                header = []
                width = {}
                for i in range(columns):
                    header.append(categories[i])
                    width[i] = width.get(i, len(categories[i]) + 1)
                h = TableHeader(lrmain, width=width,
                                rows=rows, columns=columns)
                h.pack(pady=(a.TABLEYPAD, 0), fill='y')
                for i in range(columns):
                    h.set(0, i, header[i], headerf)
                rows = len(digitdict.keys())
                t = RegularTable(lrmain, width=width,
                                 rows=rows, columns=columns)
                t.pack(pady=(a.TABLEYPADNARROW, 0), fill='y')
                for i in range(rows):
                    for j in range(columns):
                        t.set(i, j, digitdict[chr(i+48)][categories[j]], bodyf)

        # selected list available throughout
        selected = []  # initializing list of tuples (num, name)
        on_off_list = []  # values will be 1 (on) or 0 (off)
        counter = 0
        # put checklist in sidebar
        sb = SideBar(self.root)
        sb.place(relwidth=a.SBRELW,
                 relheight=a.SBRELH,
                 rely=a.SBRELY,
                 relx=a.SBRELX)
        for num, name in enumerate(a.NUMBER_REPRESENTATION_MENU, start=0):
            # default with some checked (configure in ancillary)
            if name in a.NUMBER_REPRESENTATION_DEFAULT_MENU:
                on_off_list.append(tk.IntVar(value=1))
                selected.append((num, name))
            else:
                on_off_list.append(tk.IntVar(value=0))
            picker = SBCheckButton(sb,
                                   text=name,
                                   variable=on_off_list[num],
                                   command=partial(modify_selected, num, name))
            picker.grid(column=0, row=counter, pady=2, padx=6, sticky="w")
            counter += 1
        submit = SBButton(sb,
                          f=f'{a.FTITLE} {a.FSMALLER} bold underline',
                          fg="black",
                          text="GET VALUES",
                          command=lambda selected=selected:
                              show_reps(sorted(selected)))
        submit.grid(column=0, row=counter+1, pady=10, padx=0, sticky='w')
        # draw a new main window
        lrmain = MainWindow(self.root)
        lrmain.place(relwidth=a.MWRELW,
                     relheight=a.MWRELH,
                     rely=a.MWRELY,
                     relx=a.MWRELX)
        show_reps(sorted(selected))

    # Number Fun Facts Functions
    def do_num_fun_facts(self, *args):
        '''
        prepare screen, collect & process user input,
        display results for Fun Facts
        '''
        l1 = "Enter a base 10 number"
        l2 = "Fun Facts and factors will be returned"
        sb, ffmain, ffinput = self.make_top_area_with_entry_box(l1, l2)
        ffinput.config(width=round(a.ENTRYBOXWIDTH * .60))
        ffinput.bind('<Return>', lambda event:
                     (ffcalcs(event, ffinput.get()),
                      ffinput.delete(0, 'end')))

        def ffcalcs(self, number):
            '''
            subfunction for collection and display of results
            '''
            p = inflect.engine()
            outputframe = MainWindow(ffmain)
            outputframe.place(relwidth=1,
                              relheight=1,
                              relx=0,
                              rely=.18)
            if not clean_integer(number) or int(number) > a.MAXNUMBER:
                l3 = RegLabel(outputframe,
                              text=f"Please enter a valid number "
                              f"(positive integer without commas, max {a.MAXNUMBER}).",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
            else:
                num = int(number)
                finalnumlabel = RegLabel(outputframe,
                                         text=f"{num:,}",
                                         font=f'{a.FTITLE} {a.FMEDIUM} bold')
                finalnumlabel.pack()
                ntextbox = tk.Text(outputframe,
                                   bg=a.BG1, width=50, height=50, bd=0,
                                   highlightcolor=a.BG1,
                                   highlightbackground=a.BG1,
                                   highlightthickness=0,
                                   font=f'{a.FDATA} {a.FSMALL}',
                                   pady=15, wrap="word", state='normal')
                ntextbox.tag_configure('center', justify='center')
                ntextbox.pack()
                if is_prime(num):
                    primeinfo = f"Is a prime number.\n\n"
                    ntextbox.insert(tk.END, primeinfo, 'center')
                elif num == 1:
                    pass
                else:
                    flist = factors(num)
                    flist.append(num)  # include num itself in factor list
                    flist_display = p.join([str(n) for n in flist])
                    ntextbox.insert(tk.END,
                                    f"Has {len(flist)} factors:"
                                    f"\n {flist_display}.\n\n",
                                    'center')
                    ntextbox.insert(tk.END, f"Prime factorization:\n"
                                    f"{get_prime_factors(num)}.\n\n", 'center')
                if is_square(num):
                    sq = f"Is a perfect square ({get_square_root(num)}).\n\n"
                    ntextbox.insert(tk.END, sq, 'center')
                if is_cube(num):
                    cu = f"Is a perfect cube ({get_cube_root(num)}).\n\n"
                    ntextbox.insert(tk.END, cu, 'center')
                if is_fibonacci(num):
                    fi = f"Is a Fibonacci number.\n\n"
                    ntextbox.insert(tk.END, fi, 'center')
                if is_triangular(num):
                    tr = f"Is a triangular number.\n\n"
                    ntextbox.insert(tk.END, tr, 'center')
                ntextbox['state'] = ['disabled']

    # Number Sequences Functions
    def do_num_sequences(self, *args):
        '''
        prepare screen, collect & process user input,
        display results for Sequences
        '''

        def modify_selected(num, name):
            '''continuous updating of on/off status of checkboxes
            in selected list
            '''
            if on_off_list[num].get() == 0:
                if (num, name) in selected:
                    selected.remove((num, name))
            if on_off_list[num].get() == 1:
                if num not in selected:
                    selected.append((num, name))

        # selected list available throughout
        selected = []  # a list of tuples (enumeration for order, name)
        on_off_list = []  # corresponds to selected list with on/off status
        counter = 0
        # draw sidebar and build checklist
        sb = self.place_sidebar()
        for num, name in enumerate(sorted(a.NUMBER_SEQUENCES_MENU), start=0):
            # default may include full list
            if name in a.NUMBER_SEQUENCES_DEFAULT_MENU:
                on_off_list.append(tk.IntVar(value=1))
                selected.append((num, name))
            else:
                on_off_list.append(tk.IntVar(value=0))
            choose_rep = SBCheckButton(sb,
                                       text=name,
                                       variable=on_off_list[num],
                                       command=partial(modify_selected,
                                                       num, name))
            choose_rep.grid(column=0, row=counter,
                            pady=5, padx=10, sticky="w")
            counter += 1
        # draw main window and footer
        numseqmain = MainWindow(self.root)
        numseqmain.place(relwidth=a.MWRELW,
                         relheight=a.MWRELH,
                         rely=a.MWRELY,
                         relx=a.MWRELX)
        self.place_footer('')
        # designate area for instructions
        introarea = MainWindow(numseqmain)
        introarea.place(relwidth=1,
                        relheight=.15,
                        rely=.02,
                        relx=0)
        # display instructions
        l1 = RegLabel(introarea,
                      text="Enter lower limit and upper limit, inclusive",
                      font=f'{a.FTITLE} {a.FMEDIUM} bold')
        l1.pack()
        l2 = RegLabel(introarea,
                      text="Sequences between the limits will be returned",
                      font=f'{a.FPLAIN} {a.FSMALL}')
        l2.pack()
        # designate area for entry boxes for collection of user input
        # 2 entry boxes on 1 line
        entryboxarea = MainWindow(numseqmain)
        entryboxarea.place(relwidth=1,
                           relheight=.15,
                           rely=.1,
                           relx=a.LBRELW)
        # label and entry box for lower limit
        lowerlabel = RegLabel(entryboxarea, text="Lower limit:")
        lowerlabel.grid(row=0, column=0,
                        pady=(a.ENTRYBOXYPAD, a.ENTRYBOXYPAD//2))
        lowerlimitinput = EntryBox(entryboxarea)
        lowerlimitinput.configure(width=a.ENTRYBOXWIDTH//2)
        lowerlimitinput.grid(row=0, column=1,
                             padx=(15, 40),
                             pady=(a.ENTRYBOXYPAD, a.ENTRYBOXYPAD//2))
        lowerlimitinput.focus_force()
        # label and entry box for upper limit
        upperlabel = RegLabel(entryboxarea, text="Upper limit:")
        upperlabel.grid(row=0, column=2, pady=a.ENTRYBOXYPAD)
        upperlimitinput = EntryBox(entryboxarea)
        upperlimitinput.configure(width=a.ENTRYBOXWIDTH//2)
        upperlimitinput.grid(row=0, column=3,
                             padx=(15, 0),
                             pady=a.ENTRYBOXYPAD)
        # functionality of lower and upper limit entry boxes
        lowerlimitinput.bind('<Tab>',
                             upperlimitinput.focus_force())
        upperlimitinput.bind('<Tab>',
                             lowerlimitinput.focus_force())
        lowerlimitinput.bind('<Return>',
                             lambda event:
                             (numsequences(lowerlimitinput.get(),
                                           upperlimitinput.get(),
                                           selected),
                              lowerlimitinput.delete(0, 'end'),
                              upperlimitinput.delete(0, 'end')))
        upperlimitinput.bind('<Return>',
                             lambda event:
                             (numsequences(lowerlimitinput.get(),
                                           upperlimitinput.get(),
                                           selected),
                              lowerlimitinput.delete(0, 'end'),
                              upperlimitinput.delete(0, 'end'),
                              lowerlimitinput.focus_force()))

        def numsequences(lower, upper, selected):
            '''
            subfunction for collection and display of results
            '''
            p = inflect.engine()
            selected = [item[1] for item in selected]
            outputframe = MainWindow(numseqmain)
            outputframe.place(relwidth=1,
                              relheight=1,
                              relx=0,
                              rely=.2)
            if not clean_integer(lower) or not clean_integer(upper):
                l3 = RegLabel(outputframe,
                              text=f"Please enter 2 valid numbers "
                              f"(non-zero integers only, no commas).",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
                self.place_footer('')
            elif int(lower) > a.MAXNUMBER or int(upper) > a.MAXNUMBER:
                l3 = RegLabel(outputframe,
                              text=f"Sorry, number "
                              f" cannot exceed {a.MAXNUMBER}.",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
                self.place_footer('')
            elif int(lower) >= int(upper):
                l3 = RegLabel(outputframe,
                              text=f"Lower limit must be "
                              f"less than upper limit.",
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
                self.place_footer('')
            elif int(upper) - int(lower) > 1000:
                l3 = RegLabel(outputframe,
                              text=f'Range must not exceed 1000',
                              font=f'{a.FPLAIN} {a.FSMALL}')
                l3.pack()
                self.place_footer('')
            else:
                low = int(lower)
                high = int(upper)

                frangel = RegLabel(outputframe,
                                   text=f"Range {low:,} - {high:,}",
                                   font=f'{a.FTITLE} {a.FMEDIUM} bold')
                frangel.pack()
                textframe = MainWindow(outputframe)  # to hold scrollbar
                textframe.place(relwidth=1,
                                relheight=.6,
                                relx=0,
                                rely=.05)
                ntextbox = tk.Text(textframe, bg=a.BG1,
                                   width=50, height=50, bd=0,
                                   highlightcolor=a.BG1,
                                   highlightbackground=a.BG1,
                                   highlightthickness=0,
                                   font=f'{a.FDATA} {a.FSMALL}',
                                   pady=15, wrap="word", state='normal')
                ntextbox.tag_configure('center', justify='center')
                scroller = tk.Scrollbar(textframe)
                scroller.pack(side='right', fill='both')
                ntextbox.configure(yscrollcommand=scroller.set)
                scroller.config(command=ntextbox.yview)
                ntextbox.pack(expand=True)
                # default is for all sequences to be displayed
                # user can deselect from default condition
                if "Squares" in selected:
                    slist = get_squares(low, high)
                    if not slist:
                        slist_display = "None"
                    else:
                        slist_display = p.join([str(n) for n in slist])
                    squareinfo = f"Perfect squares: {slist_display}\n\n"
                    ntextbox.insert(tk.END, squareinfo, 'center')
                if "Cubes" in selected:
                    clist = get_cubes(low, high)
                    if not clist:
                        clist_display = "None"
                    else:
                        clist_display = p.join([str(n) for n in clist])
                    cubeinfo = f"Perfect cubes: {clist_display}\n\n"
                    ntextbox.insert(tk.END, cubeinfo, 'center')
                if "Primes" in selected:
                    plist = get_primes_in_range(low, high)
                    if not plist:
                        plist_display = "None"
                    else:
                        plist_display = p.join([str(n) for n in plist])
                    primeinfo = f"Prime numbers: {plist_display}\n\n"
                    ntextbox.insert(tk.END, primeinfo, 'center')
                if "Fibonacci" in selected:
                    flist = get_fib_nums_in_range(low, high)
                    if not flist:
                        flist_display = "None"
                    else:
                        flist_display = p.join([str(n) for n in flist])
                    fibinfo = f"Fibonacci numbers: {flist_display}\n\n"
                    ntextbox.insert(tk.END, fibinfo, 'center')
                ntextbox['state'] = 'disabled'

    # DO EXTRAS SECTION
    def do_extras(self, *args):
        todo = args[0]
        self.logobox_update(f'EXTRAS\n{todo}')
        self.drop_down_menus()
        if "Ref" in todo:
            self.do_references()
        if "Links" in todo:
            self.do_links()

    # Links
    def do_links(self, *args):
        '''
        display a list of links
        links open in a new browser tab when clicked
        '''

        # toggle footer display of url when hovering over link
        def button_hover(url, e):
            self.place_footer(url)

        def button_leave(e):
            self.place_footer(' ')

        # prep window, display list of links (from dict in ancillary)
        sb = SideBar(self.root)
        sb.place(relwidth=a.SBRELW,
                 relheight=a.SBRELH,
                 rely=a.SBRELY,
                 relx=a.SBRELX)
        linksmain = MainWindow(self.root)
        linksmain.place(relwidth=a.MWRELW,
                        relheight=a.MWRELH,
                        rely=a.MWRELY,
                        relx=a.MWRELX)
        linkstitle = RegLabel(linksmain, text="LINKS",
                              font=f'{a.FTITLE} {a.FMEDIUM} bold')
        linkstitle.pack(pady=(25, 5))
        buttonlist = {}
        for name, url in (sorted(a.LINKSDICT.items())):
            lbutton = HyperLinkButton(linksmain, name, url)
            lbutton.pack()
            lbutton.bind("<Enter>", func=partial(button_hover, url))
            lbutton.bind("<Leave>", func=partial(button_leave))
        self.place_footer('')

    # Reference (Images)
    def do_references(self, *args):
        '''
        presents sidebar with image options
        selected item displays in main window
        '''

        sb = self.place_sidebar()
        for rpic in sorted(a.IMAGE_TITLE_MENU):
            sbb = SBButton(sb, text=str(rpic))
            sbb.configure(command=lambda rpic=rpic: show_refimage(rpic))
            sbb.pack()
        # draw an empty main frame
        refmain = MainWindow(self.root)
        refmain.place(relwidth=a.MWRELW,
                      relheight=a.MWRELH,
                      rely=a.MWRELY,
                      relx=a.MWRELX)
        refmsg = RegLabel(refmain,
                          text="Choose an image from the menu to the left.",
                          font=f'{a.FTITLE} {a.FMEDIUM} bold')
        refmsg.pack(expand=True, anchor='center')
        self.place_footer_with_popup("Image Sources", a.IMAGE_SOURCE_INFO)

        def show_refimage(refpic):
            '''displays images from reference list in  main frame
            imgs resized per current window size at time of img display
            image size may be reduced, never enlarged
            global statement required for display of img within a function
            '''
            # clear main window
            imageframe = MainWindow(refmain)
            imageframe.place(relwidth=1, relheight=1,
                             rely=0, relx=0)
            # image preparations
            global openimage
            # grab dimensions of  underlying display area
            w = round(0.8 * int(self.root.winfo_width()))
            h = round(0.8 * int(self.root.winfo_height()))
            # grab image, get dimensions, compare to frame dimensions
            # w, h are frame dimensions;
            # i.width and i.height are image dimentsions
            i = Image.open(f'images/{refpic}.png')
            # adjustment factors - for improved visualization
            adjh = 25
            adjw = 15
            if (i.width + (adjw * 2) < w and i.height + (adjh * 2) < h):
                fraction = 1
            elif (i.width + (adjw * 2) > w and
                  i.width + (adjw * 2) - w > i.height + (adjh * 2) - h):
                fraction = (i.width + (adjw * 2) - w) / i.width
                fraction = 1 - fraction
            elif (i.width + (adjw * 2) > w and
                  i.width + (adjw * 2) - w < i.height + (adjh * 2) - h):
                fraction = (i.height + (adjh * 2) - h) / i.height
                fraction = 1 - fraction
            elif i.height + (adjh * 2) > h:
                fraction = (i.height + (adjh * 2) - h) / i.height
                fraction = 1 - fraction
            else:
                fraction = 1
            # adjust image size in proportion to fit the current frame
            resized = i.resize((round(i.width * fraction),
                                round(i.height * fraction)))
            openimage = ImageTk.PhotoImage(resized)
            # overlay frame so new image replaces previous
            imgframe = MainWindow(imageframe)
            imgframe.place(relheight=1, relwidth=1)
            name = RegLabel(imgframe, text=refpic,
                            font=f'{a.FTITLE} {a.FMEDIUM} bold')
            name.pack(pady=(15, 0))
            img = RegLabel(imgframe, image=openimage,
                           bg=a.BG1, anchor='center')
            img.pack(side='top', padx=adjw, pady=adjh)

    # GUI COMPONENTS
    def place_sidebar(self):
        '''draw an empty sidebar'''
        sb = SideBar(self.root)
        sb.place(relwidth=a.SBRELW,
                 relheight=a.SBRELH,
                 rely=a.SBRELY,
                 relx=a.SBRELX)
        return sb

    def place_borderless_sidebar(self):
        sb = SideBar(self.root)
        sb.place(relwidth=a.SBRELW,
                 relheight=a.SBRELH,
                 rely=a.SBRELY,
                 relx=a.SBRELX)
        sb.config(highlightbackground=a.BG1, highlightthickness=0)
        return sb

    def place_footer(self, text):
        t = FooterWidget(self.root, text)
        t.place(relw=1-a.FBRELW, relheight=a.FOOTRELH+.01,
                relx=a.FBRELW, rely=a.FOOTRELY-.01)
        return t

    def place_footer_with_popup(self, text, popupmessage):
        t = FooterWidgetWithPopUpMessage(self.root, text, popupmessage)
        t.place(relw=1-a.FBRELW, relheight=a.FOOTRELH+.01,
                relx=a.FBRELW, rely=a.FOOTRELY-.01)
        return t

    def logobox_update(self, hword=f"Toolbox"):
        '''
        defines logo area in the upper left corner
        updates to current info on navigation location
        clears any footer note
        '''
        global tbimage  # global designation required within functions
        imagestring = "images/toolboxFavicon-32x32.png"
        logobox = tk.Frame(self.root, bg=a.BG2)
        logobox.place(relwidth=a.LBRELW,
                      relheight=a.LBRELH,
                      x=a.LBX,
                      y=a.LBY)
        tbimage = ImageTk.PhotoImage(Image.open(imagestring))
        tblabel = tk.Label(logobox,
                           bg=a.BG2,
                           text=f'{hword}',
                           image=tbimage,
                           compound="top")
        tblabel.place(relheight=a.LBLRELSIZE,
                      relwidth=a.LBLRELSIZE)
        tblabel.configure(font=f'{a.FPLAIN} {a.FSMALL-3}',
                          highlightthickness=a.LBHLT,
                          highlightbackground=a.BG2)
        # clear any footer upon redirection with new footer, no message
        self.place_footer('')
        return logobox, tblabel

    def quit_button(self):
        '''places a quit button lower left, in footer section'''
        footer = tk.Frame(self.root, bg=a.BG1)
        footer.place(relwidth=a.FOOTRELW,
                     relheight=a.FOOTRELH,
                     relx=a.FOOTRELX,
                     rely=a.FOOTRELY)
        tk.Button(footer,
                  text="Quit",
                  font=f'{a.FPLAIN} {a.FMEDIUM} bold',
                  bg=a.BG2,
                  activebackground=a.ABG_SPECIAL,
                  activeforeground=a.AFG1,
                  bd=a.FBBD,
                  highlightbackground=a.HLBG,
                  highlightthickness=a.FBHLT,
                  command=self.root.destroy).place(relwidth=a.FBRELW,
                                                   relheight=a.FBRELH,
                                                   relx=a.FBRELX,
                                                   rely=a.FBRELY)

    def drop_down_menus(self):
        '''
        placement of main navigation tool
        3 dropdown menus
        commands go to activity functions
        '''
        # frame
        dd = tk.Frame(self.root, bg=a.BG2)
        dd.place(relwidth=a.DDRELW,
                 relheight=a.DDRELH,
                 rely=a.DDRELY,
                 relx=a.DDRELX)

        # 3 main drop down menus
        wordsdd = HeaderOptionMenu(dd, "WORDS", *a.WORDSMENU,
                                   command=self.do_words)
        numbersdd = HeaderOptionMenu(dd, "NUMBERS", *a.NUMBERSMENU,
                                     command=self.do_numbers)
        extrasdd = HeaderOptionMenu(dd, "EXTRAS", *a.EXTRASMENU,
                                    command=self.do_extras)
        wordsdd.place(relwidth=a.DDMRELW, relheight=a.DDMRELH,
                      relx=a.DDMRELX, rely=a.DDMRELY)
        numbersdd.place(relwidth=a.DDMRELW, relheight=a.DDMRELH,
                        relx=a.DDMRELX * 4, rely=a.DDMRELY)
        extrasdd.place(relwidth=a.DDMRELW, relheight=a.DDMRELH,
                       relx=a.DDMRELX * 7, rely=a.DDMRELY)

    def firstmessage(self, message):
        '''landing screen at program start
        uses full window width to center message
        '''
        global bgimage
        mw = MainWindow(self.root)
        mw.place(relwidth=a.MWRELW+a.SBRELW,
                 relheight=a.MWRELH,
                 rely=a.MWRELY,
                 relx=a.SBRELX)
        bgimage = Image.open("images/jiggy_big.png")
        # resize proportionally to fit window size
        resized = bgimage.resize((round(a.WIDTH * .5),
                                  round(a.WIDTH * .5 * (2/3))))
        bgimage = ImageTk.PhotoImage(resized)
        bgLabel = tk.Label(mw, image=bgimage, bg=a.BG1)
        bgLabel.place(relwidth=1, relheight=1, x=45, y=0, anchor='nw')
        fmlabel = tk.Label(mw,
                           text=message,
                           font=f'{a.FTITLE} {a.FXXLARGE} bold',
                           bg=a.BG1, fg=a.FG1, image=bgimage, compound='bottom')
        fmlabel.pack(expand=True, anchor='center')

    def make_top_area_with_entry_box(self, l1text, l2text, extraeb=1):
        '''
        draws top section: 2 lines intro instruction & 1-2 entry boxes
        returns sidebar, main window, and entry box objects
        '''
        # draw empty sidebar
        sb = SideBar(self.root)
        sb.place(relwidth=a.SBRELW,
                 relheight=a.SBRELH,
                 rely=a.SBRELY,
                 relx=a.SBRELX)
        # draw a main window
        main = MainWindow(self.root)
        main.place(relwidth=a.MWRELW,
                   relheight=a.MWRELH,
                   rely=a.MWRELY,
                   relx=a.MWRELX)
        entryboxarea = MainWindow(main)
        entryboxarea.place(relwidth=1,
                           relheight=.30,
                           rely=.02,
                           relx=0)
        l1 = RegLabel(entryboxarea, text=l1text,
                      font=f'{a.FTITLE} {a.FMEDIUM} bold')
        l1.pack()
        l2 = RegLabel(entryboxarea, text=l2text,
                      font=f'{a.FPLAIN} {a.FSMALL}')
        l2.pack()
        eb1 = EntryBox(entryboxarea)
        eb1.pack(pady=a.ENTRYBOXYPAD)
        eb1.focus_force()
        if extraeb != 1:
            eb2 = EntryBox(entryboxarea)
            eb2.pack(pady=a.ENTRYBOXYPAD)
            return sb, main, eb1, eb2
        return sb, main, eb1


# component/widget classes
# General
class EntryBox(tk.Entry):
    '''create a stylized tk entry box'''
    def __init__(self, parent, **kwargs):
        tk.Entry.__init__(self, parent,
                          width=a.ENTRYBOXWIDTH,
                          bg=a.ENTRYBOXBACKGROUND,
                          font=f'{a.FPLAIN} {a.FMEDIUM}',
                          fg=a.ENTRYBOXTEXTCOLOR,
                          selectbackground=a.BG2)


class FooterWidget(tk.Frame):
    '''create a stylized tk frame for use as footer'''
    def __init__(self, parent, message=''):
        tk.Frame.__init__(self, parent, bg=a.BG1)
        label = tk.Label(self, text=message,
                         font=f'{a.FPLAIN} {a.FXTINY}',
                         bg=a.BG1, fg=a.FG1)
        label.place(relx=.01, rely=1, anchor='sw')


class FooterWidgetWithPopUpMessage(tk.Frame):
    '''
    stylized tk frame for use as a footer with a pop up message
    '''
    def __init__(self, parent, message='', popupmessage=''):
        tk.Frame.__init__(self, parent, bg=a.BG1)
        label = tk.Label(self, text=message,
                         font=f'{a.FPLAIN} {a.FXTINY}',
                         bg=a.BG1, fg=a.FG1)
        label.place(relx=.01, rely=1, anchor='sw')
        ToolTip(label, msg=popupmessage,
                font=f'{a.FPLAIN} {a.FXTINY}',
                bg=a.DDMTOPBG)


class HeaderOptionMenu(tk.OptionMenu):
    '''create a stylized tk option menu'''
    def __init__(self, parent, setting, *args, **kwargs):
        self.var = tk.StringVar(parent)
        self.var.set(setting)
        tk.OptionMenu.__init__(self, parent, self.var, *args, **kwargs)
        self.config(font=f'{a.FPLAIN} {a.FMEDIUM} bold',
                    bg=a.DDMTOPBG,
                    activebackground=a.DDMABG,
                    highlightthickness=a.DDMHLT,
                    highlightcolor=a.BG1)
        self['menu'].config(bg=a.DDMTOPBG,
                            activebackground=a.DDMDROPABG,
                            activeforeground=a.DDMDROPAFG)


class HyperLinkButton(tk.Frame):
    '''
    stylized tk button that displays name and links to url on click
    '''
    def __init__(self, parent, name, url, **kwargs):
        tk.Frame.__init__(self, parent, bg=a.BG1, **kwargs)
        linkbutton = tk.Button(self, bg=a.BG1, text=name,
                               highlightbackground=a.BG1,
                               highlightthickness=0, bd=0,
                               activebackground=a.BG2, activeforeground=a.AFG2,
                               fg="blue", cursor="hand1",
                               font=f'{a.FPLAIN} {a.FMEDIUM} bold',
                               pady=1)
        linkbutton.configure(command=lambda url=url: callwebpage(url))
        linkbutton.pack()


class MainWindow(tk.Frame):
    '''create a stylized tk frame'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=a.BG1)


class RegLabel(tk.Label):
    '''create a stylized tk label'''
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        self.config(bg=a.BG1, highlightbackground=a.BG1,
                    highlightthickness=0, fg=a.FG1)


# Sidebar
class SideBar(tk.Frame):
    '''create a stylized frame for use as a sidebar'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=a.BG1, highlightbackground=a.HLBG,
                          highlightthickness=a.HLT)


class SBButton(tk.Button):
    '''create a stylized tk Button for use in the sidebar'''
    def __init__(self, parent, f=f'{a.FTITLE} {a.FSMALL-1} bold', **kwargs):
        tk.Button.__init__(self, parent, **kwargs)
        self.config(bg=a.BG1,
                    font=f,
                    bd=a.BD,
                    highlightthickness=a.HLT,
                    highlightbackground=a.BG1,
                    activebackground=a.BG2,
                    activeforeground=a.AFG2,
                    pady=3)


class SBCheckButton(tk.Checkbutton):
    '''create a stylized tk checkbutton for use in the sidebar'''
    def __init__(self, parent, f=f'{a.FTITLE} {a.FTINY} bold', **kwargs):
        tk.Checkbutton.__init__(self, parent, **kwargs)
        self.config(bg=a.BG1,
                    font=f,
                    bd=a.BD,
                    highlightthickness=a.HLT,
                    highlightbackground=a.BG1,
                    activebackground=a.BG1,
                    activeforeground=a.AFG2,
                    pady=3)


class SBWVWidget(tk.Frame):
    '''
    create a stylized frame for use in the word value side bar
    buttons  allow view or download of wordlists with specific wv
    '''
    def __init__(self, parent, scale, number):
        tk.Frame.__init__(self, parent)
        self.config(bg=a.BG1, pady=10)
        l1 = RegLabel(self, text=f"{scale}",
                      font=f'{a.FPLAIN} {a.FTINY} bold')
        l1.pack()
        l2 = RegLabel(self, text=f"Word Value {number}",
                      font=f'{a.FPLAIN} {a.FTINY}')
        l2.pack()
        b1 = SBButton(self, f=f'{a.FTITLE} {a.FXTINY} bold', text="View",
                      command=lambda number=number:
                          self.view_wv_list(scale, number))
        b2 = SBButton(self, f=f'{a.FTITLE} {a.FXTINY} bold', text="Download",
                      command=lambda number=number:
                          self.create_wv_text_file(scale, number))
        b1.pack(side="left", fill="x")
        b2.pack(side="right", fill="x")

    def view_wv_list(self, scale, wv):
        '''
        gathers a list of words that match given scale and wv
        data includes number of words
        info is displayed in a pop up window
        '''
        # collect info on window geometry for pop up window
        results = []
        root_x = pzt.root.winfo_rootx()
        root_y = pzt.root.winfo_rooty()
        root_w = pzt.root.winfo_width()
        root_h = pzt.root.winfo_height()
        # define offsets for pop up window
        tw_x = root_x + round(0.8 * root_w)
        tw_y = root_y + round(0.5 * root_h)
        # create pop up window
        text_window = tk.Tk()
        text_window.title(f'{scale} - Word Value {wv}')
        text_window.geometry(f'300x500+{tw_x}+{tw_y}')
        textframe = tk.Frame(text_window)
        results = get_words_with_set_value(wv, scale)
        results = [word.upper().strip() for word in results]
        number_of_words = len(results)
        decoration_length = len(str(number_of_words)) + 6
        results = ('\n'.join(results))
        output = tk.Text(textframe, height=25, width=24,
                         font=f'{a.FDATA} {a.FSMALL}')
        introtext = f'{number_of_words} words\n{"-" * decoration_length}\n'
        output.insert('end', introtext)
        output.insert('end', results)
        output.pack(side="left", expand=True)
        output.config(state='disabled')
        scroller = tk.Scrollbar(textframe)
        scroller.pack(side='right', fill='both')
        output.config(yscrollcommand=scroller.set)
        scroller.config(command=output.yview)
        textframe.pack(expand=True)
        pzt.place_footer(f"{a.dictnote}")

        # text file of word value results
    def create_wv_text_file(self, scale, wv):
        '''
        gathers a create a text file with name wv(scale)(#).txt
        see footnote in main window for name of the file written
        '''
        results = get_words_with_set_value(wv, scale)
        results = [word.upper() for word in results]
        filename = f'{scale.lower()}_wv{wv}.txt'
        with open(filename, 'w') as f:
            f.write(f'{len(results)} words\n')
            for word in results:
                f.write(f'{word}\n')
        pzt.place_footer(f"wrote file {scale.lower()}_wv{wv}.txt"
                         f" with {len(results)} words -- {a.dictnote}")


# Tables - basic table and header table as subclass (with changed font)
class RegularTable(tk.Frame):
    def __init__(self, parent, width, rows, columns):
        tk.Frame.__init__(self, parent)
        self.table_data = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text=f"row {row}/col {column}",
                                 width=width[column], bg=a.BG1)
                label.grid(row=row, column=column,
                           sticky="nsew", padx=0, pady=0)
                current_row.append(label)
            self.table_data.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value, f=f'{a.FDATA} {a.FMEDIUM}'):
        cell = self.table_data[row][column]
        cell.configure(text=value, font=f,
                       bg=a.BG1, fg=a.FG1, anchor="center")


class TableHeader(RegularTable):
    def __init__(self, parent, width, rows, columns,
                 f=f'{a.FTITLE} {a.FMEDIUM} bold underline'):
        super().__init__(parent, width, rows, columns)

    def set(self, row, column, value,
            f=f'{a.FTITLE} {a.FMEDIUM} bold underline'):
        cell = self.table_data[row][column]
        cell.configure(text=value, font=f,
                       bg=a.BG1, fg=a.FG1, anchor="center")


def main():
    pzt.run()


if __name__ == "__main__":
    pzt = PuzzleTools()
    main()
