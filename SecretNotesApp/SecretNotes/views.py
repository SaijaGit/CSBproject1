
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import SecretNote
from django.db import connection
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Remove the comment from the following line to fix flaw 4 Cryptographic Failures
#fernet = Fernet(settings.FERNET_KEY)

# Comment the following line to fix flaw 3 CSRF
@csrf_exempt
@login_required
def addView(request):
	if request.method == 'POST':
		note = request.POST.get('note')
		print("addView: note = ", note)
		owner = request.user
		print("addView: owner = ", owner)

		# Remove the comment from the following lines to fix flaw 4 Cryptographic Failures
		#encrypted_note = fernet.encrypt(note.encode())#('ascii'))#(note.encode('utf-8'))
		#print("addView: encrypted_note = ", encrypted_note)
		#secretnote = SecretNote.objects.create(owner=owner, note=encrypted_note)

		# Comment the following line to fix flaw 4 Cryptographic Failures
		secretnote = SecretNote.objects.create(owner=owner, note=note)

		print("addView: secretnote = ", secretnote)
		secretnote.save()
		print("addView: secretnote.note", secretnote.note)
		print("homePageView: AFTER ADD!! SecretNote.objects.all().count() = ", SecretNote.objects.all().count())

	return redirect('/')


@login_required
def deleteView(request):

	if request.method == 'POST':
		noteToDelete_id = request.POST.get('note_id')

	elif request.method == 'GET':
		noteToDelete_id = request.GET.get('note_id')

	try:
		noteToDelete = SecretNote.objects.get(pk = noteToDelete_id)

		# Comment the following line to fix flaw 4 Cryptographic Failures
		noteToDelete_text = noteToDelete.note

		# Remove the comment from the following line to fix flaw 4 Cryptographic Failures
		#noteToDelete_text = fernet.decrypt(noteToDelete.note).decode()

	except SecretNote.DoesNotExist:
		print("deleteView: The secret note that you are trying to delete does not exist!")
		return redirect('/')
	
	# Remove the comment from the following 5 lines to fix flaw 2 Broken Access Control
	#owner = noteToDelete.owner
	#user = request.user
	#if owner != user :
	#	print("deleteView: You are trying to delete a secret note, that is not owned by you!")
	#	return redirect('/')
	
	# Comment the following 3 lines to fix flaw 1 Injection
	sql_request = f"DELETE FROM SecretNotes_secretnote WHERE id = '{noteToDelete_id}' AND note = '{noteToDelete_text}'"
	with connection.cursor() as cursor:
		cursor.executescript(sql_request)
	
	# Remove the comment from the following line to fix flaw 1 Injection
	# noteToDelete.delete()

	print("deleteView: AFTER DELETE! SecretNote.objects.all().count() = ", SecretNote.objects.all().count())
	return redirect('/')




@login_required
def homePageView(request):


	print("homePageView: request = ", request)
	print("homePageView: SecretNote.objects.all().count() = ", SecretNote.objects.all().count())

	user = request.user

	secretnotes_owned_by = SecretNote.objects.filter(owner=user)
	secretnotes = []
	
	for secretnote in secretnotes_owned_by:

		note_text = secretnote.note

		# Remove the comment from the following lines to fix flaw 4 Cryptographic Failures
		#try:
		#	note_text = fernet.decrypt(secretnote.note.strip()).decode()#.decode('utf-8')
		#	print("homePageView: note_text", note_text)
		#except InvalidToken as e:
		#	print("homePageView: Error decrypting note: InvalidToken")
		#except Exception as e:
		#	print("homePageView: Error decrypting note:", str(e))
		
		secretnotes.append({
			'id': secretnote.id,
			'note': note_text
		})
	

	context = {
			'secretnotes': secretnotes,
        	'user': user,
        }
	print("homePageView: secretnotes = ", secretnotes)
	return render(request, 'SecretNotes/index.html', context)

