from io import BytesIO
import csv
import json
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import cm, mm, inch
from reportlab.platypus import Image, SimpleDocTemplate, Frame, Spacer
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

from django.http import HttpResponse
from django.shortcuts import render

styles = getSampleStyleSheet()

def generate_case_report(case, cs_docs):
    
    cName = case[0]
    cNumber = case[1]
    cTitle = case[2]
    cDescr = case[3]
    cDate = case[4]
    cLocation = case[5]
    
    filename = cNumber+"_"+cName+"_report.pdf"
    fileN = cNumber + "_"+cName+"_report"
   # logo =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/reporting/images/crime_loud_logo.jpg")
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+ filename
 
    buffer = BytesIO()
    #might have to change margins depending on what mamzo wants
    my_pdf = SimpleDocTemplate(buffer, rightMarging=72, leftMargin=72, topMargin=15, bottomMargin=50)
    
    
    #container for the pdf elements
    elements = []
    
    '''
    f = Image(logo)
    f.hAlign = 'CENTER'
    f.drawHeight = 1.5*inch
    f.drawWidth = 4 *inch
    elements.append(f)
    '''
    styles=getSampleStyleSheet()
    styleN = styles["Normal"]
    styleH = styles["Heading1"]
    styleH.alignment = TA_CENTER
    
    elements.append(Paragraph('<h1>'+'Case Name: '+ cName+'</h1>',styleH))
    elements.append(Paragraph('<h3>'+'Case Number: '+ cNumber+'</h3>',styleH))
    elements.append(Paragraph('<h3>'+'Title: '+ cTitle+'</h3>',styleH))
    elements.append(Paragraph('<h3>'+'Description: '+ cDescr+'</h3>',styleH))
    elements.append(Paragraph('<h3>'+'Date: '+ cDate+'</h3>',styleH))
    elements.append(Paragraph('<h3>'+'Location: '+ cLocation+'</h3>',styleH))
    
    elements.append(Spacer(width=0, height=0.1*cm))
    
    ##############################################
    
    tdata = [[Paragraph('<b>' + 'Crime Scene Uploads' + '</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,0),1, colors.black),
                                ('BACKGROUND',(0,0),(-1,-1),colors.lightblue)#Give total a grey background)
                              ]))
    table._argW[0]=7.0*inch
    elements.append(table)
    elements.append(Spacer(width=0, height=1*cm))
    
    tdata = [[Paragraph('<b>User Name</b>',styleN),
              Paragraph('<b>Date</b>',styleN),
              Paragraph('<b>Action</b>',styleN),
              Paragraph('<b>Description</b>',styleN),
              Paragraph('<b>PDE Date </b>', styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    table._argW[0]=2.5*inch #Set the size(width) of the first column in the table
    table._argW[1]=1.5*inch
    table._argW[2]=1.5*inch
    table._argW[3]=1.5*inch
    table._argW[4]=1.5*inch
    
    
    elements.append(table)
    elements.append(Spacer(width=0, height=1*cm))
    '''
    this part of the table must loop through the community aray to display all available information
    for example:
    
    for k in cs_docs:
    
        tdata = [k[0], k[1],k[2], k[3],k[4]]
        table2 = Table(tdata, colWidths=None, rowHeights=None)
        table2.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
         #table=Table(tdata, colWidths=80, rowHeights=30)
        table2._argW[0]=2.5*inch #Set the size(width) of the first collumn in the table
        table2._argW[1]=1.5*inch
        table2._argW[2]=1.5*inch
        table2._argW[3]=1.5*inch
        table2._argW[4]=1.5*inch
        elements.append(table2)
        
    elements.append(Spacer(width=0, height=1*cm))
    '''
    
    my_pdf.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

