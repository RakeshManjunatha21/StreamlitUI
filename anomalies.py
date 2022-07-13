#Import Modules
import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import datetime
#from datetime import datetime

# @st.cache()
# def load_file2():
#     data = pd.read_csv('server_data.csv')
#     return data

# @st.cache()
# def load_file3():
#     server_anomalies_average = pd.read_csv('server_anomalies_averages.csv')
#     return server_anomalies_average

def to_excel(df):
    """
    Function to convert to Excel
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def site_details(df):
    site_list = []
    for val in df['Site Dimensions Site Name']:
        site_list.append(val)
    site_list = set(site_list)
    site_list = list(site_list)
    return(site_list)


def partner_based_server_details_test(data1,server_anomalies_average,df_daily_test):
    i = 0
    grp_ps = data1.groupby(['Partner Details Partner Name','Site Dimensions Site Name'])
    for name, df in grp_ps:
        grp = df.groupby('Endpoint details Resource Device Type')
        for name1, df1 in grp:
            cnt = df1.shape[0]
            try:
                avg = server_anomalies_average.loc[name[1]][name1]
            except:
                avg = 0
            try:
                if cnt > avg:
                #print("In")
                    df_daily_test['Partner Name'][i] = name[0]
                    df_daily_test['Server Details'][i] = name1
                    df_daily_test['Average Ticket'][i] = avg
                    df_daily_test['Test Date Ticket'][i] = cnt
                    df_daily_test['Site Name'][i] = name[1]                
                    i = i + 1
            except:
                pass
    df_daily_test = df_daily_test[df_daily_test['Partner Name'] != 0]
    return df_daily_test
    
def server_anomolies(data,test_date):
    # server_anomalies_average = load_file3()
    server_anomalies_average = pd.read_csv('server_anomalies_averages.csv')
    server_anomalies_average = server_anomalies_average.set_index('Site_name')
    data1 = data.copy()
    data1['Ticket Date']= pd.to_datetime(data1['Ticket Date']).dt.date
    mask = (data1['Ticket Date'] == test_date)
    data1 = data1.loc[mask]

    #df_daily_test = pd.DataFrame(columns=['Partner Name','Server Details','Average Ticket','Test Date Ticket', 'Site Name'])
    df_daily_test = pd.DataFrame(columns=['Partner Name','Server Details','Average Ticket','Test Date Ticket', 'Site Name'])
    zero_value = [0 for val in range(37320)]
    df_daily_test['Partner Name'] = zero_value
    df_daily_test['Server Details'] = zero_value
    df_daily_test['Average Ticket'] = zero_value
    df_daily_test['Test Date Ticket'] = zero_value
    df_daily_test['Site Name'] = zero_value

    # partner_name_test = []
    # for val in data1['Partner Details Partner Name']:
    #     partner_name_test.append(val)
    # partner_name_test = set(partner_name_test)
    # partner_name_test = list(partner_name_test)
    
    #calling function - partner_based_server_details_test
    
    df_daily_test_final = partner_based_server_details_test(data1,server_anomalies_average,df_daily_test)
    return df_daily_test_final


def selected_page_func():
    """
    Functions to Show Anamolies and Download, feedback dashboard.
    """
    st.title('Anomalies')
    #data = load_file2()
    data = data = pd.read_csv('server_data.csv')
    period_list=data["Endpoint details Resource Device Type"].unique().tolist()
    server_name = st.selectbox("Server Name", period_list, index=0, help='Choose by which server you want to look at the metrics. The default is always the most recent month.')
    
    test_date = st.date_input("Select the Start Date", datetime.date(2021, 5, 6), help='Choose the test date you want to look at the metrics. The default is always the most start of the dataset.')
    # number = st.number_input('Set Threashold for a server')
    # st.write('Threashold set for the server', number)
    df_daily_test_final = server_anomolies(data,test_date)


    # anomolies_tab = {"Server Name":["Linux Server","Public IP"],"Partner Name":["lmstech",'Bralin Technology Solutions'],"Site Name":["Ken Grody Ford","Lyon Living"],"Average Monthly Ticket Generating":[200,96],"Current Month Ticket Generated":[204,102],"Family Condition":["RMM Agent","General(Up/Down/Reboot)"]}
    # ano_tab = pd.DataFrame(anomolies_tab)
    st.write(df_daily_test_final)
    df_xlsx = to_excel(df_daily_test_final)
    st.download_button(label='📥 Download Server Anomalies',
                                data=df_xlsx ,
                                file_name= 'server_anomolies.xlsx')



#comment_box = []

    st.write("**Add your actions that you have taken to resolve the tickets:**")
    form = st.form("comment")
    name = form.text_input("Name")
    comment = form.text_area("Comment")
    submit = form.form_submit_button("Add comment")

    if submit:
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #comment_box.append([name,comment])
        #db.insert(conn, [[name, comment, date]])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
    
        #st.write(comment_box)
        st.experimental_rerun()

    #st.warning("Linux Server is generating more tickets (204) than its usual (200)")