import googleapiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetOperator(object):
    spreadsheet_id: str

    def __init__(self, spreadsheet_id, credentials_file_name):
        self.spreadsheetId = spreadsheet_id
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file_name,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = googleapiclient.discovery.build('sheets', 'v4', http=self.httpAuth)

    def read_range(self, list_name, range_in_list, majorDimension='ROWS'):
        values = None
        try:
            values = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"\'{list_name}\'!{range_in_list}",
                majorDimension=majorDimension
            ).execute()
        except Exception as e:
            return values
        return values

    def write_data_to_range(self, list_name, range_in_list, data, majorDimension='ROWS'):
        try:
            self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data":
                        [
                            {"range": f"\'{list_name}\'!{range_in_list}",
                             "majorDimension": majorDimension,
                             "values": data}
                        ]
                }
            ).execute()
        except Exception as e:
            return
