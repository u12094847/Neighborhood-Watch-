import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt
from crime_loud.settings import MEDIA_ROOT
from flask import send_file
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.views.static import serve
from recaptcha.client import captcha
from reporting import views as view

import os

def home(request):
    return render_to_response("web_interface/login.html",
                              locals(),
                              context_instance = RequestContext(request))

def IncidentResponce(request):
    results = views.IncidentResponce(request)
    res = json.loads(results.content)
    if res['type'] == 1:
        print res['cases']
        return render_to_response("web_interface/incident_response.html",
                              {'name': request.session['user']['first_name'],
                               'surname': request.session['user']['last_name'],
                               'userID': request.session['user']['identity'],
                               'case': res['cases']})

@csrf_exempt
def registerNewUser(request):
    userID = request.POST['registerID']
    userName = request.POST['registerName']
    userSurname = request.POST['registerSurname']
    userEmail = request.POST['registerEmail']
    userPassword = request.POST['registerPassword']
    
    if request.method == "POST":
        data = {
                'userID' : userID,
                'userName': userName,
                'userSurname': userSurname,
                'userEmail': userEmail,
                'userPassword': userPassword,
            }
        
        results = views.registerNewUser(request, json.dumps(data))
        res = json.loads (results.content)
        
        name = res['name']
        
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html", { 'name':name,
                                                                     'surname':res['userSurname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['userEmail'],
                                                                     })
        
        else:
            return render_to_response("web_interface/login.html", { 'name':name})
    else:
        print "Web_interface views: registerNewUser --- GET method instead of POST used"
        return Http404()
    
@csrf_exempt
def reCaptchalogin(request):
     # talk to the reCAPTCHA service  
    response = captcha.submit(  
        request.POST.get('recaptcha_challenge_field'),  
        request.POST.get('recaptcha_response_field'),  
        '6Leu-PsSAAAAAFcLbrwJocmUAJDl4Vt62-CA1rnN',  
        request.META['REMOTE_ADDR'],)
    
    userEmail =request.POST['loginEmail']
    userPassword = request.POST['loginPassword']
    user_ip = request.POST['user_ip']
    login_count = request.POST['login_count']
    if(login_count == ''):
            login_count = 0
    current_ip = request.META['REMOTE_ADDR']
    if(user_ip == ''):
        user_ip = current_ip

    if (user_ip == current_ip):
        login_count = int(login_count) + 1
    
    if request.method == 'POST':
        data = {
            'userEmail':userEmail,
            'userPassword':userPassword
        }
        
        results = views.login(request, json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            if res['userRole'] == 'user':
                return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         })
            elif res['userRole'] == 'LEA' or res['userRole'] == 'DFI' :
                return render_to_response("web_interface/law_enforcement.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],'video':res['video'], 'date':res['date']})
            elif res['userRole'] == 'JDY':
                return render_to_response("web_interface/judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseName':res['caseName'],
                                                                         "caseNumber":res['caseNumber']})
            elif res['userRole'] == 'SA':
                return render_to_response("web_interface/administrator.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],'video':res['video'], 'date':res['date']})
                
        else:
            captcha_response = 'YOU MUST BE A ROBOT'
            return render_to_response("web_interface/login.html",{ 'type':-1,'captcha_response': captcha_response,
                                                                  'user_ip':user_ip, 'login_count':login_count
                })
        
    else:
        print "Web_interface views: login --- GET method instead of POST used"
        return Http404()
    
@csrf_exempt
def login(request):
    userEmail =request.POST['loginEmail']
    userPassword = request.POST['loginPassword']
    user_ip = request.POST['user_ip']
    login_count = request.POST['login_count']
    if(login_count == ''):
            login_count = 0
    current_ip = request.META['REMOTE_ADDR']
    if(user_ip == ''):
        user_ip = current_ip

    if (user_ip == current_ip):
        login_count = int(login_count) + 1
    
    if request.method == 'POST':
        data = {
            'userEmail':userEmail,
            'userPassword':userPassword
        }
        
        results = views.login(request, json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            if res['userRole'] == 'user':
                return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         })
            elif res['userRole'] == 'LEA' or res['userRole'] == 'DFI' :
                return render_to_response("web_interface/law_enforcement.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],'video':res['video'], 'date':res['date']})
            elif res['userRole'] == 'JDY':
                return render_to_response("web_interface/judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseName':res['caseName'],
                                                                         "caseNumber":res['caseNumber']})
            elif res['userRole'] == 'SA':
                return render_to_response("web_interface/administrator.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],'video':res['video'], 'date':res['date']})
                
        else:
            return render_to_response("web_interface/login.html",{ 'type':-1,
                                                                  'user_ip':user_ip, 'login_count':login_count
            })
        
    else:
        print "Web_interface views: login --- GET method instead of POST used"
        return Http404()
    
@csrf_exempt
def imageUpload(request):
    title = request.POST['imageTitle']
    description = request.POST['imageDescription']
    location = request.POST['imageLocation']
    date = request.POST['imageDate']
    
    userID = request.session['user']['identity']
   
    data = {
        'title':title,
        'description': description,
        'location':location,
        'date':date,
        'userID':userID,
    }

    results = views.imageUpload(request, json.dumps(data))
    res = json.loads(results.content)
    
    return render_to_response("web_interface/landing.html",{'type':res['type'], 'name':res['name'],
                                                            'surname':res['surname'],
                                                            })

@csrf_exempt
def imageUploadLEA(request):
    case= request.POST['role']
    description = request.POST['imageDescription']
   
    data = {
        'case':case,
        'description': description,
    }

    results = views.imageUploadLEA(request, json.dumps(data))
    res = json.loads(results.content)
    
    return render_to_response("web_interface/incident_response.html",{'type':res['type'], 'name':res['name'],
                                                            'surname':res['surname'],
                                                            'userID':res['userID'], 'case':res['case']})

def viewProfile(request):
    userID = request.session['user']['identity']
    
    data = {
        'userID':userID
    }
    results = views.viewProfile(request, json.dumps(data))
    res = json.loads(results.content)
    
    
    return render_to_response("web_interface/profile.html",{'type':res['type'], 'name':res['name'],
                                                            'surname':res['surname'],
                                                            'userID':res['userID'], 'email':res['email'],
                                                            'photoUploads':res['photoUploads'], 'videoUploads':res['videoUploads'],
                                                            'audioUploads':res['audioUploads']})
    
def backHome(request):
    userRole = request.session['user']['userRole']
    name = request.session['user']['first_name']
    surname = request.session['user']['last_name']
    if userRole == 'user':
        return render_to_response("web_interface/landing.html",{'name':name, 'surname':surname} )
    elif userRole == 'LEA' or userRole == 'DFI':
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        return render_to_response("web_interface/law_enforcement.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'], 'date':res['date']})
        
    elif userRole == 'JDY':
        result = views.jdyHomePage(request)
        res = json.loads(result.content)
        return render_to_response("web_interface/judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName']})
    elif userRole == 'SA':
        pass

@csrf_exempt
def UploadAudio(request):
    if request.method == 'POST':
        title = request.POST['audioTitle']
        description = request.POST['audioDescription']
        location = request.POST['audioLocation']
        date = request.POST['audioDate']
        filename = request.FILES['audioFileUpload']
        
        data = {
            'title':title,
            'description':description,
            'location':location,
            'date':date,
        }
        
        results = views.UploadAudio(request,json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     })
        else:
            return render_to_response("web_interface/landing.html", { 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                    })

@csrf_exempt
def UploadAudioLEA(request):
    if request.method == 'POST':
        description = request.POST['audioDescription']
        case = request.POST['role']
        filename = request.FILES['audioFileUpload']
        
        data = {
            'case':case,
            'description':description,
        }
        
        results = views.UploadAudioLEA(request,json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            return render_to_response("web_interface/incident_response.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'case':res['case']
                                                                     })
        else:
            return render_to_response("web_interface/incident_response.html", { 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                    })
        
@csrf_exempt
def UploadVideo(request):
    if request.method == 'POST':
        title = request.POST['videoTitle']
        description = request.POST['videoDescription']
        location = request.POST['videoLocation']
        date = request.POST['videoDate']
        filename = request.FILES['videoFileUpload']
        
        data = {
            'title':title,
            'description':description,
            'location':location,
            'date':date,
        }
        
        results = views.UploadVideo(request,json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     })
        else:
            return render_to_response("web_interface/landing.html", { 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     })
        
@csrf_exempt
def UploadVideoLEA(request):
    if request.method == 'POST':
        case = request.POST['role']
        description = request.POST['videoDescription']
        filename = request.FILES['videoFileUpload']
        
        data = {
            'case':case,
            'description':description,
        }
        
        results = views.UploadVideoLEA(request,json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            return render_to_response("web_interface/incident_response.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'case': res['case']
                                                                     })
        else:
            return render_to_response("web_interface/incident_response.html", { 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'case': res['case']
                                                                     })
        
def logout(request):
    request.session.delete()
    views.logout(request)
    return render_to_response("web_interface/login.html")


def takePhoto(request):  
    return render_to_response("web_interface/takePhoto.html")

def viewImage(request,image_id):
    results = views.viewImage(request,json.dumps({'image':image_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/view_image_LEA.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':1})
    else:
        return render_to_response("web_interface/view_image_LEA.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':-1})
    
def viewImageJDY(request,image_id):
    results = views.viewImage(request,json.dumps({'image':image_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/view_image_JDI.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':1})
    else:
        return render_to_response("web_interface/view_image_JDI.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':-1})

    
def assignCaseImage(request,image_id,case_id):
    result = views.assignCase(request,json.dumps({'case':case_id, 'pde':image_id}))
    res = json.loads(result.content)
    if res['type'] == 1:
        results = views.viewImage(request,json.dumps({'image':image_id}))
        res = json.loads(results.content)
        print "lol"
        if res['type'] == 1:
            return render_to_response("web_interface/view_image_LEA.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],

                                                                        'images':image_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    elif res['type'] == -1:
        results = views.viewImage(request,json.dumps({'image':image_id}))
        res = json.loads(results.content)
        print "lol times two"
        if res['type'] == 1:
            return render_to_response("web_interface/view_image_LEA.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    
    

def viewVideo(request,video_id):
    results = views.viewVideo(request,json.dumps({'image':video_id}))
    res = json.loads(results.content)
    if res['type'] == 1:
        return render_to_response("web_interface/view_video_LEA.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id,
                                                                        'oldHash': res['oldHash'],
                                                                        'newHash': res['newHash'],
                                                                        'type':1})
    else:
        return render_to_response("web_interface/view_video_LEA.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id,
                                                                        'oldHash': res['oldHash'],
                                                                        'newHash': res['newHash'],
                                                                        'type':-1})
    
def viewVideoJDY(request,video_id):
    results = views.viewVideo(request,json.dumps({'image':video_id}))
    res = json.loads(results.content)
    if res['type'] == 1:
        print "its a success"
        return render_to_response("web_interface/view_video_JDI.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':1})
    else:
         return render_to_response("web_interface/view_video_JDI.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':-1})
    
def assignCaseVideo(request,video_id,case_id):
    result = views.assignCase(request,json.dumps({'case':case_id, 'pde':video_id}))
    res = json.loads(result.content)
    if res['type'] == 1:
        results = views.viewVideo(request,json.dumps({'image':video_id}))
        res = json.loads(results.content)
        print "lol"
        if res['type'] == 1:
            return render_to_response("web_interface/view_video_LEA.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    elif res['type'] == -1:
        results = views.viewVideo(request,json.dumps({'image':video_id}))
        res = json.loads(results.content)
        print "lol times two"
        if res['type'] == 1:
            return render_to_response("web_interface/view_video_LEA.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})


def viewAudio(request,audio_id):
    results = views.viewAudio(request,json.dumps({'audio':audio_id}))
    res = json.loads(results.content)
    if res['type'] == 1:
        return render_to_response("web_interface/view_audio_LEA.html", {'audio':res['audioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':1})
    else:
        return render_to_response("web_interface/view_audio_LEA.html", {'audio':res['audioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':-1})
    
def viewAudioJDY(request,audio_id):
    results = views.viewAudio(request,json.dumps({'audio':audio_id}))
    res = json.loads(results.content)
    if res['type'] == 1:
        return render_to_response("web_interface/view_audio_JDI.html", {'audio':res['audioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':1})
    else:
       return render_to_response("web_interface/view_audio_JDI.html", {'audio':res['audioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash'],
                                                                        'type':-1})
    
def assignCaseAudio(request,audio_id,case_id):
    result = views.assignCase(request,json.dumps({'case':case_id, 'pde':audio_id}))
    res = json.loads(result.content)
    if res['type'] == 1:
        results = views.viewAudio(request,json.dumps({'audio':audio_id}))
        res = json.loads(results.content)
        print "lol"
        if res['type'] == 1:
            return render_to_response("web_interface/view_audio_LEA.html", {'audio':res['audioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    elif res['type'] == -1:
        results = views.viewAudio(request,json.dumps({'audio':audio_id}))
        res = json.loads(results.content)
        print "lol times two"
        if res['type'] == 1:
            return render_to_response("web_interface/view_audio_LEA.html", {'audio':res['vaudioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})

@csrf_exempt    
def addCase(request):
    name = request.POST['name']
    number = request.POST['number']
    title = request.POST['title']
    description = request.POST['description']
    date = request.POST['date']
    location = request.POST['location']
    print "in web interface "+ number
    data = {
        'name':name,
        'number':number,
        'title':title,
        'description': description,
        'date':date,
        'location':location
    }
    results = views.addCase(request,json.dumps(data))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        if res['type'] == 1:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    else:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        if res['type'] == 1:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
        
@csrf_exempt
def deletePDE(request):
    pde_id = request.POST['ID']
    results = views.deletePDE(request, json.dumps({'id':pde_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        if res['type'] == 1:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    else:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        if res['type'] == 1:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})

@csrf_exempt
def deleteLEA(request):
    pde_id = request.POST['ID']
    results = views.deleteLEA(request, json.dumps({'id':pde_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        if res['type'] == 1:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    else:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        if res['type'] == 1:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})

@csrf_exempt    
def RegisterAuthorizedUser(request):
    name = request.POST['registerName'],
    surname = request.POST['registerSurname']
    idNo = request.POST['registerID']
    email = request.POST['registerEmail']
    role = request.POST['role']
    pwd = request.POST['registerPassword']
    
    data = {
        'name':name,
        'surname': surname,
        'idNo':idNo,
        'email':email,
        'role': role,
        'password':pwd
    }
    
    results = views.registerAuthorzedUser(request,json.dumps(data))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        return render_to_response("web_interface/administrator.html",{ 'name':res['name'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    else:
        result = views.leaHomePage(request)
        res = json.loads(result.content)
        return render_to_response("web_interface/administrator.html",{ 'name':res['name'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})

@csrf_exempt
def downloadFile(request):
    filename = request.POST['ID']
    Type = request.POST['type']

    if Type == 'image':
        filename = 'C:/Users/Mamelo/Documents/GitHub/crime_loud/crime_loud/media/photo/'+filename
    elif Type == 'audio':
        filename = 'C:/Users/Mamelo/Documents/GitHub/crime_loud/crime_loud/media/audio/'+filename
    else:
        filename = 'C:/Users/Mamelo/Documents/GitHub/crime_loud/crime_loud/media/video/'+filename
    wrapper = FileWrapper(file(filename,'rb'))
    response = HttpResponse(wrapper, content_type='text/jpeg')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    response['Content-Length'] = os.path.getsize(filename)
    return response
    
def viewPdeViaCase(request,ID):
    result = views.viewPdeViaCase(request,json.dumps({'ID':ID}))
    res = json.loads(result.content)
    if request.session['user']['userRole'] == "JDY":
        return render_to_response("web_interface/judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName']})
    else:
        return render_to_response("web_interface/view_judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName']})

def viewPdeViaCaseD(request,ID):
    result = views.viewPdeViaCaseD(request,json.dumps({'ID':ID}))
    res = json.loads(result.content)
    if request.session['user']['userRole'] == "JDY":
        return render_to_response("web_interface/judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName']})
    else:
        return render_to_response("web_interface/documentation.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName'],
                                                                         'case_id':ID})
        

def viewByCase(request):
    result = views.viewByCase(request)
    res = json.loads(result.content)
    return render_to_response("web_interface/view_judiciary.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName']})

def documentation(request):
    result = views.documentation(request)
    res = json.loads(result.content)
    return render_to_response("web_interface/documentation.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'images':res['images'],
                                                                         'audio':res['audio'],
                                                                         'video':res['video'],
                                                                         'date':res['date'],
                                                                         'case':res['case'],
                                                                         'case_id':res['case_id'],
                                                                         'caseNumber':res['caseNumber'],
                                                                         'caseName':res['caseName']})

def viewImageLEA(request,image_id):
    results = views.viewImageLEA(request,json.dumps({'image':image_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/view_image_documentation.html", {'image':res['imageName'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'type':1,
                                                                        'caseNumber':res['caseNumber'],
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash']})
    else:
        return render_to_response("web_interface/view_image_documentation.html", {'image':res['imageName'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'type':-1,
                                                                        'caseNumber':res['caseNumber'],
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash']})
    
def viewAudioLEA(request,audio_id):
    results = views.viewAudioLEA(request,json.dumps({'audio':audio_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/view_audio_documentation.html", {'audio':res['audioName'],
                                                                        'caseNumber': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id,
                                                                        'type':1,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash']})
    else:
        return render_to_response("web_interface/view_audio_documentation.html", {'audio':res['audioName'],
                                                                        'caseNumber': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id,
                                                                        'type':-1,
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash']})
    
def viewVideoLEA(request,video_id):
    results = views.viewVideoLEA(request,json.dumps({'video':video_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/view_video_documentation.html", {'video':res['videoName'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'caseNumber':res['caseNumber'],
                                                                        'videos':video_id,
                                                                        'type':1,
                                                                        'oldHash': res['oldHash'],
                                                                        'newHash':res['newHash']})
    else:
        return render_to_response("web_interface/view_video_documentation.html", {'video':res['videoName'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id,
                                                                        'caseNumber':res['caseNumber'],
                                                                        'type':-1,
                                                                        'oldHash': res['oldHash'],
                                                                        'newHash':res['newHash']})
    
def assignCaseImageLEA(request,image_id,case_id):
    result = views.assignCaseLEA(request,json.dumps({'case':case_id, 'pde':image_id}))
    res = json.loads(result.content)
    if res['type'] == 1:
        results = views.viewImageLEA(request,json.dumps({'image':image_id}))
        res = json.loads(results.content)
        print "lol"
        if res['type'] == 1:
            return render_to_response("web_interface/view_image_documentation.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'case-description': res['case-description'],
                                                                        'incident': res['incident'],
                                                                        'images':image_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    elif res['type'] == -1:
        results = views.viewImage(request,json.dumps({'image':image_id}))
        res = json.loads(results.content)
        print "lol times two"
        if res['type'] == 1:
            return render_to_response("web_interface/view_image_documentation.html", {'image':res['imageName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'case-description': res['case-description'],
                                                                        'incident': res['incident']})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
 
def assignCaseVideoLEA(request,video_id,case_id):
    result = views.assignCaseLEA(request,json.dumps({'case':case_id, 'pde':video_id}))
    res = json.loads(result.content)
    if res['type'] == 1:
        results = views.viewVideoLEA(request,json.dumps({'video':video_id}))
        res = json.loads(results.content)
        print "lol"
        if res['type'] == 1:
            return render_to_response("web_interface/view_video_documentation.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    elif res['type'] == -1:
        results = views.viewVideoLEA(request,json.dumps({'video':video_id}))
        res = json.loads(results.content)
        print "lol times two"
        if res['type'] == 1:
            return render_to_response("web_interface/view_video_documentation.html", {'video':res['videoName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'videos':video_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
        
def assignCaseAudioLEA(request,audio_id,case_id):
    result = views.assignCaseLEA(request,json.dumps({'case':case_id, 'pde':audio_id}))
    res = json.loads(result.content)
    if res['type'] == 1:
        results = views.viewAudioLEA(request,json.dumps({'audio':audio_id}))
        res = json.loads(results.content)
        print "lol"
        if res['type'] == 1:
            return render_to_response("web_interface/view_audio_documentation.html", {'audio':res['audioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})
    elif res['type'] == -1:
        results = views.viewAudioLEA(request,json.dumps({'audio':audio_id}))
        res = json.loads(results.content)
        print "lol times two"
        if res['type'] == 1:
            return render_to_response("web_interface/view_audio_documentation.html", {'audio':res['vaudioName'],
                                                                        'caseName': res['caseNumber'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'audios':audio_id})
        else:
            return render_to_response("web_interface/law_enforcement.html",{'name':res['name'],
                                                                        'surname':res['surname'],
                                                                        'images':res['images'],
                                                                        'audio':res['audio'],
                                                                        'video':res['video'],
                                                                        'date':res['date']})

def Search(request,case_id):
    data = {
        'case_id':case_id
    }
    result = views.Search(request,json.dumps(data))
    res = json.loads(result.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/search.html",{'name':res['name'],
                                      'surname':res['surname'],
                                      'images':res['images'],
                                      'audio':res['audio'],
                                      'video':res['video'],
                                      'date':res['date'],
                                      'case_id':case_id,
                                      'case_name':res['case_name'],
                                      'case_number':res['case_number'],
                                      'type':1
                                })
    else:
        return render_to_response("web_interface/search.html",{'name':res['name'],
                                      'surname':res['surname'],
                                      'case_id':case_id,
                                      'type':-1
                                })
    
def auditlog(request):
    result = views.Auditlog(request)
    res = json.loads(result.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/auditlog.html",{'name':res['name'],
                                      'surname':res['surname'],
                                      'login':res['login'],
                                      'comPDE': res['comPDE'],
                                      'authPDE': res['authPDE']
                                })

def getDeleted(request):
    result = views.getDeleted(request)
    res = json.loads(result.content)
    
    if res['type'] == 1:
         return render_to_response("web_interface/deleted.html",{'name':res['name'],
                                      'surname':res['surname'],
                                      'community':res['community'],
                                      'authorized': res['authorized'],
                                      'date':res['date']
                                })
        
def viewImageDel(request,image_id):
    results = views.viewImageDel(request,json.dumps({'image':image_id}))
    res = json.loads(results.content)
    
    if res['type'] == 1:
        return render_to_response("web_interface/deleted_image.html", {'image':res['imageName'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'type':1,
                                                                        'caseNumber':res['caseNumber'],
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash']})
    else:
        return render_to_response("web_interface/deleted_image.html", {'image':res['imageName'],
                                                                        'cases':res['cases'],
                                                                        'date':res['date'],
                                                                        'location': res['location'],
                                                                        'description':res['description'],
                                                                        'title': res['title'],
                                                                        'surname':res['surname'],
                                                                        'name':res['name'],
                                                                        'images':image_id,
                                                                        'type':-1,
                                                                        'caseNumber':res['caseNumber'],
                                                                        'oldHash':res['oldHash'],
                                                                        'newHash':res['newHash']})