from .models import *
import datetime
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
#from simplecrypt import encrypt, decrypt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import hashlib
import binascii

key = '0123456789abcdef'
encrytion = AES.new(key)

def pad(s):
    return s+((16-len(s)% 16)*'{')

#def encrypt(plain):
#    result =encrytion.encrypt(pad(plain))
#    return result

def decrypt(cipher):
   # ciphertext = binascii.a2b_base64(cipher)
    dec = encrytion.decrypt(cipher).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-l]

def encrypt(plain):
    return encrytion.encrypt(pad(plain))

def registerNewUser(userID,username,surname,email,password,request):
    text_name = binascii.b2a_base64(encrypt(username))
    text_surname = binascii.b2a_base64(encrypt(surname))
    text_password = binascii.b2a_base64(encrypt(password))
    text_email = binascii.b2a_base64(encrypt(email))
    user = Person(first_name=text_name, last_name=text_surname,email=text_email, id=userID,password=text_password,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user', 'first_name': username, 'last_name':surname}
    #print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    found = False
    email = ""
    for i in user:
        print "________________________________________"
        print i.email
        text = binascii.a2b_base64(i.email)
        email = decrypt(text)
        if email == userEmail:
            userE = Person.objects.get(id=i.id)
            found = True
        
            
    if found == False:
        return ""
    
    print "but i got here"
    password = decrypt(binascii.a2b_base64(userE.password))
    name=decrypt(binascii.a2b_base64(userE.first_name))
    surname=decrypt(binascii.a2b_base64(userE.last_name))
    if password == userPassword:
        request.session['user']={'identity':userE.id,'userRole':userE.userRole,'first_name':name,'last_name':surname}
        audit = LoginAuditLog(person_id=userE,action="Login",date=datetime.datetime.now())
        audit.save()
        if userE.userRole == 'user':
            data = {
                'name':name,
                'surname':surname,
                'userID':userE.id,
                'email':email,
                'userRole':userE.userRole
            }
        elif userE.userRole == 'LEA' or userE.userRole == 'DFI' or userE.userRole == 'SA' :
            pde = pdeAttribute.objects.filter()
            images = []
            audio = []
            video = []
            for value in pde:
                if value.photo and value.deleted == False:
                    name = value.photo.name
                    sts = name.split('/')
                    images.append({'title': value.title, 'data': sts[1],'id':value.id})
                elif value.audio and value.deleted == False:
                    name = value.audio.name
                    sts = name.split('/')
                    audio.append({'title': value.title, 'data': sts[1],'id':value.id})
                elif value.video and value.deleted == False:
                    name = value.video.name
                    sts = name.split('/')
                    video.append({'title': value.title, 'data': sts[1],'id':value.id})
            
            data = {
                'images':images,
                'audio':audio,
                'video':video,
                'date':str(datetime.date.today())
            }
        else:
            case = personCase.objects.filter(person=userE)
            cases = []
            
            for value in case:
                temp = []
                temp.append(value.case.id)
                temp.append(value.case.caseNumber)
                temp.append(value.case.caseName)
                cases.append(temp)

            pde = pdeAttribute.objects.filter(caseAttribute=case[0].case)
            images = []
            audio = []
            video = []
            for val in pde:
                if val.photo and val.deleted == False:
                    name = val.photo.name
                    sts = name.split('/')
                    images.append({'title': val.title, 'data': sts[1],'id':val.id})
                elif val.audio and val.deleted == False:
                    name = val.audio.name
                    sts = name.split('/')
                    audio.append({'title': val.title, 'data': sts[1],'id':val.id})
                elif val.video and val.deleted == False:
                    name = val.video.name
                    sts = name.split('/')
                    video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
            data = {
                'images':images,
                'audio':audio,
                'video':video,
                'case':cases,
                'caseName': case[0].case.caseName,
                'caseNumber': case[0].case.caseNumber,
                'date':str(datetime.date.today())
            }
            
        return data
    else:
        return ""
    
def logout(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
    audit = LoginAuditLog(person_id=userE,action="Logout",date=datetime.datetime.now())
    audit.save()
    return True

def UploadAudio(Title,Description,Location,Date,request):
    file = request.FILES['audioFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    print hashed.digest()
    text = binascii.b2a_base64(encrypt(hashed.hexdigest()))
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=text,Person=user,audio=file)
    upload.save()
    audit = AuditLogPDE(person_id=user,action="Added",pde_title=Title,pde_date=datetime.datetime.now(),pde_location=Location,date=datetime.datetime.now())
    audit.save()
    return True

def UploadAudioLEA(Case,Description,request):
    file = request.FILES['audioFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    print " when uploaded"
    print hashed.hexdigest()
    enc_data = binascii.b2a_base64(encrypt(hashed.hexdigest()))
   
    cases = case.objects.get(id=Case)
    upload = leaDigitalEvidence(description=Description,date=datetime.datetime.now(),digitalData=enc_data,Person=user,case=cases,audio=file)
    upload.save()
    audit = AuditLogDigitalEvidence(case=cases,person_id=user,action="Added",pde_date=datetime.datetime.now(),date=datetime.datetime.now(),pde_description=Description)
    audit.save()
    
    cases = getUserCases(request)
        
    data = {
            'case':cases
        }
    return data

def UploadVideo(Title,Description,Location,Date,request):
    file = request.FILES['videoFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    text = binascii.b2a_base64(encrypt(hashed.hexdigest()))
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=text,Person=user,video=file)
    upload.save()
    audit = AuditLogPDE(person_id=user,action="Added",pde_title=Title,pde_date=datetime.datetime.now(),pde_location=Location,date=datetime.datetime.now())
    audit.save()
    return True

def UploadVideoLEA(Case,Description,request):
    file = request.FILES['videoFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    #public_key = key.publickey()
    #hash = SHA256.new(file.read()).digest()
    #enc_data = public_key.encrypt(hash,32)
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    enc_data = encrypt(hashed.hexdigest())
    cases = case.objects.get(id=Case)
    upload = leaDigitalEvidence(case=cases,description=Description,date=datetime.datetime.now(),digitalData=binascii.b2a_base64(enc_data),Person=user,video=file)
    upload.save()
    audit = AuditLogDigitalEvidence(case=cases,person_id=user,action="Added",pde_date=datetime.datetime.now(),date=datetime.datetime.now(),pde_description=Description)
    audit.save()
    
    cases= getUserCases(request)
    data = {
            'userID':user.id,
            'case': cases
        }
    return data

def uploadImage(request, title_, description_, location_, date_, userID_):
    image = request.FILES['imageFileUpload']
    
    per = Person.objects.get(id = userID_)  #getting the object of the user who is currently logged in
    hashed = hashlib.sha256() 
    hashed.update(image.read()) #hashing the uploaded image
    text = binascii.b2a_base64(encrypt(hashed.hexdigest())) #encryting and converting the results into ASCII
    pde = pdeAttribute(title=title_, description=description_, location=location_, date=datetime.datetime.now(),digitalData=text, Person=per, photo=image)
    pde.save() #data saved into the database
    audit = AuditLogPDE(person_id=per,action="Added",pde_title=title_,pde_date=datetime.datetime.now(),pde_location=location_,date=datetime.datetime.now())
    audit.save() #audit
    return True
    
def uploadImageLEA(request, case_, description_):
    image = request.FILES['imageFileUpload']
    per = Person.objects.get(id=request.session['user']['identity'])#getting the object of the user who is currently logged in
    hashed = hashlib.sha256() #creating a hashlib object
    hashed.update(image.read()) #hashing the uploaded image
    enc_data = binascii.b2a_base64(encrypt(hashed.hexdigest())) #encryting and converting the results into ASCII
    cases = case.objects.get(id=case_) #getting the case that the images is uplouded for

    pde = leaDigitalEvidence(case=cases, description=description_,date=datetime.datetime.now(),digitalData=enc_data, Person=per, photo=image)
    pde.save() #data saved into the database
    audit = AuditLogDigitalEvidence(person_id=per,action="Added",pde_date=datetime.datetime.now(),date=datetime.datetime.now(),pde_description=description_,case=cases)
    audit.save() #logging act
    cases= getUserCases(request)
   
    data = {
            'userID':per.id,
            'case':cases
        }
    return data

def viewProfile(userID):
    data = []
    
    per = Person.objects.get(id = userID) 
    allUploads = pdeAttribute.objects.filter(Person = per)
    
    photoUploads = []
    videoUploads = []
    audioUploads = []
    
    for upload in allUploads:
        if upload.video:
            name = upload.video.name
            sts = name.split('/')
            print sts
            list = []
            list.append(upload.title)
            list.append(sts[1])
            videoUploads.append(list)
            
        elif upload.photo:
            name = upload.photo.name
            sts = name.split('/')
            list = []
            list.append(upload.title)
            list.append(sts[1])
            photoUploads.append(list)
        
        
        
        elif upload.audio:
            name = upload.audio.name
            sts = name.split('/')
            list = []
            list.append(upload.title)
            list.append(sts[1])
            audioUploads.append(list)
            

    data.append(decrypt(binascii.a2b_base64(per.first_name)))
    data.append(decrypt(binascii.a2b_base64(per.last_name)))
    data.append(per.id)
    data.append(decrypt(binascii.a2b_base64(per.email)))
    data.append(photoUploads)
    data.append(videoUploads)
    data.append(audioUploads)
    
    return data

def viewImage(request,image):
    pde = pdeAttribute.objects.get(id=image)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.photo.read())
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        if pde.caseAttribute:
            cases = pde.caseAttribute.caseNumber
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'status': 'success',
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'imageName':sts[1],
            'arrayCases':list,
            'oldHash': plaintext,
            'newHash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        if pde.caseAttribute:
            cases = pde.caseAttribute.caseNumber
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'status': 'success',
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':case,
            'imageName':sts[1],
            'arrayCases':list,
            'oldHash': plaintext,
            'newHash': hashed.hexdigest()
        }
        return data
    

def leaHomePage(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
    pde = pdeAttribute.objects.filter()
    images = []
    audio = []
    video = []
    for value in pde:
        if value.photo and value.deleted == False:
            name = value.photo.name
            sts = name.split('/')
            images.append({'title': value.title, 'data': sts[1],'id':value.id})
        elif value.audio and value.deleted == False:
            name = value.audio.name
            sts = name.split('/')
            audio.append({'title': value.title, 'data': sts[1],'id':value.id})
        elif value.video and value.deleted == False:
            name = value.video.name
            sts = name.split('/')
            video.append({'title': value.title, 'data': sts[1],'id':value.id})
    
            
    data = {
                'images':images,
                'audio':audio,
                'video':video,
                'date':str(datetime.date.today())
        }
    return data

def jdyHomePage(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
    case = personCaseAttribute.objects.filter(person=userE)
    cases = []
    for value in case:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)
        
    pde = pdeAttribute.objects.filter(caseAttribute=case[0].case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo and val.deleted == False:
            name = val.photo.name
            sts = name.split('/')
            images.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.audio and val.deleted == False:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.video and val.deleted == False:
            name = val.video.name
            sts = name.split('/')
            video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
    data = {
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': case[0].case.caseName,
        'caseNumber': case[0].case.caseNumber,
        'date':str(datetime.date.today())
        }
    return data

def assignCase(pdeID,caseID,request):
    pde = pdeAttribute.objects.get(id=pdeID)
    cases = case.objects.get(id=caseID)
    per = Person.objects.get(id=request.session['user']['identity'])
    au = AuditLogPDE(person_id=per,action='added to case',date=datetime.datetime.now(),pde_title=pde.title,pde_date=pde.date,pde_location=pde.location,case=cases)
    au.save()
    pde.caseAttribute = cases
    pde.save()
    return True

def viewVideo(request,video):
    pde = pdeAttribute.objects.get(id=video)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.video.read())
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        if pde.caseAttribute:
            cases = pde.caseAttribute.caseNumber
    
        Iname = pde.video.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'status': 'success',
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'videoName':sts[1],
            'arrayCases':list,
            'oldHash': plaintext,
            'newHash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        if pde.caseAttribute:
            cases = pde.caseAttribute.caseNumber
    
        Iname = pde.video.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'status': 'failed',
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'videoName':sts[1],
            'arrayCases':list,
            'oldHash': plaintext,
            'newHash': hashed.hexdigest()
        }
    
        return data

def viewAudio(request,audio):
    pde = pdeAttribute.objects.get(id=audio)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.audio.read())
    
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        if pde.caseAttribute:
            cases = pde.caseAttribute.caseNumber
    
        Iname = pde.audio.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'status': 'success',
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'audioName':sts[1],
            'arrayCases':list,
            'oldHash': plaintext,
            'newHash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        if pde.caseAttribute:
            cases = pde.caseAttribute.caseNumber
    
        Iname = pde.audio.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'status': 'failed',
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'audioName':sts[1],
            'arrayCases':list,
            'oldHash': plaintext,
            'newHash': hashed.hexdigest()
        }
    
        return data

def addCase(case_name, case_number, request,Title,Description,Date,Location):
    user = Person.objects.get(id=request.session['user']['identity'])
    file = request.FILES['imageFileUpload']
    cases = case(caseName=case_name,caseNumber=case_number,person=user,title=Title,description=Description,date=Date,location=Location,case_date=datetime.datetime.now(),textDoc=file)
    cases.save()
    person = personCase(person=user,case=cases)
    person.save()
    audit = AuditLogCase(person_id=user,action="Added",old_value="None",new_value=case_name,date=datetime.datetime.now())
    audit.save()
    return True

def deletePDE(pde_id,request):
    user = Person.objects.get(id=request.session['user']['identity'])
    pde = pdeAttribute.objects.get(id=pde_id)
    audit = AuditLogPDE(person_id=user,action="Deleted",pde_title=pde.title,pde_date=pde.date,pde_location=pde.location, date=datetime.datetime.now())
    audit.save()
    pde.deleted = True
    pde.save()
    return True

def RegisterAuthorizedUser(request, name, surname, idNo, role, Password, mail):
    text_name = binascii.b2a_base64(encrypt(name))
    text_surname = binascii.b2a_base64(encrypt(surname))
    text_password = binascii.b2a_base64(encrypt(Password))
    text_email = binascii.b2a_base64(encrypt(mail))
    user = Person(first_name=text_name, last_name=text_surname, id=idNo, email=text_email,password=text_password, userRole= role)
    user.save()
    return True
    
def viewPdeViaCase(request,ID):
    userE = Person.objects.get(id=request.session['user']['identity'])
    caseP = personCase.objects.filter(person=userE)
    cases = []
    
    for value in caseP:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)
        
    Case = case.objects.get(id=ID)
    pde = pdeAttribute.objects.filter(caseAttribute=Case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo and val.deleted == False:
            name = val.photo.name
            sts = name.split('/')
            images.append({'title': val.title,'data': sts[1],'id':val.id})
        elif val.audio and val.deleted == False:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.video and val.deleted == False:
            name = val.video.name
            sts = name.split('/')
            video.append({'title': val.title,'data': sts[1],'id':val.id})
            
    data = {
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': Case.caseName,
        'caseNumber': Case.caseNumber,
        'date':str(datetime.date.today())
        }
    return data

def viewPdeViaCaseD(request,ID):
    userE = Person.objects.get(id=request.session['user']['identity'])
    caseP = personCase.objects.filter(person=userE)
    cases = []
    
    for value in caseP:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)
        
    Case = case.objects.get(id=ID)
    pde = leaDigitalEvidence.objects.filter(case=Case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo and val.deleted == False:
            name = val.photo.name
            sts = name.split('/')
            images.append({'data': sts[1],'id':val.id})
        elif val.audio and val.deleted == False:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'data': sts[1],'id':val.id})
        elif val.video and val.deleted == False:
            name = val.video.name
            sts = name.split('/')
            video.append({'data': sts[1],'id':val.id})
            
    data = {
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': Case.caseName,
        'caseNumber': Case.caseNumber,
        'date':str(datetime.date.today())
        }
    return data

def viewByCase(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
    case = personCase.objects.filter(person=userE)
    cases = []
            
    for value in case:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)

    pde = pdeAttribute.objects.filter(caseAttribute=case[0].case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo and val.deleted == False:
            name = val.photo.name
            sts = name.split('/')
            images.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.audio and val.deleted == False:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.video and val.deleted == False:
            name = val.video.name
            sts = name.split('/')
            video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
    data = {
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': case[0].case.caseName,
        'caseNumber': case[0].case.caseNumber,
        'date':str(datetime.date.today())
    }
            
    return data

def getUserCases(request):
    per = Person.objects.get(id=request.session['user']['identity'])
    Pcase = personCase.objects.filter(person=per)
    
    cases = []
    for x in Pcase:
        data = []
        data.append(x.case.id)
        data.append(x.case.caseName)
        data.append(x.case.caseNumber)
        cases.append(data)
    
    return cases
        
def Documentation(request):
    per = Person.objects.get(id=request.session['user']['identity'])
    cases = getUserCases(request)
    
    case1 = cases[0]
    caseObj = case.objects.get(id=case1[0])
    pde = leaDigitalEvidence.objects.filter(case=caseObj)
    
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo and val.deleted == False:
            name = val.photo.name
            sts = name.split('/')
            images.append({'data': sts[1],'id':val.id})
        elif val.audio and val.deleted == False:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'data': sts[1],'id':val.id})
        elif val.video and val.deleted == False:
            name = val.video.name
            sts = name.split('/')
            video.append({'data': sts[1],'id':val.id})
            
    data = {
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'case_id':case1[0],
        'caseName': caseObj.caseName,
        'caseNumber': caseObj.caseNumber,
        'date':str(datetime.date.today())
    }
    return data

def viewImageLEA(request,image):
    pde = leaDigitalEvidence.objects.get(id=image)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.photo.read())
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'imageName':sts[1],
            'arrayCases':list,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'imageName':sts[1],
            'arrayCases':list,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
    
        return data
    
def viewAudioLEA(request,audio):
    pde = leaDigitalEvidence.objects.get(id=audio)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.audio.read())
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.audio.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'audioName':sts[1],
            'arrayCases':list,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.audio.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'audioName':sts[1],
            'arrayCases':list,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
    
        return data

def viewVideoLEA(request,video):
    pde = leaDigitalEvidence.objects.get(id=video)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.video.read())
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.video.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'incident': str(pde.case.date),
            'videoName':sts[1],
            'arrayCases':list,
            'caseNumber':cases,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.video.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'incident': str(pde.case.date),
            'videoName':sts[1],
            'arrayCases':list,
            'caseNumber':cases,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
        return data
    
def assignCaseLEA(pdeID,caseID):
    pde = leaDigitalEvidence.objects.get(id=pdeID)
    cases = case.objects.get(id=caseID)
    
    pde.case = cases
    pde.save()
    return True;

def deletePDE_LEA(pde_id,request):
    user = Person.objects.get(id=request.session['user']['identity'])
    pde = leaDigitalEvidence.objects.get(id=pde_id)
    audit = AuditLogDigitalEvidence(person_id=user,action="Deleted",pde_date=pde.date, pde_description= pde.description, date=datetime.datetime.now())
    audit.save()
    pde.deleted = True
    pde.save()
    
    return True

def Search(request,case_id):
    cases = case.objects.get(id=case_id)
    pde = pdeAttribute.objects.filter(location=cases.location)
    pde1 = pdeAttribute.objects.filter(location=' hatfield ')
    print str(pde)
    
    images = []
    audio = []
    video = []
    if pde:
        for i in pde:
            print "i traverse" + i.title
            if i.date.date() == cases.date.date():
                print "am in here"
                if i.photo and i.deleted == False:
                    print "ininininininniniiiinnnnninininin"
                    name = i.photo.name
                    sts = name.split('/')
                    images.append({'title': i.title, 'data': sts[1],'id':i.id})
                elif i.audio and i.deleted == False:
                    name = i.audio.name
                    sts = name.split('/')
                    audio.append({'title': i.title, 'data': sts[1],'id':i.id})
                elif i.video and val.deleted == False:
                    name = i.video.name
                    sts = name.split('/')
                    video.append({'title': i.title, 'data': sts[1],'id':i.id})
        print str(images)
        data = {
            'images':images,
            'audio':audio,
            'video':video,
            'date':str(cases.date.date()),
            'case_name': cases.caseName,
            'case_number': cases.caseNumber
        }
        return data
    else:
        return ""
    
def getCaseData(request,case_id):
    Case = case.objects.get(id=case_id)
    
    data = []
    data.append(Case.caseName)
    data.append(Case.caseNumber)
    data.append(Case.title)
    data.append(Case.description)
    data.append(str(Case.date))
    data.append(Case.location)
    
    return data
    
def getPDEdata(request,case_id):
    Case = case.objects.get(id=case_id)
    digital = AuditLogDigitalEvidence.objects.filter(case=Case)
    
    data = []
    for d in digital:
        temp = []
        temp.append(d.person_id.first_name + " "+ d.person_id.last_name)
        temp.append(str(d.date))
        temp.append(d.action)
        temp.append(d.pde_description)
        temp.append(str(d.pde_date))
        data.append(temp)
    
    return data
        
def auditLog(request):
    login = LoginAuditLog.objects.all()
    logins = []
    for i in login:
        temp = []
        name = binascii.a2b_base64(i.person_id.first_name)
        name = decrypt(name)
        surn = binascii.a2b_base64(i.person_id.last_name)
        surn = decrypt(surn)
        temp.append(name+ " "+ surn)
        date = i.date.strftime("%Y-%m-%d %H:%M:%S")
        temp.append(str(date))
        temp.append(i.action)
        logins.append(temp)
    
    pdeC = AuditLogPDE.objects.all()
    CommPDE = []
    for i in pdeC:
        temp=[]
        name = binascii.a2b_base64(i.person_id.first_name)
        name = decrypt(name)
        surn = binascii.a2b_base64(i.person_id.last_name)
        surn = decrypt(surn)
        temp.append(name+ " "+surn)
        temp.append(i.pde_title)
        date = i.date.strftime("%Y-%m-%d %H:%M:%S")
        temp.append(str(date))
        date = i.pde_date.strftime("%Y-%m-%d %H:%M:%S")
        temp.append(str(date))
        temp.append(i.action)
        if i.case:
            temp.append(i.case.caseName+" "+i.case.caseNumber)
        else:
            temp.append('None')
        CommPDE.append(temp)
        
    pdeA = AuditLogDigitalEvidence.objects.all()
    AuthPDE=[]
    for i in pdeA:
        temp = []
        name = binascii.a2b_base64(i.person_id.first_name)
        name = decrypt(name)
        surn = binascii.a2b_base64(i.person_id.last_name)
        surn = decrypt(surn)
        temp.append(name+ " "+surn)
        date = i.date.strftime("%Y-%m-%d %H:%M:%S")
        temp.append(str(date))
        date = i.pde_date.strftime("%Y-%m-%d %H:%M:%S")
        temp.append(str(date))
        temp.append(i.action)
        if i.case:
            temp.append(i.case.caseName+" "+i.case.caseNumber)
        else:
            temp.append('None')
        AuthPDE.append(temp)
        
    data = []
    data.append(logins)
    data.append(CommPDE)
    data.append(AuthPDE)
    return data
        
def getDeleted(request):
    comPDE = pdeAttribute.objects.filter(deleted=True)
    authPDE = leaDigitalEvidence.objects.filter(deleted=True)
    
    community = []
    authorized = []
    
    imagesC = []
    audioC = []
    videoC=[]
    for val in comPDE:
        if val.photo:
            name = val.photo.name
            sts = name.split('/')
            imagesC.append({'title': val.title,'data': sts[1],'id':val.id})
        elif val.audio:
            name = val.audio.name
            sts = name.split('/')
            audioC.append({'title': val.title,'data': sts[1],'id':val.id})
        elif val.video:
            name = val.video.name
            sts = name.split('/')
            videoC.append({'title': val.title,'data': sts[1],'id':val.id})
    
    community.append(imagesC)
    community.append(audioC)
    community.append(videoC)
    
    images = []
    audio =[]
    video = []
    for val in authPDE:
        if val.photo:
            name = val.photo.name
            sts = name.split('/')
            images.append({'data': sts[1],'id':val.id})
        elif val.audio:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'data': sts[1],'id':val.id})
        elif val.video:
            name = val.video.name
            sts = name.split('/')
            video.append({'data': sts[1],'id':val.id})
            
    authorized.append(images)
    authorized.append(audio)
    authorized.append(video)
    
    combined = []
    combined.append(community)
    combined.append(authorized)
    return combined
    
def viewImageDel(request,image):
    pde = leaDigitalEvidence.objects.get(id=image)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.photo.read())

    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
        
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'imageName':sts[1],
            'arrayCases':list,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
    
        return data
    else:
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
        print "darli dont plsssssssssssssssssssssssssssssssss"
        data = {
            'title':pde.case.title,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'caseNumber':cases,
            'imageName':sts[1],
            'arrayCases':list,
            'oldhash': plaintext,
            'newhash': hashed.hexdigest()
        }
        return data