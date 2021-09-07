from urllib import request
import re
from html import unescape

from char_read import getch as getchar
import sys

#................................................................ Useful Helper Functions ........................................................................#

"""
Function to wait for User-input
"""
def prompter():
    print('Press Any Key to Continue...', end=' ')
    sys.stdout.flush()

    prompt = getchar()
    print()

    pass


""" 
Function to check whether (string) s 
matches the pattern of (regex) r
"""
def re_match(r,s):
    # re matching has to be greedy
    parts = re.split(r, s)
    if len(parts) != 2 or len(parts[0])!=0 or len(parts[1])!=0:
        return False
    return True


""" 
Function to read an HTML file int a string, remove newlines & 
unescape HTML escape-characters from string, for ease of processing
"""
def html2str(fname):
    # Open HTML file as UTF-8 text, and read into a string
    with open(fname, encoding='utf-8') as hfile:
        hstr = hfile.read()
    
    hstr = hstr.replace('\n', ' ')
    hstr = unescape(hstr)
    
    return hstr


"""
Function to take valid input within specified numeric range
"""
def validr_input(lower, upper, display_msg, display_msg_2='', repeat_msg=None):
    opt_range = '(' + str(lower+1) + '-' + str(upper+1) + ')'
    
    if repeat_msg is None:
        repeat_msg = '[Enter index ' + opt_range + '] : '

    display_msg += ' ' + opt_range + ' ' + display_msg_2 + ': '

    try:
        reqnum = int(input(display_msg)) - 1
        if reqnum not in range(lower,upper+1):
            raise ValueError
    
    except Exception:
        reqnum = upper+1
        print('Invalid! Re-enter.')
    
    while reqnum not in range(lower,upper+1):
        try:
            reqnum = int(input(repeat_msg)) - 1
            if reqnum not in range(lower,upper+1):
                raise ValueError
        
        except Exception:
            print('Invalid! Re-enter.')

    return reqnum


#............................................................................ Primary A8T1 Functions ..........................................................................#


"""
------------------------------------------------------------------------------------------------------------------
    Function to Take User-input of Genre from list of valid genres, and download corresp. webpage as HTML file
------------------------------------------------------------------------------------------------------------------
"""
def in_genre():
    genredict = []
    genredict.append(('Action & Adventure', "https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/"))
    genredict.append(('Animation', "https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/"))
    genredict.append(('Drama', "https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/"))
    genredict.append(('Comedy', "https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/"))
    genredict.append(('Mystery & Suspense', "https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/"))
    genredict.append(('Horror', "https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/"))
    genredict.append(('Sci-Fi', "https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/"))
    genredict.append(('Documentary', "https://www.rottentomatoes.com/top/bestofrt/top_100_documentary_movies/"))
    genredict.append(('Romance', "https://www.rottentomatoes.com/top/bestofrt/top_100_romance_movies/"))
    genredict.append(('Classics', "https://www.rottentomatoes.com/top/bestofrt/top_100_classics_movies/"))

    print('List of Genres:')
    for i,genre in enumerate(genredict):
        print(str(i+1) + '. ' + genre[0])
    print()

    # Take genre as user-input, to display movie-list
    reqnum = int(input('Select a Genre [Enter index (1-10)] : ')) - 1
    while reqnum not in range(10):
        print('Invalid! Re-enter.')
        reqnum = int(input('[Enter index (1-10)] : ')) - 1

    reqgenre, requrl = genredict[reqnum]

    # Download & Save HTML file of Top-100 list from corresp. URL
    response = request.urlopen(requrl)
    content = response.read()
    
    with open(reqgenre+'.html', 'wb') as f:
        f.write(content)

    return reqgenre



"""
---------------------------------------------------------------------------------------------------------------------------------------
    Function for Error-checking & Extracting Movie-list with URLs (as list of tuples of Dictionary Key:Value) from HTML (as string)
---------------------------------------------------------------------------------------------------------------------------------------
"""
def listmov_table(mlist_str):
    # Extract all Tables with opening tag like <table class="table">
    regex_tstart = r'<table[\s]*[\s]class[\s]*=[\s]*"table"[\s]*>'
    regex_tend = r'</table[\s]*>'

    table_occs = re.split(regex_tstart, mlist_str)
    
    # Expecting at least 1 such Table (to extract info from)
    if len(table_occs) < 2:
        return None

    table_occs = table_occs[1:]
    for i, table in enumerate(table_occs):
        table_occs[i] = (re.split(regex_tend, table))[0]

    """................... Error checking within Extracted Table(s); Identifying target table & extracting info ..........................."""

    # Some simple regex operation like re.findall("<a[^<]*</a>", table_occs[0]) could ideally find every Movie Name & URL in 3-4 lines... 
    # However, the following code snippet has been written for the purpose of Robustness... So that...
    # Whatever HTML file may get downloaded, this will handle almost all possible errors.
    # And also add extra flexibility to handle slight variations in formatting.
    
    tablefound = False

    for i, table in enumerate(table_occs):
        try:
            t_head,t_cont = re.split(r'</thead[\s]*>', table)
        
        except ValueError:
            # Didnt have exactly one </thead> tag... Unexpected
            continue
                
        ##............... 1. Check Column headings to verify if correct table was found
        regex_chstart = r'<th[\s]*>|<th[\s][^<]*>'
        regex_chend = r'</th[\s]*>'
        headcols = re.split(regex_chstart, t_head)
        if len(headcols) != 5:
            continue
        
        headcols = headcols[1:]
        for j,headcol in enumerate(headcols):
            headcols[j] = (re.split(regex_chend, headcol))[0]
        
        colsfound = True

        # Col-2 header definition:-- <span class="some_string">Rating</span><span class="some_string">Tomatometer</span> ;
        # OR; <span class="some_string">Tomatometer</span><span class="some_string">Rating</span>
        # with any no. of whitespaces allowed in between, wherever possible
        col2_re_half1 = r'<span[\s]*[\s]class[\s]*=[\s]*"[^"]*"[\s]*>[\s]*Rating[\s]*</span[\s]*>[\s]*'
        col2_re_half2 = r'<span[\s]*[\s]class[\s]*=[\s]*"[^"]*"[\s]*>[\s]*Tomatometer[\s]*</span[\s]*>[\s]*'
        col2_re = (r'[\s]*' + col2_re_half1 + col2_re_half2) + "|" + (r'[\s]*' + col2_re_half2 + col2_re_half1)
        
        # List of expected regular expressions for each column header
        regex_heads = [r'[\s]*Rank[\s]*', col2_re, r'[\s]*Title[\s]*', r'[\s]*No.[\s]of[\s]Reviews[\s]*']
        
        # Match col headings to expected heading formats
        for s,r in zip(headcols, regex_heads):
            if not re_match(r,s):
                colsfound = False
                break
        
        if not colsfound:
            continue
        
        ##............. 2. Checking the content rows of the table, for further verification
        regex_rstart = r'<tr[\s]*>'
        regex_rend = r'</tr[\s]*>'
        
        table_rows = re.split(regex_rstart, t_cont)
        
        if len(table_rows) != 101:
            continue
        
        table_rows = table_rows[1:]
        
        # Check columns of each row
        regex_cstart = r'<td[\s]*>|<td [^<]*>'
        regex_cend = r'</td[\s]*>'
        
        # Check movie 'Title' (3rd) column specifically as well, as we extract info from there
        regex_mcol_utag_s = r'[\s]*<a[\s]*[\s]href[\s]*=[\s]*"'
        regex_mcol_utag_e = r'"[\s]*class[\s]*=[\s]*"[^"]*"[\s]*>'
        regex_mcol_s = regex_mcol_utag_s + '/m/[^"]*' + regex_mcol_utag_e
        regex_mcol_e = r'</a[\s]*>[\s]*'
        regex_mcol = regex_mcol_s + r'[^<]*' + regex_mcol_e
        
        tablefound = True
        movie_dict = []     # Dictionary of (Movie Name : Movie URL)
        
        for j,row in enumerate(table_rows):
            table_rows[j] = (re.split(regex_rend, row))[0]
            cols = re.split(regex_cstart, table_rows[j])
            
            # Must have 4 columns (to match 4 column headers)
            if len(cols) != 5:
                tablefound = False
                break
            
            # Check if Movie 'Title' column is in correct format
            movie_col = (re.split(regex_cend, cols[3]))[0]
            
            if not re_match(regex_mcol, movie_col):
                tablefound = False
                break
            
            # Extract Movie name
            mcol_tagstripped = (re.split(regex_mcol_s, movie_col))[1]
            movie_name = (re.split(regex_mcol_e, mcol_tagstripped))[0]
            movie_name = movie_name.strip()
            
            # Extract Movie URL
            mcol_utag = (re.findall(regex_mcol_s, movie_col))[0]
            mcol_utag_estripped = (re.split(regex_mcol_utag_e, mcol_utag))[0]
            movie_url = (re.split(regex_mcol_utag_s, mcol_utag_estripped))[1]
            
            movie_dict.append((movie_name, 'https://www.rottentomatoes.com'+movie_url))
        
        
        ##......... 3. Stop further search for target table, if all conditions matched
        if tablefound:
            return movie_dict

    if not tablefound:
        return None



"""
---------------------------------------------------------------------
 Function to Download RT webpage of entered movie from top-100 list 
---------------------------------------------------------------------
"""
def down_movie(reqgenre, movie_dict):
    # Display top-100 list of movies in Requested Genre
    print('Top 100 Movies in', reqgenre ,'Genre (Pick One) :')
    print('------------------------------------------------------------')
    for i,movie in enumerate(movie_dict):
        print(str(i+1) + '. ' + movie[0])
    print()

    # Take movie as user-input, to download 
    reqnum = int(input('Select a Movie [Enter index (1-100)] : ')) - 1
    while reqnum not in range(100):
        print('Invalid! Re-enter.')
        reqnum = int(input('[Enter index (1-100)] : ')) - 1

    reqmovie, requrl = movie_dict[reqnum]

    # Download & Save HTML file from corresp. URL
    response = request.urlopen(requrl)
    content = response.read()

    with open('Movie_webpage.html', 'wb') as f:
        f.write(content)

    return reqmovie


"""
--------------------------------------------------------
 Function to Log the Query 
--------------------------------------------------------
"""
def logger(reqgenre, reqmovie):
    with open('log.txt', 'a') as f:
        print(reqgenre, ' -- ', reqmovie, end='  --  ', file=f)



##.................................................................. Driver Program for direct execution ....................................................................##

if __name__ == '__main__':
    reqgenre = in_genre()
    mlist_str = html2str(reqgenre+'.html')
    
    movie_dict = listmov_table(mlist_str)

    # No table matched expected Target Table formatting
    if movie_dict is None:
        print('Unexpected issue occurred with Downloaded HTML!')
        exit()

    reqmovie = down_movie(reqgenre, movie_dict)

    logger(reqgenre, reqmovie)
