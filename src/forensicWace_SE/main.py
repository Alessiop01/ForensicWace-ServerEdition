from flask import Flask, render_template, request, redirect, url_for, send_file

import os
import tempfile

# Import Custom Modules
import forensicWace_SE.extraction as extraction
import forensicWace_SE.utils as utils
import forensicWace_SE.globalConstants as globalConstants
import forensicWace_SE.reporting as reporting

app = Flask(__name__, static_folder='/')

# Retrieve base Path
basePath = os.path.dirname(os.path.abspath(__file__))

# Configure each folder into the app
app.config['deviceExtractions_FOLDER'] = os.path.join(basePath, globalConstants.deviceExtractions_FOLDER)
app.config['assetsImage_FOLDER'] = os.path.join(basePath, globalConstants.assetsImage_FOLDER)
app.config['systemTMP_FOLDER'] = tempfile.gettempdir()

# Dictionary to store all the variables and data for each connected host
hostsData = {}


# region Host Data Management
def AddOrUpdateHostData(hostId, data):
    """Creates or updates data for the host based on hostId.
    If hostId is NOT in the list then ADDs it to the list.
    If the hostId IS already in the list then UPDATE its values."""
    if hostId in hostsData:
        hostsData[hostId].update(data)
    else:
        hostsData[hostId] = data


def RemoveHostData(hostId):
    """Deletes all the data for the host based on hostId."""
    if hostId in hostsData:
        del (hostsData[hostId])
# endregion

# region  Route Definitions


# region / (index)
@app.route('/')
def Index():
    """Defines the logic for the index page.
    If the hostId is NOT in the list then shows the page to select the device extraction to be used.
    If the hostId IS already in the list then shows the page to select the functionality to be used."""

    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        availableDeviceExtractionList = extraction.GetDeviceExtractionList(app.config['deviceExtractions_FOLDER'])
        return render_template('index.html',
                               availableDeviceExtractionList=availableDeviceExtractionList,
                               numberOfAvailableDevicesExtractions=len(availableDeviceExtractionList),
                               url_for=url_for
                               )
    else:
        databasePath = basePath + "/" + globalConstants.deviceExtractions_FOLDER + "/" + hostsData[clientId]['udid'] + globalConstants.defaultDatabase_PATH

        databaseSHA256 = utils.CalculateSHA256(databasePath)
        databaseMD5 = utils.CalculateMD5(databasePath)
        databaseSize = round(utils.GetFileSize(databasePath), 1)

        return render_template('homepage.html',
                               udid=hostsData[clientId]['udid'],
                               name=hostsData[clientId]['name'],
                               ios=hostsData[clientId]['ios'],
                               databaseSHA256=databaseSHA256,
                               databaseMD5=databaseMD5,
                               databaseSize=databaseSize
                               )
# endregion


# region ChooseExtraction
@app.route('/ChooseExtraction')
def ChooseExtraction():
    """Adds the information about the selected extracted backup to the system dictionary for the hostId."""
    clientId = request.remote_addr
    AddOrUpdateHostData(clientId, {"udid": request.args.get('udid')})
    AddOrUpdateHostData(clientId, {"name": request.args.get('name')})
    AddOrUpdateHostData(clientId, {"ios": request.args.get('ios')})
    AddOrUpdateHostData(clientId, {"messageType": "All"})
    return redirect(url_for('Index'))
# endregion


# region ChangeLogo
@app.route('/ChangeLogo', methods=['GET', 'POST'])
def ChangeLogo():
    """Shows the page to upload a new logo for the tool.
    If called in a POST call, gets the logo uploaded by the user and saves it as png file."""
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Create the file path and name
            filename = os.path.join(app.config['assetsImage_FOLDER'], 'Logo.png')
            # Save the received file in the Assets folder for images
            file.save(filename)
    return render_template('changeLogo.html')
# endregion


# region Exit
@app.route('/Exit')
def Exit():
    """Redirect the user to the index page to select a new backup extraction.
    Deletes all the data related to the hostId."""
    # Retrieve remote hostId
    clientId = request.remote_addr

    # Delete all data related to the remote host
    RemoveHostData(clientId)

    return redirect(url_for('Index'))
# endregion


# region ChatList
@app.route('/ChatList')
def ChatList():
    errorMsg = None

    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    if clientId in hostsData and 'chatListData' in hostsData[clientId]:
        chatListData = hostsData[clientId]['chatListData']
    else:
        chatListData, errorMsg = extraction.GetChatList(basePath, hostsData[clientId]['udid'])
        AddOrUpdateHostData(clientId, {"chatListData": chatListData})

    if errorMsg:
        return render_template('chatList.html',
                               errorMsg=errorMsg,
                               chatListData=None,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)
    else:
        return render_template('chatList.html',
                               errorMsg=errorMsg,
                               chatListData=chatListData,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)

@app.route('/ExportChatList')
def ExportChatList():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    if clientId in hostsData and 'chatListData' in hostsData[clientId]:
        chatListData = hostsData[clientId]['chatListData']
    else:
        chatListData, errorMsg = extraction.GetChatList(basePath, hostsData[clientId]['udid'])
        AddOrUpdateHostData(clientId, {"chatListData": chatListData})

    generatedReportZip = reporting.ExportChatList(hostsData[clientId]['udid'], chatListData)

    return send_file(generatedReportZip, as_attachment=True)
# endregion


# region InsertPhoneNumber
@app.route('/InsertPhoneNumber')
def InsertPhoneNumber():
    return render_template('insertPhoneNumber.html')
# endregion


# region PrivateChat
@app.route('/PrivateChat', methods=['POST'])
def PrivateChat():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))
    else:
        deviceUdid = hostsData[clientId]['udid']

        phoneNumber = request.form['phoneNumber']
        retrievedMessageType = request.form['messageType']
        messageType = 0

        if request.form['phoneNumber'] is None or request.form['phoneNumber'] == '':
            return render_template('insertPhoneNumber.html', errorMsg=globalConstants.invalidPhoneNumberErrorMsg)

        # Convert retrieved messageType from string to integer if is a number
        if retrievedMessageType != -1:
            if retrievedMessageType.isdigit():
                messageType = int(retrievedMessageType)

        chatCounters, messages, errorMsg = extraction.GetPrivateChat(basePath, hostsData[clientId]['udid'], phoneNumber[-10:])  # phoneNumber[-10:] --> Pass the last 10 characters inserted

        userProfilePicPath = extraction.GetMediaFromBackup(basePath, deviceUdid, phoneNumber[-10:], False, True)
        dbOwnerProfilePicPath = extraction.GetMediaFromBackup(basePath, deviceUdid, 'Photo', False, True)

        warningFilteredMsg = None

        # Filter messages to view on the page
        if messageType is not None and messageType == globalConstants.imageMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.imageMediaType or m['ZMESSAGETYPE'] == globalConstants.oneTimeImageMediaType]     # Images
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "IMAGES"
        elif messageType is not None and messageType == globalConstants.videoMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.videoMediaType or m['ZMESSAGETYPE'] == globalConstants.oneTimeVideoMediaType]     # Video
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "VIDEOS"
        elif messageType is not None and messageType == globalConstants.audioMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.audioMediaType]  # Audio
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "AUDIOS"
        elif messageType is not None and messageType == globalConstants.contactMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.contactMediaType]  # Contact
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "CONTACTS"
        elif messageType is not None and messageType == globalConstants.positionMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.positionMediaType]  # Position
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "POSITIONS"
        elif messageType is not None and messageType == globalConstants.urlMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.urlMediaType]  # URLs
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "URLS"
        elif messageType is not None and messageType == globalConstants.fileMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.fileMediaType]  # File
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "FILES"
        elif messageType is not None and messageType == globalConstants.gifMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.gifMediaType]  # Gif
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "GIFS"
        elif messageType is not None and messageType == globalConstants.stickerMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.stickerMediaType]  # Sticker
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "STICKERS"

        if phoneNumber == globalConstants.invalidPhoneNumber:
            return render_template('insertPhoneNumber.html',
                                   errorMsg=globalConstants.invalidPhoneNumberErrorMsg)
        else:
            return render_template('privateChat.html',
                                   phoneNumber=utils.FormatPhoneNumber(phoneNumber),
                                   unformattedPhoneNumber=phoneNumber,
                                   chatCounters=chatCounters,
                                   messages=messages,
                                   GetSentDateTime=utils.GetSentDateTime,
                                   GetReadDateTime=utils.GetReadDateTime,
                                   deviceUdid=deviceUdid,
                                   GetMediaFromBackup=extraction.GetMediaFromBackup,
                                   userProfilePicPath=userProfilePicPath,
                                   dbOwnerProfilePicPath=dbOwnerProfilePicPath,
                                   str=str,
                                   imageMediaType=globalConstants.imageMediaType,
                                   videoMediaType=globalConstants.videoMediaType,
                                   audioMediaType=globalConstants.audioMediaType,
                                   contactMediaType=globalConstants.contactMediaType,
                                   positionMediaType=globalConstants.positionMediaType,
                                   stickerMediaType=globalConstants.stickerMediaType,
                                   urlMediaType=globalConstants.urlMediaType,
                                   fileMediaType=globalConstants.fileMediaType,
                                   warningFilteredMsg=warningFilteredMsg,
                                   VcardTelExtractor = utils.VcardTelExtractor,
                                   basePath = basePath
                                   )


@app.route('/ExportPrivateChat', methods=['POST'])
def ExportPrivateChat():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))
    else:
        deviceUdid = hostsData[clientId]['udid']

        phoneNumber = request.form['phoneNumber']

    if request.form['phoneNumber'] is None or request.form['phoneNumber'] == '':
        return render_template('insertPhoneNumber.html', errorMsg=globalConstants.invalidPhoneNumberErrorMsg)

    chatCounters, messages, errorMsg = extraction.GetPrivateChat(basePath, deviceUdid, phoneNumber[-10:])  # phoneNumber[-10:] --> Pass the last 10 characters inserted

    generatedReportZip = reporting.PrivateChatReport(deviceUdid, phoneNumber, messages)

    return send_file(generatedReportZip, as_attachment=True)
# endregion


# region GpsLocations
@app.route('/GpsLocations')
def GpsLocations():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    gpsData, errorMsg = extraction.GetGpsData(basePath, hostsData[clientId]['udid'])

    if errorMsg:
        return render_template('gpsLocations.html',
                               errorMsg=errorMsg,
                               gpsData=None,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)
    else:
        return render_template('gpsLocations.html',
                               errorMsg=errorMsg,
                               gpsData=gpsData,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)

@app.route('/ExportGpsLocations')
def ExportGpsLocations():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    gpsData, errorMsg = extraction.GetGpsData(basePath, hostsData[clientId]['udid'])

    generatedReportZip = reporting.ExportGpsLocations(hostsData[clientId]['udid'], gpsData)

    return send_file(generatedReportZip, as_attachment=True)
    
# endregion


# region BlockedContacts
@app.route('/BlockedContacts')
def BlockedContacts():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    blockedContactsData, errorMsg = extraction.GetBlockedContacts(basePath, hostsData[clientId]['udid'])

    if errorMsg:
        return render_template('blockedContacts.html',
                               errorMsg=errorMsg,
                               blockedContactsData=None,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)
    else:
        return render_template('blockedContacts.html',
                               errorMsg=errorMsg,
                               blockedContactsData=blockedContactsData,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)

@app.route('/ExportBlockedContacts')
def ExportBlockedContacts():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    blockedContactsData, errorMsg = extraction.GetBlockedContacts(basePath, hostsData[clientId]['udid'])

    generatedReportZip = reporting.ExportBlockedContactsReport(hostsData[clientId]['udid'], blockedContactsData)

    return send_file(generatedReportZip, as_attachment=True)
# endregion


# region GroupList
@app.route('/GroupList')
def GroupList():
    errorMsg = None

    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    if clientId in hostsData and 'groupListData' in hostsData[clientId]:
        groupListData = hostsData[clientId]['groupListData']
    else:
        groupListData, errorMsg = extraction.GetGroupList(basePath, hostsData[clientId]['udid'])
        AddOrUpdateHostData(clientId, {"groupListData": groupListData})

    if errorMsg is not None:
        return render_template('groupList.html',
                               errorMsg=errorMsg,
                               groupListData=None,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)
    else:
        return render_template('groupList.html',
                               errorMsg=errorMsg,
                               groupListData=groupListData,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)

@app.route('/ExportGroupList')
def ExportGroupList():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    if clientId in hostsData and 'groupListData' in hostsData[clientId]:
        groupListData = hostsData[clientId]['groupListData']

    else:
        groupListData, errorMsg = extraction.GetGroupList(basePath, hostsData[clientId]['udid'])
        AddOrUpdateHostData(clientId, {"groupListData": groupListData})

    generatedReportZip = reporting.ExportGroupList(hostsData[clientId]['udid'], groupListData)

    return send_file(generatedReportZip, as_attachment=True)
# endregion


# region SelectGroup
@app.route('/SelectGroup')
def SelectGroup():
    errorMsg = None

    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))

    if clientId in hostsData and 'groupListData' in hostsData[clientId]:
        groupListData = hostsData[clientId]['groupListData']
    else:
        groupListData, errorMsg = extraction.GetGroupList(basePath, hostsData[clientId]['udid'])
        AddOrUpdateHostData(clientId, {"groupListData": groupListData})

    if errorMsg:
        return render_template('selectGroup.html',
                               errorMsg=errorMsg,
                               groupListData=None,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)
    else:
        return render_template('selectGroup.html',
                               errorMsg=errorMsg,
                               groupListData=groupListData,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables)
# endregion


# region GroupChat
@app.route('/GroupChat', methods=['POST'])
def GroupChat():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))
    else:
        deviceUdid = hostsData[clientId]['udid']

        groupName = request.form['groupName']
        retrievedMessageType = request.form['messageType']
        messageType = 0

        # Convert retrieved messageType from string to integer in is a number
        if retrievedMessageType.isdigit():
            messageType = int(retrievedMessageType)

        chatCounters, messages, errorMsg = extraction.GetGroupChat(basePath, hostsData[clientId]['udid'], groupName)

        dbOwnerProfilePicPath = extraction.GetMediaFromBackup(basePath, deviceUdid, 'Photo', False, True)

        warningFilteredMsg = None

        # Filter messages to view on the page
        if messageType is not None and messageType == globalConstants.imageMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.imageMediaType or m['ZMESSAGETYPE'] == globalConstants.oneTimeImageMediaType]     # Images
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "IMAGES"
        elif messageType is not None and messageType == globalConstants.videoMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.videoMediaType or m['ZMESSAGETYPE'] == globalConstants.oneTimeVideoMediaType]     # Video
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "VIDEOS"
        elif messageType is not None and messageType == globalConstants.audioMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.audioMediaType]  # Audio
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "AUDIOS"
        elif messageType is not None and messageType == globalConstants.contactMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.contactMediaType]  # Contact
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "CONTACTS"
        elif messageType is not None and messageType == globalConstants.positionMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.positionMediaType]  # Position
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "POSITIONS"
        elif messageType is not None and messageType == globalConstants.urlMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.urlMediaType]  # URLs
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "URLS"
        elif messageType is not None and messageType == globalConstants.fileMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.fileMediaType]  # File
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "FILES"
        elif messageType is not None and messageType == globalConstants.gifMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.gifMediaType]  # Gif
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "GIFS"
        elif messageType is not None and messageType == globalConstants.stickerMediaType:
            messages = [m for m in messages if m['ZMESSAGETYPE'] == globalConstants.stickerMediaType]  # Sticker
            warningFilteredMsg = globalConstants.chatFilterBaseMessage + "STICKERS"

        return render_template('groupChat.html',
                               groupName=groupName,
                               chatCounters=chatCounters,
                               messages=messages,
                               GetSentDateTime=utils.GetSentDateTime,
                               GetReadDateTime=utils.GetReadDateTime,
                               deviceUdid=deviceUdid,
                               GetMediaFromBackup=extraction.GetMediaFromBackup,
                               dbOwnerProfilePicPath=dbOwnerProfilePicPath,
                               str=str,
                               imageMediaType=globalConstants.imageMediaType,
                               videoMediaType=globalConstants.videoMediaType,
                               audioMediaType=globalConstants.audioMediaType,
                               contactMediaType=globalConstants.contactMediaType,
                               positionMediaType=globalConstants.positionMediaType,
                               stickerMediaType=globalConstants.stickerMediaType,
                               urlMediaType=globalConstants.urlMediaType,
                               fileMediaType=globalConstants.fileMediaType,
                               warningFilteredMsg=warningFilteredMsg,
                               formatPhoneNumber=utils.FormatPhoneNumberForPageTables,
                               vcardTelExtractor=utils.VcardTelExtractor,
                               basePath = basePath
                               )


@app.route('/ExportGroupChat', methods=['POST'])
def ExportGroupChat():
    # Retrieve remote hostId
    clientId = request.remote_addr

    if clientId not in hostsData:
        return redirect(url_for('Index'))
    else:
        deviceUdid = hostsData[clientId]['udid']
        groupName = request.form['groupName']

    if request.form['groupName'] is None or request.form['groupName'] == '':
        return render_template('selectGroup.html')

    chatCounters, messages, errorMsg = extraction.GetGroupChat(basePath, deviceUdid, groupName)

    generatedReportZip = reporting.GroupChatReport(deviceUdid, groupName, messages)

    return send_file(generatedReportZip, as_attachment=True)

# endregion


# region CheckReport
@app.route('/CheckReport', methods=['GET', 'POST'])
def CheckReport():
    reportStatus = 0

    if request.method == 'POST':
        report = request.files['report']
        if report:
            # Create the file path and name
            reportPath = os.path.join(app.config['systemTMP_FOLDER'], report.filename)
            # Save the received file in the system TMP folder
            report.save(reportPath)
        else:
            return render_template('checkReport.html',
                                   reportStatus=None,
                                   errorMessage = globalConstants.missingReport)

        certificate = request.files['certificate']
        if certificate:
            # Create the file path and name
            certificatePath = os.path.join(app.config['systemTMP_FOLDER'], certificate.filename)
            # Save the received file in the system TMP folder
            certificate.save(certificatePath)
        else:
            return render_template('checkReport.html',
                                   reportStatus=None,
                                   errorMessage=globalConstants.missingCertificate)

        reportStatus = reporting.ReportCheckAuth(reportPath, certificatePath)

        os.remove(reportPath)
        os.remove(certificatePath)

    return render_template('checkReport.html',
                           reportStatus=reportStatus,
                           errorMessage = None)
# endregion


# region DiscoverMore
@app.route('/DiscoverMore')
def DiscoverMore():
    return render_template('discoverMore.html')
# endregion

# endregion

def main():
    """Defines the main function of the application."""
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    main()
