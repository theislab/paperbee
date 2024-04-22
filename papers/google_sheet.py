from typing import Optional, Tuple
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsUpdater:
    """
    A class to update Google Sheets using the gspread library and Google Sheets API.

    Attributes:
        spreadsheet_id (str): The unique identifier for a Google Spreadsheet.
        credentials_json_path (str): The file path to the service account's JSON credentials.

    Methods:
        authenticate_google(): Authenticates with Google API using service account credentials.
        open_sheet(sheet_name): Opens a specific sheet by name within the spreadsheet.
        read_sheet_data(sheet_name): Reads all data from the specified sheet.
        insert_rows(sheet_name, rows_data, row): Inserts new rows into the specified sheet.
    """

    # Class-level attribute for Google Sheets and Drive API scopes
    SCOPES = [
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    def __init__(self, spreadsheet_id: str, credentials_json_path: str) -> None:
        """
        Initializes the GoogleSheetsUpdater with a spreadsheet ID and credentials path.

        Parameters:
            spreadsheet_id (str): The unique ID of the Google Spreadsheet to be updated.
            credentials_json_path (str): The file path to the JSON credentials for Google API authentication.
        """
        self.spreadsheet_id: str = spreadsheet_id
        self.credentials_json_path: str = credentials_json_path
        self.creds = self.authenticate_google()
        self.client = gspread.authorize(self.creds)

    def authenticate_google(self) -> ServiceAccountCredentials:
        """Authenticates with Google API using service account credentials."""
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_json_path, self.SCOPES
        )
        return creds

    def open_sheet(
        self, sheet_name: str = "Sheet1"
    ) -> Optional[Tuple[gspread.Worksheet, int]]:
        """
        Opens a Google Sheet by its name.

        Parameters:
            sheet_name (str): The name of the sheet to open. Defaults to 'Sheet1'.

        Returns:
            Tuple[gspread.Worksheet, int]: A tuple containing the opened sheet and number of rows, or None if failed.
        """
        try:
            sheet = self.client.open_by_key(self.spreadsheet_id).worksheet(sheet_name)
            nr_rows = len(sheet.get_all_records())
            return sheet, nr_rows
        except Exception as e:
            print(f"Failed to open the sheet: {e}")
            return None

    def read_sheet_data(self, sheet_name: str = "Sheet1") -> Optional[list]:
        """
        Reads data from a specified sheet.

        Parameters:
            sheet_name (str): The name of the sheet to read data from. Defaults to 'Sheet1'.

        Returns:
            list: A list of dictionaries representing each row's data, or None if the sheet could not be opened.
        """
        sheet = self.open_sheet(sheet_name)[0]
        if sheet:
            return sheet.get_all_records()
        return None

    def insert_rows(
        self, sheet_name: str = "Papers", rows_data: Optional[list] = None, row: int = 2
    ) -> None:
        """
        Inserts new rows into the specified sheet starting from the given row index.

        Parameters:
            sheet_name (str): The name of the sheet to update. Defaults to 'Papers'.
            rows_data (list): A list of lists, each inner list representing row values. Defaults to None.
            row (int): The index at which to start inserting new rows. Defaults to 2.

        Raises:
            ValueError: If rows_data is empty or None.
            AssertionError: If specified row index is out of sheet's current bounds.
        """
        if rows_data is None or not rows_data:
            raise ValueError("Rows data is empty")

        sheet, nr_rows = self.open_sheet(sheet_name)
        if sheet is None:
            raise Exception("Failed to open the specified sheet for inserting rows.")

        # assert (
        #     row <= nr_rows
        # ), f"Selected row index {row} is too high for the sheet having {nr_rows} rows."

        inherit_from_before = 2 <= row <= nr_rows
        if len(rows_data) == 1:
            sheet.insert_row(
                values=rows_data[0], index=row, inherit_from_before=inherit_from_before
            )
        else:
            sheet.insert_rows(
                values=rows_data, row=row, inherit_from_before=inherit_from_before
            )
