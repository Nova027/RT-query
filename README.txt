To execute the programs in correct order, simply open terminal in the correct location and type the following command:

make


----------------------------------------------------------------------------------------------------------------------------------------

This internally runs command "python3 task_1_2_driver.py", which makes use of the other 3 functions provided.

For the program to execute, the working directory must contain:
> A8T1_plus_Helpers.py  
> char_read.py
> A9T2_celparse.py
> task_1_2_driver.py
> Makefile


If makefile is missing, simply open the terminal within the PWD, and run :

python3 task_1_2_driver.py


-------------------------------------------------------------------------------------------------------------------------------------------

If a "Movie_webpage.html" already exists in current location for whatever reason, the Driver code offers queries for that particular movie, and doesn't start from scratch.

Else, it starts directly from Genre input, and input the choice of movies from top-100 of the genre, followed by an infinitely iterative browsing of Movie-info. A new movie can be downloaded for info extraction, to replace the current one, using "Movie recommendations".

------------------------------------------------------------------------------------------------------------------------------------------

Also, the "A9T2_celparse.py" file can be run independently as well, provided a "Celeb_webpage.html" file is currently present.



** Extensive error-handling has been done, to cover even the corner cases which do not occur in the RT pages of today. **
(See the presence of empty productions & the definitions of txt, txtlast, etc productions)