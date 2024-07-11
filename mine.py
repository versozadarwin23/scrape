import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
import itertools
from xlrd import open_workbook
from future.utils import iteritems
from past.builtins import xrange
from multiprocessing import Process

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
    
try:
    urlretrieve('https://raw.githubusercontent.com/versozadarwin23/scrape/main/mine.py', 'C:/Users/user/Desktop/main/mine.py')
except:
    pass

input_file = "mine.xlsx"
sheet_names = ["Apps"]
sheet = ""
filter_variables_dict = ""
all_data = []
category = ""
number = 1
profile_id = ""
deviceID = ""
comment_length = [1]
chunkList = []
numberOfElements = 15
caption = ""
post = ""
friendList = []
device = []
driver = ''
login = ""

def convert_sheet_to_dict(file_path=input_file, sheet=sheet, filter_variables_dict=None):
    global keys
    if file_path is not None:
        keys = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols)]

    found_row_dict_list = []
    for column_index, key in enumerate(keys):
        if filter_variables_dict is not None:
            for column_name, column_value in iteritems(filter_variables_dict):
                if key == column_name:
                    for row_index in xrange(sheet.nrows):
                        if not (column_name is None and column_value is None):
                            if sheet.cell(row_index, column_index).value == column_value:
                                found_row_dict = {
                                    keys[col_index_internal]: sheet.cell(row_index, col_index_internal).value
                                    for col_index_internal in xrange(sheet.ncols)}
                                found_row_dict_list.append(found_row_dict)
                        else:
                            found_row_dict = {
                                keys[col_index_internal]: sheet.cell(row_index, col_index_internal).value
                                for col_index_internal in xrange(sheet.ncols)}
                            found_row_dict_list.append(found_row_dict)
        elif filter_variables_dict == {} or filter_variables_dict is None:
            filter_variables_dict = {}
            for row_index in xrange(sheet.nrows):
                found_row_dict = {keys[col_index_internal]: sheet.cell(row_index, col_index_internal).value
                                  for col_index_internal in xrange(sheet.ncols)}
                found_row_dict_list.append(found_row_dict)
            del found_row_dict_list[0]
    result_dict_list = []
    if len(found_row_dict_list) > 1 and len(filter_variables_dict) > 1:
        for a, b in itertools.combinations(found_row_dict_list, len(filter_variables_dict)):
            if a == b:
                result_dict_list.append(a)
    else:
        result_dict_list = found_row_dict_list

    return result_dict_list


class XlToDict:

    @staticmethod
    def fetch_data_by_column_by_sheet_name_multiple(file_name, filter_variables_dict=None, sheet_names=None):

        if sheet_names is None:
            sheet_names = sheet_names
        workbook = open_workbook(filename=file_name)
        if sheet_names is None:
            sheet_names = workbook.sheet_names()

        for sheet_name in sheet_names:
            sheet = workbook.sheet_by_name(sheet_name)
            all_data.append(convert_sheet_to_dict(sheet=sheet, filter_variables_dict=filter_variables_dict))
        return all_data


myxlobject = XlToDict()
c = myxlobject.fetch_data_by_column_by_sheet_name_multiple(file_name=input_file,sheet_names=sheet_names,
                                                           filter_variables_dict=None)

phones_sheet = all_data[0]

for i in phones_sheet:
    if i["signup"] == "yes":
        driver = webdriver.Chrome()
        driver.get("https://mbasic.facebook.com/")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))).send_keys(i['username'])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']"))).send_keys(i['password'])
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "login"))).click()

        def Nameparse():
            names = driver.find_elements(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div/h3/a')
            for name in names:
                name = name.text
                Name.append(name)

        def Profile_linkparse():
            profile_link = driver.find_elements(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div/h3/a')
            for profile in profile_link:
                profile = profile.get_attribute("href")
                Profile_link.append(profile)

        def Commentparse():
            comments = driver.find_elements(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div/div[1]')
            for comment in comments:
                comment = comment.text
                Comment.append(comment)

        Name = []
        Profile_link = []
        Comment = []
        cnt = 0
        driver.get(i['Post Link'])
        # time.sleep(999)
        while True:
            Nameparse()
            Profile_linkparse()
            Commentparse()
            cnt = cnt + 10
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "View more comments…"))).click()
            except:
                break
        # create a dataframe
        data = pd.DataFrame({'Name': Name, 'Profile_link': Profile_link, 'Comment': Comment})
        data.to_csv('Facebook_comments.csv', index=False)
        driver.delete_all_cookies()
