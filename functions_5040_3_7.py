# تابع های مورد نیاز شرکت 5040 و همکده

import pandas as pd
import sys
import numpy as np
import datetime
import jdatetime
# import powerbi
import openpyxl
from itertools import product , permutations , combinations
import re
from collections import defaultdict,OrderedDict
import os
from itertools import product , combinations , permutations
import time
import shutil
from  time import  sleep



# from selenium import webdriver
from seleniumwire import webdriver  # ا #AttributeError: module 'OpenSSL.SSL' has no attribute 'SSLv2_METHOD' > pip install pyopenssl==22.0.0 ,pip install cryptography==38.0.4
# این جدا باید نصب بشه . ورژن
# selenium==3.14.0
# selenium-wire==4.6.0


from  selenium.webdriver.support import expected_conditions  as EC
from  selenium.webdriver.support.select import Select
from  selenium.webdriver.support.ui import WebDriverWait


from  selenium.webdriver.common.by import By
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from  webdriver_manager.chrome import ChromeDriverManager # اینم جدا باید نصب بشه


from selenium.common.exceptions import NoSuchElementException ,TimeoutException,WebDriverException ,StaleElementReferenceException




# تابع های اتمی
# تابعی که چه یه دونه تاپل
# داشت چه چندتا به لیست تبدیل میکنه
# ورودی را به لیست تبدیل میکنه
def convert_to_list(t):

    if isinstance(t, list):
        return t
    elif isinstance(t, tuple):
        return list(t)
    elif isinstance(t, pd.Series):
        return t.tolist()
    else :      # انگار این فقط میگه استرینگ باشه و دیکشنری باشه را اینجوری میده
        return [t]




# ////////
    

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # MyExecutable's In-place Temporary PASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



# //////////


def vlookup_dict(Dict_1
                 , Dict_2
                 ,
                 demand='k1v2'):  # مشترکشون ولیو اول و کلید دوم باشه - مثلا میخوایم کلید اول کلید باشه و ولیو دوم ولیو باشه
    # توجه شود که اگر شرط اخر را نزاریم هرچند که دوتا دیکشنری واژه مشترکی نداشته باشند هم میشه
    '''

    :param Dict_1:  دیکشنری اول
    :param Dict_2:  دیکشنری دوم
    :param demand:  به چه صورتی میخوای . مثلا k1k2 یعنی کلید دیکشنری اول و کلید دیکشنری دوم را میخوام که این یعنی کلید اول بشه کلید دیکشنری تازه و کلید دیکشنری دوم بشه ولیو دیکشنری تازه
    فقط حتما باید اون ولیو هاشون مشترک باشه (یعنی حد وسطشون میشه اونی که مشترک است و حذف میشه )
    :return:
    '''

    if demand == 'k1k2':
        dict_3 = {
            key_1: key_2 for key_1, val_1 in Dict_1.items()
            for key_2, val_2 in Dict_2.items()
            if val_1 == val_2
        }
    elif demand == 'k1v2':
        dict_3 = {
            key_1: val_2 for key_1, val_1 in Dict_1.items()
            for key_2, val_2 in Dict_2.items()
            if val_1 == key_2
        }
    elif demand == 'v1k2':
        dict_3 = {
            val_1: key_2 for key_1, val_1 in Dict_1.items()
            for key_2, val_2 in Dict_2.items()
            if key_1 == val_2
        }

    elif demand == 'v1v2':
        dict_3 = {
            val_1: val_2 for key_1, val_1 in Dict_1.items()
            for key_2, val_2 in Dict_2.items()
            if key_1 == key_2
        }
    return (dict_3)


# vlookup_dict()


# //////////
 # بعد از اون کلید را بجای ولیو کنه و ولیو را بجای کلید
# فقط ولیو را لیست میکنه
# میشه بعدا درست کرد که استرینگ بده یا...
def reverse_dict(origin_dict_name,export="list" ):
    if export=="list":
        durkar_nazdik={}
        for sar,category in origin_dict_name.items():
            # print(category) #دورکار
            if category in durkar_nazdik:
                durkar_nazdik[category].append(sar) # این میشه ولیو حالا میگیم به ولیو این اپند بشه
            else:
                durkar_nazdik[category]=[sar]  # این  شکلی باید ل ی ست بش   که دفعه بعد بهش اضافه بشه
        return(durkar_nazdik)  # {'دورک ار': ['مهدی نفری', 'عرفان مهدی پور'], 'حضوری': ['امین افخمی', 'شهرزاد کلانکی']}
    # opposite_dict(sarbarast_team_name_real)
    elif export=="tuple":
        durkar_nazdik={ val:key for key,val in origin_dict_name.items() }
        return (durkar_nazdik)
# //////
# به ترتیب یه لیست اسم اون لیست قدیمی را میگیره و اسم تازه میده بهش
def change_dictionary_values(input_dict, old_names, new_names):
    updated_dict = {}
    name_counter = 0

    for key, value in input_dict.items():
        if value in old_names and name_counter < len(new_names):
            updated_dict[key] = new_names[name_counter]
            name_counter += 1
        else:
            updated_dict[key] = value

    return updated_dict

# Example input dictionary
# input_dict = {
#     'C92344C2019933C5AD3D440B1AF23799': 'برگ_نخست',
#     'B48CE08AD9198E64782CFA7D2BC98EA1': 'گزارش_فروش',
#     '345BE02E59BE93E1CDCD9070282F4937': 'ثبت',
#     'D24880EE76FDB522A4B49C3F7BE15C52': 'ثبت',
#     'DA372B251209A898E8D92E6448FD0088': 'ثبت'
# }
#
# # Example old and new names lists
# old_names = ["ثبت", "ثبت", "ثبت"]
# new_names = ["ثبت", "وصولی_کارت", "وصولی_درگاه"]
#
# # Call the function to change the values
# updated_dict = change_dictionary_values(input_dict, old_names, new_names)
#
# # Print the updated dictionary
# print(updated_dict)


# /////

# چند کلید و چند ولیو
# یک کلید و چند ولیو
# چند کلید و یک ولیو

# حالا چجوری دسترسی داشته باشیم بهش
# مثلا از کلید برسی به یک ولیو

# /////////


# میخوام دونه دونه موارد را به تیمش تبدیل کنه
# بعد که توی یه سلول که لیست هست هر سلول اون مورد را دید اون تیم را بهمون بده
# بعدا بتونه روی دیتا فریم اونو پیاده کنه
def converter_dict_administrator(demand="administator_team_name"
                                 ):
    # def converter_dict(
    #                            ):
    # این نام سرپرست را میگیره و نام تیم را میده
    administator_team_name = {
        "مهدی نفری": "پرسپولیس",
        "عرفان مهدی پور": "ارتش سرخ",
        "امین افخمی": "ویژن",
        "شهرزاد کلانکی": "رکورد",
        "آرین علیزاده": "سایت و غیره",
        "سجاد دمه زاده":"اوج" ,

    }
    # از تیم سرپرست ها را میفهمیم
    team_name_administator = reverse_dict(administator_team_name)

    # از نام تیم وضعیت دورکار یا حضوری را میفهمه
    team_name_telecommuting = {
        "ارتش سرخ": "دورکار",
        "پرسپولیس": "دورکار",
        "ویژن": "حضوری",
        "رکورد": "حضوری",
        "اوج": "دورکار"
    }
    # از حضوری یا دورکار نام تیم را میفهمه
    # لیست میده
    telecommuting_team_name = reverse_dict(team_name_telecommuting)

    # از اسم سرپرست وضعیت دورکار یا حضوری را پیدا میکنیم
    # چون قبلا هرکدومشونو داشتیم میتونیم پیداش کنیم
    # با تابعی که در بالا داشتیم
    administator_telecommuting = vlookup_dict(administator_team_name, team_name_telecommuting, demand="k1v2")

    # چون دوتا ولیو داره نمیده مستقیم
    # و بعدا باید همشو یکی کنم یا لیست باشه هردوشون
    # که اگر یکیشو در لیست دید باز هم ولیوشو بده
    # یه لیست هم نمیشه به عنوان کلید باشه
    # telecommuting_administator=vlookup_dict(telecommuting_team_name,team_name_administator,demand="k1v2")
    telecommuting_administator = reverse_dict(administator_telecommuting)
    # print(telecommuting_administator)
    # converter_dict()

    if demand == "administator_team_name":
        return administator_team_name
    elif demand == "team_name_administator":
        return team_name_administator
    elif demand == "team_name_telecommuting":
        return team_name_telecommuting
    elif demand == "telecommuting_team_name":
        return telecommuting_team_name
    elif demand == "administator_telecommuting":
        return administator_telecommuting
    elif demand == "telecommuting_administator":
        return telecommuting_administator


# مثال
# converter_dict_administrator(demand="telecommuting_administator")



# //////


# تابعی میخوام که ورودی را بگیره پس از اون خروجیش را طبق لیستی که دادیم برمیگردونه
# به همون ترتیب که ورودی بود. یعنی اگر داخل پرانتز بود رجکس میکنه برمیگردونش
def sarparast_supervisor_correct(correct_list, case_list,
                                 demand='correct_value',
                                 mode_on='dataframe'):
    # از تابع تصحیح گر استفاده کردیم
    # که چه لیست داد چه یه اسم خالی داد برش گردونه به چیزی که میگیم
    correct_list, case_list = (convert_to_list(char) for char in (correct_list, case_list))
    # اینم طبق اردر دیکت زدیم که ترتیب بهم نخوره
    output = {}
    # روی تک تک اعضای لیست معیار
    for the_case in case_list:
        # تک تک اعضای مورد را بررسی کن
        for the_correct in correct_list:
            # با روش سرچ برو بگرد اگر اون مورد بود پیدا شد
            if re.search(the_correct, the_case):
                # اونو بریز ولیو کن  که کلیدش اون غلطه باشه
                output[the_case] = the_correct
                # تا پیدا کردی دیگه بقیه را ادامه نده بشکونش
                break
        else:
            # اگر نبود ولیو را خالی کن جلوی اون مورد که نیست در معیار
            output[the_case] = None
    # return(output)
    # حالا اگر در بالا نوشته بودیم کارت ولیو را لیست کن ولیو ها را برگردون
    if demand == 'correct_value':
        if mode_on == 'dataframe':
            # اینکه روی صفر باشه اولین عنصرشو میده که خوب تبعا چون با لیست میشه اولین عنصر یه لیست خالی میشه لیست
            return list(output.values())[0]
        elif mode_on == 'list_tuple':
            return list(output.values())
    # اینو که صفر کنیم درست میشه ولی فقط اولیشو میده اگر بخوایم دوتا لیست را تبدیل کنیم

    # این دیکشنری را میده
    # یعنی غلطه به عنوان کلید و درسته به عنوان ولیو میشه
    elif demand == 'dict':
        return output
# //////////




def excel_reader(file_path):
    xlsx_file=pd.ExcelFile(file_path)
    sheet_dict={}
    for the_sheet in xlsx_file.sheet_names:
        val=xlsx_file.parse(the_sheet)
        sheet_dict[the_sheet]=val
    return sheet_dict



# //////





    # //////

# این کامل نیست .
# 1- ایمپورت کلاس اگر جی دیت تایم باشه جواب نمیده
# 2- ورودی و خروجی را نمیشه گریگوری کنه . مثلا ورودی گریگوری بگیره و خروجی استرینگ یا خروجی جی دیت تایم یا خروجی گریگوری یا هر چی .
# یا رند شده کنم به 15 دقیقه یا هر روز یا هر هفته یا...
# یا فقط ساعت بده یا فقط زمان بده


# ورودی را باید تنظیم کنم که ایا یکپارچه میده یا تیکه تیکه
# jdatetime_shape_setter
# باید نوع تاریخ را بیشتر هم کنم
# آبان 1402 یا...
# یا فقط سال را بده
# یا خودش تبدیل کنه خروجی را به میلادی

def input_date_hamkade(*the_list_strs,
                       import_type="date_time",
                       import_date_shape="/",
                       import_time_shape=":",

                       export_class='jdatetime',
                       on_mode="dataframe",
                       # export_date="jalali", # اینو درست کنم که بعدا بشه  ورودی گریگوری هم باشه
                       # import_date="jalali",    #  اینو درست کنم که ورودی بشه تاریخ گریگوری و بعد تبدیل کنه و فونتشم چیزی که میخوایم بده
                       # import_font="farsi",   # اینو بعدا درست کنم که به فارسی هم بود تبدیلش کنه به انگلیسی
                       export_type="date_time",
                       export_date_shape="/",
                       export_time_shape=":",

                       ):
    '''

    :param the_list_strs:
    :param import_type:
    :param import_date_shape:
    :param import_time_shape:
    :param export_class:
    :param on_mode: string | dataframe اگر ورودی بود
    :param export_type:
    :param export_date_shape:
    :param export_time_shape:
    :return:

    '''
    the_list_strs = convert_to_list(the_list_strs)

    if import_type == 'date_time':
        jdt_list = [(jdatetime.datetime.strptime(the_date,
                                                 format=f'%Y{import_date_shape}%m{import_date_shape}%d %H{import_time_shape}%M{import_time_shape}%S'))
                    for the_date in the_list_strs]  # [jdatetime.datetime(1402, 5, 18, 14, 0)]


    elif import_type == "date":
        jdt_list = [(jdatetime.datetime.strptime(the_date,
                                                 format=f'%Y{import_date_shape}%m{import_date_shape}%d'))
                    for the_date in the_list_strs]  # [jdatetime.datetime(1402, 5, 18, 0, 0)]


    elif import_type == "time":
        jdt_list = [(jdatetime.datetime.strptime(the_date,
                                                 format=f'%H{import_time_shape}%M{import_time_shape}%S'))
                    for the_date in the_list_strs]  # [jdatetime.datetime(1279, 1, 1, 12, 0)]

    # /////////////$$$$$$$///////////////

    if export_type == 'date_time':
        jdt_list = jdt_list  # [jdatetime.datetime(1402, 5, 12, 12, 0)]
        jdt_list_str = [(jdatetime.datetime.strftime(the_jdate,
                                                     format=f'%Y{export_date_shape}%m{export_date_shape}%d %H{export_time_shape}%M{export_time_shape}%S'))
                        for the_jdate in jdt_list]

    elif export_type == "date":
        jd_list = [jd.date() for jd in jdt_list]
        jd_list_str = [(jdatetime.datetime.strftime(the_jdate,
                                                    format=f'%Y{export_date_shape}%m{export_date_shape}%d'))
                       for the_jdate in jd_list]

    elif export_type == "time":
        jt_list = [jt.time() for jt in jdt_list]  # [jdatetime.time(12, 0, 0)]
        jt_list_str = [
            f'{the_jdate.hour:02}{export_time_shape}{the_jdate.minute:02}{export_time_shape}{the_jdate.second:02}'
            for the_jdate in jt_list]

    # ////////// تنظیم خروجی
    if export_class == "jdatetime":
        if export_type == "date_time":
            if on_mode == "user_input":
                return jdt_list
            elif on_mode == "dataframe":
                return jdt_list[0]
        elif export_type == "date":
            if on_mode == "user_input":
                return jd_list
            elif on_mode == "dataframe":
                return jd_list[0]
        elif export_type == "time":
            if on_mode == "user_input":
                return jt_list
            elif on_mode == "dataframe":
                return jt_list[0]



    elif export_class == "string":
        if export_type == "date_time":
            if on_mode == "user_input":
                return jdt_list_str
            elif on_mode == "dataframe":
                return jdt_list_str[0]

        elif export_type == "date":
            if on_mode == "user_input":
                return jd_list_str
            elif on_mode == "dataframe":
                return jd_list_str[0]

        elif export_type == "time":
            if on_mode == "user_input":
                return jt_list_str
            elif on_mode == "dataframe":
                return jt_list_str[0]


# # تست اولیه روی تاریخ
# tarikh_sabt_from=   ["1401/05/31 12:05:05"]

# velayati_jdate_shape(tarikh_sabt_from,
#         import_type="date_time",
#         export_type ='date_time',
#         export_class="string",
#         import_date_shape='/',
#         import_time_shape=':',
#         export_date_shape='+',
#         export_time_shape='------' )

# # ['1401+05+31 12------05------05']


# //////



# . مشکلی که این تابع داره اینه که نمیتونه اسم ها را
# تابعی که فقط اسم شیت هایی که میخوایم را بهش میدیم
# اسم دیتا فریم هایی که میخوایم را بهش میدیم
# مسیر خروجی را بهش میدیم
# اون خودش میره به ترتیب میسازه.
# فقط  باید اسم دیتا فریم اول همون اسم شیته باشه . مثلا نمیشه اسمکارت بهکارت را دوم بیاریم و دیتا فریم کارت به کارت را اول بیاریم
# فایله باشه اور رایت میکنه نباشه از اول میسازه
def excel_export(dataframes_lists=None,sheet_names=None,export_path=None , file_names= None , format=".xlsx"):
    # . اینو فعلا همونجوری بزنم ولی بعدا فرمت و اسم فایلشو درست کنم
    sheet_names,dataframes_lists=(convert_to_list(the_input) for the_input in (sheet_names,dataframes_lists))
    data_sheets={sheet:frame for sheet ,frame in list(zip(sheet_names,dataframes_lists))}
    if os.path.isfile(export_path):
        writer=pd.ExcelWriter(export_path,engine="openpyxl",mode='a',if_sheet_exists='replace')
    else:
        writer= pd.ExcelWriter(export_path,engine='openpyxl',mode='w+')
    for sheet in data_sheets:
        data_sheets[sheet].to_excel(writer,sheet_name=sheet,index=False)
    writer.close()
    print("اجرای فایل پایتون به پایان رسید لطفا به فایل اکسل بروید")




# /////////////////
def path_downlaod(download_base='~/Downloads'):
    # آیا اینجا اگر مسیر را خوساتم تغیر بدم بره با او اس بنویسه یا با استرینگ
    download_base=os.path.expanduser(download_base)
    os.chdir(download_base)
    return (download_base)



# تابع اتمی
# این ورودی فرمت و لیست را میگیره و میچسبونه به هم و فرمتشو درست میکنه و دیگه نیاز نیست کاربر ورودی بده
def adjust_name_format(file_list_names,the_format):
    adjust_name=[ f'{char}{the_format}' for char in file_list_names ]
    return adjust_name

# ////
# بعدا باید اکسل ریدر را درون این بزنم
def change_format_xlsx(path=None,
                       files_names=('kartbekart', 'keifiat_amalkard_today', 'keifiat_amalkard_yestersay', 'op_today',
                                    'op_yesterday'),
                       old_foramt='.xls',
                       new_format='.xlsx',
                       go_there=False
                       ):
    # برو توی فولدر مدنظر
    if go_there==True:
        os.chdir(path)
    time.sleep(2)
    # درست کردن فایل های لیست ها که با تاپل سرو کار دارند
    list_corrected = convert_to_list(files_names)
    # print(list_corrected)

    if new_format == '.xlsx':
        if old_foramt == '.xls':
            formatted_xls = adjust_name_format(list_corrected, old_foramt)
            # print(formatted)
            formatted_xlsx = adjust_name_format(list_corrected, new_format)
            all_foramt = list(zip(formatted_xls, formatted_xlsx))
            # print(all_foramt) #[('kartbekart.xls', 'kartbekart.xlsx'), ('keifiat_amalkard_today.xls', 'keifiat_amalkard_today.xlsx'), ('keifiat_amalkard_yestersay.xls', 'keifiat_amalkard_yestersay.xlsx'), ('op_today.xls', 'op_today.xlsx'), ('op_yesterday.xls', 'op_yesterday.xlsx')]
            #             # الان باید هرکدومو درست کنم به اونیکی تبدیل کنم بعد دیتافریم بشه
            # for file in all_foramt:
            # این آمار اپراتور ها را تبدیل نمیکنه و خطا میده  ولی کارت به کارت و کیفیت و.. را درست میده. شاید چون مستقیم از جدوله گرفتیم و اچ دی ام ال نیست

            for char_1, char_2 in all_foramt:
                # صفر اول را باید بزاریم که اولین جدول را انتخاب میکنه و صفر دوم اشاره به کاراکتر هستش
                try:  # این ترای اکسپت برای اینه که فایل اگر از اول وجود نداشت که عوضش کنه میده
                    try:  # اینم برای اینه که دو مدل ایکس ال اس داریم یه مدل که از اچ دی ام ال میگیرن و یه مدل درستش
                        df = pd.read_html(char_1)[0]
                        # این صفر برای اینه که سطر اول را بیاره توی جدول
                        df.columns = df.loc[0]
                        df = df.iloc[1:]
                        # این میره دومی را به دیتافریم تبدیل میکنه
                        df.to_excel(char_2, index=False, sheet_name='5040')
                        ## print(file[0],file[1]) kartbekart.xls kartbekart.xlsx keifiat_amalkard_today.xls keifiat_amalkard_today.xlsx
                    # اگر فایلی واقعا xls بود
                    # و نه html
                    # با این برو
                    except:
                        df = pd.read_excel(char_1)
                        df.to_excel(char_2, index=False, sheet_name='5040')
                except FileNotFoundError:
                    print(f" وجود نداشت که تبدیل فرمت شود {char_1} در مبدا فایل")
            # elif old_foramt=='.csv':

# ////////////

# برای ورودی ها که به مرداد و تیر و.. میده باید برج را اورد
def jalali_converter(input_month=None):
    '''

    :param input_month:  اگر عدد را میدیم و ماه را میخوایم عدد را بصورت اینتیجر یعنی  2 میدیم واگر ماه را به حروف دادیم باید استرینگ باشه یعنی  'فروردین' '
    :return: خروجی عدد بود واژه میده و اگر واژه دادی عدد ماه را میده
    '''
    mah_be_borg={
        'فروردین': 1 ,
        'اردیبهشت':2 ,
        'خرداد':3 ,
        'تیر': 4,
        'مرداد': 5,
        'شهریور':6 ,
        'مهر': 7,
        'آبان':8 ,
        'آذر': 9,
        'دی': 10,
        'بهمن':11 ,
        'اسفند':12 ,
    }
    # اینم تبدیل برج به ماه
    borg_be_mah={ val:key for key , val in mah_be_borg.items()}
    if isinstance(input_month,str):
        return mah_be_borg[input_month]
    elif isinstance(input_month,int):
        return borg_be_mah[input_month]
# jalli_converter('مرداد')  #5
# jalli_converter('مرداد')  #5
# jalli_converter(7) # 'مهر'


# /////


def jalali_converter_lenmonth(input_month='اسفند',value_want='the_number'):
    the_month=jalali_converter(input_month) # اول تبدیل میکنیم اون ماهه را 
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    month_days={}
    # بعد هر کدوم را میگیم اگه پیش از مهر بود بزار ماه را ۳۱ روزه 
    # اگه ماه ماه بین ۱۲ و ۷ بود ۳۰ روزه 
    # اگه ۱۲ هم بود ۲۹ روزه 
    # البته کبیسه ها را باید بعدا تبدیل کنم 
    for month in month_list:
        if the_month<7  :
            day_list=list(range(1,32))
        elif 7< the_month<12:
            day_list=list( range(1,31))
        elif  the_month==12:
            day_list=list(range(1,30))
        month_days[month] =day_list
    # حالا اگر لیست  روزها را خواست لیست را میده وگرنه که طول و تعداد را میده
    if value_want=='the_list':
        return month_days[input_month]
    elif value_want=='the_number':
        return len(month_days[input_month])


# ////////////

# تابع های اتمی
#  این تالع ها اتمی هستن که در چندتا تابع دیگه بکار میره

# ///////////

# این تابع برای اینه که لیست ها اگر چند تا تاپل ها چندتا تاپل داشته باشند کار میکنه ولی اگر یک تاپل استرینگی داشته باشه استرینگ در نظر میگیره
# که باید درون براکت بزاریم تا درست بشه ولی چندتایی را درون براکت لیستی از تاپل میکنه
list_corrector = lambda x: list(x) if isinstance(x, tuple) else [x]


# /////////
# تابع اتمی
# این ورودی فرمت و لیست را میگیره و میچسبونه به هم و فرمتشو درست میکنه و دیگه نیاز نیست کاربر ورودی بده
def adjust_name_format(file_list_names, the_format):
    adjust_name = [f'{char}{the_format}' for char in file_list_names]
    return adjust_name




# list_corrector
# adjust_name_format
# //////////////


# پیشفرض مسیرها را میدیم به مسیریاب
# بره این مسیر یا مسیر دیگه
def path_downlaod(download_base='~\\Downloads'):
    # آیا اینجا اگر مسیر را خوساتم تغیر بدم بره با او اس بنویسه یا با استرینگ
    download_base = os.path.expanduser(download_base)
    # os.chdir(download_base)
    return (download_base)



# مسیر مقصد
def path_destination(destination='~\\Desktop\\5040_gozareshat',stay_there=False ,create_directory=True):
    destination = os.path.expanduser(destination)
    the_current=os.getcwd()
    if create_directory==True:
        # اگه تو این مقصد نبود خودت بسازش  مسیرشو
        if not os.path.exists(destination):
            os.makedirs(destination)
    if stay_there==False:
        os.chdir(the_current) # برو مسیر اولیه
    return (destination)





# مسیر فایل های مکمل فایل برای سلنیوم  و سایر اجراها
# مسیر را اینجا مینویسه که بعد کافیه فقط مسیر دیگر را با استرینگ بهش بده
# این کد مشکلی که داره اینه که اگر روتین باشه و ساپلمنت نباشه را نمیزنه
def path_supplement(supplement='~/Desktop/5040_gozareshat/supplement',go_there=False):
    supplement = os.path.expanduser(supplement)
    if not os.path.exists(supplement):
        os.makedirs(supplement)

    if go_there==True:
        os.chdir(supplement) # برو اونجا
    # میره توی ساپلمنت
    # os.chdir(supplement)
    # اگر ساپلمنت را ریترن نکنیم و این خطا را میده
    # TypeError: expected str, bytes or os.PathLike object, not NoneType
    # چون در فایل اجرا داره ران میشه و ران نیاز نداره که بری توی مسیرش
    return supplement


# میخوام بره اونجا اجراش کنه با صدا زدن این
# def run_a_py():


# ////////
# این تابع باید اصلاح بشه بره توی یه حلقه
# پشیضفرض کارت به کارته
# پیشفرض مسیر دسکتاپ میشه
# ولی هر دو را میشه عوض کرد
# این تابع همه فایل ها را میره دانلود میکنه


# run_selenium()
# پایین تر فقط تابعشو صدا بزن


# ///////
# اون فایل های دانلود شده را ترتیب بندی میکنه کافیه جلوتر فرمت را بدی
# بعدا که عوض شد فرمت پیشفرض را عوض کن
# xlsx کن

# فیلتر کردن فایل ها که چند تاشونو بهمون  بده و چندمی را بهمون بده و
# ایا به ترتیب قدیمی ترین به جدید ترین باشه ؟
# پیشفرض اینه که از اول باشه تا آخر
# مشکل فایل های ساعتی اینه که تاریخ نیمه درست میده
# ولی مبنا همینه
# میره تو مسیر سورت میکنه لیست میکنه
def filter_files(the_path='~\\Downloads', the_format='.xlsx',
                 erlier="تازه_ترین", azchand=0, tachand=1000,
                 go_there=False,
                 ):  # این پیشفرضشه که البته بعدا در تابع دیگه عوض میشه
    '''
    یه لیست به ما میده که فیلتر شده ای از اخرین فایل های دانلود است
    '''


    # چندتا فایل را میخوای از اولی تا هزارمی مثلا را بده
    # ببرش توی دایرکتوری خود کاربر
    the_path = os.path.expanduser(the_path)
    if go_there==True:
        os.chdir(the_path)  # برو توی اون مسیر


    # ایا نیازه بره تو اون مسیر

    # این اول همه فایل ها را میگرده و بر اساس فرمت فیلتر میکنه
    # بعد بر اساس اخرین زمانی که خلق شدند در اون دایرکتوری سورت میکنه
    # وگرنه باید دایرکتوریشو عوض میکردیم - اگر لامبدا نمیزدیم نمیشد بشناسه
    # بعد سورت را بر اساس تازه ترین میاریم وگرنه کهنه ترین بود
    my_list = sorted([file for file in os.listdir(the_path) if file.endswith(the_format)] ,
                     key=lambda x : os.path.getctime(os.path.join(the_path,x)),
                     reverse=True if erlier == "تازه_ترین" else False)
        # کتابخونه گت ام تایم بر اساس اخرین زمان فایل دستکاری شده است/
        # کتابخونه گت سی تایم بر اساس تاریخ خلق هستش ولی
        # اگر کپی و دستکاری بشه بعضا تاریخش هم عوض میشه

        # کتابخونه گت ام تایم بر اساس اخرین زمان فایل دستکاری شده است/
        # کتابخونه گت سی تایم بر اساس تاریخ خلق هستش ولی
        # اگر کپی و دستکاری بشه بعضا تاریخش هم عوض میشه
    # )

    return (my_list)[azchand:tachand]


# این کد بعدا باید درست بشه
# filter_files()


# ////////////
# # تابعی که میاد دونه دونه به ترتیب  تاریخ اسم گزاری میکنه . باید دانلود ها هم دقیقا به همین ترتیب باشه در سلنیوم
# # مشکلی که داره اینه که  اگه یه موقع مشکلی باشه درنمیاد
# # پیشفرضش همون تعدادیه که بالا در تابع فیلتر فایل بهش دادیم
# باید به تعداد ورودی برش بزنه

# 'kartbekart','keifiat_amalkard_today','keifiat_amalkard_yestersay','op_today','op_yesterday'

# تابع تغیر نام که به تعداد ورودی که دادیم میاد اخرین فایل های دانلودی را منطبق میکنه
# یعنی مثلا نام کارت به کارت با نام اخرین فایلی که دانلود شده منطبق میشه
# پیشفرض فایل هایی که کار میکنه روشون هم روی مسیر دانلوده که البته میشه تغیر داد




def changer_names(the_path="~\\Downloads",

                  order_name=(
                  'kartbekart', 'keifiat_amalkard_today', 'keifiat_amalkard_yestersay', 'op_today', 'op_yesterday'),
                  the_format='.xlsx',
                  filter_files_order='filter_files_Func',
                  erlier='تازه_ترین' ,
                  stay_there=False
                  ):
    '''
    stay_there=False میشه بعد از اینکه رفتی اون دایرکتوری برگرد به دایرکتوری اولت یا نه
    '''

    # اگه ترتیب را از فانکشن فیلتر فایل استفاده کنه اون متغیرهاشو میگیره
    if filter_files_order=='filter_files_Func':
        list_files=filter_files(
                                the_path=the_path,
                                the_format=the_format,
                                erlier=erlier,

                                )
    # ٫ خروجی این میشه
    # print(filter_files_order) #['saleReport (2).xlsx', 'saleReport (1).xlsx', 'saleReport.xlsx']


    the_current_path=os.getcwd() #F:\1-python-pojects\robot_software\robot_software_5040

    the_pathـexpanduser = os.path.expanduser(the_path) # ~\Downloads  هر جا باشه میبره به دایرکتوری هوم سیستم و از اونجا میبینش

    # از تابع تصحیح گر فهرست را بکار بردم
    order_name_correct = convert_to_list(order_name)

    # print(order_name_correct) #['et']

    adjust_names = [(f'{char}{the_format}') for char in order_name_correct]
    # print(adjust_names) #['et.xlsx']

    # print(adjust_names)  # ['kartbekart.xls'] یا ['kartbekart.xls', 'dasti.xls']
    # اینو به تعداد ورودیه برش میزنیم
    ## زیپ میکنیم که همه برن تو یه لیست کنار هم . اولی به اولی دومی به دومی
    # فقط باید به همون تعداد باشه
    # از اون تا تعداد را بزن

    # دو به دو اون چیزی که داریم را با اون چیزی که میخوایم زی\ میکنه
    the_list = list(zip(list_files[:len(order_name)], adjust_names))  # [('2023-08-29-02-07.xls', 'kartbekart.xls')]
    # print(the_list) #[('saleReport (2).xlsx', 'et.xlsx')]


    # دایرکتوری را عوض میکنه
    os.chdir(the_pathـexpanduser)
    # چون یه خطی میخوایم بویسیم باید درون یه لیست باشه که درون متغیر باشه
    export = [os.replace(os.path.join(the_pathـexpanduser, char_1), os.path.join(the_pathـexpanduser, char_2)) for char_1, char_2 in the_list]

    # اگه اونجا بمون فالس باشه میره برمیگرده به همون جایی که اول بود
    if stay_there==False:
        os.chdir(the_current_path)
# اینو میریزیم توی فایل اول
# چون اخرین فایل دانلودی میشه اولین فایلی که توی لیسته
# changer_names(order_name=('latest','earliest') #[('sleroprt 1.xlsx', 'latest.xlsx'), ('sale report 2.xlsx', 'earliest.xlsx')]




# این فایل یا فایل ها که ما بهش میدیم را حذف میکنه
def delete_files(
        file_names=('kartbekart', 'keifiat_amalkard_today', 'keifiat_amalkard_yestersay', 'op_today', 'op_yesterday'),
        the_format='.xlsx', path=path_destination(),go_there=False,
        stay_there=False

):

    the_current_path = os.getcwd() # دایرکتوری اولیه

    the_path = os.path.expanduser(path)


    corrected_list = convert_to_list(file_names)
    corrected_lists = adjust_name_format(corrected_list, the_format)
    # باید لیست کنی و بریزی تو یه متغیر که کار کنه
    os.chdir(the_path)
    _ = [os.remove(file_name) for file_name in corrected_lists if os.path.exists(file_name)]
    if stay_there==False:
        os.chdir(the_current_path)


# delete_files(file_names=('kartbekart','op_today','keifiat_amalkard_yestersay','keifiat_amalkard_today'),path='E:/rutin')


# ///////////////
# جابجا میکنه فایل را اگر نباشه میگه
def moving_changed_names_files(path="~/Downloads/",
                               file_list_names_rigin=(
                               'kartbekart', 'keifiat_amalkard_today', 'keifiat_amalkard_yestersay', 'op_today',
                               'op_yesterday'),
                               the_format='.xlsx',
                               the_destination=path_destination(), delete_files_destination=True,stay_there=False
                               ):

    the_current_path=os.getcwd()

    file_list_names = convert_to_list(file_list_names_rigin)

    # اول حذف کن از مقصد اگر بود
    if delete_files_destination == True:
        delete_files(file_list_names, path=the_destination)


    the_path = os.path.expanduser(path)


    # os.chdir(the_path)
    # print(os.getcwd())

    # ورودی را الان چه یکی بود چه چندتا بود درستش میکنه
    file_corrector_list = convert_to_list(
        file_list_names)  # ['kartbekart', 'keifiat_amalkard_today', 'keifiat_amalkard_yestersay', 'op_today', 'op_yesterday']
    # print(file_corrector_list)
    # ورودی را درست میکنه لیست را میگیره و به فرمت تبدیلش میکنه
    #     # این فقط میچسبونه واژه فرمتشو که بالا دادیم به استرینگش
    file_list_names_correct = adjust_name_format(file_list_names, the_format)
    # print(file_list_names_correct)

    # مسیر هر دو را باید بدیم
    # این فایل هایی است که در در ورودی داده
    # انتقال لیستی از فایل ها به مسیر مورد نظرا
    # برای هر فایل
    for file in file_list_names_correct:
        # print(file)
        # اگه فایله وجود داشت حذفش کن
        # در مسیر مقصد
        # من میخوام بگم اگر اونجا بود منتقلش کن وگرنه که هیچ یعنی
        # اگر در مبدا بود که بیارش وگرنه ارور نده


        source = os.path.join(the_path, file)
        destination = the_destination
        try:
            if os.path.exists(source):
                # print(source)
                shutil.move(source, destination)
            else:
                print(f' وجود نداشت که جابجا بشود {source} در مبدا فایل ')
        except FileNotFoundError:
            print(f" وجود نداشت که جابجا بشود {source} در مبدا فایل")


    #   ما از \س استفاده کردیم و نیاز به جابجایی نداشت با این حجال اینو گذاشتم
    if stay_there==False:
        os.chdir(the_current_path)

# //////////////

# ///////////////
# حالا باید فرمتشو تغیر بدیم
# به دیتا فریم تبدیل کنیم
# میره اونجا این فایلو میخونه
# میگیم اگه با این اسم باشه برو بخون اونو حذف کن
# پیشفرض روی xls و xlsx است
def change_format_xlsx(path=path_destination(),
                       files_names=('kartbekart', 'keifiat_amalkard_today', 'keifiat_amalkard_yestersay', 'op_today',
                                    'op_yesterday'),
                       old_foramt='.xls',
                       new_format='.xlsx'):
    # برو توی فولدر مدنظر
    os.chdir(path)
    time.sleep(2)
    # درست کردن فایل های لیست ها که با تاپل سرو کار دارند
    list_corrected = convert_to_list(files_names)
    # print(list_corrected)

    if new_format == '.xlsx':
        if old_foramt == '.xls':
            formatted_xls = adjust_name_format(list_corrected, old_foramt)
            # print(formatted)
            formatted_xlsx = adjust_name_format(list_corrected, new_format)
            all_foramt = list(zip(formatted_xls, formatted_xlsx))
            # print(all_foramt) #[('kartbekart.xls', 'kartbekart.xlsx'), ('keifiat_amalkard_today.xls', 'keifiat_amalkard_today.xlsx'), ('keifiat_amalkard_yestersay.xls', 'keifiat_amalkard_yestersay.xlsx'), ('op_today.xls', 'op_today.xlsx'), ('op_yesterday.xls', 'op_yesterday.xlsx')]
            #             # الان باید هرکدومو درست کنم به اونیکی تبدیل کنم بعد دیتافریم بشه
            # for file in all_foramt:
            # این آمار اپراتور ها را تبدیل نمیکنه و خطا میده  ولی کارت به کارت و کیفیت و.. را درست میده. شاید چون مستقیم از جدوله گرفتیم و اچ دی ام ال نیست

            for char_1, char_2 in all_foramt:
                # صفر اول را باید بزاریم که اولین جدول را انتخاب میکنه و صفر دوم اشاره به کاراکتر هستش
                try:  # این ترای اکسپت برای اینه که فایل اگر از اول وجود نداشت که عوضش کنه میده
                    try:  # اینم برای اینه که دو مدل ایکس ال اس داریم یه مدل که از اچ دی ام ال میگیرن و یه مدل درستش
                        df = pd.read_html(char_1)[0]
                        # این صفر برای اینه که سطر اول را بیاره توی جدول
                        df.columns = df.loc[0]
                        df = df.iloc[1:]
                        # این میره دومی را به دیتافریم تبدیل میکنه
                        df.to_excel(char_2, index=False, sheet_name='5040')
                        ## print(file[0],file[1]) kartbekart.xls kartbekart.xlsx keifiat_amalkard_today.xls keifiat_amalkard_today.xlsx
                    # اگر فایلی واقعا xls بود
                    # و نه html
                    # با این برو
                    except:
                        df = pd.read_excel(char_1)
                        df.to_excel(char_2, index=False, sheet_name='5040')
                except FileNotFoundError:
                    print(f" وجود نداشت که تبدیل فرمت شود {char_1} در مبدا فایل")
            # elif old_foramt=='.csv':


# /////////////////////////
 # . این تابع میاد طبق ورودی که میدیم رند میکنه روبه پایین
# .فقط ساعت را
def round_timestamp(timestamp, interval_minutes,round="down"):
    if round=="down":
        # رند میکنه روبه پاینن
        rounded_minutes = int(np.floor(timestamp.minute / interval_minutes) * interval_minutes)
        # این میاد تبدیل میکنه اون دقیقه را به چیزی که بدست اورده بودیم .
        # و ثانیه هم صفر اگر ندیم بقیشو خودش میزنه
        return timestamp.replace(minute=rounded_minutes, second=0)
    elif round=="round":
        # رند میکنه اگر بالا بود میره بالا و اگر پاینی بود میره پایین
        rounded_minutes = int(np.round(timestamp.minute / interval_minutes) * interval_minutes)
        # این میاد تبدیل میکنه اون دقیقه را به چیزی که بدست اورده بودیم .
        # و ثانیه هم صفر اگر ندیم بقیشو خودش میزنه
        return timestamp.replace(minute=rounded_minutes, second=0)


# /////////////////////////


# . تابعی که اگر دیتا فریم تازه را میریزه زیر فایل اکسلی که از پیش داشتیم
def excel_appender(path=None,
                 file_name=None,
                 format=".xlsx",
                 # excell_name=None,
                sheet_name="hamkade"   ,
                df_new=None,
                add_update="row"
                 ):

    # اگه روی سطر بروز رسانی کنیم میشه صفر و اگر روی ستون  میشه یک
    if add_update=="row":
        the_axis=0
    elif add_update=="column":
        the_axis=1
    try:
        # . یه همچین فایلی را بساز اگر نبود خودشو اولین بار بریز توش
        merged_file_name=file_name+format
        path=path+'/'  # معمولا چون مسیر را تا خود اون میدیم یادمون میره اینو بزاریم . پیشفرض اینو میزاریم
        try:
        # خوندن وصولی کل ریخته شده از فایل قبل
            excel_already=excel_reader(path+merged_file_name)
            excel_already_df=excel_already[sheet_name]
            updated=pd.concat([excel_already_df,df_new],axis=the_axis)
            updated=updated.drop_duplicates()  # رکورد های تکراری را اگر باشند حذف میکنه
        except FileNotFoundError:  # اگر وجود نداش اولین بار خود فایله را بریزه توش
            updated=df_new
        excel_export(updated,sheet_names=sheet_name,export_path=path+merged_file_name)
    except AttributeError:
        pass

# ///////////
#
# sabt_df["مبلغ_وصول"]=sabt_df.apply(
#     lambda row :
#     row["مبلغ_ثبت"]
#     if (row["وضعیت وصولی"]=="تایید شده") and (row["وضعیت فاکتور"]=="پرداخت شده")
#     else 0 ,
#     axis=1
# ).astype(int)
# sabt_df["مبلغ_وصول"]



# ////////////

# تابع سام ایف . رو یه دونه شرط میشه زد فقط مبلغ را میاره اینور
def excell_sumif(df_destination=None,
                    df_search=None ,
                    df_destination_column_name=None,
                    df_search_coulm_name=None ,
                    sum_culumn_of_search_df=None,
                    number_df=2):

    df_new=df_destination[df_destination_column_name].apply(
    lambda row: df_search.loc [(df_search[df_search_coulm_name] == row,sum_culumn_of_search_df)].sum())
    return df_new

# بکار بردن سام ایف
# df_new_1=excell_sumif(df_destination=test_df,
#             df_search=kartbekart ,
#             df_destination_column_name="نام کارشناس",
#             df_search_coulm_name="اپراتور ثبت کننده" ,
#             sum_culumn_of_search_df="جمع فاکتور",
#             number_df=2)
# df_new_1

# sabt_df['first_sum'] = sabt_df['نام_تیم'].apply(lambda x:
#                     (oprator_df.loc[oprator_df['نام_تیم']==x,"فاکتور کارتابلی (تعداد)"])
#                     .sum()
#                                         )


# ///////////////
#
# # تابعی کهم بروز یکنه دفعه بعدی
# به اندازه 15 دقیقه یا همون دقیقه کهم خودمون یدیم بهش بریز توی کارنت

def jdatetime_updater_next(date_from, date_to, interval_minutes):
    from datetime import timedelta
    import jdatetime
    # اول تبدیل ورودی ها به جی دیت تایم
    date_from_j = jdatetime.datetime.strptime(date_from, '%Y/%m/%d %H:%M:%S')
    date_to_j = jdatetime.datetime. strptime(date_to,'%Y/%m/%d %H:%M:%S')

    # یه تایم دلتا ابجکت میسازیم
    interval = timedelta(minutes=interval_minutes)

    # تاریخ ابتدا را میریزیم توی کنونی
    current_date = date_from_j
    # حالا تا وقتی که کمتر و مساوی است از تا
    while current_date <= date_to_j:
        # تاریخ کنونی را برگردون
        yield current_date.strftime('%Y/%m/%d %H:%M:%S')
        # به اندازه 15 دقیقه یا همون دقیقه کهم خودمون یدیم بهش بریز توی کارنت
        current_date += interval




# //////////////////

#  . این کار نمیکنه
#
# # . تغیر درون فایل تکست برای خروجیconda که قابل خوندن در پیپ یا در کوندا باشه
# def change_conda_export(path="C:/Users/pcrr", file_input_name=None,file_export="requirements",format=".text"):
#     # conda list - e > req.txt  خروجی این شکلی میشه
#     import os
#     os.chdir(path)
#     with open(f"{file_input_name}.{format}", 'r') as file:
#         # همه خط ها را بیار بخون
#         lines = file.readlines()
#
#     # پردازش فایله
#     new_lines = []
#     # هر خط را بخون
#     for line in lines:  #
#         parts = line.strip().split('=')
#         if len(parts) > 1:
#             new_line = '='.join(parts[:-1])
#             new_lines.append(new_line)
#
#     # رایت میکنه مینویسه در فایل تازه
#     with open(f'{file_export}.{format}', 'w') as file:
#         for line in new_lines:
#             file.write(line + '\n')  # برای هر خط بخون بنویسش و بعد یه دونه اینتر بزن
#








# //////////////////
# تابعی که یه سشن باز  میکنه
# یعنی دقیقه میریزه توی اون مسیری که گفتیم اون کروم را که از کروم اصلی استفاده نکنه
def open_session(port="8484", user_dir=None, chrome_drv_dir=None):



    # selenium.__version__ #'4.1.0'
    # seleniumwire.__version__ #'4.6.0'
    # from seleniumwire import webdriver
    # # from  selenium import webdriver
    # from selenium.webdriver.chrome.service import Service
    # user_dir=user_chrome_directory
    # try:
    #     options=webdriver.ChromeOptions()
    #     options.add_argument(f"user-data-dir={user_dir}")
    #     service=Service(executable_path=ChromeDriverManager().install())
    #     driver=webdriver.Chrome(service=service,options=options)
    # except OSError :
    #     pass



    # user_dir = "E:/N/1-namjoo5040/0-selenium-os-pandas-streamlit-scadule/hamkade/user_dir_already_1"
    options = webdriver.ChromeOptions()

    # service=Service(executable_path=ChromeDriverManager().install())


    # options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors') # خطاهای اس اس ال را نادیده میگیره این .ssl اچتیتی پی را به اچ تی تی پی اس تبدیل میکنه  .
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"]) # خطاهای سرتیفیکیت را نادیده میگیره
    # options.add_experimental_option("excludeSwitches", ["eneble-logging"]) # سویچ ها مثل هدلس و سرتیفیکیشن ارور ها هستند اینجا میگیم درنظر نگیرشون
    # chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {"profile.default_content_setting_values.notifications": 2}  #  اینم ترجیحات  را میاره روی دو یعن نباشند
    options.add_experimental_option("prefs", prefs)

    options.add_argument(f"--remote-debugging-port={port}") # از این پورته سیستم یمره
    options.add_argument(f'user-data-dir={user_dir}') # دایرکتوری ای که کروم را بسازه کجا باشه
    options.add_argument('--disable-notifications') # اون ناتیفیکیشن هایی که  از طرف سایت میاره را میبنده
    options.add_argument('--disable-infobars') # اینفورمیشن بار و ها را نیشون نمیشه
    options.add_argument('--no-first-run')  # نخستین تجربه  را  که کروم میده رد میکنه
    # options.add_argument('--log-level=DEBUG') # ارورها را نشون میده بهمون
    options.add_argument('--no-default-browser-check') # بروزر پیشفرض را نشون نده بهمون
    options.add_argument("--disable-extensions") # اکستنشن هایی که برای اولین بار میاد بالا را نشون نمیده


    # options.add_argument('--log-level=0')  # ارور کنسول
    # options.add_argument('--log-level=1') # وارنینگ
    # options.add_argument('--log-level=2') #  اینفو
    # options.add_argument('--log-level=3') # دیباگ

    options.add_argument('--log-level=OFF') # بدون ارور کنسول یا لاگینگ


    # options.add_argument('start-maximized')

    # options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--headless")  # هدلس اجرا میکنه
    # options_2.add_argument('--disable-gpu')  # برای هدلس یه ا نوشته بود اینم نیازه
    # options.add_argument('--headless=new')
    # options.add_argument('--headless=old')
    # https: // stackoverflow.com / questions / 46920243 / how - to - configure - chromedriver - to - initiate - chrome - browser - in -headless - mode - throug

    # options.add_argument("--safebrowsing-disable-download-protection")
    # options.add_argument("safebrowsing-disable-extension-blacklist")

    driver = webdriver.Chrome(chrome_drv_dir,
                              options=options)

    return driver



# این تابع هم قبلی را ادامه میده که نیاز نیست دوباره باز کنه
# همون پورت همون دایرکتوری
def continue_session(port="8484", user_dir=None, chrome_drv_dir=None):

    # service_2 = Service(executable_path=ChromeDriverManager().install())
    # user_dir = "E:/N/1-namjoo5040/0-selenium-os-pandas-streamlit-scadule/hamkade/user_dir_already_1"
    # chrome_driver_directory = r"/chromedriver-win64-119.0.6045.105-win64.exe"
    options_2 = webdriver.ChromeOptions()


    options_2.add_experimental_option(f"debuggerAddress", f"localhost:{port}")
    options_2.add_argument(f'user-data-dir={user_dir}')
    options_2.add_argument('--disable-notifications')  # اون ناتیفیکیشن هایی که  از طرف سایت میاره را میبنده
    options_2.add_argument('--disable-infobars')  # اینفورمیشن بار و ها را نیشون نمیشه
    options_2.add_argument('--no-first-run')  # نخستین را رد میکنه
    options_2.add_argument('--no-default-browser-check')  # بروزر پیشفرض نداره
    # options_2.add_argument('--log-level=DEBUG')  # ارور را نشون میده
    # options_2.add_argument('--log-level=0')# کنسول ارور
    # options_2.add_argument('--log-level=1')# وارنینگ
    # options_2.add_argument('--log-level=2')#  اینفو
    # options_2.add_argument('--log-level=3')# دیباگ

    # options_2.add_argument('--disable-gpu')  #
    # options_2.add_argument('--no-sandbox')
    driver_3 = webdriver.Chrome(chrome_drv_dir,
                                options=options_2)
    return driver_3


# ////////

# . احراز هویت را با اولی میره
# باز کردن تب ها را با دومی
# شایدم بشه بقیه را با سدومی و چهارمی بره

# ////////



# ////////

# ورودی دیکشنری میگیره که یو ار ال بداره . بعد با اون میره باز میکنه و بعد ای دی را هم میگه
# این مورد بیشتر به درد این میخوره که مثلا  برای کارت به کارت و درگاه که یه صفحه باید باز بشه  با یه یو ار ال تفاوت بزاره
# به شرطی که باز کنه اون موارد را . و صفحه اش باز بشه

# تابعی که باز میکنه و اگر بخوایم ای دیشونو هم میده بهمون
def tab_opener(dict_tab_name_url=None,driver=None ,export="open" ): # ایدی و یوار ال میگیره و بهمون ای دی سلنیومشونو میده که اون تب ها را با اون اسم ها گره میزنه

    '''
    dict_tab_name_url: این یه دیکشنری با یو ار ال میگیره
    :param driver: این درایور را میگره
    :return: در نهایت خروجی یه ای دی است با باز کردن صفحه اون تب ها که بالا بهش دادیم
    :export: دو نوع است open و open_and_dict که دومی هم باز میکنه و هم ای دی را معرفی میکنه میریزه توی دیکشنری و در حالت اول فقط باز میکنه
    '''

    # هر تب و یو ار الی که دادیم را میگیره
    # صفحه اشو باز میکنه
    # میره تو صفحه
    execute_dictionary = {}
    for tab_name, url in dict_tab_name_url.items():
        driver.execute_script(f"window.open('','{tab_name}');")  # یه تب تازه باز کن
        # sleep(1)
        driver.switch_to.window(
            driver.window_handles[-1] )  # میندازه اون عنوان را کلید را به اون تب و بازش میکنه یو ار الشو
        driver.get(url)  # حالا اون یو آر ال را بده به درایور و اونا را باز کن

        if export=="open_and_dict":
            execute_dictionary[tab_name] = driver.window_handles[-1]
    # اگر طول داشت یعنی خالی نبود بده وگرنه فقط اپن را اضافه کن
    if len(execute_dictionary )>0:
        return execute_dictionary



# ///////


# فیلتر میکنیم دیکشنری کلی را با موارد اون لیست که دادیم
# ما کلی دیکشنری را میدیم ولی ممکنه بعضی  را نیاز بداریم
def filter_dict_based_list(all_dict=None , nedded_list=None):
  # اول لیست میکنه اون موارد را که اگر یکی هم بود را کانورت میکنه
    pages_hamkade = {page: all_dict[page] for page in nedded_list if page in all_dict}
         # ولیو را در اون کلی میگیره و اسم را از اون لیستی که دادیم و   وفیلتر شده است میگیره
     #'همکده_گزارش_فروش': 'https://panel.hamkadeh.com/sale/reports'
    return pages_hamkade

# ///////// پروژه
# . حالا اونایی که نا مشترک هستند را بده . اونایی که مشترک هستند را بده
# اونایی که ولیوشون یکی هستند
# اونایی که کلیدشون یکی هستند


# ///////

# ///

# نشانی یو ار ال همکده و 5040 و اتومیشن
# . بعدشم میشه نوع یو ار نام یو ار ال را میاره
def the_holding_urls_tabs ( demand_site="همکده",
                       targets="tabs_urls",
                       ):
    '''

    :param demand_site: همکده یا محصول یا اتوماسیون .

    :param targets:urls یا tabs_titles

                         tabs_titles نامی است که در تایتل سایت با اون نام تب باز میشه

    :return: خروجی در نهایت یه دیکشنری هستش کافیه صدا کنیم اون خروجی هدفی که میخوایم را بهمون میده
    '''


    if demand_site=="همکده" :
        if targets=="tabs_urls" :
            desired_name_to_url = {
                "همکده_گزارش_فروش": "https://panel.hamkadeh.com/sale/reports",
                "همکده_ثبت": "https://panel.hamkadeh.com/factor/list",
                "همکده_وصولی_کارت": "https://panel.hamkadeh.com/factor/list",
                "همکده_وصولی_درگاه": "https://panel.hamkadeh.com/factor/list",
                "همکده_ویپ": "https://panel.hamkadeh.com/voip/list",
                "همکده_برگ_نخست": "https://panel.hamkadeh.com",
                "همکده_استخراج": "https://panel.hamkadeh.com/sale/entries/extraction-entries",
                "همکده_فاکتور_کاربردی": "https://panel.hamkadeh.com/factor/my-list" ,

            }

            return desired_name_to_url
        elif targets=="tabs_titles":
            desired_name_to_title_name = {
                "گزارش_فروش": "نمایش گزارش فروش",
                "وصولی_کارت": "نمایش فاکتور های سیستم",
                "وصولی_درگاه": "نمایش فاکتور های سیستم",
                "ثبت": "نمایش فاکتور های سیستم",
                "ویپ": "نمایش اطلاعات تماس ها",
                "برگ_نخست": "داشبورد مدیریت",
                "مانیتورینگ": "مانیتورینگ سوپروایزر",
                "شناسایی_کیستی": "ورود به مدیریت سامانه",
                "استخراج": "",
                "فاکتور_کاربردی": "",
                # "محصول_ویپ_تست":""
            }
            return desired_name_to_title_name
    elif demand_site =="محصول" :
        if targets =='tabs_urls' :
            mahsul_urls={
            "محصول_گزارش_فروش": "https://panel.5040.me/reports/sale-data",
            "محصول_ثبت": "https://panel.5040.me/factor/list",
            "محصول_وصولی_درگاه": "https://panel.5040.me/factor/list",
            "محصول_وصولی_کارت_پاداش": "https://panel.5040.me/factor/list",
            "محصول_وصولی_کارت_روتین": "https://panel.5040.me/factor/list",
            "محصول_ویپ": "https://panel.5040.me/voip/logs",
            "محصول_برگ_نخست": "https://panel.5040.me/",
            "محصول_استخراج": "https://panel.5040.me/sale/entries/extraction",
            "محصول_مخزن": "https://panel.5040.me/sale/entries/list" ,
            # "محصول_ویپ_تست": "https://panel.5040.me/voip/logs",

            }
            return mahsul_urls
        elif targets =="tabs_titles":
            mahsul_urls={
            "محصول_گزارش_فروش": "سامانه مدیریتی 5040",
            "محصول_ثبت": "سامانه مدیریتی 5040",
            "محصول_وصولی_درگاه": "سامانه مدیریتی 5040",
            "محصول_وصولی_کارت_پاداش": "سامانه مدیریتی 5040",
            "محصول_وصولی_کارت_روتین": "سامانه مدیریتی 5040",
            "محصول_ویپ": "سامانه مدیریتی 5040",
            "محصول_برگ_نخست": "سامانه مدیریتی 5040",
            "محصول_استخراج": "سامانه مدیریتی 5040",
            "محصول_مخزن": "سامانه مدیریتی 5040" ,
            # "محصول_ویپ_تست":"سامانه مدیریتی 5040"

            }
            return mahsul_urls
    # اتوماسیون
    elif demand_site == "خودکارساز" :
        if targets =='tabs_urls' :
            aoutomation_urls={
                "خودکارساز_برگ_نخست" :"https://my.5040.me/dashboard" ,
                "درخواست":"https://my.5040.me/requests/create",
                "نامه_دریافتی":"https://my.5040.me/tickets/inbox"
            }
            return aoutomation_urls
        elif targets =="tabs_titles" :
            aoutomation_tabs={
                "خودکارساز_برگ_نخست" :"اتوماسیون اداری 5040" ,
                "درخواست":"اتوماسیون اداری 5040",
                "نامه_دریافتی":"اتوماسیون اداری 5040",
            }
            return aoutomation_tabs




# //////

# یابنده نام های تب ها یا یو ار ال تب های کنون که با اون درایور باز هستند
def tab_id_finder(driver= None ,vlaue_demand="tabs_urls") :
    '''
        # این تابع در بین همه تابعی هایی که باز با اون درایور را به ما میده
        . توجه شود که اگر دستی هم م یه تب اصافه کنیم باز
        هم اسم اونو بهمون میده حتی اگر خود درایور باز نکرده باشه

     :param driver: درایوری که نیاز هست را واسش باید بشناسیم
     :param vlaue_demand: اون ولیو دیکشنری که tabs_urls و یا tabs_titles و یا  tabs_source داره
     :return: خروجی در نهایت یه دیکشنری است که بسته به ولیو که انتخاب کردیم یا عنوان صفحه را میده به ما یا یو ار ال
     صفحه را میده یا سورس اون را میده

     شکل خروجی
      'DD79B8F024426E479E5251CCF827A941': 'https://panel.5040.me/voip/logs',
    '''
    the_dict={}
    for window_handle in driver.window_handles:
        driver.switch_to.window(window_handle)
        if vlaue_demand == "tabs_titles":
            the_dict[driver.current_window_handle]=driver.title
        elif vlaue_demand =="tabs_urls":
            the_dict[driver.current_window_handle]=driver.current_url
        elif vlaue_demand =="tabs_source":
            the_dict[driver.current_window_handle]=driver.page_source
    return  the_dict



# /////// پروژه
# دراپ داپلیکیت را میخوام در دیکشنری
# اونایی که ولیو یکسان دارند
# اونایی که کلید یکسان دارند
# اونایی که هر دو یکسان دارند


# //// پروژه
# یا اون کلید هایی که ولیوی یکسان دارند چند تا هستند


# //////


def different_id_from_one_url_or_title_to_name (
                                    urls_or_tabs=None ,
                                    dict_name_to_url_or_tab=None,
                                    dict_id_to_url_or_tab=None,
                                    desired_export_dict="name_to_id"
                                      ):
    '''

    :param urls_or_tabs:  یو ار ال ای یا اسم تبی که باید اون تب کارهای متفاوتی انجام بده
    :param dict_name_to_url_or_tab: یه دیکشنری بده که اسم قرار دادی باشه و یو ار ال یا عنوان تب روش باشه
    :param dict_id_to_url_or_tab: دیکشنری ای باشه که ای دی های موقت را پیدا کرده و یو ار ال را میده
    :param desired_export_dict:شکل خروجی دیکشنری که میده ای دی را بگیره و اسم را بده یا برعکس اسم را بگیره و ای دی را بده یعنی name_to_id  باشه
    :return:چیزی که یمخوایم اخر سر اینه که هر ای دی به یک  نام بچسبه id_to_name. و اونایی هم که کار متفاوت انجام میدن هم باشند
    08DACADE9FAB1F65EF57FDB84DB61C75:  گزارش_فروش
    خروجی یه دیکشنری است
    '''
    url_or_tab = convert_to_list(urls_or_tabs)[0]
    # ویلوکاپ میزنیم که از ای دی نام قراردادی را بیاره
    dict_id_to_name = vlookup_dict(dict_id_to_url_or_tab, dict_name_to_url_or_tab, "k1k2") #'3CD7A19F4CB24E7C29E068B0ADFFC485': 'محصول_وصولی_کارت_روتین',
    #اینم ویلوکاپ میزنیم تا بر اساس اشتراک ای دی اون یو ار ال یا تب را کلید کنه و ولیوش به ما اسم بده


    dict_url_or_tab_to_name=vlookup_dict(dict_id_to_url_or_tab ,dict_id_to_name ,"v1v2") #{'https://panel.5040.me/': 'محصول_برگ_نخست',

    # این وارونه میکنه  یعنی اسم یو ار ال را کلید میکنه و ولیو را اسم میکنه - ولی چون یه یو ار ال چند تا ولیو داره پس میاد لیست ای از یو ار ال ها میده
    names_reapeaed_list=reverse_dict(dict_name_to_url_or_tab)[url_or_tab]
    # چون برعکس کرده لیست میده حالا ما کلید را به عنوان یو ار ال یا تب میدیم و اون به ما لیست تکراریشو میده
     #    ['محصول_ثبت',
     # 'محصول_وصولی_درگاه',
     # 'محصول_وصولی_کارت_پاداش',
     # 'محصول_وصولی_کارت_روتین']


    # برای هر تعداد تکراری هاش که داره اسم اصلی را بده که با چه اسمی الان میشناسه اون اسم را هی تکرار کن بده
    old_list=[(dict_url_or_tab_to_name[url_or_tab]) for i in range(len(names_reapeaed_list))]
    # ['محصول_وصولی_کارت_روتین',
#  'محصول_وصولی_کارت_روتین',
#  'محصول_وصولی_کارت_روتین',
#  'محصول_وصولی_کارت_روتین']

    # # این تابعیه که اسم ولیو ها را با اون چیزی که میخوام تغیر میده
    # اینجا
    updated_dict = change_dictionary_values(dict_id_to_name,old_list,names_reapeaed_list )
    if desired_export_dict == "id_to_name":
        return updated_dict
    elif desired_export_dict=="name_to_id":
        return reverse_dict(updated_dict,export="tuple")


# پروژه . همینو تو یه دونه تعین کن
# که هی نیاز نباشه که اشتراک گیری و تفاوت گیری باشه
# راه 1- یه تابع تو درتو بنویسم
# 2- یه حلقه بنویسم

# /////////


def select_tab_by_name(desired_name=None,
                       dict_name_to_id=None,
                       driver=None
                       ):
    '''
    :param desired_name:  اسم قراردادی که میخوای را اینجا وارد کن
    :param dict_name_to_id: دیکشنری ای که اسم بدی بهش و ای دی بده را هم اینجا وارد کن
    :return: خروجی ر نهایت میاره روی صفحه ی که اون اسمو روش گذاشتیم
    '''
    for window_handle in driver.window_handles:
        # sleep(0.5)
        driver.switch_to.window(window_handle)
        if driver.current_window_handle == dict_name_to_id[desired_name]:
            break


# ////////

def set_theory_dict(
        methode="union_dict" ,
        first =None,
        sec=None
):
    '''
    :param methode:
                    union_dict   اجتماع دو دیکشنری را میده
                    . که یعنی کلید- ولیو هایی که در هر دو هستند
                    را میده چه در این باشه چه در اون .

                    intersection_dict مواردی که اشتراک هستند یعنی مواردی
                     که هم در این است هم در اون

                    difference_dict مواردی که در اولی هست فقط ولی در دومی نیست . یعنی
                    نا اشتراک های اولی . اولی مطلق
                    اگر یه موقع تفاظل دومی را خواستی بگیری کافیه دومی را اول بنویسی

    :param first: دیکشنری اولی
    :param sec: دیکشنری دوم
    :return: خروجی یه دیکشنری هستش
    '''
    # اجتماع
    union_keys= first.keys() | sec.keys()
    # اشتراک
    intersection_keys = first.keys() & sec.keys()

    # تفاضل
    difference_keys = first.keys() - sec.keys()

    # این میاد اجتماع دو تا را میده . عضو تکراری هم حذف میکنه
    if methode=="union_dict":
        # اینجا ولیوشونو اختصاص میده بهشون
        # چون اشتراک یعنی یا تو اینه یا تو اون میگیم برو اونو ببین اگر بود که بگیر و اگر نبود اون یکی را بگیر
        union={ key: first.get(key,sec.get(key)) for key in union_keys }
        return union
    # چون فرق نمیکنه اشتراک هر دو در اولی هم است پس اولی را اشاره میکنیم
    elif methode=="intersection_dict":
        intersection={key: first[key] for key in intersection_keys}
        return intersection
    # تفاضل دو مجموعه که اولی را چون حساب میکنه فقط نا اشتراک هایی که در اولی هستند را میده
    elif methode =="difference_dict":
        difference={ key: first[key] for key in difference_keys }
        return difference



# ////////////


# تابعی که تاریخ را هر بار اول خالی میکنه و بعد پر میکنه با چیزی که ما زدیم
def fill_date_hamkade(xpath=None,date=None,driver=None):
    input_fieled=driver.find_element_by_xpath(xpath)
    input_fieled.clear()   # پاکش کن
    def delete_filled():
        actions = ActionChains(driver) #  فعالیت زنجیره ای
        actions.move_to_element(input_fieled) #میره اونو انتخاب میکنه
        actions.click(input_fieled)   # کلیک میکنه روش
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)  # کنترل میزنه و ای میزنه
        actions.send_keys(Keys.DELETE)   # دیلیت میکنه
        actions.perform()   # اجرا کن
    delete_filled()    # یه بار ای (حرف انگلیسی a) میندازه اگر دوبار بزنیم  درست میشه
    delete_filled()
    def fill_date():
        input_fieled.send_keys(str(date))
    fill_date()







# //////////////////////

# باید انواع دیو و .. را بشناسم انواع عم و... که بتونم دریافتشون کنم.
# برای سلنیوم
# انواع کلاس های اچ دی ام ال برای انتخاب و فیلتر

# https://demoqa.com/select-menu


# btn dropdown-toggle btn-light
# vs__dropdown-option
# مثل کلاس نوع پرداخت همکده که مانع الجمع هستند
# از بین لیست یکی را انتخاب کنه





# /////
# منوی او.لیه را میاره اگر بود باز میکنه
def menu_bar_click(menu_bar_xpath=None,driver=None):
    # menu_bar_xpath="/html/body/div[2]/div[1]/nav/div/ul[1]/li/a"
    menu_bar=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,menu_bar_xpath)))
        # driver_2.find_element(By.XPATH,menu_bar_xpath)
    driver.implicitly_wait(5)
    if menu_bar.is_displayed():
        menu_bar.click()
    print("ok")




# ///////

def hamkade_aoutantication(driver=None,
                            user_name=None,
                           password=None,
                           phone=None,
                           user_xpath=None,
                           password_xpath=None,
                           phone_xpath=None,
                           radio_xpath=None,
                            remembermark_xpath=None,
                            image_verification_xpath=None,
                           submition_sms_xpath=None,
                           submition_call_xpath=None,
                           sms_apear_xpath=None,
                           sms_input_box_xpath=None,
                           submition_last_xpath=None
                           ):
    try :
        user_name_box =WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH,user_xpath)))

        driver.implicitly_wait(2)
        user_name_box=driver.find_element_by_xpath(
            user_xpath).send_keys(user_name)

        password_box = driver.find_element_by_xpath(
            password_xpath).send_keys(password)

        if radio_xpath != None:
            radio = driver.find_element_by_xpath(
                radio_xpath).click()

        if phone != None:
            driver.find_element_by_xpath(
            phone_xpath).send_keys(phone)

        if remembermark_xpath != None:
            remember_click = driver.find_element_by_xpath(
                remembermark_xpath).click()
        if image_verification_xpath !=None:
                    driver.find_element_by_xpath(
            image_verification_xpath).send_keys(input('اعداد درون تصویر گذاشته شده در سایت را همینجا وارد کنید'))

        if submition_sms_xpath != None:
            submition_sms = driver.find_element_by_xpath(
                submition_sms_xpath).click()
        elif submition_call_xpath != None :
            submition_sms = driver.find_element_by_xpath(
            submition_call_xpath).click()

        if sms_apear_xpath != None :
            sms_appear= WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, sms_apear_xpath)))
        sms_input_box=WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH,sms_input_box_xpath))
        ).send_keys(input(" رمز پیامک فرستاده شده به گوشی خود را همینجا وارد کنید"))
        # sms_input_box = driver.find_element_by_xpath(
        #     sms_input_box_xpath).send_keys(
        #     input('رمز پیامک فرستاده شده به گوشی خود را همینجا وارد کنید'))
        submition_last = driver.find_element_by_xpath(
            submition_last_xpath).click()
    except :
        pass


# //////////



# ///////


# def select_drop_down_vs_select_GENERAL(
#         driver=None,
#         xpath_vs_search=None,
#         xpath_vs_selected=None,
# ):
#     '''
#     مورد جنرال وقتی است که برای هر موردی که به این صورت باشه کار میکنه ولی غیر جنرال برای کارهای همکده یا محصول یا اتوماسیون است. در این جنرال کلی ایکس پت میده ولی در موردی که کلی باشه کافیه اسم خاصشو بدیم
#     :param driver:
#     :param xpath_vs_search:  این منوی اصلی را باز میکنه و پس از اینکه این باز شد بقیه باز میشن و معمولا فرمتش div هستش اخرش
#     :param xpath_vs_selected: ul/li[2] اخرش که باید اون پنجره باز باشه
#     :return: درنهیات میره باز میکنه و پس از اون اون موردو پیدا میکنه
#
#     '''
#     driver.find_element(By.XPATH,xpath_vs_search).click()
#     element=driver.find_element(By.XPATH,(xpath_vs_selected))
#
#     # زنجیره اگر موردی بود که داشت درونش میاد اونو حذف میکنه و اینو میزاره
#     webdriver.ActionChains(driver=driver).move_to_element(element).click(element).perform()



# ///////
#
#
# def mahsul_drop_down_vs_select(driver=None,title_vs_selected=None,li_selected=None ):
#     if title_vs_selected=="سیستم فروش" :
#         the_xpath_vs_search="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[3]/fieldset/div/div/div/div/div[1]"
#         if  li_selected =="سیستم فروش تست پیامک" :
#             the_xpath_vs_selected="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[3]/fieldset/div/div/div/ul/li[1]"
#         elif li_selected =="تست 1" :
#             the_xpath_vs_selected="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[3]/fieldset/div/div/div/ul/li[2]"
#         elif  li_selected =="لیگ طلایی 5040" :
#             the_xpath_vs_selected="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[3]/fieldset/div/div/div/ul/li[3]"
#         elif  li_selected =="اقساط" :
#             the_xpath_vs_selected="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[3]/fieldset/div/div/div/ul/li[4]"
#         elif li_selected =="لیگ اصلی 5040" :
#             the_xpath_vs_selected="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[3]/fieldset/div/div/div/ul/li[5]"
#     select_drop_down_vs_select_GENERAL(
#         driver=driver,
#         xpath_vs_search=the_xpath_vs_search,
#         xpath_vs_selected=the_xpath_vs_selected)
#         # return system_foosh_xpath_select ,system_forosh



# //////////

def setter_datetime_on_5040(
        driver_3=None,
        the_legend_date='بازه زمانی - شروع' ,
        the_date=None,
        the_label='تایید',
        hour_minute=True,
        wait=60
):
    driver_3.implicitly_wait(wait)
    # تاریخ ای که گرفتیم از بالا را به فرمت تبدیل میکنه که بتونیم با اشاره سال و ماه و روز بیاره .
    # استرینگ بگیره تبدیل شده بده
    date_destination=jdatetime.datetime.strptime(the_date,"%Y/%m/%d %H:%M")
    # برای درایور ۶۰ ثانیه صبر میزاریم که اگر نشد وایسته و اگر دید که کلیک کنه



    # روی لیبله کلیک کن
    driver_3.find_element(By.XPATH,f'//legend[normalize-space(text())="{the_legend_date}"]').click()

    # روی سال که بالا راست هست کلیک کن
    year_select=driver_3.find_element(By.XPATH,f"//div[@class='vpd-year-label direction-prev']//span[1]")
    year_select.click()

    try:
        # علی رغم اینکه ویت گذاشتم برای سال بازم اینجا ارور داد که اینترسپت داد و اینو گذاشتم درست شد
        year_in_years=WebDriverWait(driver_3,wait).until(EC.visibility_of_element_located((By.XPATH,f"//div[contains(@class,'vpd-addon-list-item') and (normalize-space(text())={date_destination.year}) ]")))
        # رفت توی سال سال مدنظر را انتخاب کن
        year_in_years.click()
    except :
        year_in_years=WebDriverWait(driver_3,wait).until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'vpd-addon-list-item') and (normalize-space(text())={date_destination.year}) ]")))
        # رفت توی سال سال مدنظر را انتخاب کن
        year_in_years.click()


    try:
        month_select=WebDriverWait(driver_3,wait).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class,'vpd-addon-list-item') and (normalize-space(text())='{jalali_converter(date_destination.month)}' )]")))
        month_select.click()

    except :
                # بعد که ماه میاد روی ماه کلیک کن. اول تبدیل شده ماه باشه بعد کلیک کن
        month_select=WebDriverWait(driver_3,wait).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'vpd-addon-list-item') and (normalize-space(text())='{jalali_converter(date_destination.month)}' )]")))
        month_select.click()


    try:
        day_selec=WebDriverWait(driver_3,wait).until(EC.visibility_of_element_located((By.XPATH,f"//span[@class='vpd-day-text' and normalize-space(text())='{date_destination.day}']")))
        # روی روز کلیک کن
        day_selec.click()
    # استیل المنت میداد که اینو بزنی کار میکنه
    except :
        day_selec=WebDriverWait(driver_3,wait).until(EC.element_to_be_clickable((By.XPATH,f"//span[@class='vpd-day-text' and normalize-space(text())='{date_destination.day}']")))
        # روی روز کلیک کن
        day_selec.click()



    # چون در اتوماسیون این نبود که ساعت و تاریخ را انتخاب کنیم این بخش را بیاره
    # فالس بشه
    if hour_minute ==True:
        # بعد ساعت ها را و دقایق را پیدا کن در یک لیست هست
        the_hour=driver_3.find_elements(By.XPATH,f"//input[@type='tel']")
        # بعد اون ساعت و دقیقه را دبل کلیک کن و روش کلیک کن
        ActionChains(driver_3).double_click(the_hour[0]).send_keys(f'{date_destination.hour}').perform()
        ActionChains(driver_3).double_click(the_hour[1]).send_keys(f'{date_destination.minute}').perform()

    # بعد روی تایید یا اگر مورد دیگری مثل اکنون یا انصراف بود روی اون کلیک کن
    click_on_text=driver_3.find_element(By.XPATH,f"//button[@type='button' and normalize-space (text())='{the_label}']")
    click_on_text.click()





# ////////

def vs_select_drop_down(
        driver=None,
        vs_selected_option=None,
        li_vs_selected=None,
        methode="full_xpath"
):
    '''
            مورد جنرال وقتی است که برای هر موردی که به این صورت باشه کار میکنه ولی غیر جنرال برای کارهای همکده یا محصول یا اتوماسیون است. در این جنرال کلی ایکس پت میده ولی در موردی که کلی باشه کافیه اسم خاصشو بدیم
    :param driver: حتما
    :param vs_selected_option: این منوی اصلی را باز میکنه و پس از اینکه این باز شد بقیه باز میشن و معمولا فرمتش div هستش اخرش
    :param li_vs_selected:  ul/li[2] اخرش که باید اون پنجره باز باشه
         درنهیات میره باز میکنه و پس از اون اون موردو پیدا میکنه
        فقط برای بهتر پیدا کردن اول دکمه منوی کرکره ای باز بشه و پس از اون انتخاب بشه
        # <li role="option" id="vs3__option-2" class="vs__dropdown-option">
    #           آذرخش(حسین ترابی گودرزی)
        #         </li>


    '''
    if methode =="full_xpath":
        driver.implicitly_wait(1)
        the_first=driver.find_element(By.XPATH,vs_selected_option)
        the_first.click()
        element=driver.find_element(By.XPATH,(li_vs_selected))
            # زنجیره اگر موردی بود که داشت درونش میاد اونو حذف میکنه و اینو میزاره
        # driver.implicitly_wait(1)
        webdriver.ActionChains(driver=driver).move_to_element(element).click(element).perform()

# /////////////////

def mahsul_vs_selector_option(driver=None,legend=None ,option_list=None,
                                    dict_legend=None , dict_options=None
                                  ):
    option_list=convert_to_list(option_list)
    for li in option_list:
        driver.implicitly_wait(2)
        vs_select_drop_down(
                driver=driver,
                vs_selected_option=dict_legend[legend],li_vs_selected=dict_options[li])

# ///////


def mahsul_day_settter(driver=None,
                        day=None,
                       day_span_class="vpd-day-text",
                        wait_clickable=3,
                       ):
    '''
    <span class="vpd-day-text">12</span> اینو باید بکشی بیرون
    :param driver:
    :param day:
    :param day_span_class:
    :param wait_clickable:
    :return:
    '''

    wait=WebDriverWait(driver,wait_clickable)
    #  حالا روزو باید تعین کنیم
    wait.until(EC.presence_of_element_located((By.XPATH,f"//span[@class='{day_span_class}' and text()={str(day)}]")))
    time.sleep(2)
    driver.find_element_by_xpath(f"//span[@class='{day_span_class}' and text()={str(day)}]").click()






# ////////

def mahsul_time_setter(driver=None,
                       hour=None,
                       minute=None,
                       hour_xpath=None,
                       minute_xpath=None,
                        confirm_xpath=None,
                       wait_clickable=3
                       ):
    '''

    :param driver:
    :param hour:
    :param minute:
    :param hour_xpath:
    :param minute_xpath:
    :param confirm_xpath:
    :param wait_clickable:
    :return:
    '''
    WebDriverWait(driver,wait_clickable).until(EC.visibility_of_element_located((By.XPATH,confirm_xpath)))
    hour_click=driver.find_element(By.XPATH,hour_xpath)
    minute_click=driver.find_element(By.XPATH,minute_xpath)
    ActionChains(driver).double_click(hour_click).send_keys(f"{str (hour)}").perform()
    ActionChains(driver).double_click(minute_click).send_keys(f"{str (minute)}").perform()
    driver.find_element(By.XPATH,confirm_xpath).click()


# /////////


def date_year(driver=None,
              date_destination_year=None,

              system_vpd_lable_xpath="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[2]/fieldset/div/span/div/div/div/div[2]/div[1]/div/span",

              year_click="/html/body/div[2]/div[1]/div[3]/div[3]/div/section/div[1]/div/div[2]/form/div/div[2]/fieldset/div/span/div/div/div/div[1]/div[1]/span",

              year_div_class_current="vpd-addon-list-item vpd-selected",
                year_div_class_others="vpd-addon-list-item",
              wait=3
              ):
    '''

    :param driver: درایوری که رسونده
    :param date_destination_year: 1402 که دستی میدیم فقط سال را اینجا میدیم
    :param system_vpd_lable_xpath: آذر 1402 یا شبیه اون
    :param year_click:  اون سال جاری را معمولا نشون میده بالا سمت راست هستش
    vpd-addon-list-item vpd-selected شبیه این میشه
    :param year_div_class_current: توی کلیک که میکنیم پس از انتخاب روی سال بالا سمت راست اون سالی که برای امسال هست کلاسش فرق میکنه میشه selected
    :param year_div_class_others: بقیه کلاس مجزایی دارند
    vpd-addon-list-item
    :return:
    '''
    WebDriverWait(driver,wait).until(EC.visibility_of_element_located((By.XPATH,year_click)))
    year_click=driver.find_element(By.XPATH,year_click)
    system_vpd_lable=driver.find_element(By.XPATH,system_vpd_lable_xpath).text
    system_month=jalali_converter(system_vpd_lable.split()[0])
    system_year=int(system_vpd_lable.split()[1])
    the_year=' '+str(date_destination_year)+' '
    if system_year ==date_destination_year :
        year_click.click()
        year_div_class=year_div_class_current
    elif system_year !=date_destination_year:
        year_click.click()
        year_div_class=year_div_class_others
    driver.find_element(By.XPATH,f"//div[@class='{year_div_class}' and text()='{the_year}']").click()


# ///////////

# در خواستی ورودی کلیک
def click_request_mahsul (driver=None,the_butten_xpath=None,wait_time_sec=10):
    wait=WebDriverWait(driver,wait_time_sec)
    wait.until(EC.visibility_of_element_located((By.XPATH,the_butten_xpath)))
    driver.find_element(By.XPATH,the_butten_xpath).click()




# /////////




# ////////

def retry_attempts(
        driver=None,
        try_number_max=3,
        function_or_variable=None,
        wait_second=5,
):
    for the_try in range(try_number_max) :
        try :
            function_or_variable
        except NoSuchElementException:
            driver.close()
            time.sleep(wait_second)
    raise  Exception( f"بود {the_try} تلاش " )



# /////

def all_tags_finder_5040(driver=None,
                    mother_class="span",
                    sub_class="menu-title text-truncate",

                    ):
    '''
    :param driver:  اسم درایور را که داریم کار میکنیم  میاریم
    :param mother_class: span | div
    :param sub_class: اسم کلاس را برای نمونه در  SPAN.menu-title text-truncate میشه
    menu-title text-truncate
    که کافیه در استرینگ اینرا بدیم
    :return: یه دیکشنری میتونه بده که بعد میشه کلیک کرد یا هر کار دیگر کرد

    این میشه یه نمونه که کلیک که میکنیم اونو میاره کلیک میکنه فقط باید قابل دید باشه
    all_tags_finder_5040(driver=driver_2,span_class="menu-title text-truncate")['داشبورد'].click()

    '''

    tags_dict={}
    all_tags=driver.find_elements(By.XPATH,f"//{mother_class}[@class='{sub_class}']" )
    for tag in all_tags:
        if tag.text !='':
            tags_dict[tag.text]=driver.find_element(By.XPATH,f"//{mother_class}[@class='{sub_class}' and text()='{tag.text}']")
    return tags_dict




# ////////

def selenium_write_text_on_box(driver=None,
                title_request_text=None,
                title_request_text_xpath=None,
                methode_write='clear_write',
                wait=3
                   ):
    '''
    :param driver:
    :param title_request_text:
    :param title_request_text_xpath:
    :param methode_write: 'clear_write' | 'append' که دومی به ته میچسبونه و هر چی داشته باشه را پاک نمیکنه و اولی پاک میکنه و جایگزینش اینو میزنه
    :return:
    '''
    wait=WebDriverWait(driver,wait)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, title_request_text_xpath)))
    element=driver.find_element(By.XPATH,title_request_text_xpath)
    if methode_write=='clear_write':
        element.clear()
        element.send_keys(f"{title_request_text}")
    elif methode_write=='append':
        webdriver.ActionChains(driver=driver).move_to_element(element).send_keys(f"{title_request_text}").perform()


# ///////////


def click_by_legend_for_drop_down_1sub(driver=None,
                                  the_legend=None,
                                  methode_want="click",
                                  wait=3,
                                  the_tag_name="legend"
                                  ):


    WebDriverWait(driver,wait).until(EC.visibility_of_element_located((By.XPATH,f"//{the_tag_name}[text()='{the_legend}']")))
    legend_element = driver.find_element(By.XPATH, f"//{the_tag_name}[text()='{the_legend}']")
    if methode_want=="click":
        legend_element.click()
    elif methode_want =="read":
        return legend_element

# ////////

# ///////////

# ماندن روی کلیک
# در سلنیوم



# ////

# انتخاب وقتی که یک منوی ابشاری باز شده است. یکی از گزینه ها
def drop_down_clicked(driver=None,
                    mother_class="li",
                    sub_class="vs__dropdown-option",
                     the_text=None,
                     methode_want='click',
                      wait=3
                     ):
    '''
    این پس از اینکه منوی اصلی باز شده میاره
    :param driver:
    :param mother_class:
    :param sub_class:
    :param the_text:
    :param methode_want:
    :param wait:
    :return:
    '''
    WebDriverWait(driver,wait).until(EC.visibility_of_element_located((By.XPATH,f"//{mother_class}[contains(@class, '{sub_class}') and normalize-space(text())='{the_text}']")))
    li_or_div_element = driver.find_element(By.XPATH, f"//{mother_class}[contains(@class, '{sub_class}') and normalize-space(text())='{the_text}']")
    if methode_want=="click":
        li_or_div_element.click()
    elif methode_want =="read":
        return li_or_div_element



# /////////
# ///////


def click_or_read_vpd_1class(driver=None,
                         mother_class='div',
                         sub_class='vpd-year-label direction-prev',
                         methode='click',
                        wait=3
                         ):
    year_xpath=f"//{mother_class}[@class='{sub_class}']"
    WebDriverWait(driver,wait).until(EC.visibility_of_element_located((By.XPATH,year_xpath)))
    element_year=driver.find_element(By.XPATH,year_xpath)
    if methode == 'click':
        element_year.click()
    elif methode == 'read_text':
        return element_year.text
    elif methode=="element":
        return element_year


# ///////////


def click_by_label_for_calender_5040Automation(
        driver=None,
        mother_class='fieldset',
        sub_mother_class='form-group',
        child_class='div',
        sub_child_class='label',
        label ='تاریخ جریان' ,
        wait=3,
        methode='click',
           ):
        xpath_expression=f"//{mother_class}[@class='{sub_mother_class}']//{child_class}[{sub_child_class}[normalize-space(text())='{label}']]"
        wait_=WebDriverWait(driver,wait)
        box_input_element=driver.find_element(By.XPATH,xpath_expression)
        wait_.until(EC.visibility_of_element_located((By.XPATH,xpath_expression)))
        if methode=='click':
            box_input_element.click()
        elif methode=='read':
            return box_input_element


# /////////

def click_and_select_by_text_1subclass(driver=None,
                             wait=3,
                             mother_class='div',
                             sub_class=None ,
                             text_input_select=None,
                             methode='click'
                             ):
    '''
    این با معرفی یک کلاس بالاش فقط متن را میکشه بیرون

    :param driver: مثلا driver_2 که برای خود
    :param wait: چند ثانیه وایسته  تا ببینه المنت را و کلیک کنه پیشفرض روی 3 است
    :param mother_class: div مثلا که بالا مجموع است
    :param sub_class:  مثلا vpd-actions
    :param text_input_select: اون متنی که درونش نوشته شده است
    :param methode: متد . click یا text که تکست را میده
    یا خود element  که بعدا هر کاری میخوایم روی اون انجام بدیم
    :return: خروجی بر اساس متد است . که اگر click باشه کلیک میکنه
    '''
    the_xpath=f"//{mother_class}[@class='{sub_class}' and normalize-space(text())= '{text_input_select}']"
    the_wait=WebDriverWait(driver,wait)
    the_wait.until(EC.visibility_of_element_located((By.XPATH,the_xpath)))
    the_element=driver.find_element(By.XPATH,(the_xpath))
    if methode=='click':
        the_element.click()
    elif methode=='element':
        return the_element
    elif methode=='text':
        return the_element.text

# //////////

def click_and_select_by_text_2subclass(
    driver=None,
    wait=3,
    mother_class=None,
    sub_class=None,
    text_input_select=None,
    sub_class_2=None,
    methode='click',):
    '''

    :param driver: مثلا driver_2 که برای خود
    :param wait: چند ثانیه وایسته  تا ببینه المنت را و کلیک کنه پیشفرض روی 3 است
    :param mother_class: div مثلا که بالا مجموع است
    :param sub_class:  مثلا vpd-actions
    :param sub_class_2: اون مورد مثلا buttun
    :param text_input_select: اون متنی که درونش نوشته شده است
    :param methode: متد . click یا text که تکست را میده
    یا خود element  که بعدا هر کاری میخوایم روی اون انجام بدیم
    :return: خروجی بر اساس متد است . که اگر click باشه کلیک میکنه
    '''
    the_xpath=f"//{mother_class}[contains(@class,'{sub_class}')]//{sub_class_2}[normalize-space (text())='{text_input_select}'] "
    the_wait=WebDriverWait(driver,wait)
    the_wait.until(EC.presence_of_element_located((By.XPATH,the_xpath)))
    the_element=driver.find_element(By.XPATH,(the_xpath))
    if methode=='click':
        the_element.click()
    elif methode=='element':
        return the_element
    elif methode=='text':
        return the_element.text


# ///////


# اسم گذاری موقعیت ها
def naming_s(name='name',the_number_characters=None , infix ='-'):
    '''
    این تابع به تعداد ای که میدیم  اون اسمه را با عدد تولید میکنه
    :param name: 'name' | 'my_name'
    :param the_number_characters: 3   | ['alef', 'be', 'gim'] میشه هم عدد بنویسیم و هم یه لیست بدیم که به تعداد اون لیست میاد اون حرفه مارو اضافه میکنه و اونو میسازه
    توجه شود که اعضای اون لیست را نمیده بلکه اون name را میده
    :infix : '_' |'!' هرچیزی که بشه متصل کنه دو تا کلمه را با هم . اینجا عدد را با _ به حرف need وند میکنه
    :return: ['naed_1', 'naed_2', 'naed_3']
    '''
    if isinstance(the_number_characters,tuple|list|str):
        the_name=convert_to_list(the_number_characters)
        all_names=[]
        for char in range(1,len(the_name)+1):
            all_names.append('%s%s%i'%(name,str (infix),char))
        return (all_names)
    elif isinstance(the_number_characters,int):
        all_names=[]
        for char in range(1,the_number_characters+1):
            # print(char)
            all_names.append('%s%s%i'%(name,str(infix),char))
        return (all_names)


# //////////

# برونسپاریش یه واژه نامه هستش
# این تابعهمه اسم های قراردادی و یو ار الشو میگیره . بعد لیستی که میخوایم از اون را میگیره بعد همه اونها را باز میکنه
def mahsul_open_all_tabs(driver=None ,
                    all_dict=the_holding_urls_tabs(demand_site="محصول", targets="tabs_urls"),
                    the_wanted_tabs_list=None
                    ):


    the_wanted_tabs_list=convert_to_list(the_wanted_tabs_list)
    all_name_to_url=filter_dict_based_list(the_holding_urls_tabs(demand_site="محصول", targets="tabs_urls") ,
                       nedded_list=the_wanted_tabs_list
                       )
    tab_opener(all_name_to_url, driver=driver, export="open")


# ///////////

def finder_id_pages_avtive_all_mahsul(driver=None,all_name_to_url=the_holding_urls_tabs(demand_site="محصول", targets="tabs_urls")):

    id_to_url = tab_id_finder(driver, vlaue_demand="tabs_urls")
    # id_to_url

    # از فاکتور میاد همه موارد مختلف و خروجی مختلفی که میخوایم را میکشه بیرون
    # با اسم قراردادی ما
    # این همه یو ار ال هایی که هستند را میگیره به علاوه اون موردی که برای فاکتور ها بود
    url = 'https://panel.5040.me/factor/list'
    the_dict_id_to_name_factors = different_id_from_one_url_or_title_to_name(urls_or_tabs=url,
                                                                                dict_name_to_url_or_tab=all_name_to_url,
                                                                             dict_id_to_url_or_tab=id_to_url,
                                                                             )

    all_tabs_factors_different = reverse_dict(the_dict_id_to_name_factors, export='tuple')
    # all_tabs_factors_different

    # این برای ویپ میاد موارد مختلف را میگیره و ای دی قراردادی میسازه
    url = 'https://panel.5040.me/voip/logs'
    the_dict_id_to_name_voip = different_id_from_one_url_or_title_to_name(urls_or_tabs=url,
                                                                          dict_name_to_url_or_tab=all_name_to_url,
                                                                          dict_id_to_url_or_tab=id_to_url, )

    all_tabs_voip_different = reverse_dict(the_dict_id_to_name_voip, export='tuple')
    # all_tabs_voip_different


    # چون برخی از دیکشنری ها با هم یکی نیستند این باگ را این درست میکنه . هرچند بعدا باید درست کنم که یه لیست بگیه و کار کنه


    # چون اولی همه تب ها است به علاوه تب فاکتور ها که کارهای مختلفی میکنه  و دومی همه است به علاوه تب ویپ . بنابراین ما میایم فیلتر میکنیم که با ست توری دیکت این کار را میکنیم و پیشفرضش اشتراک است
    the_dict_id_to_name = reverse_dict(set_theory_dict(first=all_tabs_factors_different, sec=all_tabs_voip_different),
                                       export="tuple")
    # the_dict_id_to_name

    # میشه همینو بزنیم توی تابع که به تعداد حساب کنیم . یعنی بیاد سنتز را با  جدیده بگیره و
    # هی مشترک بگیره
    return the_dict_id_to_name


# ////////






# ///////
def select_panel_5040_drop_down(driver_3=None,
                                the_legend=None ,
                                list_select=None,
                                ):
    '''
    driver_3=driver_3
    the_legend='نوع پرداخت' ,
    list_select=('آنلاین','کارت به کارت'),
    '''

    list_select=convert_to_list(list_select)
    for select in list_select:
        paying_type=driver_3.find_element(By.XPATH,f"//legend[normalize-space(text())='{the_legend}']")
        paying_type.click()
        driver_3.find_element(By.XPATH,f"//li[normalize-space(text())='{select}']").click()


# ///////


def cut_and_change_a_new_file_downloaded(
        driver_2=None,
        the_file_name=('None'+' '+str(jdatetime.datetime.now().date())), # پیشفرض اینا هست ولی عوضش میشه کرد . چی بشه اسمش
        download_base = path_downlaod(),
        the_format = '.xlsx',
        erlier = "تازه_ترین",
        the_destination=path_destination(create_directory=True,
                                         destination='~\\Desktop\\5040_gozareshat',

                                         ),
        delete_files_destination=True,

        # پیشفرض هرجا بود برو دسکتب ا میشه ولی عوضش هم کرد ,
        THE_DOWNLOAD_CLICK_OR_FUNCTION=None
):
    # the_file_name = "vosuli_dargah"
    # بررسی کن اینجا تعداشو
    # تا وقتی که زیاد نشده بود وایستا بعدش بشکن
    before = len(filter_files(the_path=download_base,the_format=the_format,erlier=erlier,))

    # print(before) #9
    # recive()  # دانلودش کن
    THE_DOWNLOAD_CLICK_OR_FUNCTION
    # sleep(1)
    after = 0 #
    # print(after) #0
    while after <= before:
        driver_2.implicitly_wait(1)
        after = len(filter_files(the_path=download_base,the_format=the_format,erlier=erlier,
                              ))

    # اسمشو عوض میکنیم
    changer_names(the_path=download_base,
                  order_name=the_file_name,
                    the_format=the_format,

                  )

    # حالا جاشو تغیر میدیم
    moving_changed_names_files(path=download_base,
                               file_list_names_rigin=the_file_name,
                               the_destination=the_destination,
                                delete_files_destination=delete_files_destination,

                               )


# ////////


# بخش seleniumwire  -  devtools


# /////


# میخوام یه چیزی در هر جای صفحه که داره انجام میده . مادامی که در این صفحه است هر مموقع اومد کلیک کنه از اول انام بده
def is_error_alert_present_on_5040(driver=None,
                                    wait=3,
                                   # error_5040_list=[ 'Unauthenticated.','ارتباط با وب سرویس قطع می باشد' , 'Too Many Attempts.',]
                                   ):

    error_5040_list=[
        'Unauthenticated.',
        'ارتباط با وب سرویس قطع می باشد' ,
        'Too Many Attempts.',
    ]

    for error in error_5040_list:
        try:
            WebDriverWait(driver,wait).until(EC.visibility_of_element_located((By.XPATH,f"//div[@role='alert']//small[contains(normalize-space(text()), '{error}')]")))
            print(f'error_{error}')
            return True

        except TimeoutException:
            pass   # اینو میزاریم که پس از بررسی اولین مورد هم ادامه بده
    return False




# /////////
# گرفتن اینکه بیس سایت چیه
def get_aouthority_of_a_site(driver=None,the_site='https://panel.5040.me/',what_do_you_want='authority-url'):
#     '''
#     این کد یک یو ار ال را میگیره و بیس را بهمون برمیگردونه
#     یا بیس ای پی ای را
#         هر چند به نظر هم این خودش درخواست را میگیره
#     from urllib.parse import urlparse
#     '''
    driver.get(the_site)
    from urllib.parse import urlparse
    my_referer_list=[]
    my_aoutority_list=[]
    # پیدا کردن بیس و سایت مبنا
    for request in driver.requests:
        if request.response:
            referer = request.headers.get('referer')
            # my_aoutority_list += [referer] if referer not in my_aoutority_list else []  # این نان را هم میاره
            # این کد اپند میکنه درون لیست وگرنه هیچی را نمیاره
            my_referer_list += [referer] if referer and referer not in my_referer_list else []  # این نان ها را نمیاره . ایف ریفر همون ایف ریفر نات نان هستش  که همون یعنی ایف ترو بود که نان فالس است

            # حالا هم پیدا کردن بیس
            if referer:
                authority =urlparse(referer).netloc
                my_aoutority_list+= [authority] if authority and authority not in my_aoutority_list else []
                # print(f"authority: {authority}")
    if what_do_you_want=='authority-url':
        the_selected=[char for char in my_aoutority_list if 'api' not in char]

        if len (the_selected) >1:
            return the_selected
        elif len (the_selected)==1:
            return the_selected[0]
    elif what_do_you_want=='authority-api':
        the_selected=[char for char in my_aoutority_list if 'api'  in char]
        if len (the_selected) >1:
            return the_selected
        elif len (the_selected)==1:
            return the_selected[0]

    elif 'referers_list':
        return my_referer_list

# ///////////



def get_Ratelimit_Remaining(driver=None,
                            the_site='https://panel.5040.me/' ,
                            what_want='the_remain'):
    '''
    این تابع بهش فقط درایور را میدیم خودش میگه چقدر دیگه مونده لیمیتینگ ریت ما
    what_want='the_remain' |  the_limit | both (tuple)
    '''

    # driver.requests
    # try:
    #     the_site = driver.current_url
    # except:
    #     the_site=the_site

    driver.get(the_site)
    print(the_site)
    # print(current_url) #https://panel.5040.me/auth/login
    the_remain=5000  # یه عددی میزاریم که رکورد کوچکترین را پیدا کنه
    rate_limit=0
    for request in driver.requests:
        # print(request.url)
        if request.response:
            # print( request.response , request.host , request.path , request.url , request.response.status_code)  #200  panel.5040.me /js/chunk-ed01dcce.7f9545e8.js https://panel.5040.me/js/chunk-ed01dcce.7f9545e8.js 200
            # print('request url is ',request.url)

            # اینجا ایکس ریت لیمیت ها را میریزیم تو یه متغیر
            # print(request.response.headers.get('X-Ratelimit-Limit')) #None None None 60 None None 60 None
            rate_limit_limit=request.response.headers.get('X-Ratelimit-Limit')

              # اولش با همون حدود لیمیت اغاز  میکنیم
            rate_limit_remain=request.response.headers.get('X-Ratelimit-Remaining')

            if rate_limit_limit:   #  چون بعضی از پاسخ ها none هستند یا بعضی اصا ریت لیمیت ندارن
                # print(f'X-Ratelimit-Limit: {rate_limit_limit}')
                # print(f'X-Ratelimit-Remaining: {rate_limit_remain}')

                # اینجا میتونه کوچکترین را پیدا کنه
                if int(rate_limit_remain) < int(the_remain):
                    #  و ترتیب نداره اینجا کوچیکترینه را که پیدا کرد میفرسته به بالا و رکورد را پیدا کنه . چون نامنظم میاره
                    the_remain=int(rate_limit_remain)
                    rate_limit=int(rate_limit_limit)
                    # print('now the remain is:',the_remain)
    if what_want=='the_remain':
        return the_remain
    elif what_want=='the_limit':
        return rate_limit
    elif 'both':
        return (rate_limit ,the_remain)
            # X-Ratelimit-Limit: 60
            # X-Ratelimit-Limit: 60
            # X-Ratelimit-Limit: 60
            # ایا هر کلیک یک ریکوییت میفرسته  ؟


# //////

# اینترسپتور
# mock ماک
def intercept_togather_block_mock(all_request):
# بلاک کردن درخواست
# def block_png(all_request):
    the_url='https://panel.5040.me/logo-square.png'
    # for req in driver.requests:  # توجه شود که نیاز نیست که ریکویست ها در حلقه باشند
    # برای تست و دیدن اینکه کار میکنه یا نه بهتره که حلقه بزنی و req را بیاری ولی برای کار باید بدون حلقه کار کنی
    if '.png' in all_request.url:
        # print(all_request.url)
        all_request.abort()



# //////



# streamlit

# تابعی که تاریخ جلالی را با سلکت میسازه و خروجی را میده تاریخ انتخاب شده را میده به صورت جلالی یا میلادی
def calender_selected_jalali_st(col1,
                                title='از چه بازه زمانی',
                                frmt='gr',
                                identifier='',
                                the_size=18,
                                
                                alignment = 'center',
                                color='blue'
                               ):
    

    
    # این کلیدو میاریم که این ارور DuplicateWidgetID را نخوریم و یگانه باشند هر کلید
    year_widget_id = f"{title}_year_{identifier}"
    month_widget_id = f"{title}_month_{identifier}"
    day_widget_id = f"{title}_day_{identifier}"
    
    

    the_size=the_size
    title=title
    alignment = 'center'
    col1.markdown(f"<h2 style='font-size:{the_size}px; text-align:{alignment}; color:{color};'>{title}:</h2>",
                  unsafe_allow_html=True) 

    
    
    year_list=list(range(1380,1420))
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    #  اینجا هم کلید را میاره که یگانه باشه
    year=col1.selectbox('برگزیدن سال',year_list,index=year_list.index(now_time.year),key=year_widget_id) # تعین دیفالت
    month=col1.selectbox( 'برگزیدن ماه' ,month_list,index=month_list.index(jalali_converter(now_time.month)),key=month_widget_id)
    # اون روزی که انتخاب میشه . اون بازه زمانی میاد بر اساس ماه
    
    
    day_list=jalali_converter_lenmonth(input_month=month,value_want='the_list')
    # اینو میزنیم که ماه ها که پیشفرضشون روی روزی است و عوض بشن دیگه مشکل نداشته باشن و امتحان کنه و نشد خودش بزاره روی اخری
    try:
        day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( now_time.day),key=day_widget_id)
    except:
        day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( day_list[-1]),key=day_widget_id )
        


    # تبدیل چیزی که اانتخاب شده به فرمت ها
    selected_date_jl=jdatetime.datetime.strptime(f"{year}/{jalali_converter(month)}/{day}","%Y/%m/%d" )
    selected_date_gr=pd.to_datetime(selected_date_jl.togregorian()).date()
    selected_date_jl=selected_date_jl.date()
    # col1.write(selected_date_jl)
    #col1.write(selected_date_gr)
    
    if frmt=='gr':
        return selected_date_gr # هم میسازه و هم برمیگردونه موقع فراخوانی
    elif frmt=='jl':
        return selected_date_jl


# ////////
# تغیر
# این فاصله بین اسپیس ها را درست میکنه در فارسی 
  # نام_کالا<ــــ نام کالا
def farsi_underscore_pd(df):
    new_col=[re.sub(' +','_',colname) for colname in df.columns.tolist() ]   
    df.rename(columns=dict(zip(df.columns,new_col)),inplace=True)
    return df

