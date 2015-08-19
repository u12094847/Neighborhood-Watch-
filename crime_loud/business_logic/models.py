from django.db import models
from Crypto.Cipher import AES
import binascii

key = '0123456789abcdef'
encrytion = AES.new(key)

def pad(s):
    return s+((16-len(s)% 16)*'{')

def encrypt(plain):
    return encrytion.encrypt(pad(plain))

def decrypt(cipher):
    dec = encrytion.decrypt(cipher).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-l]

#Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    id = models.CharField(max_length=13, primary_key = True)
    email = models.CharField(max_length=1000)
    password=models.CharField(max_length=1000)
    userRole=models.CharField(max_length=4)
    
    def __unicode__(self):
        return decrypt(binascii.a2b_base64(self.first_name))
     #return self.first_name
'''
class caseAttribute(models.Model):
    caseName = models.CharField(max_length=30)
    caseNumber=models.CharField(max_length=20)
    person = models.ForeignKey(Person)
    
    def __unicode__(self):
      return self.caseName + " "+self.caseNumber

class personCaseAttribute(models.Model):
    person = models.ForeignKey(Person)
    case = models.ForeignKey(caseAttribute)
    
    def __unicode__(self):
      return self.case.caseNumber
'''

class case(models.Model):
    caseName = models.CharField(max_length=30)
    caseNumber=models.CharField(max_length=20)
    person = models.ForeignKey(Person)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    date = models.DateTimeField()
    case_date = models.DateTimeField(null=True)
    location = models.CharField(max_length=30)
    textDoc = models.FileField(upload_to='document',null=True)
    
    def __unicode__(self):
      return self.caseName + " "+self.caseNumber

class pdeAttribute(models.Model):
    title = models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    location=models.CharField(max_length=40)
    date=models.DateTimeField()
    digitalData=models.CharField(max_length=1000,null=True)
    caseAttribute=models.ForeignKey(case, null=True)
    Person = models.ForeignKey(Person) #Person who uploaded
    photo = models.FileField(upload_to='photo',null=True)
    video = models.FileField(upload_to='video',null=True)
    audio = models.FileField(upload_to='audio',null=True)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
    
class leaDigitalEvidence(models.Model):
    date=models.DateTimeField()
    description=models.CharField(max_length=100, null=True)
    digitalData=models.CharField(max_length=1000,null=True)
    case=models.ForeignKey(case, null=True)
    Person = models.ForeignKey(Person) #Person who uploaded
    photo = models.FileField(upload_to='photo',null=True)
    video = models.FileField(upload_to='video',null=True)
    audio = models.FileField(upload_to='audio',null=True)
    textDoc = models.FileField(upload_to='text',null=True)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return decrypt(binascii.a2b_base64(self.Person.first_name)) + str(self.id)
    
class personCase(models.Model):
    person = models.ForeignKey(Person)
    case = models.ForeignKey(case)
    
    def __unicode__(self):
      return self.case.caseNumber
    
class AuditLogCase(models.Model):
    person_id = models.ForeignKey(Person)
    action = models.CharField(max_length=20)
    date = models.DateTimeField()
    old_value=models.CharField(max_length=100,null=True)
    new_value=models.CharField(max_length=100,null=True)
    
class AuditLogPDE(models.Model):
    person_id = models.ForeignKey(Person)
    action=models.CharField(max_length=20)
    date = models.DateTimeField()
    pde_title=models.CharField(max_length=100)
    pde_date = models.DateTimeField()
    pde_location = models.CharField(max_length=40)
    case =models.ForeignKey(case,null=True)

class AuditLogDigitalEvidence(models.Model):
    person_id = models.ForeignKey(Person)
    action=models.CharField(max_length=20)
    date = models.DateTimeField()
    pde_date = models.DateTimeField()
    pde_description = models.CharField(max_length=100,null=True)
    case = models.ForeignKey(case, null = True)

class LoginAuditLog(models.Model):
    person_id = models.ForeignKey(Person)
    action = models.CharField(max_length=7)
    date = models.DateTimeField()
    


