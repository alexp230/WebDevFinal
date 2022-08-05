Operaterates correctly on:
	IDE: 
	 - VSCode

	Python:
	 - Python 3.8.5 (Base conda)
 	 - Python 3.9.12 (Base conda)
	(Haven't tested on any other versions but should work fine)
 
	Framework:
	 - Flask 1.1.2

	Library:
	 - Werkzeug 2.0.3

	Browser:
	 - Google Chrome


Instructions: 

Once you have cloned this repository you will need to make sure you have all these versions listed above to guarentee a working website.

After this is complete, open the repository folder in VSCode and make sure that your python interpreter is set to conda. Now you should be able 

to change into the directory containing this repository in your Windows command prompt, once inside this folder, run the 'signinup.py' file to 

boot up the server. You may get a few errors in the beginning telling you to make sure you have all the libraries installed. When installing 
 
these, make sure that you are using the proper pip command based off which version of python you are using (pip install, pip3 install)

After installing the required libraries you should be able to run the python file 'signinup.py'. This should get the server up and running

and by going to the websites url (http://127.0.0.1:5000) and now should be able to view our website.