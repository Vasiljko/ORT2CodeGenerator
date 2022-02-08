from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import fitz
import cv2

linesToPrint = []

with open("microProgram.txt") as f:
    lines = f.readlines()
    for line in lines:
        if line[0] == '!' or len(line)<=1:
            continue
        line = line.replace(', ', ',')
        line = line.replace(' (','(')
        line = line.strip()
        line = line[:-1]
        linesToPrint.append(line.strip())

i = 0
row = 0
num_page = 0

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFont("Helvetica", 9)
output = PdfFileWriter()
#packet.seek(0)

x = 403
y = 756
step_y = 36
br = 0

x_img1 = 232
y_img1 = 745
widht_img1 = 150
height_img1 = 30

x_img2 = 46
y_img2 = 745
width_img2 = 150
height_img2 = 30

img_step = 36.1


while i != len(linesToPrint):
    s = linesToPrint[i]
    if "br" not in s:
        if row == 17:
            row = 0
            can.showPage()
            can.setFont("Helvetica", 9)
            num_page+=1
        
        can.drawImage("obican.png", x_img1, y_img1-row*img_step, widht_img1, height_img1)
        can.drawImage("linija.png", x_img1+50, y_img1-row*img_step-8, 1,8)
        can.drawImage("obican.png", x_img2, y_img1-row*img_step, widht_img1, height_img1)
        can.drawImage("linija.png", x_img2+50, y_img1-row*img_step-8, 1,8)

        upravljacka = ""
        for k in range(7, len(s)):
            if k+1<len(s) and s[k]=='b' and s[k+1] == 'r':
                pos = k+2
                break
            pos = k+1
            upravljacka+=s[k]
        
        if upravljacka[-1] == ',':
            upravljacka = upravljacka[:-1]


        if len(s) <= 26:
            can.drawString(x, y-step_y*row, s)
            can.drawString(x_img1+10, y-step_y*row, upravljacka)
        else:
            fi = ""
            se = ""
            for k in range(len(s)):
                if s[k]==',' and k<=26 and len(s)-k-1 <=26:
                    fi = s[:k]
                    se = s[k+1:]
                    break

            upravljacka_fi = ""
            upravljacka_se = ""
            for k in range(len(upravljacka)):
                if upravljacka[k]==',' and k<=25 and len(upravljacka)-k-1 <=25:
                    upravljacka_fi = upravljacka[:k+1]
                    upravljacka_se = upravljacka[k+1:]
                    break
            
            can.drawString(x, y-step_y*row+7, fi)
            can.drawString(x, y-step_y*row-7, se)
            can.drawString(x_img1+10, y-step_y*row+7, upravljacka_fi)
            can.drawString(x_img1+10, y-step_y*row-7, upravljacka_se)
        row+=1
       
    else:
        if row == 16 or row == 17:
            row = 0
            can.showPage()
            can.setFont("Helvetica", 9)
            num_page+=1

        can.drawImage("obican.png", x_img1, y_img1-row*img_step, widht_img1, height_img1)
        can.drawImage("uslovni.png", x_img1, y_img1-(row+1)*img_step, width_img2, height_img2)
        can.drawImage("linija.png", x_img1+50, y_img1-row*img_step-8, 1,8) #posle obicne kutije
        can.drawImage("linija.png", x_img1+50, y_img1-(row+1)*img_step-8, 1,8) #posle uslovnog skoka

        can.drawImage("obican.png", x_img2, y_img1-row*img_step, widht_img1, height_img1)
        can.drawImage("uslovni.png", x_img2, y_img1-(row+1)*img_step, width_img2, height_img2)
        can.drawImage("linija.png", x_img2+50, y_img1-row*img_step-8, 1,8) #posle obicne kutije
        can.drawImage("linija.png", x_img2+50, y_img1-(row+1)*img_step-8, 1,8) #posle uslovnog skoka

        upravljacka = ""
        for k in range(7, len(s)):
            if k+1<len(s) and s[k]=='b' and s[k+1] == 'r':
                pos = k+2
                break
            pos = k+1
            upravljacka+=s[k]

        if len(upravljacka)>0 and upravljacka[-1] == ',':
            upravljacka = upravljacka[:-1]

        signal = ""
        step = ""
        if s[pos]==' ':
            step = s[pos+5:]
        elif s[pos] == '(':
            for k in range(pos+4, len(s)):
                if s[k] == ' ':
                    pos = k
                    break
                signal+=s[k]
            step = s[pos+10:-1]
        else:
            signal = s[pos:]


        
        can.drawString(x_img1+40, y-step_y*(row+1), signal)
        can.drawString(x_img1+127, y-step_y*(row+1), step)

        can.drawString(x_img2+40, y-step_y*(row+1), signal)
        can.drawString(x_img2+127, y-step_y*(row+1), step)      
        if len(s) <= 35:
            can.drawString(x, y-step_y*row, s)   
            can.drawString(x_img1+10, y-step_y*row, upravljacka)
        else:
            fi = ""
            se = ""
            for k in range(len(s)):
                if s[k]==',' and k<=30 and len(s)-k-1 <=30:
                    fi = s[:k]
                    se = s[k+1:]
                    break

            upravljacka_fi = ""
            upravljacka_se = ""
            for k in range(len(upravljacka)):
                if upravljacka[k]==',' and k<=25 and len(upravljacka)-k-1 <=25:
                    upravljacka_fi = upravljacka[:k+1]
                    upravljacka_se = upravljacka[k+1:]
                    break

            can.drawString(x, y-step_y*row+7, fi)
            can.drawString(x, y-step_y*row-7, se)
            can.drawString(x_img1+10, y-step_y*row+7, upravljacka_fi)
            can.drawString(x_img1+10, y-step_y*row-7, upravljacka_se)
        row+=2


    i += 1

if row != 0:
    can.showPage()
    num_page+=1

can.save()

packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("proba.pdf", "rb"))

for i in range(num_page):
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(i))
    output.addPage(page)

destination_name = "PopunjenFormular.pdf"
outputStream = open(destination_name, "wb")
output.write(outputStream)
outputStream.close()
