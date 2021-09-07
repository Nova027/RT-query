import A8T1_plus_Helpers as A8T1
from A8T1_plus_Helpers import html2str, prompter, validr_input

from os import path, remove, rename
from urllib import request

import re

import ply.lex as lex
import ply.yacc as yacc

from A9T2_celparse import parse_celpage



#.......................................................................... Initial Setup ...................................................................#

# List to store query-fields & Corresponding Results (extracted)
# Cast-Crew Sub-details fields defined at Parse-time dynamically (depending on no. of cc-members)
movie_data = [
			  ['1. Movie Name', None],
			  ['2. Directors', []],
			  ['3. Writers', []],
			  ['4. Producers', []],
			  ['5. Original Language', None],
			  ['6. Cast & Crew', []],
			  ['7. Storyline', None],
			  ['8. Box Office (USA)', None],
			  ['9. Runtime', None],
			  ['10. Movie Recommendations', []],
			  ['11. Where to Watch', []]
			 ]




# Check if the Assgn8 HTML Output exists
if not path.isfile('Movie_webpage.html'):
	# If not.... Perform Assgn8 Task-1 & Download 'Movie_webpage.html' (as not already done)
	reqgenre = A8T1.in_genre()
	mlist_str = html2str(reqgenre+'.html')

	movie_dict = A8T1.listmov_table(mlist_str)

	# No table matched expected Target Table formatting
	if movie_dict is None:
		print('Unexpected issue occurred with Downloaded HTML!')
		exit()

	A8T1.down_movie(reqgenre, movie_dict)







#.......................................................................... Extra Query-Functions ...................................................................#






def reset_data():
	global movie_data

	movie_data = [
					['1. Movie Name', None],
					['2. Directors', []],
					['3. Writers', []],
					['4. Producers', []],
					['5. Original Language', None],
					['6. Cast & Crew', []],
					['7. Storyline', None],
					['8. Box Office (USA)', None],
					['9. Runtime', None],
					['10. Movie Recommendations', []],
					['11. Where to Watch', []]
				]

	pass






#........... Update Movie table with info about given celeb
def celinfo_update(celeb_id):
	# Download & Save HTML file from corresp. URL
	response = request.urlopen('https://www.rottentomatoes.com' + movie_data[5][1][celeb_id][1])
	content = response.read()

	with open('Celeb_webpage.html', 'wb') as f:
		f.write(content)

	# Make A9T2 parse the downloaded celeb webpage HTML
	celdata = parse_celpage()

	# Save the data extracted
	for info_id in celdata:
		movie_data[5][1][celeb_id][info_id][1] = celdata[info_id]






#.......... Display requested Info of requested Celebrity
def celq_process(celeb_id, info_id):
	target = movie_data[5][1][celeb_id][info_id]

	query = target[0][3:]
	print()
	print(query, ':')

	if info_id != 6:
		# Basic info (Birthday, Lowest/Highest rated movie)
		print(target[1])

	else:
		movlist = target[1]
		
		# Take filter-year as input
		try:
			filter_year = int(input('Enter Year to filter (Enter "-1" for no-filter): '))	# Considering year-no. can only be +ve
			print()
			if filter_year == -1:
				print('.......... Displaying full list ..........')
			else:
				print('.......... Displaying movies on/after', filter_year, '..........')

		except:
			print('\n.......... Invalid input ignored. Displaying full list ..........')
			filter_year = -1

		filtered_movlist = [mov for (movyear,mov) in movlist if movyear >= filter_year]

		for fmov in filtered_movlist:
			print(fmov)

	prompter()













#................................................................................ Defining Lexing Rules .............................................................................#

tokens = ('TITLE_OPEN', 'DIRECTOR_LABEL','WRITER_LABEL','PRODUCER_LABEL','LANGUAGE_LABEL','BOXOFF_LABEL','RUNTIME_LABEL', 'PLOT_OPEN', 'RECSPAN_OPEN', 'WTWLIST_OPEN', 'WTW',
			'MINFO_VALUE_OPEN', 'TSPAN_OPEN', 'CSPAN_OPEN', 'RECLINK', 'CCILINK', 'LINK', 'CONTENT', 'DIV_CLOSE', 'A_CLOSE', 'SPAN_CLOSE', 'TITLE_CLOSE', 'BREAK')


# Defining Token strings only, would cause precedence order to be implicit as per string length
# So... Defining Token functions to explicitly handle Precedence order (Solves prefix problem)

#................... Relevant Labelled Sections ....................#

def t_DIRECTOR_LABEL(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-label[\s]subtle"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-label"[\s]*>[\s]*Director[\s]*:[\s]*</div[\s]*>'
	return t

def t_WRITER_LABEL(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-label[\s]subtle"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-label"[\s]*>[\s]*Writer[\s]*:[\s]*</div[\s]*>'
	return t

def t_PRODUCER_LABEL(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-label[\s]subtle"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-label"[\s]*>[\s]*Producer[\s]*:[\s]*</div[\s]*>'
	return t

def t_LANGUAGE_LABEL(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-label[\s]subtle"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-label"[\s]*>[\s]*Original[\s]*[\s]Language[\s]*:[\s]*</div[\s]*>'
	return t

def t_BOXOFF_LABEL(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-label[\s]subtle"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-label"[\s]*>[\s]*Box[\s]*[\s]Office[\s]*[\s]\([\s]*Gross[\s]*[\s]USA[\s]*\)[\s]*:[\s]*</div[\s]*>'
	return t

def t_RUNTIME_LABEL(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-label[\s]subtle"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-label"[\s]*>[\s]*Runtime[\s]*:[\s]*</div[\s]*>'
	return t




#................... Relevant Open-tags. ....................#

def t_WTWLIST_OPEN(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"where-to-watch__body"[\s]*>'
	return t

def t_TITLE_OPEN(t):
	r'<title[\s]*>'
	return t

def t_PLOT_OPEN(t):
	r'<div[\s]*[\s]id[\s]*=[\s]*"movieSynopsis"[^>]*[\s]data-qa[\s]*=[\s]*"movie-info-synopsis"[\s]*>'
	return t

def t_MINFO_VALUE_OPEN(t):
	r'<div[\s]*[\s]class[\s]*=[\s]*"meta-value"[\s]*[\s]data-qa[\s]*=[\s]*"movie-info-item-value"[\s]*>'
	return t

def t_RECSPAN_OPEN(t):
	r'<span[\s]*[\s]slot[\s]*=[\s]*"title"[\s]*[\s]class[\s]*=[\s]*"recommendations-panel__poster-title"[\s]*>'
	return t

def t_TSPAN_OPEN(t):
	r'<span[\s]*[\s]title[\s]*=[\s]*"[^"]*"[\s]*>'
	return t

def t_CSPAN_OPEN(t):
	r'<span[\s]*[\s]class[\s]*=[\s]*"characters[\s]subtle[\s]smaller"[\s]*[\s]title[\s]*=[\s]*"[^"]*"[\s]*>'
	return t




#................... Link-tags & a-tags .......................#

def t_RECLINK(t):
	r'<a[\s]*[\s]href[\s]*=[\s]*"[^"]*"[\s]*[\s]class[\s]*=[\s]*"recommendations-panel__poster-link"[\s]*>'

	linkurl = ((t.value).split('"'))[1]
	t.value = linkurl.strip()

	return t


def t_CCILINK(t):
	r'<a[\s]*[\s]href[\s]*=[\s]*"[^"]*"[\s]*[\s]class[\s]*=[\s]*"[^"]*"[\s]*[\s]data-qa[\s]*=[\s]*"cast-crew-item-link"[\s]*>'

	linkurl = ((t.value).split('"'))[1]
	t.value = linkurl.strip()

	return t


def t_LINK(t):
	r'<a[\s]*[\s]href[\s]*=[\s]*"[^"]*"[^>]*>'
	
	linkurl = ((t.value).split('"'))[1]
	t.value = linkurl.strip()
	
	return t


def t_WTW(t):
	r'<affiliate-icon[\s]*[\s]name[\s]*=[\s]*"[^"]*"[^>]*>'

	watch_src = ((t.value).split('"'))[1]
	t.value = watch_src.strip()

	return t




#................... Close-tags & Misc. ....................#

def t_TITLE_CLOSE(t):
	r'</title[\s]*>'
	return t

def t_DIV_CLOSE(t):
	r'</div[\s]*>'
	return t

def t_A_CLOSE(t):
	r'</a[\s]*>'
	return t

def t_SPAN_CLOSE(t):
	r'</span[\s]*>'
	return t

def t_BREAK(t):
	r'<br/>'
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



#................... Define Lexer
lex.lex()







#............................................................................ Defining Parsing Grammar ........................................................................#


# Start Symbol
def p_S(p):
	'S : txt m_title txt m_rec_list txt m_wtw_table txt mi_plot txt mi_language txt mi_director txt mi_producer txt mi_writer txt mi_boxoff txt mi_runtime txt mi_castcrew_ls txt'
	p[0] = "Parsed."


# YACC does bottom-up parsing & SR conflicts are handled by favouring "shift"... Hence prefix problem is handled.
# RR conflicts are handled by giving precedence to the rule declared first... 
# Hence precedence in case of ambiguity is specified as below order.

#.................................... Value-based ....................................#

def p_m_title(p):
	'''m_title : TITLE_OPEN CONTENT TITLE_CLOSE
			   |
	'''
	if len(p) > 1:
		res = p[2].strip()
		reslist = res.split('-')
		movie_data[0][1] = '-'.join(reslist[:-1])


def p_mi_plot(p):
	'''mi_plot : PLOT_OPEN CONTENT DIV_CLOSE
			   | 
	'''
	if len(p) > 1:
		movie_data[6][1] = p[2].strip()


def p_mi_language(p):
	'''mi_language : LANGUAGE_LABEL MINFO_VALUE_OPEN CONTENT DIV_CLOSE
				   | 
	'''
	if len(p) > 1:
		movie_data[4][1] = p[3].strip()


def p_mi_runtime(p):
	'''mi_runtime : RUNTIME_LABEL MINFO_VALUE_OPEN CONTENT DIV_CLOSE
				  | 
	'''
	if len(p) > 1:
		movie_data[8][1] = p[3].strip()


def p_mi_boxoff(p):
	'''mi_boxoff : BOXOFF_LABEL MINFO_VALUE_OPEN CONTENT DIV_CLOSE
				 | 
	'''
	if len(p) > 1:
		movie_data[7][1] = p[3].strip()



#.................................. List-based .....................................#

# For Directors, Writers, Producers.... 
# (Links are always present).... 
# (If page missing, RT maintains Dummy links)
def p_val_list(p):
	'''val_list : LINK CONTENT A_CLOSE CONTENT val_list
				| LINK CONTENT A_CLOSE
	'''
	if len(p) == 4:
		p[0] = p[2].strip()
	
	else:
		p[0] = p[2].strip() + '\n' + p[5]



def p_mi_director(p):
	'''mi_director : DIRECTOR_LABEL MINFO_VALUE_OPEN val_list DIV_CLOSE
				   | 
	'''
	if len(p) > 1 and len(p[3]) != 0:
		movie_data[1][1] = p[3].split('\n')


def p_mi_writer(p):
	'''mi_writer : WRITER_LABEL MINFO_VALUE_OPEN val_list DIV_CLOSE
				 | 
	'''
	if len(p) > 1 and len(p[3]) != 0:
		movie_data[2][1] = p[3].split('\n')


def p_mi_producer(p):
	'''mi_producer : PRODUCER_LABEL MINFO_VALUE_OPEN val_list DIV_CLOSE
				   | 
	'''
	if len(p) > 1 and len(p[3]) != 0:
		movie_data[3][1] = p[3].split('\n')




#.................... Where to Watch

def p_wtw_list(p):
	'''wtw_list : wtw_list txt WTW
				| 
	'''
	if len(p) != 1:
		(movie_data[10][1]).append(p[3].strip())


def p_m_wtw_table(p):
	'''m_wtw_table : WTWLIST_OPEN wtw_list DIV_CLOSE
				   | 
	'''




#....................... Cast-Crew Members

def p_mi_castcrew_ls(p):
	'''mi_castcrew_ls : mi_castcrew_ls txt cc_member
					  | 
	'''


def p_cc_member(p):
	'''cc_member : CCILINK TSPAN_OPEN CONTENT SPAN_CLOSE A_CLOSE CSPAN_OPEN BREAK CONTENT BREAK CONTENT SPAN_CLOSE
				 | CCILINK TSPAN_OPEN CONTENT SPAN_CLOSE A_CLOSE CSPAN_OPEN BREAK CONTENT BREAK SPAN_CLOSE
				 | CCILINK TSPAN_OPEN CONTENT SPAN_CLOSE A_CLOSE CSPAN_OPEN BREAK CONTENT SPAN_CLOSE
				 | CCILINK TSPAN_OPEN CONTENT SPAN_CLOSE A_CLOSE CSPAN_OPEN BREAK SPAN_CLOSE
				 | TSPAN_OPEN CONTENT SPAN_CLOSE CSPAN_OPEN BREAK CONTENT BREAK CONTENT SPAN_CLOSE
				 | TSPAN_OPEN CONTENT SPAN_CLOSE CSPAN_OPEN BREAK CONTENT BREAK SPAN_CLOSE
				 | TSPAN_OPEN CONTENT SPAN_CLOSE CSPAN_OPEN BREAK CONTENT SPAN_CLOSE
				 | TSPAN_OPEN CONTENT SPAN_CLOSE CSPAN_OPEN BREAK SPAN_CLOSE
	'''
	linkf = True

	if (p[1].strip())[0] == '<':
		ccname = p[2].strip()
		cclink = None
		linkf = False
	else:
		ccname = p[3].strip()
		cclink = p[1].strip()

	if len(p)==7 or (len(p)==9 and linkf):
		char_or_role = '<Unspecified>'

	elif len(p) == 8:
		char_or_role = '(' + p[6].strip() + ')'

	elif len(p) == 9:
		char_or_role = p[6].strip()

	elif len(p) == 10:
		if linkf:
			char_or_role = '(' + p[8].strip() + ')'
		else:
			char_or_role = p[6].strip() + ' (' + p[8].strip() + ')'

	elif len(p) == 11:
		char_or_role = p[8].strip()

	else:
		char_or_role = p[8].strip() + ' (' + p[10].strip() + ')'

	crlist = char_or_role.split(',')
	for i,cr in enumerate(crlist):
		crlist[i] = cr.strip()

	char_or_role = ', '.join(crlist)

	ccinfo = [ ccname, 
			   cclink, 
			   char_or_role, 
			   ['1. Highest Rated Film', None], 
			   ['2. Lowest Rated Film', None],
			   ['3. Birthday', None],
			   ['4. His/Her Other Movies', []] 
			 ]

	(movie_data[5][1]).append(ccinfo)





#......................... Movie-Recomm.s list

def p_m_rec_list(p):
	'''m_rec_list : m_rec_list movie_rec
				  | 
	'''


def p_movie_rec(p):
	'''movie_rec : RECLINK RECSPAN_OPEN CONTENT SPAN_CLOSE A_CLOSE
				 | RECSPAN_OPEN CONTENT SPAN_CLOSE
	'''
	if len(p) == 4:
		(movie_data[9][1]).append( (p[2].strip(), None) )
	
	else:
		(movie_data[9][1]).append( (p[3].strip(), p[1].strip()) )




#............................. Miscellaneous & Error-handling ................................#

# Least precedence for the randomly appearing tokens
# None of the "Label" tokens or Marker tokens are included in RHS, 
# except TSPAN_OPEN .... Will be handled as 
# "Shift" is favoured for SR conflict
def p_txt(p):
	'''txt : CONTENT txt
		   | MINFO_VALUE_OPEN txt
		   | DIV_CLOSE txt
		   | SPAN_CLOSE txt
		   | A_CLOSE txt
		   | BREAK txt
		   | 
	'''


# Syntax Error handling rule (Ignore unexpected tokens)
def p_error(p):
	pass






#............ Defining parser

hparser = yacc.yacc(debug=0)







#...................................................... Read Data & Parse (Tokenization is implicit) ....................................................#

movie_str = html2str('Movie_webpage.html')

hparser.parse(movie_str)





#...................................................................... Query Processing .................................................................#

# Offer list of available queries
# Perform User-specified query & get result

while True:
	back_option = False

	print('.......................................................................................................')
	print()
	print('Enter Movie Query (Options):')
	
	for md in movie_data:
		print(md[0])
	print('12. Quit')

	qnum = validr_input(0, 11, 'Select an option')

	if qnum == 11:
		break

	query = movie_data[qnum][0]
	query = query[3:].strip()
	print()
	print(query, ':')


	#........................... Perform suitable action acc to query ............................#


	#................ Multi-value cases (Director, Producer, Writer, Watch-source)
	if qnum == 1 or qnum == 2 or qnum == 3 or qnum == 10:
		res = movie_data[qnum][1]
		for r in res:
			print(r)




	#.................... Recursive case (Recommendation browsing)
	elif qnum == 9:
		reclist = movie_data[qnum][1]
		rcount = len(reclist)


		print('Browse Movie Recommendations (List):-')
		for i, rec in enumerate(reclist):
			print(str(i+1) +". " + rec[0])
		print(str(rcount+1) +". <<Go back to Main Menu>>")

		rec_qnum = validr_input(0, rcount, 'Select from options', 'to explore Movie [WARNING! Irreversible action] ')


		if rec_qnum == rcount:
			back_option = True

		elif reclist[rec_qnum][1] is None:
			print('<Webpage Missing, Cannot Download!> (Old movie not removed)')

		else:
			# Download new Movie from Recomm. list
			requrl = 'https://www.rottentomatoes.com' + reclist[rec_qnum][1]
			response = request.urlopen(requrl)
			content = response.read()

			with open('Movie_webpage.html', 'wb') as f:
				f.write(content)

			# Reset Parser (Req.d if Celebrity parser (in same directory) replaced current parser!)
			lex.lex()
			hparser = yacc.yacc(debug=0)
			
			# Reset old info & Parse info from new movie HTML
			reset_data()
			movie_str = html2str('Movie_webpage.html')
			hparser.parse(movie_str)

			print('New Movie ready to Browse! (Old removed)')
			





	#................... Hierarchical case (Individual cast info browsing)
	elif qnum == 5:
		cclist = movie_data[qnum][1]
		ccount = len(cclist)

		while True:
			print('- - - - - - - - - - - - - - - - - - - - - - - - -')
			print('Browse Cast & Crew info (List):-')
			for i, cc in enumerate(cclist):
				print(str(i+1) +". " + cc[0] + " : " + cc[2])
			print(str(ccount+1) +". <<Go back to Main Menu>>")

			subqnum = validr_input(0, ccount, 'Select an option')


			if subqnum == ccount:
				back_option = True
				break

			elif cclist[subqnum][1] is None:
				print('<Webpage Missing, Cannot display info>')
				prompter()

			else:
				q_ccmem = cclist[subqnum]

				# Check if Celeb-info is missing
				# If yes, download Celebrity HTML & use 
				# info-extraction fns from A9T2_celparse
				if q_ccmem[3][1] is None:
					celinfo_update(subqnum)		# Call fn to update Movie-info list with A9T2-data

				# Answer Celeb-query
				print()
				print('See info about', q_ccmem[0], ':')
				for f in range(3,7):
					print(q_ccmem[f][0])
				print('5. <<Go back to Main Menu>>')

				celinf_qnum = 3 + validr_input(0, 4, 'Select an option')

				if celinf_qnum == 7:
					back_option = True
					break

				celq_process(subqnum, celinf_qnum)

			# End-of-while (Repeats Cast-Crew Browsing List) 
			# (Select last option to go back to Main menu)




	#....................... Single-value cases (All other)
	else:
		print(movie_data[qnum][1])


	# End of an iteration of Movie-info querying
	print()
	if not back_option:
		prompter()






#........................................................... Clean-up ......................................................#

if path.isfile('Movie_WP_processed.html'):
	remove('Movie_WP_processed.html')

rename('Movie_webpage.html', 'Movie_WP_processed.html')



if path.isfile('Celeb_WP_processed.html'):
	remove('Celeb_WP_processed.html')

if path.isfile('Celeb_webpage.html'):
	rename('Celeb_webpage.html', 'Celeb_WP_processed.html')