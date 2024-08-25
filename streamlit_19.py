import streamlit as st
import pandas as pd
import warnings
import sqlite3
import plotly.express as px
import datetime , jdatetime
from datetime import *
import re
import math 


def farsi_underscore_pd(df):
    new_col=[re.sub(' +','_',colname) for colname in df.columns.tolist() ]    
    df.rename(columns=dict(zip(df.columns,new_col)),inplace=True)
    return df

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






def jalali_converter_lenmonth(input_month='اسفند',value_want='the_number'):
    the_month=jalali_converter(input_month) # اول تبدیل میکنیم اون ماهه را 
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    month_days={}
    # بعد هر کدوم را میگیم اگه پیش از مهر بود بزار ماه را ۳۱ روزه 
    # اگه ماه ماه بین ۱۲ و ۷ بود ۳۰ روزه 
    # اگه ۱۲ هم بود ۲۹ روزه 
    # البته کبیسه ها را باید بعدا تبدیل کنم 
    for month in month_list:
        if the_month<7 :
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





# تابعی که تاریخ جلالی را با سلکت میسازه و خروجی را میده تاریخ انتخاب شده را میده به صورت جلالی یا میلادی
def calender_selected_jalali_st(col1,
                                title='از چه بازه زمانی',
                                frmt='gr',
                                identifier='', # کلید های مختلفی از یک تابع با این میشه ساخت
                                the_size=18,
                                
                                alignment = 'center',
                                color='blue',
                                default_day='today'
                               ):
    
    
    
    # این کلیدو میاریم که این ارور DuplicateWidgetID را نخوریم و یگانه باشند هر کلید
    year_widget_id = f"{title}_year_{identifier}"
    month_widget_id = f"{title}_month_{identifier}"
    day_widget_id = f"{title}_day_{identifier}"
    
    

    
    col1.markdown(f"<h2 style='font-size:{the_size}px; text-align:{alignment}; color:{color};'>{title}:</h2>",
                  unsafe_allow_html=True) 
    
    
    now_time=jdatetime.datetime.now()
    year_list=list(range(1380,1420))
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    #  اینجا هم کلید را میاره که یگانه باشه
    year=col1.selectbox('برگزیدن سال',year_list,index=year_list.index(now_time.year),key=year_widget_id) # تعین دیفالت
    month=col1.selectbox( 'برگزیدن ماه' ,month_list,index=month_list.index(jalali_converter(now_time.month)),key=month_widget_id)
    # اون روزی که انتخاب میشه . اون بازه زمانی میاد بر اساس ماه
    
    
    day_list=jalali_converter_lenmonth(input_month=month,value_want='the_list')
    # اینو میزنیم که ماه ها که پیشفرضشون روی روزی است و عوض بشن دیگه مشکل نداشته باشن و امتحان کنه و نشد خودش بزاره روی اخری
    
    # زمان اکنون را برمیگزینیم
    
    if default_day=='today':
        try:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( now_time.day),key=day_widget_id)
        except:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( day_list[-1]),key=day_widget_id )
            
    elif default_day=='yesterday':
        try:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( (now_time.day)-1),key=day_widget_id)
        except:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( (day_list[-1])-1),key=day_widget_id )
            
        
    

    # تبدیل چیزی که اانتخاب شده به فرمت ها
    selected_date_jl=jdatetime.datetime.strptime(f"{year}/{jalali_converter(month)}/{day}","%Y/%m/%d" )
    selected_date_gr=pd.to_datetime(selected_date_jl.togregorian()).date()
    selected_date_jl=selected_date_jl.date()
    #col1.write(selected_date_jl)
    #col1.write(selected_date_gr)
    
    if frmt=='gr':
        return selected_date_gr # هم میسازه و هم برمیگردونه موقع فراخوانی
    elif frmt=='jl':
        return selected_date_jl



    



# @st.cache
# def get_data():
#     path = r'cars.csv'
#     return pd.read_csv(path)
# df = get_data()

# ////////////////////////////////////////////////////////

# خوندن دیتا فریم اصلی با پانداس 
cnx=sqlite3.connect(f'concreteDB9.db') 
df_naive=pd.read_sql_query(f"SELECT * FROM concreteTB",con=cnx)
# st.dataframe(df)

# فارسی میکنیم اندراسکورسرستون هارا
farsi_underscore_pd(df=df_naive)

# فیلتر میکنیم که فقط سیمان ها را بگیره اگر هم مشکلی پیش بیاد
df=df_naive[df_naive['نام_کالا'].str.contains('سیمان')]




warnings.filterwarnings('ignore')
st.set_page_config(page_title='شرکت سیمان',
                  page_icon=':bar_chart',
                   # layout='wide'
                  )

tilte_pge='آمار سیمان'
font_size=30
alignment='center'
st.markdown(
    f"<h1 style='font-size:{font_size};text-align:{alignment};'>{tilte_pge}</h1>",
    unsafe_allow_html=True
)

# st.subheader(" قرار دادن  مشخصات سیمان ")

# st.write(df.columns)

column1,column2,column3,column4 = st.columns(4)



with column1:
    column1=st.sidebar 
    column1.write('سیمان ها را برگزینید')
    # column1.markdown(f"<h2 style='font-size:{the_size}px; text-align:{alignment}; color:{color};'>{title}:</h2>",
    #               unsafe_allow_html=True) 
    
    commodities_lst = df['نام_کالا'].unique().tolist()
    # اینجا به ازای هر کدوم از این موارد یه چک باکس درست میکنیم 
    each=math.ceil(len(commodities_lst))    
    # st.write(columns) 
    all_commodities={} 
    for commodity in commodities_lst: 
        all_commodities[commodity]=column1.checkbox(commodity)
    # اینجا موارد را اگر ترو بودند در لیست میریزیم
    select_commodities=[commodity for commodity , trutness in all_commodities.items() if trutness]
    # st.write(select_commodities)
    # حالا اونایی که ترو هستند را در لیست ریخته را بیار درون دیتا فریم فیلتر کن





#  . حالا میخوام به ازای هرتیکی که میخوره یه خط بسازه
# بعداهم بیاد پیشفرض تعین کنه که رو کدومشون باشه . مثلا اونی که اکثریت تکرار اومده مثلا اگاه روی اون بزاره 












df["تاریخ_عرضه_جلالی"] = df["تاریخ_عرضه"].apply(lambda x:
                                           jdatetime.datetime.strptime(x,'%Y/%m/%d').date())
df['تاریخ_عرضه_میلادی'] = df['تاریخ_عرضه'].apply(lambda x: pd.to_datetime(jdatetime.datetime.strptime(x, '%Y/%m/%d').togregorian()).date()) 
df = df.sort_values(by='تاریخ_عرضه')   # این سورت را انجام میدیم چون در پلات خودش سورت نمیکنه 
#  . قبلش نکردم چون شاید توی تبدیل به تاریخ های میلادی مشکل ایجاد کنه حالا جایگزینش کن که تاریخ ها را طبق روال بده
# df['تاریخ_عرضه']=df['تاریخ_عرضه'].apply(lambda x: re.sub(r'\/(0{1})', '/', x))
# df['تاریخ_عرضه']=df['تاریخ_عرضه'].apply(lambda x: int(re.sub(r'\/', '', x))).astype(str)
# ////////درست کردن استریم لیت


with column3: 
    # column2=st.sidebar 
    the_from=calender_selected_jalali_st(col1=column3,title='از چه بازه زمانی' ,identifier='from',color='purple',default_day='yesterday')
    # column2.write('✨' * 3) 
with column2:
    the_to=calender_selected_jalali_st(col1=column2,title='تا چه بازه زمانی',identifier='to',color='cyan',default_day='today')
    df1=df[df['تاریخ_عرضه_میلادی'].between(the_from,the_to)]
    


st.write('✨' * 30)

with column1:
    column1.write('✨' * 3) 
    selected_options = {}
    # منوی کرکره ای
    the_select_box_list = ['کارگزار', 'تولید_کننده', 'عرضه_کننده']
    # با هر بار select به روز میشه
    filtered_df = df1.copy()
    for column in the_select_box_list:
        options = df[column].unique().tolist() 
        options.insert(0,'همه') 
        selected_options[column] = column1.selectbox(f":{' '+column+' '}را برگزینید", options,) # این هم اجرا میکنه هم میریزه تو دیکشنری 
    # st.write(filtered_df)
    for column, option in selected_options.items(): 
        if option != 'همه': 
            filtered_df = filtered_df[filtered_df[column]==option]
    



options = ['همه_قیمت_های_هرروز', 'کمترین_قیمتها', 'بیشترین_قیمتها']
default_option = 'کمترین_قیمتها'
default_index = options.index(default_option)


# این وسط میندازه
st.markdown("""
    <style>
    .stRadio [role=radiogroup]{
        align-items: center;
        justify-content: center;
    }
    </style>
""",unsafe_allow_html=True)

the_radio=st.radio(
    '' ,
    options,
    horizontal=True,
   index=default_index,
    # key='radio-container',  # Assign a key to the radio button container
    # help='radio-container'  # Apply the custom class to the container
)


# if the_radio=='کمترین_قیمتها':
#     st.write('این کمترینه')
if select_commodities : 
    selected_df = filtered_df[filtered_df['نام_کالا'].isin(select_commodities)]
    
    if the_radio=='کمترین_قیمتها': 
        min_indices = selected_df.groupby(['تاریخ_عرضه_جلالی' , 'نام_کالا' ])['قیمت_پایه'].transform('min')
        radio_df = selected_df[selected_df['قیمت_پایه'] == min_indices ].reset_index(drop='index')
        
        
    elif the_radio=='بیشترین_قیمتها': 
        max_indices = selected_df.groupby(['تاریخ_عرضه_جلالی' , 'نام_کالا' ])['قیمت_پایه'].transform('max')
        radio_df = selected_df[selected_df['قیمت_پایه'] == max_indices ].reset_index(drop='index')
        
    elif the_radio=='همه_قیمت_های_هرروز':  
        radio_df=selected_df 
    
    # حالا پلات
    # اینجا میشه تاریخ را بزنیم ولی پایین در تایتل تاریخ را چیز دیگه بزنیم
    # ولی اگر تاریخ عرضه را بزنیم که استرینگه در دوتا پلات کنار هم انگار میاره
    fig=px.line(radio_df,x='تاریخ_عرضه_جلالی',
                y='قیمت_پایه',
                color='نام_کالا',
                # facet_col='تاریخ_عرضه', 
               # markers=True, 
                hover_data=['کارگزار', 'تولید_کننده', 'عرضه_کننده'] # این بره روش نشون میده تاریخ عرضشو اطلاعات دیگرشو میاره
               )
    fig.update_xaxes(title_text='تاریخ_عرضه',tickangle=-45,tickformat='%Y/%m/%d')  # این فقط نشون میده تایتل را . من نمیخوام 
    fig.update_traces(mode='markers+lines') # افزودن مارک لاین
    fig.update_layout(
        title=dict(text="مقایسه قیمت ها ی سیمان ها در بازه های تاریخی", font=dict(size=20,color='#5E1916'), #RebeccaPurple
                   x=0.15 ,#  این تیتر را میاره چپ یا راست
                   # automargin=True,
                    # yref='paper',
                  ))
                   
    st.plotly_chart(fig)
    st.write(radio_df)




    




