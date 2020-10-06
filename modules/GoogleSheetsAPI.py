import googleapiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from modules.models import Equipment, Movement


class GoogleSheetOperator(object):

    def __init__(self, spreadsheet_id, credentials_file_name):
        self.spreadsheet_id = spreadsheet_id
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
        return values.get('values')

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
            print(e)
            return


class GoogleSynchronizer(GoogleSheetOperator):

    def __init__(self, spreadsheet_id, credentials_file_name):
        super().__init__(spreadsheet_id, credentials_file_name)

    def get_equipments(self):
        return self.read_range(list_name='Список оборудования', range_in_list='A2:G')

    def get_movements_list(self):
        return self.read_range(list_name='Перемещение оборудования', range_in_list='A2:D')

    # def sync_moves(self, start_line, data):
    #     self.write_data_to_range(list_name='Перемещение оборудования (Тест)',
    #                              range_in_list=f'A{start_line}:D',
    #                              data=data)

    def add_new_movement(self, id):
        count_of_movement = Movement.select().count()
        movement = Movement.get(Movement.it_id == id)
        return self.write_data_to_range(list_name='Перемещение оборудования',
                                        range_in_list=f'A{count_of_movement + 1}:C{count_of_movement + 1}',
                                        data=[[str(Equipment.get(Equipment.id == movement.it_id).it_id),
                                               str(movement.korpus), str(movement.room)]])

    def edit_in_table(self, item: Equipment):
        data = [[item.type, item.mark, item.model, item.serial_num]]
        self.write_data_to_range(list_name='Список оборудования',
                                 range_in_list=f'D{int(item.it_id) + 1}:G{int(item.it_id) + 1}',
                                 data=data)
