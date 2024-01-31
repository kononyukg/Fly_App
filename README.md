
# Fly_App

The project helps to optimize the search for direct flights. Finds the cheapest round-trip flight in about the next four months.

## About

Using the interface, the user enters the city of departure and arrival and the approximate number of days he plans to stay there.
There are windows in the interface that show the history of search results, the current search and the result of the current search. The user can also send himself an SMS with the flight data and can also send himself an email with a link to booking this flight. Also, all successful search results are saved in Google Sheet.

## Getting Started

### Prerequisites

* python 3.10

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/kononyukg/Fly_Alert
   ```
2. Install packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create `.env` file
4. Create yuor own copy of Google Sheet [https://docs.google.com/spreadsheets/d/11o28YvPz-ZTiCqc_R869qUAu0uhL_uyK6b4M8ZzTnCY/edit#gid=0](https://docs.google.com/spreadsheets/d/11o28YvPz-ZTiCqc_R869qUAu0uhL_uyK6b4M8ZzTnCY/edit#gid=0)
   * Connect Google Sheet with Sheety API at [https://sheety.co/](https://sheety.co/), it is important to use the same Google account
   * In Sheety API create new project and enable the GET, POST and PUT options
   * Copy endpoint
  ```js
   SHEET_ENDPOINT =
   ```
5. Get a free API Key at [https://tequila.kiwi.com/portal/login](https://tequila.kiwi.com/portal/login)
   * Register with the Kiwi Partners Flight Search API
   * Create your "Solution"
   * When registering for your API key choose Meta Search as your product type
   * Then choose One-Way and Return
   * Click on create
   * If the website prompts you for the type of partnership you can either choose any of them
   * Copy Api key
   ```js
   API_KEY =
   ```
6. Sing up for free at [https://www.twilio.com/en-us](https://www.twilio.com/en-us)
   * Get started for free
   * Sing up to get a free Twilio account
   * Confirm your email and phone number
   * Then answer a few questions
   * "...write code?" -> Yes
   * "...language?" -> PYTHON
   * "...goal today?" -> Use Twilio in a project
   * "...to do first?" -> Send or receive SMS
   * Get a Trial Number
   * Copy constants
   ```js
   ACCOUNT_SID =
   AUTH_TOKEN =
   TWILIO_PHONE_NUMBER =
   YOUR_PHONE_NUMBER =
   ```
7. Google Account 
   * Go to your Google Account and choose Security on the left panel
   * On the Signing in to Google tab, select App Passwords
   * Click on Select app and pick Other, then named it 
   * Click Select device and choose the Windows Computer
   * Click on Generate
   * Password is the 16-character code in the yellow bar on your device
   * Copy password and your email
    ```js
   YOUR_EMAIL_SMTP =
   YOUR_PASSWORD_SMTP =
   ```
8. URL of your Google Sheet
   * Copy paste Url of your Google Sheet 
   ```js
   YOUR_SHEET_URL =
   ```
9. Enter your constant in `.env` file
10. Run APP
    * Run FlyApp.exe
    * or
    ```sh
    cd .\fly_app
    ```
    ```sh
    python .\main.py
    ```
## Usage
1. Enter Departure city, Destination city and Days on the Trip
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/menu.png)
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/pop_up.png)
2. Press "ADD Data"
   * The entered data will appear in the "New search request" 
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/add.png)
3. Press "Let's search"
   * Result data will appear in the "Search result"
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/result.png)
4. Now you can send an SMS with the data
   * You can send data only to your phone number, because Twilio account is free
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/sms.jpg)
5. Also you can send an email with the data and booking link, only Gmail
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/warning.png)
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/link.png)
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/link_result.png)
6. Press "Open Sheet"
   ![alt text](https://github.com/kononyukg/Fly_App/blob/master/fly_app/img_read/sheet.png)
7. Also you can check prices awery day automatically
   * Sing in at [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
   * Upload Files 
   ```sh
   auto_check.py
   google_sheet_data.py
   message_manager.py
   search_flight_data.py
   ```
   * In this files delite "import os", "from dotenv import load_dotenv" and "load_dotenv()"
   * Then put the values of the constants insted of "os.environ.get(...)"
   * Create new console
   * Create new Task, set a time and take the command from below
   ```sh
   python3 auto_check.py
   ```
