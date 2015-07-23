###################################
# Django view	                    #	 
# Author: Oshadha		      #
# Date: 2010/03/08                #
# Python version: 2.6.2           #
# Django version: 1.1.1	      #
###################################


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from datetime import datetime
from testproject.testapplication.models import LocationLogger, CiviguardUsersModel
from testproject.testapplication.forms import CiviguardUsersForm, CiviguardUsers, CiviguardUsersLogin, CiviguardUpdatesForm
from testproject.testapplication.encryption import encrypt
from testproject.testapplication.locationlog import func_user, get_locale
from django.core.mail import EmailMultiAlternatives
import random
import twilio
import sys
import re
from django.conf import settings
import captcha
 


def test_form(request):
	return render_to_response('index.html', context_instance=RequestContext(request))


def check_form(request):
	if request.method == 'POST':
		form = CiviguardUsers(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				name = cd['fullName']
				email = cd['emailAdd']
				password2 = encrypt(cd['password2'])
				phone = cd['cellPhone']
				phoneType = cd['phoneType']
				region = ''
				res = domain(request)
				if res[0] == True:
					region = res[1]
				else:
					region = 'None'
				return render_to_response('signup2.html', {'name': name, 'email': email, 'password2': password2, 'phone': phone, 'pt': phoneType, 'rg': region})
			except Exception, ex:
				# sys.stderr.write('Value error: %s\n' % str(ex)
				return HttpResponse("Error %s" % str(ex))
		else:
			return HttpResponse('Error')
	else:
		form = CiviguardUsers()
	return render_to_response('signup1.html', context_instance=RequestContext(request))


def save_form(request):
	if request.method == 'POST':
		form = CiviguardUsersForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				newUser = form.save()
				toemail = cd['emailAdd']
				u_id = gen_account(toemail)
				domain_parts = request.get_host().split('.')
        			ac_link = ''
				res = domain(request)
				if res[0] == True:
					ac_link = 'http://%s.civiguard.me/activate/%s' % (res[1], u_id)
				else:
					ac_link = 'http://%s.civiguard.me/activate/%s' % (res[1], u_id)
				sub = 'Please activate your CiviGuard account!'
				email(sub, toemail, ac_link)
				return HttpResponseRedirect('/confirmation/')
			except Exception, ex:
				# sys.stderr.write('Value error: %s\n' % str(ex)
				return HttpResponse('Error %s' % form.errors)
		else:
			return HttpResponse('Error %s' % form.errors)
	else:
		form = CiviguardUsersForm()
	return render_to_response('signup1.html', context_instance=RequestContext(request))


def confirmation(request):
	if request.method == 'GET':
		return render_to_response('signup3.html', context_instance=RequestContext(request))
	else:
		return HttpResponse(None)


def validate_user(request):
	 if request.method == 'POST':
		vld_value = request.POST.get('validateValue')
		vld_id = request.POST.get('validateId')
		vld_error = request.POST.get('validateError')
		
		array_to_js = [vld_id, vld_error, ""]
	
		userLst = CiviguardUsersModel.objects.filter(emailAdd = vld_value)		

		if userLst:
			array_to_js[2] = "false"
	 		jsonvalue = simplejson.dumps({'jsonValidateReturn': array_to_js})
		 	return HttpResponse(jsonvalue)
	 	else:
			array_to_js[2] = "true"
			x = simplejson.dumps(array_to_js)
			jsonvalue = simplejson.dumps({'jsonValidateReturn': array_to_js})
			return HttpResponse(jsonvalue)
	 else:				
	 	return HttpResponse('You cannot access this page')


def thanks(request):
	if request.method == 'GET':
		return render_to_response('thanksconf.html', context_instance=RequestContext(request))
	else:
		return HttpResponse(None)


def getupdates(request):
	if request.method == 'GET':
		ipAddress = request.META['HTTP_X_FORWARDED_FOR'] 
		return render_to_response('getupdates1.html', {'ip': ipAddress}, context_instance=RequestContext(request))
	else:
		return HttpResponse(None)


def signup(request):
	if request.method == 'GET':
		return render_to_response('signup1.html', context_instance=RequestContext(request))
	else:
		return HttpResponse(None)


def login_page(request):
	if request.method == 'GET':
		try:
			u_id = request.session.get('u_id')
			civ_user = CiviguardUsersModel.objects.get(userKey=u_id)
			pNumber = civ_user.cellPhone
			pType = civ_user.phoneType
			uemail = civ_user.emailAdd
			return render_to_response('editinfo.html', {'tpNum': pNumber, 'pt': pType, 'email': uemail}, context_instance=RequestContext(request))			
		except:	
			return render_to_response('signup4.html', context_instance=RequestContext(request))
	else:
		return HttpResponse(None)

		
def gen_account(email):
	key = ''.join(random.sample('ObguMyrhDsBysdumsdqhlisdCEsfgkjf', 30))
	user = CiviguardUsersModel.objects.get(emailAdd=email)
	user.userKey = key
	user.save()
	return key


def activate_account(request, key):
	if request.method == 'GET':
		user = CiviguardUsersModel.objects.get(userKey=key)
		u_eamil = user.emailAdd
		u_phone = user.cellPhone
		if user:
			if user.activated == 1:
				already = 'You have already confirmed your email'
				return render_to_response('signup5.html', {'npnumber': u_phone, 'userEmail': u_eamil, 'activated': already}, context_instance=RequestContext(request))
			else:
				user.activated = 1
				user.save()
				activated = 'Your account is now activated with a valid email address.'
				return render_to_response('signup5.html', {'npnumber': u_phone, 'userEmail': u_eamil, 'activated': activated}, context_instance=RequestContext(request))
		else:
			return HttpResponse('Error in verification key')
	else:
		return HttpResponse('Error')


def save_updates(request):
	if request.method == 'POST':
		form = CiviguardUpdatesForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				updateForm = form.save()
				return HttpResponseRedirect('/thanks/')
			except:
				error = 'There are some errors in the form'
				return render_to_response('getupdates1.html', {'error': error}, context_instance=RequestContext(request))
		else:
			error = "You haven't specifiy your name"
			ipAddress = request.META['HTTP_X_FORWARDED_FOR'] 
			return render_to_response('getupdates1.html', {'error': error, 'ip': ipAddress}, context_instance=RequestContext(request))			
	else:
		return HttpResponse('Cannot access..!')						
		


def user_login(request):
	if (request.method == 'POST') | (request.method == 'GET'):
		form = CiviguardUsersLogin(request.POST)
		if form.is_valid():
			errMsg = 'The Email ID or Password you entered is incorrect'
			cd = form.cleaned_data
			try:
				uemail = cd['emailAdd']
				upass = encrypt(cd['password'])
				cUser = CiviguardUsersModel.objects.get(emailAdd=uemail)
				pNumber = cUser.cellPhone
				pType = cUser.phoneType	
				if (cUser.password2 == upass) & (cUser.emailAdd == uemail):			
					if cUser.activated == 1:
						request.session['u_id'] = cUser.userKey
						return render_to_response('editinfo.html', {'tpNum': pNumber, 'pt': pType, 'email': uemail}, context_instance=RequestContext(request))
					else:
						actError = 'Your account is not activated'
						return render_to_response('signup4.html', {'lgerror': actError}, context_instance=RequestContext(request))
				else:
					return render_to_response('signup4.html', {'lgerror': errMsg}, context_instance=RequestContext(request))									
			except Exception, ex:
				return render_to_response('signup4.html', {'lgerror': str(ex)}, context_instance=RequestContext(request))									
		elif request.session.get('u_id'):
			u_id = request.session.get('u_id')
			civ_user = CiviguardUsersModel.objects.get(userKey=u_id)
			pNumber = civ_user.cellPhone
			pType = civ_user.phoneType
			uemail = civ_user.emailAdd
			return render_to_response('editinfo.html', {'tpNum': pNumber, 'pt': pType, 'email': uemail}, context_instance=RequestContext(request))
		else:
			form = CiviguardUsersLogin()
		return render_to_response('signup4.html', {'form': form}, context_instance=RequestContext(request))
	else:
		form = CiviguardUsersLogin()
	return render_to_response('signup4.html', context_instance=RequestContext(request))


def mobile_ver(request):
	if request.method == 'POST':
		uemail = request.POST['userEmail']
		reval = request.POST['reval']
		uVal = request.POST['val']
		getUsr = CiviguardUsersModel.objects.get(emailAdd=uemail)
		rNum = random.randrange(1,40162,1)
		getUsr.mobVerCode = rNum
		getUsr.save()
		mobNumber = getUsr.cellPhone
		account = twilio.Account(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN)
		d = {
    			'To' : mobNumber,
    			'From' : '707-809-5994',
    			'Body' : 'Hello CiviGuard user! Please register your device using code %s' % rNum
		}
		try:
    			print account.request('/%s/Accounts/%s/SMS/Messages' % \
                              		(settings.API_VERSION, settings.ACCOUNT_SID), 'POST', d)
		except Exception, e:
			error = 'We encounted an error while sending the verification code'
			return render_to_response('signup5error.html', {'error': error},  context_instance=RequestContext(request))	
		if uVal == 'resend':
			notice = 'Verification code is re-sent'
			return render_to_response('signup6.html', {'userEmail': uemail, 'notice': notice, 'reval': reval},  context_instance=RequestContext(request))			
		elif reval == 'code':
			return render_to_response('signup6.html', {'userEmail': uemail, 'reval': reval}, context_instance=RequestContext(request))			
		else:
			return render_to_response('signup6.html', {'userEmail': uemail},  context_instance=RequestContext(request))
	else:
		return render_to_response('signup4.html', context_instance=RequestContext(request))		


def complete(request):
	if request.method == 'POST':
		try:
			vcode = request.POST['userCode']
			u_email = request.POST['userEmail']
			reval = request.POST['reval']
			cUser = CiviguardUsersModel.objects.get(mobVerCode=vcode)
			if cUser:
				if reval == 'code':
					u_pnumber = cUser.cellPhone
					u_ptype = cUser.phoneType
					notice = 'Changes have been made successfully'
					return render_to_response('editinfo.html', {'tpNum': u_pnumber, 'pt': u_ptype, 'email': u_email, 'notice': notice}, context_instance=RequestContext(request))
				else:
					u_key = cUser.userKey
					return render_to_response('new.html', {'u_id': u_key}, context_instance=RequestContext(request))
			else:
				error = 'Verification code you have entered is invalid, try resending the code %s %s' % (vcode, cUser.mobVerCode)
				return render_to_response('signup6.html', {'error_code': error, 'userEmail': u_email}, context_instance=RequestContext(request))
		except Exception, ex:
			error = ex
			return render_to_response('signup6.html', {'error_code': error}, context_instance=RequestContext(request))		
	else:
		return render_to_response('signup4.html', context_instance=RequestContext(request))
		

def email(sub, tomail, ac_link):
	subject, fromemail, to  = sub, 'support@civiguard.com', tomail
	text_content = """ Thanks for registering with us please activate your account by clicking the following link: 
			     
			     if you encounter any problem please contact us through support@civiguard.com """
	html_content = """ <p>Thanks for registering with us please activate your account by clicking the following <strong>link:</strong></p><br/>
			     %s <br/>
			     <p>if you encounter any problem please contact us through support@civiguard.com</p> """ % ac_link
	msg = EmailMultiAlternatives(subject, text_content, fromemail, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()


def facebook(request):
	if request.method == 'GET':
		 return render_to_response('signup7.html', context_instance=RequestContext(request))
	else:
		return HttpResponse('Error') 


def fgpass(request):
	if request.method == 'POST':
		check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
		if check_captcha.is_valid is False:
			error = 'The verification code you have entered is not valid'
			return render_to_response('emailpassword.html', {'error': error}, context_instance=RequestContext(request))
		else:
			try:
				toemail = request.POST['userEmail']
				user_key = ''.join(random.sample('Lksrtg8945ljkfsfd397470CfDbPh', 15))
				user_obj = CiviguardUsersModel.objects.get(emailAdd=toemail)
				user_obj.passResetCode = user_key
				user_obj.save()
				link = ''
				res = domain(request)
				if res[0] == True:
					link = 'http://%s.civiguard.me/resetmail/?pvalue=%s' % (res[1], user_key)
				else:
					link = 'http://%s.civiguard.me/resetmail/?pvalue=%s' % (res[1], user_key)
				fromemail = 'support@civiguard.me'
				subject = 'Password Reset'
				text_content = """ You can reset your password by visiting this link %s """ % link
				msg = EmailMultiAlternatives(subject, text_content, fromemail, [toemail])
				msg.send()
				return render_to_response('notice.html', {'email': toemail}, context_instance=RequestContext(request))
			except Exception, ex:
				return HttpResponse('Error %s' % ex) 
				#error = 'Your email is not registered with our service'
				#return render_to_response('emailpassword.html', {'error': error}, context_instance=RequestContext(request))
	else:
		return render_to_response('emailpassword.html', context_instance=RequestContext(request))


def resetmail(request):
	if request.method == 'GET':
		req_val = request.GET['pvalue'] 
		return render_to_response('resetpassword.html', {'req_val': req_val}, context_instance=RequestContext(request)) 
	else:
		return HttpResponse('Error')


def resetpage(request):
	if request.method == 'GET':
		return render_to_response('emailpassword.html', context_instance=RequestContext(request)) 
	else:
		return HttpResponse('Error')


def resetpassword(request):
	if request.method == 'POST':
		upass = request.POST['password2']
		userVal = request.POST['reqval']
		user_obj = CiviguardUsersModel.objects.get(passResetCode=userVal)
		user_obj.password2 = encrypt(upass)
		user_obj.save()
		return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/resetpassword/')


def localeset(request):
	if request.method == 'POST':
		user_data = request.POST['data']
		u_data = func_user(user_data)
		return HttpResponse("success")
	else:
		return HttpResponse('Error')


def domain(request):
	domain_parts = request.get_host().split('.')
	if (len(domain_parts) > 2) or (len(domain_parts) == 2 and domain_parts[1].find('localhost') != -1):
		subdomain = domain_parts[0]
		if (subdomain == '') or (subdomain.lower() == 'www'):
			return False, subdomain
		else:
			return True, subdomain
	else:
		return False


def edituser(request):
	if request.method == 'POST':
		u_email = request.POST['email']
		u_pass = request.POST['password2']
		u_pass_en = encrypt(u_pass)
		u_ptype = request.POST['phoneType']
		u_pnumber = request.POST['cellPhone']
		user_obj = CiviguardUsersModel.objects.get(emailAdd=u_email)
		reg = re.compile('^[*]+$')
		user_obj.phoneType = u_ptype
		if bool(reg.match(u_pass)) | (user_obj.password2 == u_pass_en):
			pass
		else:
			user_obj.password2 = u_pass
		if user_obj.cellPhone != u_pnumber:
			user_obj.cellPhone = u_pnumber
			user_obj.save()
			notice = 'Since your mobile number has been changed we need to confirm it'
			return render_to_response('signup5.html', {'activated': notice, 'code': 'code', 'npnumber': u_pnumber, 'userEmail': u_email}, context_instance=RequestContext(request))			
		else:
			user_obj.save()
			notice = 'Changes have been made successfully'
			return render_to_response('editinfo.html', {'tpNum': u_pnumber, 'pt': u_ptype, 'email': u_email, 'notice': notice}, context_instance=RequestContext(request))
	else:
		return HttpResponse('Error')	


def load_map(request):
	if request.method == 'GET':
		try:
			if request.session.get('u_id'):
				u_id = request.session.get('u_id')
				return render_to_response('editinfomap.html', {'u_id': u_id}, context_instance=RequestContext(request))
			else:
				return render_to_response('endsession.html', context_instance=RequestContext(request))			
		except Exception:
			return render_to_response('endsession.html', context_instance=RequestContext(request))			
	else:
		return HttpResponse("Error")


def getlocale(request):
	if request.method == 'POST':
		u_id = request.session['u_id']
		user_obj = CiviguardUsersModel.objects.get(userKey=u_id)
		email = user_obj.emailAdd
		lonlatuser = get_locale(email)
		return HttpResponse(lonlatuser)
	else:	
		return HttpResponse('Error')	


def logout(request):
	if request.method == 'GET':
		try:
			del request.session['u_id']	
			return HttpResponse("You're logged out.")	
    		except KeyError:
        		return HttpResponse("You're already logged out.")
	else:
		return HttpResponse("Error")


def test(request):
	if request.method == 'GET':
		jjsn = get_locale() 
		return HttpResponse(jjsn)
	else:
		return HttpResponse("Error")
		

		