import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import shutil
from datetime import datetime

from config import *

# file_path = ConfigDrive.DATASET_EXCEL_PATH
# data_dir = ConfigDrive.DATASET_DIR
# datasets_dir = ConfigDrive.DRIVE_DATA_DIR

def get_file_from_link(drive_link):
    response = requests.get(drive_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    file_name = soup.find('meta', {'property': 'og:title'})['content']
    return file_name

class ExportDrive:

    def __init__(self, file_path, data_dir, dataset_dir):
        self.excel_data = pd.read_excel(file_path, sheet_name=None, skiprows=0)
    
        self.file_path = file_path
        self.data_dir = data_dir
        self.dataset_dir = dataset_dir

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def from_sheet(self, name_sheet):
        sheet_data = self.excel_data[name_sheet]
        sheet_dict = sheet_data.to_dict(orient='list')

        # ['STT', 'Mã sinh viên', 'Họ và tên', 'Lớp', 'Link ảnh', 'Ghi chú']
        column_names = list(sheet_data.columns)
        # print(len(sheet_data))

        for i in range(len(sheet_data)):
            id_col = sheet_dict[column_names[1]][i]
            name_col = sheet_dict[column_names[2]][i]
            subject_col = sheet_dict[column_names[3]][i]
            links_col = sheet_dict[column_names[4]][i].split(",")

            dir_col = os.path.join(self.data_dir, str(id_col))

            if not os.path.exists(dir_col):
                os.makedirs(dir_col)

            for link in links_col:
                try:
                    file_name = get_file_from_link(link.strip())
                    datasets_file = os.path.join(self.datasets_dir, file_name)
                    data_file = os.path.join(dir_col, file_name)

                    shutil.copy(datasets_file, data_file)
                except Exception as e:
                    line = ""
                    with open(ConfigDrive.EXPORT_LOG_PATH, 'a', encoding='utf-8') as file:
                        now = datetime.now()
                        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                        line += f"-----ERROR: {e}\n"
                        line += f"{current_time}|:{id_col} - {name_col} - {subject_col}\n"
                        line += f"{file_name} - {dir_col}"
                        file.write(f'{line}\n')

class ImageExtension:

    def normalize(images_dir, accept_extension=['.JPEG', '.png', '.PNG', '.jpeg', '.jpg', '.JPG']):
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                # extension = os.path.splitext(file)[1]
                old_path = os.path.join(root, file)
                names = file.split(".")
                extens = names[-1]
                if not extens in accept_extension: 
                    name = "".join(names[:-1])
                    new_path = os.path.join(root, f"{name}.{extens}")
                    os.rename(old_path, new_path)

class CountDataset:

    def count(target_dir):
        image_count = []

        for ms in os.listdir(target_dir):
            ms_dir = os.path.join(target_dir, ms)
            len_dir = len(os.listdir(ms_dir))
            image_count.append(len_dir)
            # if len_dir == 4:
            #     print(f"{ms_dir} - {len_dir}")
            for file in os.listdir(ms_dir):
                file_name = os.path.join(ms_dir, file)
            if not os.path.isfile(file_name):
                print(ms_dir)

        print(set(image_count))







