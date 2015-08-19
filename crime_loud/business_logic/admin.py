from django.contrib import admin
from .models import Person, pdeAttribute, AuditLogCase, AuditLogPDE, personCase, AuditLogDigitalEvidence, case,leaDigitalEvidence,LoginAuditLog

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person,PersonAdmin)
'''
class caseAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(caseAttribute,caseAttributeAdmin)
'''
class pdeAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(pdeAttribute,pdeAttributeAdmin)

class AuditLogCaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(AuditLogCase,AuditLogCaseAdmin)

class AuditLogPDEAdmin(admin.ModelAdmin):
    pass
admin.site.register(AuditLogPDE,AuditLogPDEAdmin)

class personCaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(personCase,personCaseAdmin)

class AuditLogDigitalEvidenceAdmin (admin.ModelAdmin):
    pass
admin.site.register(AuditLogDigitalEvidence,AuditLogDigitalEvidenceAdmin)

class caseAdmin(admin.ModelAdmin):
    pass
admin.site.register(case,caseAdmin)
'''
class personCaseAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(personCaseAttribute, personCaseAttributeAdmin)
'''
class leaDigitalEvidenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(leaDigitalEvidence,leaDigitalEvidenceAdmin)

class LoginAuditLogAdmin(admin.ModelAdmin):
    pass
admin.site.register(LoginAuditLog,LoginAuditLogAdmin)



