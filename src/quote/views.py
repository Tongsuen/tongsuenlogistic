
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.shortcuts import render
import os.path
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image, TableStyle,Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from textwrap import wrap
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import time
from datetime import datetime
from reportlab.lib import utils

from .form import QuoteForm
from .models import QuoteModel, TypeQuote
# Create your views here.
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings


pdfmetrics.registerFont(TTFont('PrompFont', settings.STATIC_ROOT + '/resource/thai_font/Sun-ExtA.ttf'))
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

def get_image(path, width=3*inch):
    try:
        img = utils.ImageReader(path)

        iw, ih = img.getSize()
        aspect = ih / float(iw)

        return Image(path, width=width, height=(width * aspect))
    except OSError:
        img = utils.ImageReader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tt.png'))

        iw, ih = img.getSize()
        aspect = ih / float(iw)

        return Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'noimage.gif'), width=2*inch, height=(2*inch * aspect))


def createPDFTable(id_quote):

    obj = QuoteModel.objects.get(pk=id_quote)

    print(obj.created_date)
    print(obj.updated_date)
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer,pagesize=letter,
                        rightMargin=20,leftMargin=20,
                        topMargin=10,bottomMargin=18,title="quote")

    Story=[]
    logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tt.png')

    im = get_image(logo,width=PAGE_WIDTH/5)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='normal', alignment=TA_LEFT, fontName='PrompFont', fontSize=10,spaceAfter = 10, spaceBefore =10))
    styles.add(ParagraphStyle(name='normal-1', alignment=TA_LEFT, fontName='PrompFont', fontSize=11,spaceAfter = 10, spaceBefore =10))

    styles.add(ParagraphStyle(name='header-quote', alignment=TA_CENTER, fontName='PrompFont', fontSize=16   ,spaceAfter = 10, spaceBefore =10))
    styles.add(ParagraphStyle(name='header', alignment=TA_LEFT, fontName='PrompFont', fontSize=14,spaceAfter = 2, spaceBefore =2))
    styles.add(ParagraphStyle(name='address', alignment=TA_JUSTIFY, fontName='PrompFont', fontSize=14,spaceAfter = 2, spaceBefore =2))
    s = styles["normal"]
    s.wordWrap = 'CJK'

    data = [
        ['', ''],
        [im, Paragraph("TONG SUEN LOGISTICS CO.,LTD", styles["normal-1"])],
        ['', Paragraph("1/8, Soi Rom Klao 23, Rom Klao Road, Khlong Sam", styles["normal"])],
        ['',Paragraph("Prawet, Lat Krabang, Bangkok, Thailand 10520", styles["normal"])],
        ['',Paragraph("Tel.: (66)02-105-3848 / (66)062-462-2938 / 098-524-2545", styles["normal"])],
        ['',Paragraph("Fax.: (66)02-105-3847", styles["normal"])],
        ['',Paragraph("E-mail: sermpong@tongsuenlogistics.co.th", styles["normal"])],
        ['', ""],
        ['', ""],
    ]
    style = TableStyle([
                        ('ALIGNMENT',(0,0),(0,7),'CENTER'),
                        ('ALIGNMENT',(1,1),(-1,-1),'LEFT'),
                        ('SPAN',(0,1),(0,6)),
                        ('LINEABOVE',(0,8),(1,8),1.0,colors.black),
                     ])


    t=Table(data,colWidths=PAGE_WIDTH/2,rowHeights=20)
    t.setStyle(style)
    Story.append(t)


    #tq = SubCategory.objects.get(pk=given_pk)
    Story.append(Paragraph("<u>%s quote</u>" % obj.type_quote.name_type_en, styles["header-quote"]))
    Story.append(Spacer(1, 12))

    strg = '{d.day}/{d.month}/{d.year} {d.hour}:{d.minute}:{d.second}'.format(d=obj.created_date)
    data = [
    [Paragraph("Name:&nbsp;&nbsp;", styles["normal"]),  Paragraph(u"Last <i>%s</i>   First <i>%s</i> " % (obj.last_name , obj.first_name), styles["normal"])],
    [Paragraph("Company Name:", styles["normal"]),  Paragraph(u"<i>%s</i>" % obj.name_company, styles["normal"])],
    [Paragraph("Email:", styles["normal"]),  Paragraph(u"<i>%s</i>" % obj.email, styles["normal"])],
    [Paragraph("Tel:", styles["normal"]),  Paragraph(u"Office: <i>%s</i> Mobile: <i>%s</i> Fax: <i>%s</i> " % (obj.tel_office,obj.tel_mobile,obj.tel_fax), styles["normal"])],
    [Paragraph("Type Product:", styles["normal"]),  Paragraph(u"<i>%s</i>" % obj.type_product, styles["normal"])],
    [Paragraph("Direction:", styles["normal"]),  Paragraph(u"<i>%s</i>" % obj.direction, styles["normal"])],
    [Paragraph("Detail:", styles["normal"]), Paragraph( u"<i>%s</i>" % obj.detail, styles["normal"])],
    [Paragraph("Date Create:", styles["normal"]),  Paragraph(u"<i>%s</i>" % strg, styles["normal"])],
    [Paragraph("Attachment File:", styles["normal"]), [ Paragraph(u"<i>%s</i>" % obj.file_path.path, styles["normal"]),get_image(obj.file_path.path,width=PAGE_WIDTH/3)]],
    ]

    #TODO: Get this line right instead of just copying it from the docs
    style = TableStyle([
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ('ALIGNMENT', (1,8), (1,8), "CENTER"),
                           ('VALIGN', (0,0), (0,8), "MIDDLE"),
                           ])

    #Configure style and word wrap
    t=Table(data,colWidths=PAGE_WIDTH/2.25)
    t.setStyle(style)

    #Send the data and build the file
    Story.append(t)

    Story.append(Spacer(1, 22))

    doc.build(Story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
def createPDF():
    # Create the HttpResponse object with the appropriate PDF headers.
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer,pagesize=letter)


    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tt.png')
    p.drawImage(fn, 50, 620,width=150, height=150, mask='auto')

    y_ori_address = 740

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFillColorRGB(45/255, 62/255, 70/255) #choose your font colour
    p.setFont("Helvetica", 14) #choose your font type and font size
    p.drawString(320,y_ori_address,"TONG SUEN LOGISTICS CO.,LTD") # write your text
    p.setFont("Helvetica", 10)
    y_ori_address -= 20
    p.drawString(320,y_ori_address,"1/8, Soi Rom Klao 23, Rom Klao Road, Khlong Sam")
    y_ori_address -= 20
    p.drawString(320,y_ori_address,"Prawet, Lat Krabang, Bangkok, Thailand 10520 ")
    y_ori_address -= 20
    p.drawString(320,y_ori_address,"Tel.: (66)02-105-3848 / (66)062-462-2938 / 098-524-2545 ")
    y_ori_address -= 20
    p.drawString(320,y_ori_address,"Fax.: (66)02-105-3847 ")
    y_ori_address -= 20
    p.drawString(320,y_ori_address ,"E-mail: sermpong@tongsuenlogistics.co.th")

    #draw line
    y_ori_address =y_ori_address-40
    p.line(PAGE_WIDTH*.2,y_ori_address,PAGE_WIDTH*.8,y_ori_address)

    # quote type
    p.setFont("Helvetica", 16)
    y_ori_address = y_ori_address-40
    p.drawCentredString(PAGE_WIDTH/2.0,y_ori_address ,"Transport Quote")

    #text detail

    p.setFont("Helvetica", 10)
    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"First")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "Lorem Ipsum"
    wraped_text = "\n".join(wrap(text, 55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)

    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"Company Name")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "Eastern Indian Company"
    wraped_text = "\n".join(wrap(text, 55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)

    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"Email")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "AlexForthyEgg@EasternIndian.co.th"
    wraped_text = "\n".join(wrap(text,55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)

    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"Tel")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "0989876543"
    wraped_text = "\n".join(wrap(text, 55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)

    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"Type Product")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "product type. A grouping of similar kinds of manufactured goods or services. A product type might"
    wraped_text = "\n".join(wrap(text, 55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)

    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"direction")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "Bengali Malaysia"
    wraped_text = "\n".join(wrap(text, 55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)

    y_ori_address = y_ori_address-40
    p.drawString(PAGE_WIDTH*0.1,y_ori_address ,"detail")
    t = p.beginText(PAGE_WIDTH/2,y_ori_address)
    text = "Product Types. Create a separate product type definition for each category of catalog entries that you sell. For example, you might have a product type for movies, another for books, a third for electronics, etc. When thinking about creating new product types, the most significant differences are the Class "
    wraped_text = "\n".join(wrap(text, 55)) # 80 is line width
    t.textLines(wraped_text)
    p.drawText(t)


    dt = datetime.now()

    # str.format
    strg = '{d.day}/{d.month}/{d.year} {d.hour}:{d.minute}:{d.second}'.format(d=dt)

    p.drawCentredString(PAGE_WIDTH/2,20 ,strg)

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def pdf_generate(request):

    if request.method == "POST" :

        form = QuoteForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            # file is saved
            new_quote = form.save()
            response = HttpResponse(content_type='html')
            response['Content-Disposition'] = 'attachment; filename="testfile.pdf"'
            response.write(createPDFTable(new_quote.pk))
            return response


            # msg = EmailMessage('Quote', 'Quote Body', 'tongsuenDev@gmail.com', ['atp12112@gmail.com'])
            # msg.content_subtype = "html"  # Main content is now text/html
            # pdf=createPDFTable(new_quote.pk)
            # msg.attach('quote.pdf',pdf,'application/pdf')
            # msg.send()
            # return render(request,"homepage.html",{})
            #if len(request.FILES) != 0:
        else:
            print("fail")
