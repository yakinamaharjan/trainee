import pandas as pd
import os

class ExportManager:
    def __init__(self):
        self.cfile = 'queries.csv'
        self.xfile = 'queries.xlsx'

    def export(self, qr: str, data: list):
        """
        Exports all records to a csv file and a excel file.

        Args:
            qr (str): Type of query.
            data (list): List of records.
        """
        q = pd.DataFrame([[qr] + [''] * (len(data[0]) - 1)]) if data else pd.DataFrame([[qr]])
        df = pd.DataFrame(data)

        try:
            q.to_csv(self.cfile, mode='a', index=False, header=False)
            df.to_csv(self.cfile, mode='a', index=False, header=False)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
        
        try:
            if os.path.exists(self.xfile): 
                df_existing = pd.read_excel(self.xfile, header=None)
                df_combined = pd.concat([df_existing, q, df], ignore_index=True)
            else:
                df_combined = pd.concat([q, df], ignore_index=True)

            df_combined.to_excel(self.xfile, index=False, header=False)
        except Exception as e:
            print(f"Error exporting data to Excel: {e}")