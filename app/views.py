from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from datetime import datetime
from django.utils import formats
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
import os

def index(request):
	global data 
	data ={
	"nom_entreprise": "xxxxx",
	"lieu_entreprise": "xxxxx",
	"date": "xxxxx",
	"mail_entreprise":"xxxxx@gmail.com"
    }
	context = {}
	now = datetime.now()
	date_fr=formats.date_format(now,"d F Y",use_l10n=True)
	#date_fr = now.strftime("%d %B %Y")

	
	if request.method == "POST":
		if "add" in request.POST:
			nom_entreprise=request.POST.get("nom_entreprise")
			lieu_entreprise=request.POST.get("lieu_entreprise")
			mail_entreprise=request.POST.get("mail_entreprise")

			data ={
		"nom_entreprise": nom_entreprise,
		"lieu_entreprise": lieu_entreprise,
		"date": date_fr,
		"mail_entreprise": mail_entreprise,

    }
	 
	return render(request, 'app/index.html',data)

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os



def mail_entreprise(request, entreprise, mail_entreprise):
	subject = "Demande de stage"
	message = f'''Cher(e) Monsieur/Madame le/la responsable {entreprise},
Je me permets de vous contacter afin de postuler pour un stage au sein de votre entreprise {entreprise} . Je suis actuellement étudiant 3 ème année de licence en Informatique à l'ENI, et je suis très intéressé par l'opportunité de rejoindre votre entreprise pour compléter ma formation pratique.


Je suis particulièrement attiré par le développement Web Django, devops et administration Système et réseaux, et je suis convaincu que ce stage me permettrait d'acquérir des compétences précieuses dans le domaine.Voilà ainsi de suite mon Cv et ma lettre de motivation'''
    
	from_email = settings.EMAIL_HOST_USER
	to_mail = mail_entreprise
	
    # Instanciation de la classe DownloadPDF
	download_pdf_view = DownloadPDF.as_view()
    
    # Génération du PDF pour la lettre de motivation
	pdf_response = download_pdf_view(request)
	pdf_content = pdf_response.content

	LM = "/home/server/Downloads/LM_Eddy_Nilsen.pdf"

	
	try:
		email = EmailMessage(subject, message, from_email, [to_mail])
		email.attach_file("CV_Eddy_Nilsen.pdf")
		email.attach_file(LM)
		email.send()
	except Exception as e:
		print(f"Erreur lors de l'envoi de l'email: {str(e)}")
	finally:
        # Supprimer le fichier PDF temporaire
		try:
			os.remove(LM)
		except OSError as e:
			print(f"Erreur lors de la suppression du fichier: {str(e)}")
	return render(request,'app/mail_entreprise.html',locals())

class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('app/cv.html', data)
		response = HttpResponse(pdf, content_type='application/pdf')
		fichier=data['nom_entreprise']
		#filename = " LM_%s.pdf" %(fichier)
		filename = " LM_Eddy_Nilsen.pdf"
		content = "attachment; filename=%s" %(filename)
		response['Content-Disposition'] = content
		return response

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#Opens up page as PDF

class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('app/cv.html', data)
		return HttpResponse(pdf, content_type='application/pdf')






