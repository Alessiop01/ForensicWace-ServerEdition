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


def PrivateChatReport(udid, phoneNumber, extractedData):

    # Define pages margins
    left_margin = 50
    right_margin = 50
    bottom_margin = 100
    top_margin = 100

    buffer = BytesIO()

    # Configure the document
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Create the canvas for the report
    c = canvas.Canvas(buffer, pagesize=A4)

    # Get starting positions to start writing
    x_offset = left_margin
    y_offset = c._pagesize[1] - top_margin

    # Define message box characteristics
    message_box_height = 40
    message_box_radius = 20

    # Define colors to use
    message_box_color_green = HexColor('#DCF8C6')
    message_box_color_blue = HexColor('#C6E9F9')
    message_box_text_color = HexColor('#000000')

    # Set line height
    line_height = 30

    # Insert logo and page number on the first page
    c.drawImage(basePath + "/assets/img/Logo.png", A4[0] / 2 - 150, A4[1] - 65, width=300, height=52.5)
    page_num = c.getPageNumber()
    text = "Page %s" % page_num
    c.drawCentredString(105 * mm, 20 * mm, text)
    c.line(15 * mm, 25 * mm, 195 * mm, 25 * mm)

    previousSender = globalConstants.NotAssigned

    for chat in extractedData:

        # Check if the point where to write is inside the bottom margin
        # If YES save the ended page and update the position
        if y_offset < bottom_margin:
            c.showPage()
            y_offset = c._pagesize[1] - top_margin

            # Insert logo and page number on the page
            c.drawImage(basePath + "/assets/img/Logo.png", A4[0] / 2 - 150, A4[1] - 65, width=300, height=52.5)
            page_num = c.getPageNumber()
            text = "Page %s" % page_num
            c.drawCentredString(105 * mm, 20 * mm, text)
            c.line(15 * mm, 25 * mm, 195 * mm, 25 * mm)

        message_text = chat['text']
        message_width = 0
        if chat['ZMESSAGETYPE'] == 0:
            message_width = c.stringWidth(message_text, 'Helvetica', 12)

        message_box_width = message_width + 40
        message_box_height = 40

        mediaType = -1
        if chat['ZMESSAGETYPE'] == 1:
            mediaType = 1
        elif chat['ZMESSAGETYPE'] == 2:
            mediaType = 2
            message_width = c.stringWidth(utils.ConvertSeconds(chat['duration']), 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 3:
            mediaType = 3
            message_width = c.stringWidth(utils.ConvertSeconds(chat['duration']), 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 4:
            mediaType = 4
            message_width = c.stringWidth(chat["ZPARTNERNAME"], 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 5:
            mediaType = 5
            message_width = c.stringWidth(str(chat['latitude']) + " , " + str(chat["longitude"]), 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 6:
            mediaType = 6
        elif chat['ZMESSAGETYPE'] == 7:
            mediaType = 7
        elif chat['ZMESSAGETYPE'] == 8:
            mediaType = 8
            if chat['text'] != 'None':
                message_width = c.stringWidth(chat['text'], 'Helvetica', 12)
                message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 11:  # GIF ID
            mediaType = 11
            message_width = c.stringWidth("GIF", 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 14:
            mediaType = 14
            message_width = c.stringWidth(globalConstants.DeletedMessageInChatReport, 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 15:  # Sticker ID
            mediaType = 15
            message_width = c.stringWidth("Sticker", 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 38:  # Foto 1 time view
            mediaType = 38
            message_width = c.stringWidth("Image", 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 39:  # Video 1 vtime iew
            mediaType = 39
            message_width = c.stringWidth(utils.ConvertSeconds(chat['duration']), 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 46:
            mediaType = 46
            message_width = c.stringWidth("Poll", 'Helvetica', 12)
            message_box_width = message_width + 52
        elif chat['ZMESSAGETYPE'] == 0:
            mediaType = 0  # Just a text message

        # Check if the box exceeds the margin
        # If NO then set the box dimensions
        if message_box_width > c._pagesize[0] - right_margin - left_margin:
            message_box_width = c._pagesize[0] - right_margin - left_margin

        # Check who wrote the message, then set the right color, user name and phone number
        if previousSender != chat['user']:
            if chat['user'] is not None:
                c.setFillColor(message_box_color_blue)
                c.drawString(x_offset, y_offset, chat['ZPARTNERNAME'] + " - " + "(" + utils.FormatPhoneNumberForPageTables(chat['user']) + ")")
                y_offset -= 50
            else:
                c.setFillColor(message_box_color_green)
                c.drawString(x_offset, y_offset, globalConstants.DatabaseOwner)
                y_offset -= 50
        else:
            y_offset -= 30

        # Split the text on multiple rows
        lines = []
        line = ''
        if chat['ZMESSAGETYPE'] == 0:
            words = chat['text'].split()
            for word in words:
                if len(line + word) > 85:
                    lines.append(line)
                    line = word + ' '
                    message_box_height += 18
                    y_offset -= 18
                else:
                    line += word + ' '
            lines.append(line)

        num_lines = len(lines)

        # Check if the point where to write is inside the bottom margin
        # If YES save the ended page and update the position
        if y_offset < bottom_margin:
            c.showPage()
            y_offset = c._pagesize[1] - top_margin - num_lines * 35

            # Inserimento logo e numero di pagina sulla pagina
            c.drawImage(basePath + "/assets/img/Logo.png", A4[0] / 2 - 150, A4[1] - 65, width=300, height=52.5)
            page_num = c.getPageNumber()
            text = "Page %s" % page_num
            c.drawCentredString(105 * mm, 20 * mm, text)
            c.line(15 * mm, 25 * mm, 195 * mm, 25 * mm)

        # Set the right color and design the rectangle
        c.setFillColor(message_box_color_blue if chat['user'] is not None else message_box_color_green)
        c.roundRect(x_offset, y_offset, message_box_width, message_box_height, message_box_radius, stroke=0, fill=1)
        c.setFillColor(message_box_text_color)

        if mediaType == 1:
            c.drawImage(basePath + "/assets/img/icons/CameraNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/CameraUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            y_offset -= 16
        elif mediaType == 2:
            c.drawImage(basePath + "/assets/img/icons/VideoNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/VideoUser.png",
                x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, utils.ConvertSeconds(chat['duration']))
            y_offset -= 16
        elif mediaType == 3:
            c.drawImage(basePath + "/assets/img/icons/MicNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/MicUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, utils.ConvertSeconds(chat['duration']))
            y_offset -= 16
        elif mediaType == 4:
            c.drawImage(basePath + "/assets/img/icons/ContactNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/ContactUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, chat["ZPARTNERNAME"])
            y_offset -= 16
        elif mediaType == 5:
            c.drawImage(basePath + "/assets/img/icons/PositionNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/PositionUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6,
                         str(chat['latitude']) + " , " + str(chat['longitude']))
            y_offset -= 16
        elif mediaType == 6:
            c.drawImage( basePath + "/assets/img/icons/GroupNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/GroupUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            y_offset -= 16
        elif mediaType == 7:
            c.drawImage(basePath + "/assets/img/icons/LinkNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/LinkUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            y_offset -= 16
        elif mediaType == 8:
            c.drawImage(basePath + "/assets/img/icons/DocNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/DocUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            if chat["text"] != 'None':
                c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, chat['text'])
            y_offset -= 16
        elif mediaType == 11:
            c.drawImage(basePath + "/assets/img/icons/GifNum.png" if chat['user'] == 'Database owner' else basePath + "/assets/img/icons/GifUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, "GIF")
            y_offset -= 16
        elif mediaType == 14:
            c.drawImage(basePath + "/assets/img/icons/BinNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/BinUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, globalConstants.DeletedMessageInChatReport)
            y_offset -= 16
        elif mediaType == 15:
            c.drawImage(basePath + "/assets/img/icons/StickerNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/StickerUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, "Sticker")
            y_offset -= 16
        elif mediaType == 38:
            c.drawImage(basePath + "/assets/img/icons/OneTimeNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/OneTimeUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, "Image")
            y_offset -= 16
        elif mediaType == 39:
            c.drawImage(basePath + "/assets/img/icons/OneTimeNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/OneTimeUser.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, utils.ConvertSeconds(chat['duration']))
            y_offset -= 16
        elif mediaType == 46:
            c.drawImage(basePath + "/assets/img/icons/PollNum.png" if chat['user'] is not None else basePath + "/assets/img/icons/PollUSer.png", x_offset + 14, y_offset + message_box_height / 2 - 7, width=12, height=12)
            mediaType = -1
            c.drawString(x_offset + 32, y_offset + message_box_height / 2 - 6, "Poll")
            y_offset -= 16

        # Check if the number of lines is >= 2
        # If YES them update the Y coordinate
        if num_lines >= 2:
            y_offset += message_box_height / 2 - 20

        # Print the message into the box
        for line in lines:
            c.drawString(x_offset + 20, y_offset + message_box_height / 2 - 6, line)
            y_offset -= 16

        if chat['user'] is None:
            c.setFont("Helvetica", 8)
            c.drawString(x_offset, y_offset, "Send date: " + utils.GetSentDateTime(chat['dateTimeInfos']))
            y_offset -= 12
            c.drawString(x_offset, y_offset, "Reading date: " + utils.GetReadDateTime(chat['dateTimeInfos']))
        else:
            c.setFont("Helvetica", 8)
            c.drawString(x_offset, y_offset, "Send date: " + chat['receiveDateTime'] + " UTC")

        y_offset -= 26
        c.setFont("Helvetica", 12)

        previousSender = chat['user']

    print("prima di c.save()")
    # Save the PDF file
    c.save()
    print("prima di doc.build(c, onFirstPage=CreateVerticalDocHeaderAndFooter, onLaterPages=CreateVerticalDocHeaderAndFooter)")
    # Build the output PDF file
    #doc.build(c, onFirstPage=CreateVerticalDocHeaderAndFooter, onLaterPages=CreateVerticalDocHeaderAndFooter)
    print("prima di buffer.seek(0)")
    # Move buffer to initial position
    buffer.seek(0)

    # Certificate the output report
    certificatedReportZip = certification.CertificateReportAndZipFiles(udid, buffer.getvalue(),
                                                                       globalConstants.PrivateChat, phoneNumber)

    buffer.close()

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


def ExportGroupList(udid, extractedDataList):

    # Define data structure
    data = [["GroupName", "LastMessage", "NumberOfMessages", "NotificationStatus"]]

    # Foreach extracted data, add it into the previous defined structure
    for extractedData in extractedDataList:
        groupNotificationStatus = globalConstants.Enabled

        # If the field contains a value, then the group has been muted
        if extractedData["Is_muted"] is not None:
            groupNotificationStatus = globalConstants.Disabled

        data.append([extractedData["Group_Name"],
                     extractedData["Message_Date"],
                     extractedData["Number_of_Messages"],
                     groupNotificationStatus])

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
    certificatedReportZip = certification.CertificateReportAndZipFiles(udid, buffer.getvalue(), globalConstants.GroupListReport)

    # Return generated file
    return certificatedReportZip