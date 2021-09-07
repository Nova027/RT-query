import ply.lex as lex
import ply.yacc as yacc

from A8T1_plus_Helpers import html2str


# Data Structure to store Celeb data

celeb_data = {3:None , 4:None , 5:None , 6:[]}



#................................................................................ Defining Lexing Rules .............................................................................#


tokens = ('HI_RATED_OPEN', 'LO_RATED_OPEN', 'BDAY_OPEN', 'FILM_TABLE_OPEN', 'FILM_TITLE_OPEN', 
		  'FILM_YEAR_OPEN', 'COL_CLOSE', 'TABLE_CLOSE', 'P_CLOSE', 'CONTENT')


def t_HI_RATED_OPEN(t):
	r'<p[\s]*[\s]class[\s]*=[\s]*"[^"]*"[\s]*[\s]data-qa[\s]*=[\s]*"celebrity-bio-highest-rated"[\s]*>[\s]*Highest[\s]*[\s]Rated[\s]*:'
	return t

def t_LO_RATED_OPEN(t):
	r'<p[\s]*[\s]class[\s]*=[\s]*"[^"]*"[\s]*[\s]data-qa[\s]*=[\s]*"celebrity-bio-lowest-rated"[\s]*>[\s]*Lowest[\s]*[\s]Rated[\s]*:'
	return t


def t_BDAY_OPEN(t):
	r'<p[\s]*[\s]class[\s]*=[\s]*"celebrity-bio__item"[\s]*[\s]data-qa[\s]*=[\s]*"celebrity-bio-bday"[\s]*>[\s]*Birthday[\s]*:'
	return t


def t_FILM_TABLE_OPEN(t):
	r'<div[\s]*>[\s]*<h3[\s]*[\s]class[\s]*=[\s]*"[^"]*"[\s]*[\s]data-qa[\s]*=[\s]*"[a-z]*-filmography-movies-[a-z]*"[\s]*>[\s]*Movies[\s]*</h3[\s]*>[\s]*<div[\s][^>]*>[\s]*<table[\s]*>'
	return t


def t_FILM_TITLE_OPEN(t):
	r'<td[\s]*[\s]class[\s]*=[\s]*"celebrity-filmography__title"[\s]*>'
	return t


def t_FILM_YEAR_OPEN(t):
	r'<td[\s]*[\s]class[\s]*=[\s]*"celebrity-filmography__year"[\s]*>'
	return t


def t_COL_CLOSE(t):
	r'</td[\s]*>'
	return t


def t_TABLE_CLOSE(t):
	r'</table[\s]*>'
	return t


def t_P_CLOSE(t):
	r'</p[\s]*>'
	return t



#.................... Other Content .....................#

# All Other Non-tag Content
def t_CONTENT(t):
	r'[^<>]+'
	return t

# Least preference among all other Tags (No return => Token discarded)
# Removes unnecessary tags in between (Ease of processing)
def t_TAG(t):
	r'<[^>]+>'
	pass



# A string containing ignored characters (spaces and tabs)
t_ignore  = ' >\t'


# Error handling rule
def t_error(t):
	print("Discarding invalid character '%s'" % t.value[0])
	t.lexer.skip(1)





#................................................................... Defining Grammar Production rules......................................................................#

#........ Start symbol ........#
# Each non-terminal used, also produces <empty>, so the absence of any of the fields causes no problem
def p_S(p):
	'S : txt hi_rated txt lo_rated txt bday txt filmography txtlast'
	p[0] = 'Done!'



#................................... Value-based ...................................#

def p_hi_rated(p):
	'''hi_rated : HI_RATED_OPEN CONTENT CONTENT P_CLOSE
				| HI_RATED_OPEN CONTENT P_CLOSE
				| 
	'''
	# Assumption : If only 1 content section -> Rating is not displayed
	if len(p) == 4:
		celeb_data[3] = p[2].strip() + '\n' + 'Rating : __'

	elif len(p) == 5:
		celeb_data[3] = p[3].strip() + '\n' + 'Rating : ' + p[2].strip()



def p_lo_rated(p):
	'''lo_rated : LO_RATED_OPEN CONTENT CONTENT P_CLOSE
				| LO_RATED_OPEN CONTENT P_CLOSE
				| 
	'''
	# Assumption : If only 1 content section -> Rating is not displayed
	if len(p) == 4:
		celeb_data[4] = p[2].strip() + '\n' + 'Rating : __'

	elif len(p) == 5:
		celeb_data[4] = p[3].strip() + '\n' + 'Rating : ' + p[2].strip()



def p_bday(p):
	'''bday : BDAY_OPEN CONTENT P_CLOSE
			| 
	'''
	if len(p) != 1:
		celeb_data[5] = p[2].strip()



#................................... List-based ...................................#


def p_filmography(p):
	'''filmography : FILM_TABLE_OPEN txt_table film_rows
				   | 
	'''


def p_film_rows(p):
	'''film_rows : FILM_TITLE_OPEN CONTENT COL_CLOSE txt_table FILM_YEAR_OPEN CONTENT COL_CLOSE txt_table film_rows
				 | TABLE_CLOSE
	'''
	if len(p) > 2:
		f_title = p[2].strip()
		f_ystr = p[6].strip()
		
		try:
			f_year = int(f_ystr)
			f_title += ' (' + f_ystr + ')'

		except Exception:
			f_year = 3021		# Indicative of unknown --> Large no. used as key; to ensure "ON / AFTER" filter displays movie last
			f_title += ' ( <<Unreleased / Unknown>> )'

		celeb_data[6].append((f_year, f_title))





#................................... Miscellaneous & Error-handling ...................................#

# If TV table doesn't appear, all potential nuisance tokens are handled by txt production
# If txt cannot at some point, txtlast handles all tokens henceforth


# Keeping separate txt_table production ensures that txt_table doesn't eat up the TABLE_CLOSE token, like txt would have. Hence, the table_rows production is forced to terminate
# at the first appearance of TABLE_CLOSE terminal....
# ..... after which txtlast can take over seamlessly.

# Haven't removed TABLE_CLOSE from txt production, to allow appearance of tables before filmography (even though it doesn't in current RT pages)

# In case filmography section is missing, txt production will keep parsing until it can't. May even parse till end, and txtlast can then simply derive <empty>
# (Of course, filmography will also have to derive to <empty> at the very end in that case. Not as per expectation, but not a problem)

# If filmography is not missing, but no rows are present, even then TABLE_CLOSE token must come (since <table> open occurred) ... So, won't cause a problem.




# Handles random content before Filmography non-terminal appears
def p_txt(p):
	'''txt : CONTENT txt
		   | COL_CLOSE txt
		   | TABLE_CLOSE txt
		   | P_CLOSE txt
		   | 
	'''


# Handles random content within Film table
def p_txt_table(p):
	'''txt_table : CONTENT txt
		   		 | COL_CLOSE txt
			   	 | P_CLOSE txt
			   	 | 
	'''



# Handles random content after Film table
def p_txtlast(p):
	'''txtlast : txtlast CONTENT
		   	   | txtlast COL_CLOSE
		   	   | txtlast P_CLOSE
		   	   | txtlast TABLE_CLOSE
		   	   | txtlast FILM_TITLE_OPEN
		   	   | txtlast FILM_YEAR_OPEN
		   	   | 
	'''








# Syntax Error handling rule (Ignore unexpected tokens)
def p_error(p):
	pass


#............................................................................................ Driver portion ........................................................................#


# Function to define Lexer, Parser
# and Parse celebrity webpage.
def parse_celpage():
	lex.lex()
	hparser = yacc.yacc(debug=0)

	global celeb_data
	celeb_data = {3:None , 4:None , 5:None , 6:[]}
	
	celpage_str = html2str('Celeb_webpage.html')
	hparser.parse(celpage_str)

	return celeb_data



# Demonstration (debug) code to be run to check celeb-parsing
# Executes if this code is directly executed, and not via import.
if __name__ == '__main__':
	celdata = parse_celpage()

	print(celdata)