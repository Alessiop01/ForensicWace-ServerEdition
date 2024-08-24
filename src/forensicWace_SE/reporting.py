import os

import forensicWace_SE.utils as utils
import forensicWace_SE.certification as certification
import forensicWace_SE.globalConstants as globalConstants

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from io import BytesIO

basePath = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def CreateHorizontalDocHeaderAndFooter(canvas, doc):
    canvas.saveState()
    canvas.restoreState()
    page_num = canvas.getPageNumber()
    text = "Page %s" % page_num
    canvas.drawCentredString(148.5 * mm, 20 * mm, text)
    canvas.line(15 * mm, 25 * mm, 282 * mm, 25 * mm)


def CreateVerticalDocHeaderAndFooter(canvas, doc):
    canvas.saveState()
    canvas.drawImage(basePath + "/assets/img/Logo.png", A4[0] / 2 - 158, A4[1] - 65, width=300, height=52.5)
    print(basePath + "/assets/img/Logo.png")
    canvas.restoreState()
    page_num = canvas.getPageNumber()
    text = "Page %s" % page_num
    canvas.drawCentredString(105 * mm, 20 * mm, text)
    canvas.line(15 * mm, 25 * mm, 195 * mm, 25 * mm)


def ExportGpsLocations(udid, extractedDataList):

    # Define data structure
    data = [["Sender", "Receiver", "Date", "Latitude", "Longitude"]]

    # Foreach extracted data, add it into the previous defined structure
    for extractedData in extractedDataList:
        data.append([utils.FormatPhoneNumberForPageTables(extractedData["Sender"]),
                     utils.FormatPhoneNumberForPageTables(extractedData["Receiver"]),
                     extractedData["MessageDate"],
                     extractedData["Latitude"],
                     extractedData["Longitude"]])

    buffer = BytesIO()

    # Configure the document
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Define an array to store all the elements to be printed in the output file
    fileElements = []

    # Define table structure
    table = Table(data, colWidths=[100, 110, 110, 110])

    # Define style of the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])

    # Apply style to the created table
    table.setStyle(style)

    # Add the table to the output document
    fileElements.append(table)

    # Build the output PDF file
    doc.build(fileElements, onFirstPage=CreateVerticalDocHeaderAndFooter, onLaterPages=CreateVerticalDocHeaderAndFooter)

    # Move buffer to initial position
    buffer.seek(0)

    # Certificate the output report
    certificatedReportZip = certification.CertificateReportAndZipFiles(udid, buffer.getvalue(), globalConstants.GpsDataReport)

    # Return generated file
    return certificatedReportZip


def ExportChatList(udid, extractedDataList):

    # Define data structure
    data = [["Contact", "Username", "Phone number", "Number of messages", "Last Message Date"]]

    # Foreach extracted data, add it into the previous defined structure
    for extractedData in extractedDataList:
        data.append([extractedData["Contact"],
                     extractedData["UserName"],
                     utils.FormatPhoneNumberForPageTables(extractedData["PhoneNumber"]),
                     extractedData["NumberOfMessages"],
                     extractedData["MessageDate"]])

    buffer = BytesIO()

    # Configure the document
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Define an array to store all the elements to be printed in the output file
    fileElements = []

    # Define table structure
    table = Table(data, colWidths=[100, 110, 110, 110])

    # Define style of the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])

    # Apply style to the created table
    table.setStyle(style)

    # Add the table to the output document
    fileElements.append(table)

    # Build the output PDF file
    doc.build(fileElements, onFirstPage=CreateVerticalDocHeaderAndFooter, onLaterPages=CreateVerticalDocHeaderAndFooter)

    # Move buffer to initial position
    buffer.seek(0)

    # Certificate the output report
    certificatedReportZip = certification.CertificateReportAndZipFiles(udid, buffer.getvalue(), globalConstants.ChatListReport)

    # Return generated file
    return certificatedReportZip


def ExportBlockedContactsReport(udid, extractedDataList):

    # Define data structure
    data = [["Name", "Phone number"]]

    # Foreach extracted data, add it into the previous defined structure
    for extractedData in extractedDataList:
        if extractedData["Name"] is None:
            extractedData["Name"] = globalConstants.notAvailable
        data.append([extractedData["Name"], utils.FormatPhoneNumberForPageTables(extractedData["PhoneNumber"])])

    buffer = BytesIO()

    # Configure the document
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Define an array to store all the elements to be printed in the output file
    fileElements = []

    # Define table structure
    table = Table(data, colWidths=[100, 110, 110, 110])

    # Define style of the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])

    # Apply style to the created table
    table.setStyle(style)

    # Add the table to the output document
    fileElements.append(table)

    # Build the output PDF file
    doc.build(fileElements, onFirstPage=CreateVerticalDocHeaderAndFooter, onLaterPages=CreateVerticalDocHeaderAndFooter)

    # Move buffer to initial position
    buffer.seek(0)

    # Certificate the output report
    certificatedReportZip = certification.CertificateReportAndZipFiles(udid, buffer.getvalue(), globalConstants.BlockedContactsReport)

    # Return generated file
    return certificatedReportZip