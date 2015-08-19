from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from web_services import views
from .api import *
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

def get_case_report(request,case_id):
    
    #get the case id from the interface to get the other details from the business logic
   # case_id = request.POST['case_id']
    data = {
        'case_id':case_id
    }
    
    #get all required information about the case for the report
    result = views.getCaseInformationForReport(request, json.dumps(data))
    
    res = json.loads(result.content)
    
    # the case information is pplaced in an array called case with all initial details
    case = res['case_info']
    
    '''
    case_name = case[0]
    case_number = case[0]
    case_title = case[0]
    case_description = case[0]
    case_date = case[0]
    case_location = case[0]
    '''
    
    # the community uploads will be a 2d array with each field an upload from a person in the community
   
    
    # the crime scene documentation will be in same format as the community one
    #MAMZO WHAT IS THE DIFFERENCE IN DATA FOR THESE TWO??
    cs_docs = res['cs_docs']
    
    
    return generate_case_report(case, cs_docs)