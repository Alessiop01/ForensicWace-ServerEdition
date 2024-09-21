import os
import rfc3161ng
import zipfile
import tempfile

import forensicWace_SE.utils as utils
import forensicWace_SE.globalConstants as globalConstants

basePath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

def CertificateReportAndZipFiles(udid, tempReport, reportTypeExtension, phoneNumber = None, groupName = None):
    tempDir = tempfile.gettempdir()

    if(reportTypeExtension == globalConstants.PrivateChat):
        reportName = udid + reportTypeExtension + phoneNumber + ".pdf"
        certificateName = udid + reportTypeExtension + phoneNumber + ".tsr"
    elif (reportTypeExtension == globalConstants.GroupChat):
        reportName = udid + reportTypeExtension + groupName + ".pdf"
        certificateName = udid + reportTypeExtension + groupName + ".tsr"
    else:
        reportName = udid + reportTypeExtension + ".pdf"
        certificateName = udid + reportTypeExtension + ".tsr"

    reportPath = os.path.join(tempDir, reportName)
    certificatePath = os.path.join(tempDir, certificateName)

    if (reportTypeExtension == globalConstants.PrivateChat):
        certificatedReportZipFileName = os.path.join(tempDir, udid + reportTypeExtension + phoneNumber + ".zip")
    elif (reportTypeExtension == globalConstants.GroupChat):
        certificatedReportZipFileName = os.path.join(tempDir, udid + reportTypeExtension + groupName + ".zip")
    else:
        certificatedReportZipFileName = os.path.join(tempDir, udid + reportTypeExtension + ".zip")


    filesToZip = [
        reportPath,
        certificatePath,
    ]

    # Remove files if already exist
    utils.DeleteFilesIfExist([certificatedReportZipFileName])

    # Save temporary the report
    with open(reportPath, "wb") as f:
        f.write(tempReport)
        print(f"Generated file: {reportPath}")

    certificate = open(basePath + "/assets/reportCertificate/tsa.crt", 'rb').read()

    # create the object
    rt = rfc3161ng.RemoteTimestamper("https://freetsa.org/tsr", certificate=certificate, hashname='sha256')

    # file to be certificated
    with open(reportPath, 'rb') as f:
        timestamp = rt.timestamp(data=f.read())

    with open(certificatePath, 'wb') as f:
        f.write(timestamp)
        print(f"Generated file: {certificatePath}")

    with zipfile.ZipFile(certificatedReportZipFileName, 'w') as zipf:
        for file in filesToZip:
            if os.path.isfile(file):
                zipf.write(file, os.path.basename(file))
        print(f"Generated file: {certificatedReportZipFileName}")

    # Remove generated files
    utils.DeleteFilesIfExist(filesToZip)

    return certificatedReportZipFileName