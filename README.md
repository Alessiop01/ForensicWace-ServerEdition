# Forensic Wace

Welcome to the repository of Forensic Wace Server Edition, an upgrade of my Bachelor's thesis project in Computer Forensics. This project represents the result of my study focused on the extraction of chats and other informations contained inside the whatsapp database, extracted from Apple iOS devices.

![Logo.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FLogo.png)

## Installation

In order to start using the Forensic Wace Server Edition you need to install it.

To do this, open a terminal window as administrator and run the command below.

```bash
pip install git+https://github.com/Alessiop01/ForensicWace-ServerEdition
```

## Usage
To start the Forensic Wace GUI, execute the command below in any terminal window:

```python
forensic-wace-se
```

Once the command to start the tool has been run on the server machine on which it will run, a web browser is needed to access the GUI.
It is recommended to use Google Chrome as browser.

### Homepage BEFORE selecting Device backup
![Select Backup.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FSelect%20Backup.png)

### Homepage AFTER selecting Device backup
![Homepage.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FHomepage.png)

### Chat List page
Within this page, a table containing the list of extracted chats will be populated.
Only the chats that have a number of messages greater than 0 will be displayed since Whatsapp saves a conversation even by just opening the chat with a contact, even without having written any messages.
Inside the table will be shown:
- First and last name of the contact in the address book
- Username chosen by the contact when signing up for the platform
- Phone number of the contact
- Number of messages exchanged in the chat
- Date of the last message exchanged
- Button with a quick link to the chat

![Chat List.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FChat%20List.png)

### Select Phone Number page
Within this page the user should enter the phone number of the contact whose conversation is to be extracted. Once the input is completed he or she will have to click on the green button at the bottom of the keypad. The program will automatically redirect to the page that will show the conversation extraction.

![Select Phone Number.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FSelect%20Phone%20Number.png)

### Private Chat page
Inside this page some counters related to the chat will be shown in the upper boxes, and in the lower part the extracted chat will be shown.
By clicking on the boxes at the top you can filter the chat by taking advantage of various default filters.
To return to the original chat with all messages and all media just click on the “Total Messages” box.

![Private Chat.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FPrivate%20Chat.png)

### GPS Locations page
Within this page a table will be populated containing the list of GPS locations exchanged by and with the user who owns the database.
Within the table will be reported:
- Phone number/group name relative to the sender
- Phone number/group name relative to the recipient
- Date and time when the sending occurred
- Coordinates about the latitude
- Coordinates about the longitude
- Button with a quick link to the location on Google Maps platform.

In case the sender or recipient of the exchanged location should be the database owner, automatically the tool will display the string “Database Owner”.

![GPS Locations.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FGPS%20Locations.png)

### Blocked Contacts page
Within this page a table will be populated containing the list of contacts blocked by the user who owns the database.
Within the table will be shown:
- Username of the blocked user
- Phone number associated with the username

In case the username of the contact cannot be found within the database, automatically the tool will display the string “Name not available”.

![Blocked Contacts.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FBlocked%20Contacts.png)

### Group List page
A table containing the list of extracted group chats will be populated in this page.
Groups that have a number of messages equal to 0 will also be displayed.
Within the table will be shown:
- Name of the group
- Date of the last message exchanged
- Number of messages exchanged in the chat
- Status of notifications related to the group

![Group List.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FGroup%20List.png)

### Group Chat page
Inside this page some counters related to the chat will be shown in the upper boxes, and in the lower part the extracted chat will be shown.
By clicking on the boxes at the top you can filter the chat by taking advantage of various default filters.
To return to the original chat with all messages and all media just click on the “Total Messages” box.
For each received message, the name and phone number of the user who sent the message is also displayed.

![Group Chat.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FGroup%20Chat.png)

### Change Logo page
Through this page, users will be able to upload from their PCs an image that will become the tool's new logo.
In this way, it will be possible to change the logo shown on the generated reports

![Change Logo.png](src%2FforensicWace_SE%2Fassets%2Fimg%2FGitHub%20Screen%2FChange%20Logo.png)

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
