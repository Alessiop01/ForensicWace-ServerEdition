from flask import Flask, render_template, request, redirect, url_for

import os

import extraction
import utils


app = Flask(__name__ , static_folder='assets')

# Folders name variables
deviceExtractions_FOLDER = 'deviceExtractions'
assetsImage_FOLDER = 'assets/img'

defaultDatabase_PATH = '/7c/7c7fba66680ef796b916b067077cc246adacf01d'   # SQLite Database file is called by default '7c7fba66680ef796b916b067077cc246adacf01d' and it is stored under the '7c' folder inside the device backup

# Configure each folder into the app
app.config['deviceExtractions_FOLDER'] = deviceExtractions_FOLDER
app.config['assetsImage_FOLDER'] = assetsImage_FOLDER

# Dictionary to store all the variables and data for each connected host
hostsData = {}

# region Host Data Management
def AddOrUpdateHostData(hostId, data):
    """Creates or updates data for the host based on host Id.
    If host Id is NOT in the list then ADDs it to the list.
    If the host Id IS already in the list then UPDATE its values."""
    if hostId in hostsData:
        hostsData[hostId].update(data)
    else:
        hostsData[hostId] = data

def RemoveHostData(hostId):
    """Deletes all the data for the host based on host Id."""
    if hostId in hostsData:
        del(hostsData[hostId])
# endregion

# region  Route Definitions

# Homepage
@app.route('/')
def Index():
    # Retrieve remote host Id
    clientId = request.remote_addr

    if clientId not in hostsData:
        availableDeviceExtractionList = extraction.GetDeviceExtractionList(app.config['deviceExtractions_FOLDER'])
        return render_template('index.html',
                               availableDeviceExtractionList=availableDeviceExtractionList,
                               numberOfAvailableDevicesExtractions=len(availableDeviceExtractionList),
                               url_for=url_for
                               )
    else:
        databasePath = deviceExtractions_FOLDER + "/" + hostsData[clientId]['udid'] + defaultDatabase_PATH

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

# /Choose extracted device udid
@app.route('/ChooseExtraction')
def ChooseExtraction():
    clientId = request.remote_addr
    AddOrUpdateHostData(clientId, {"udid": request.args.get('udid')})
    AddOrUpdateHostData(clientId, {"name": request.args.get('name')})
    AddOrUpdateHostData(clientId, {"ios": request.args.get('ios')})
    return redirect(url_for('Index'))

# Upload Logo
@app.route('/ChangeLogo', methods=['GET', 'POST'])
def ChangeLogo():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Create the file path and name
            filename = os.path.join(app.config['assetsImage_FOLDER'], 'Logo.png')
            # Save the received file in the Assets folder for images
            file.save(filename)
    return render_template('ChangeLogo.html')

# Exit
@app.route('/Exit')
def Exit():
    # Retrieve remote host Id
    clientId = request.remote_addr

    # Delete all data related to the remote host
    RemoveHostData(clientId)

    return redirect(url_for('Index'))

#endregion

def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    main()
