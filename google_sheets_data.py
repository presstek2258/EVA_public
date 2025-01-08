import gspread
from google.oauth2.service_account import Credentials

from speech import TTS


class GoogleData:

    spreadsheet = []

    def __init__(self) -> None:

        data_fetched = False
        for check_num in range(10):  # tries to fetch the data multiple times
            try:

                # this is the defualt url that link to the google sheets api
                scopes_to_use = ["https://www.googleapis.com/auth/spreadsheets"]

                # this creates credentials creds which uses the creds.json for the api key
                # and scopes_to_use to connect to google sheets
                creds = Credentials.from_service_account_file(
                    "creds.json", scopes=scopes_to_use
                )

                # this authorizes our credentials creds (gc = google client)
                gc = gspread.authorize(creds)

                # now we need the id of the google sheet that we want to access
                # this is found as a chunk of the sheets url between /d/ and /edit
                sheet_id = "put sheet id here"

                self.spreadsheet = gc.open_by_key(sheet_id)

                # if successful fetched sheet exit the function
                data_fetched = True
                break

            except Exception as ex:
                # TODO   change the below to label print instead of console
                print(f"Error: could not get/open google spreadsheet data\n{ex}")
                # tts for error catching
                tts = TTS()
                tts.speak(f"failed to fetch {check_num} times... retrying")

        # if the data could not be fetched
        if not data_fetched:
            tts.speak("fatal error. failed to fetch data from google... exiting")
            exit()

    def get_google_data(self):
        return self.spreadsheet.get_worksheet(0).get_all_values()
