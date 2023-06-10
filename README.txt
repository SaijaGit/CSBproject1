# Cyber Security Base 2023: Project I

Link to the Github repository of the project: https://github.com/SaijaGit/CSBproject1
This report with links can be found in the project's readme file.

This project contains 4 errors from the OWASP 2021 list and CSRF. 


### Installation instructions: 

1. Download the project from Github 
2. Start the server with the command python manage.py runserver 
3. Open the application in a browser at http://localhost:8000/ 


### Instructions for the database: 

1. Initially, use the default database file db.sqlite
2. The database files db2.sqlite3 and db2_encrypted.sqlite3 are backup files from which you can restore a working database if necessary. 
3. If you change the content of the database file from the backup (still keep the default name db.sqlite3!), or you encounter other problems with the database, you may have to initialize the database again with the following commands:
	python manage.py makemigrations
	python manage.py migrate


## User accounts: 

Administrator: username = admin and password = admin 
User: username = bob and password = bob 
User: username = alice and password = 123




## FLAW 1: Injection

Link:
https://github.com/SaijaGit/CSBproject1/blob/570792ac97bb7ba33810a24c1a8620e0b2985c50/SecretNotesApp/SecretNotes/views.py#L69


### Description

Injection is a security flaw where software vulnerabilities allow users to inject code or other commands into an application so that they are interpreted although they should not be. They can cause the app to perform malicious actions, such as leaking or destroying data.

In this application, the injection targets the system's SQL database. It can happen if the user saves a Secret Note that contains SQL queries. When such a note is deleted in an incorrect version of the software, it is searched from the database based on the text, and it is possible that the SQL queries contained in the text are executed. 

This is because the program does the SQL queries related to deleting messages by writing them directly to the database. It also forms the query string with variables. The Django documentation says "Warning! Do not use string formatting on raw queries. … If you use string interpolation or quote the placeholder, you’re at risk for SQL injection."

NOTE! The code with Injection flaw does not work if you have already fixed the flaw 4 Cryptographic Failures! While testing the flaws, please fix them in the order they are in this essay!


### How to perform the injection:

1. Write a following secret note into "Create a New Secret Note" text area: 1'; DROP TABLE 'SecretNotes_secretnote'; --'

2. Click "Save"

3. Delete the newly created note by clicking the "Delete" button below it

4. The whole secret note database is destroyed!

5. At this point the app crashes, because it can not work without SQL table SecretNotes_secretnote


### How to fix it

Use "noteToDelete.delete()" instead of writing SQL queries straight with "cursor.executescript". cursor.executescript does not check the data, it just sends it to database. noteToDelete.delete() uses Django's own methods to delete data, and they are secured against injection. Also this approach does not send any text from the note to the database, as it only uses id-number to identify the note to remove, so it is safer also this way.

	Comment away lines: views.py 69-71
	Remove the comments from the lines: wiews.py 74

In the project's repository on Github, there is a backup for the database under the name db2.sqlite3, which you can use to restore the database file and continue using the program. 




## FLAW 2: Broken Access Control
Link:
https://github.com/SaijaGit/CSBproject1/blob/570792ac97bb7ba33810a24c1a8620e0b2985c50/SecretNotesApp/SecretNotes/views.py#L61


### Description

Broken Access Control is a security flaw, where unauthorized access is allowed to server resources or functionalities. For example, a web application might expose user-specific data, if the user manipulates query parameters or path variables. While the application requires the user to be signed in, it fails to ensure they have rights for specific actions.

The Secret Notes App has a "Delete" button for each note, which is used to delete the note. In this way, the user can delete only their own notes. However, it is also possible to delete notes by passing the note_id of as a URL parameter from the address bar of the browser. The Broken Access Control vulnerability is caused by the fact that the app does not check whether the note to be deleted belongs to the user who is signed into the application.


### How to exploit the Broken Access Control vulnerability:

In the address line of the browser, write e.g. http://localhost:8000/delete/?note_id=15 
The number in the end is the id number of the note to be deleted, which of course can be any other number, also the id number of another user's note.


### How to fix it

This vulnerability can be removed by adding a check that the note is deleted only if it is owned by the user that is signed in:
	Remove comments from views.py lines 62-66




## FLAW 3: CSRF (Cross-Site Request Forgery)
Links: https://github.com/SaijaGit/CSBproject1/blob/570792ac97bb7ba33810a24c1a8620e0b2985c50/SecretNotesApp/SecretNotes/views.py#L14
https://github.com/SaijaGit/CSBproject1/blob/570792ac97bb7ba33810a24c1a8620e0b2985c50/SecretNotesApp/SecretNotes/templates/SecretNotes/index.html#L133


### Description

CSRF enables unauthorized requests from a different site. This can happen, if the user of the app is signed in the app, but interacts with a malicious web page which secretly sends a request to the app. If the CSRF is not checked, the request from the foreign page is executed, because it is interpreted as valid based on the user's cookie. To prevent this most frameworks now have built-in CSRF defenses and browsers protect cookies more seriously.


### How to fix it

Enable the csrf_token in the “Add” form of the index.html by removing the comment tags around it:
	Remove comment tags from index.html lines 132 & 134.

Comment out the @csrf_exempt from the addView function:
	Comment out the line 14 in views.py




## FLAW 4: Cryptographic Failures
Link:
https://github.com/SaijaGit/CSBproject1/blob/570792ac97bb7ba33810a24c1a8620e0b2985c50/SecretNotesApp/SecretNotes/views.py#L11


### Description

Even if all previous security vulnerabilities are patched, the notes in this application are not very secure as they are stored in the database in text format and can be easily read with any sql file viewer.

Secret information should be stored encrypted. In the patched version of this application, notes are encrypted using Fernet cryptography, where messages are encrypted and decrypted with the same key. 

Note! In a real application, the encryption key should be hidden, e.g. using an env file, but in this project it is just defined in the settings.py file (line 132) to make testing easier. 


### How to fix it

As a result of fixing the cryptographic fault, the string-format notes become byte-format when they are encrypted. This requires changes to the database also. When fixing this, the messages stored in unencrypted string format must either be deleted first, and then the database migrated again:

1. Remove all notes from the database either manually from the app, or from command line by starting SQLite with command “sqlite3 db.sqlite3” and then emptying all notes with command “delete from SecretNotes_secretnote;”

2. Modify the format of the notes in the database in models.py: 
	Comment the line 9
	Remove the comment from the following line 15

3. After that run the following in the command line to migrate the changes into database:
	python manage.py makemigrations SecretNotes
	python manage.py migrate

4. If you encounter problems, you can remove the table using the SQLite command "DROP TABLE 'SecretNotes_secretnote';" or copy the database backup file db2_encrypted.sqlite3 and rename it to db.sqlite3. After this run the commands from step 3.

5. Add encryption to views.py by:
	commenting out lines 29 and 52
	removing comments on lines 11, 24-26, 55 and 99-105



## FLAW 5: Security Misconfiguration
Link:
https://github.com/SaijaGit/CSBproject1/blob/570792ac97bb7ba33810a24c1a8620e0b2985c50/SecretNotesApp/SecretNotesApp/settings.py#L94


### Description

Security misconfiguration flaws are a set of vulnerabilities that are caused by bad practices related to e.g. server settings, passwords and software updates. 

The problem with this application is that there are no requirements set for passwords, so users may use passwords that are not secure. Also, the administrator of the application has never changed his password, which is the default password "admin" and can therefore be easily cracked. 


### How to fix it

1. Add validation requirements for passwords to the AUTH_PASSWORD_VALIDATORS list in the settings.py: 
	Remove the comments from the lines 94-107

2. Start the app and log in as administrator with username: admin and password: admin.

3. Go to administration page on the address http://localhost:8000/admin and change password to match the new requirements. 

4. The passwords of the other users can also be changed on this page.

