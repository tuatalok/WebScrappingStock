from os import name
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import xlsxwriter
import requests
import time
import base64
from io import BytesIO


def com_name(x):
    x = x.replace('#',' ')
    x = x.split('=')
    name = x[1].split('&')
    name = name[0]
    return name

def url_edit(x):
    x = x + '&offset={0}'
    return x

def webscrapping(URL):
    URL = url_edit(URL)
    name_com = com_name(URL)

    list_page = [x for x in range(0,135,15)]
    list_td = list()

    for i in list_page :
        response = requests.get(URL.format(str(i)))
        document = BeautifulSoup(response.text,'html.parser')
        table = document.find('table' , attrs = {'class' : 'table table-info table-hover'})
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')
        for info in tr :
            td = info.find_all('td')
            row = [i.text for i in td]
            list_td.append(row)

    columns = ['Date','Open','High', 'Low' ,'Average_Price' ,'Close' ,'Change' ,'% Change','Volume' ,'Value' ,'SET_Index' ,'% Change']
    df = pd.DataFrame(list_td , columns = columns)
    df['Company_Name'] = name_com
    return df,name_com

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1',index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = to_excel(df)
    b64 = base64.b64encode(csv) # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64.decode()}">Download Excel file</a>'
    return href

st.title(
    """
    Web Scrapping Stock
    Use www.Settrade.com only
    """)
st.markdown("**Get link**: Settrade >> Company >> Historical Quotes >> Copy URL link")
URL = st.text_input("""Please Input Stock URL :""", )

x = None

if st.button('Pull Data'):
    st.markdown("**Please Input URL**")
    loading = st.text("Scrapping...")
    df_m,name = webscrapping(URL)
    st.write('# Company Name :',name,df_m)
    loading.text("Scrapping...done!")
    st.markdown(get_table_download_link(df_m), unsafe_allow_html=True)

    


    
