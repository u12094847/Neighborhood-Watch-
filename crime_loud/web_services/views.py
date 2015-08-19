import json
import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.context_processors import csrf
from business_logic import api


def registerNewUser(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    userID = json_data['userID']
    userName = json_data['userName']
    userSurname = json_data['userSurname']
    userEmail = json_data['userEmail']
    userPassword = json_data['userPassword']
    
    result = api.registerNewUser(userID, userName, userSurname, userEmail, userPassword,request)
    result = True
    
    if result == True:
        data = {
            'type':1,
            'name': userName,
            'userID':userID,
            'userSurname':userSurname,
            'userEmail':userEmail,
        }
    
    else:
        data = {
            'type':-1,
            'name':userName
        }
    
    return HttpResponse(json.dumps(data))

def login(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    userEmail = json_data['userEmail']
    userPassword = json_data['userPassword']
    
    result = api.login(userEmail, userPassword,request)
    
    if result != "":
        if request.session['user']['userRole'] == 'user':
            data = {
                'type':1,
                'name':request.session['user']['first_name'],
                'surname':request.session['user']['last_name'],
                'userRole':request.session['user']['userRole']
            }
        elif request.session['user']['userRole'] == 'LEA' or request.session['user']['userRole'] == 'DFI' or request.session['user']['userRole'] == 'SA':
            data = {
                'type':1,
                'name':request.session['user']['first_name'],
                'surname':request.session['user']['last_name'],
                'userRole':request.session['user']['userRole'],
                'images':result['images'],
                'audio': result['audio'],
                'video': result['video'],
                'date': result['date']
            }
        else:
            data = {
                'type':1,
                'name':request.session['user']['first_name'],
                'surname':request.session['user']['last_name'],
                'userRole':request.session['user']['userRole'],
                'images':result['images'],
                'audio': result['audio'],
                'video': result['video'],
                'date': result['date'],
                'case':result['case'],
                'caseName': result['caseName'],
                'caseNumber': result['caseNumber']
            }
        
    else:
        data = {
            'type': -1
        }
        
    return HttpResponse(json.dumps(data))


def imageUpload(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    title = json_data['title']
    description = json_data['description']
    location = json_data['location']
    date = json_data['date']
    userID = json_data['userID']
    
    
    result = api.uploadImage(request, title, description, location, date, userID)
    
    if result == True:
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
        
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
    
    return HttpResponse(json.dumps(data))

def imageUploadLEA(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    case = json_data['case']
    description = json_data['description']
    
    result = api.uploadImageLEA(request, case, description)
    
    if result is not None:
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'userID':result['userID'],
            'case': result['case']
        }
        
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'userID':result['userID'],
            'case': result['case']
        }
    
    return HttpResponse(json.dumps(data))

def viewProfile(request, jsonObj):
    json_data = json.loads(jsonObj)
    userID = json_data['userID']
    
    result = api.viewProfile(userID)
    
    if result != []:
        data = {
            'type':1,
            'name':result[0],
            'surname':result[1],
            'userID':result[2],
            'email':result[3],
            'photoUploads':result[4],
            'videoUploads':result[5],
            'audioUploads':result[6]
        }
    else:
        data = {
            'type':-1, #person could not be located in database
        }
        
    return HttpResponse(json.dumps(data))

    
def UploadVideo(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    title = json_data['title']
    description = json_data['description']
    location = json_data['location']
    date = json_data['date']
    #file = json_data['file']
    
    result = api.UploadVideo(title,description,location,date,request)
    if result != "":
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
        return HttpResponse(json.dumps(data))
    
def UploadVideoLEA(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    case = json_data['case']
    description = json_data['description']
    #file = json_data['file']
    
    result = api.UploadVideoLEA(case,description,request)
    if result != "":
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'userID':result['userID'],
            'case': result['case']
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'userID':result['userID'],
            'case': result['case']
        }
        return HttpResponse(json.dumps(data))
    
def UploadAudio(request, jsonObj):
    json_data = json.loads(jsonObj)
    title = json_data['title']
    description = json_data['description']
    location = json_data['location']
    date = json_data['date']
    #file = json_data['file']
    result = api.UploadAudio(title,description,location,date,request)
    if result != "":
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
        return HttpResponse(json.dumps(data))
    
def UploadAudioLEA(request, jsonObj):
    json_data = json.loads(jsonObj)
    case = json_data['case']
    description = json_data['description']
    #file = json_data['file']
    result = api.UploadAudioLEA(case,description,request)
    if result != "":
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'userID':request.session['user']['identity'],
            'case': result['case']
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'userID':result['userID'],
            'case': result['case']
        }
        return HttpResponse(json.dumps(data))
    
    
def viewImage(request,jsonObj):
    json_data = json.loads(jsonObj)
    image_id = json_data['image']
    
    result = api.viewImage(request,image_id)
    if result['status'] == "success":
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases'],
            'oldHash': result['oldHash'],
            'newHash': result['newHash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases'],
            'oldHash': result['odlHash'],
            'newHash': result['newHash']
        }
        return HttpResponse(json.dumps(data))

def assignCase(request,jsonObj):
    json_data = json.loads(jsonObj)
    case = json_data['case']
    pde = json_data['pde']
    
    result = api.assignCase(pde,case,request)
    
    if result:
        data ={
            'type': 1
        }
    else:
        data = {
            'type':-1
        }
    
    return HttpResponse(json.dumps(data))
    
def leaHomePage(request):
        res = api.leaHomePage(request)
        
        data = {
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'images':res['images'],
            'audio': res['audio'],
            'video': res['video'],
            'date': res['date']
        }
        
        return HttpResponse(json.dumps(data))
    
def jdyHomePage(request):
    res = api.jdyHomePage(request)
    print str(res)
    data = {
        'type':1,
        'name':request.session['user']['first_name'],
        'surname':request.session['user']['last_name'],
        'images':res['images'],
        'audio':res['audio'],
        'video':res['video'],
        'date':res['date'],
        'caseNumber':res['caseNumber'],
        'caseName':res['caseName'],
        'case':res['case']
    }
    return HttpResponse(json.dumps(data))

def viewVideo(request,jsonObj):
    json_data = json.loads(jsonObj)
    video_id = json_data['image']
    
    result = api.viewVideo(request,video_id)
    if result['status'] == 'success':
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'videoName':result['videoName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldHash'],
            'newHash': result['newHash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'videoName':result['videoName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldHash'],
            'newHash': result['newHash']
        }
        return HttpResponse(json.dumps(data))
    
def viewAudio(request,jsonObj):
    json_data = json.loads(jsonObj)
    video_id = json_data['audio']
    
    result = api.viewAudio(request,video_id)
    if result['status'] == 'success':
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'audioName':result['audioName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldHash'],
            'newHash': result['newHash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'audioName':result['audioName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldHash'],
            'newHash': result['newHash']
        }
        return HttpResponse(json.dumps(data))

def addCase(request,jsonObj):
    json_data = json.loads(jsonObj)
    name = json_data['name']
    number = json_data['number']
    date = json_data['date']
    location = json_data['location']
    title = json_data['location']
    description=json_data['description']
    
    
    result = api.addCase(name,number,request,title,description,date,location)
    if result:
        data = {
            'type': 1,
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type': -1
        }
        return HttpResponse(json.dumps(data))
    
def deletePDE(request,jsonObj):
    json_data = json.loads(jsonObj)
    pde = json_data['id']
    
    result = api.deletePDE(pde,request)
    if result:
        data = {
            'type':1
        }
        return HttpResponse(json.dumps(data))
    else:
        data ={
            'type':-1
        }
        return HttpResponse(json.dumps(data))
    
def deleteLEA(request,jsonObj):
    json_data = json.loads(jsonObj)
    pde = json_data['id']
    
    result = api.deletePDE_LEA(pde,request)
    if result:
        data = {
            'type':1
        }
        return HttpResponse(json.dumps(data))
    else:
        data ={
            'type':-1
        }
        return HttpResponse(json.dumps(data))

def registerAuthorzedUser(request, jsonObj):
    json_data = json.loads(jsonObj)
    name = json_data['name']
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    print name
    surname = json_data['surname']
    email = json_data['email']
    idNo = json_data['idNo']
    role = json_data['role']
    password = json_data['password']
    
    results = api.RegisterAuthorizedUser(request, name[0], surname, idNo, role, password, email)
    if results:
        data = {
            'type':1,
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1
        }
        return HttpResponse(json.dumps(data))

def viewPdeViaCase(request,jsonObj):
    json_data = json.loads(jsonObj)
    id = json_data['ID']
    res = api.viewPdeViaCase(request,id)
    data = {
        'type':1,
        'name':request.session['user']['first_name'],
        'surname':request.session['user']['last_name'],
        'images':res['images'],
        'audio':res['audio'],
        'video':res['video'],
        'date':res['date'],
        'caseNumber':res['caseNumber'],
        'caseName':res['caseName'],
        'case':res['case']
    }
    return HttpResponse(json.dumps(data))

def viewPdeViaCaseD(request,jsonObj):
    json_data = json.loads(jsonObj)
    id = json_data['ID']
    res = api.viewPdeViaCaseD(request,id)
    data = {
        'type':1,
        'name':request.session['user']['first_name'],
        'surname':request.session['user']['last_name'],
        'images':res['images'],
        'audio':res['audio'],
        'video':res['video'],
        'date':res['date'],
        'caseNumber':res['caseNumber'],
        'caseName':res['caseName'],
        'case':res['case']
    }
    return HttpResponse(json.dumps(data))

def viewByCase(request):
    res = api.viewByCase(request)
    
    data = {
        'name':request.session['user']['first_name'],
        'surname':request.session['user']['last_name'],
        'images':res['images'],
        'audio':res['audio'],
        'video':res['video'],
        'case':res['case'],
        'caseNumber':res['caseNumber'],
        'caseName':res['caseName'],
        'date':res['date']
    }
    
    return HttpResponse(json.dumps(data))

def IncidentResponce(request):
    res = api.getUserCases(request)
    data = {
        'type': 1,
        'cases':res
    }
    return HttpResponse(json.dumps(data))

def documentation(request):
    results = api.Documentation(request)
    
    data = {
        'name': request.session['user']['first_name'],
        'surname': request.session['user']['last_name'],
        'images': results['images'],
        'audio': results['audio'],
        'video': results['video'],
        'case': results['case'],
        'case_id':results['case_id'],
        'caseName': results['caseName'],
        'caseNumber': results['caseNumber'],
        'date': results['date']
    }
    
    return HttpResponse(json.dumps(data))

def viewImageLEA(request,jsonObj):
    json_data = json.loads(jsonObj)
    image_id = json_data['image']
    
    result = api.viewImageLEA(request,image_id)
    if result != "":
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(request)
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        return HttpResponse(json.dumps(data))
    
def viewAudioLEA(request,jsonObj):
    json_data = json.loads(jsonObj)
    image_id = json_data['audio']
    
    result = api.viewAudioLEA(request,image_id)
    if result != "":
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'audioName':result['audioName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(request)
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'audioName':result['audioName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        return HttpResponse(json.dumps(data))
    
def viewVideoLEA(request,jsonObj):
    json_data = json.loads(jsonObj)
    video_id = json_data['video']
    
    result = api.viewVideoLEA(request,video_id)
    if result != "":
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'incident': result['incident'],
            'caseNumber': result['caseNumber'],
            'videoName':result['videoName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(request)
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'videoName':result['videoName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        return HttpResponse(json.dumps(data))
    
def assignCaseLEA(request,jsonObj):
    json_data = json.loads(jsonObj)
    case = json_data['case']
    pde = json_data['pde']
    
    result = api.assignCaseLEA(pde,case)
    
    if result:
        data ={
            'type': 1
        }
    else:
        data = {
            'type':-1
        }
    
    return HttpResponse(json.dumps(data))
    
def getCaseInformationForReport(request,jsonObj):
    json_data = json.loads(jsonObj)
    case_id = json_data['case_id']
    
    case_info = api.getCaseData(request,case_id)
    cs_data = api.getPDEdata(request,case_id)
    
    data = {
        'case_info':case_info,
        'cs_docs':cs_data
    }
    
    return HttpResponse(json.dumps(data))

def Search(request,jsonObj):
    json_data= json.loads(jsonObj)
    case_id = json_data['case_id']
    
    res = api.Search(request,case_id)
    data = []
    if res:
        print "Theres something"
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'images':res['images'],
            'audio':res['audio'],
            'video':res['video'],
            'date':res['date'],
            'case_name':res['case_name'],
            'case_number': res['case_number']
            
        }
    else:
        print "Theres nothing"
        data={
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
        }
    return HttpResponse(json.dumps(data))

def Auditlog(request):
    res = api.auditLog(request)
    data = {
        'type':1,
        'name': request.session['user']['first_name'],
        'surname':request.session['user']['last_name'],
        'login': res[0],
        'comPDE': res[1],
        'authPDE': res[2]
    }
    return HttpResponse(json.dumps(data))

def logout(request):
    api.logout(request)
    return HttpResponse()

def getDeleted(request):
    res = api.getDeleted(request)
    data = {
        'type':1,
        'name':request.session['user']['first_name'],
        'surname':request.session['user']['last_name'],
        'community': res[0],
        'authorized': res[1],
        'date':str(datetime.datetime.today().date())
    }
    return HttpResponse(json.dumps(data))

def viewImageDel(request,jsonObj):
    json_data = json.loads(jsonObj)
    image_id = json_data['image']
    
    result = api.viewImageDel(request,image_id)
    if result != "":
        data={
            'type':1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(request)
        data = {
            'type':-1,
            'name':request.session['user']['first_name'],
            'surname':request.session['user']['last_name'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases'],
            'oldHash':result['oldhash'],
            'newHash': result['newhash']
        }
        return HttpResponse(json.dumps(data))