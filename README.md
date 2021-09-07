# RottenTomatoes Query-Answering App

To execute the programs in correct order, simply open a Linux terminal in this location and type the following command :
> make

In a non-linux environment, following command can be used instead :
> python3 task_1_2_driver.py

----------------------------------------------------------------------------------------------------------------------------------------

Makefile internally runs command "python3 task_1_2_driver.py", which makes use of the other 3 provided programs.

For the program to execute, the working directory must contain:
- task_1_2_driver.py : Main Driver program.
- A8T1_plus_Helpers.py : Helper functions.
- char_read.py : For useful input-methods used throughout.
- A9T2_celparse.py : Lexer and Parser designed for Celebrity webpages of RT.

-------------------------------------------------------------------------------------------------------------------------------------------

If a "Movie_webpage.html" already exists in current location (for whatever reason), 
The Driver code offers queries for that particular movie, and doesn't start from scratch.

Else,
It starts directly from Genre-input, and taking input the choice of movie from top-100 of that genre, 
followed by an infinitely iterative browsing of Movie-info.

A new movie webpage can be downloaded for info extraction, to replace the current one, using the "Movie recommendations" option in each movie webpage.

------------------------------------------------------------------------------------------------------------------------------------------

Also, the "A9T2_celparse.py" file can be run independently as well, provided a "Celeb_webpage.html" file is currently present.
(Initially this html will be absent, but can be either manually downloaded from RottenTomatoes (just download any webpage about a celebrity and name it "Celeb_webpage.html", 
or otherwise, it may get autodownloaded when browsing through the app, if a celebrity-based query is made).

** Extensive error-handling has been done, to cover even the corner cases which do not occur in the RT pages of today. **
(See the presence of empty productions & the definitions of txt, txtlast, etc productions)
