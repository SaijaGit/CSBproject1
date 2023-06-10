from django.db import models

from django.contrib.auth.models import User

class SecretNote(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	
	# Comment the following line to fix flaw 4 Cryptographic Failures
	note = models.TextField()

	# Remove the comment from the last line to fix flaw 4 Cryptographic Failures
	# After that run the following in the command line to migrate the changes into database:
	# python manage.py makemigrations SecretNotes
	# python manage.py migrate
	#note = models.BinaryField()