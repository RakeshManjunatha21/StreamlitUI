#Import Modules
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import datetime

# @st.cache()
# def load_file1():
#     data = pd.read_csv('server_data.csv')
#     return data


def selected_page_func():
    """
    Function for Custom Ticket Analysis
    """
    # data = load_file1()
    data = pd.read_csv('server_data.csv')
    total_no_server = len(data['Endpoint details Resource Device Type'].value_counts())
    total_no_site_name = len(data['Site Dimensions Site Name'].value_counts())
    emergency_ticket = data[data['Priority Details Priority Name'] == 'Emergency']
    medium_ticket = data[data['Priority Details Priority Name'] == 'Medium']
    low_ticket = data[data['Priority Details Priority Name'] == 'Low']
    st.title('Insights')
    c1, c2= st.columns(2)
    with c1:
        st.info("Total number of Server : "+str(total_no_server))
    with c2:
        st.info("Total number of site : "+str(total_no_site_name))

    h1, m1, l1 = st.columns(3)
    with h1:
        st.info("Count of Emergency Tickets : "+str(emergency_ticket.shape[0]))
    with m1:
        st.info("Count of Medium Tickets : "+str(medium_ticket.shape[0]))
    with l1:
        st.info("Count of Low Tickets : "+str(low_ticket.shape[0]))

    # data['Ticket Creation Details Ticket Creation Time'] = pd.to_datetime(data['Ticket Creation Details Ticket Creation Time'], errors = 'ignore')
    # data['Ticket Month'] = data['Ticket Creation Details Ticket Creation Time'].dt.month
    # data['Ticket Date'] = data['Ticket Creation Details Ticket Creation Time'].dt.date
    # data['Ticket Date'] = pd.to_datetime(data['Ticket Date'])


    st.title("Select Filters")
    with st.form(key='columns_in_form'):
    #st.sidebar.markdown("Select Filters:") 
        period_list = data["Endpoint details Resource Device Type"].unique().tolist()
        server_name = st.selectbox("Server Name", period_list, index=0, help='Choose by which server you want to look at the metrics. The default is always the most recent month.')
        start_date = st.date_input("Select the Start Date", datetime.date(2021, 5, 6), help='Choose the start time period you want to look at the metrics. The default is always the most start of the dataset.')
        end_date = st.date_input("Select the End Date", datetime.date(2022, 4, 30), help='Choose the end time period you want to look at the metrics. The default is always the most end of the dataset.')
        st.form_submit_button("Apply")
    
    #Data Filtering
    data['Ticket Date']= pd.to_datetime(data['Ticket Date']).dt.date
    datafilter = data[
        (data['Endpoint details Resource Device Type'] == server_name)
    ]
    mask = (datafilter['Ticket Date'] > start_date) & (datafilter['Ticket Date'] <= end_date)
    datafilter = datafilter.loc[mask]
  
    # Count of Tickets on datewise
    df = datafilter.copy()
    df = df[['Ticket Date', 'Family Condition Details Family Name']]
    df = df.groupby([pd.Grouper(key='Ticket Date')]).agg('count')
    df = df.reset_index()
    df = df.rename(columns={'Family Condition Details Family Name':'count'})
    fig = px.area(df, x='Ticket Date', y='count')
    st.plotly_chart(fig, use_container_width=True)


    # Distribution of Server Endpoint
    fig1 = px.pie(datafilter, names='Family Condition Details Family Name', title='Family Name')
    st.plotly_chart(fig1, use_container_width=True)


    # fig2 = px.bar(data, x='Priority Details Priority Name',color='Priority Details Priority Name',title='Ticket Priority')
    # st.plotly_chart(fig2, use_container_width=True)

    # dict_server = {"Server":['Linux Server','Vault Appliance','Public IP','SNMP'], "Average monthly":[200,143,96,38],"Parrtner name":["lmstech","eCLIPSE Network Solutions LLC","Bralin Technology Solutions","XONICWAVELLC"],"Family Conditions":["RMM Agent","Backup","General(Up/Down/Reboot)","Disk space"]}
    # dict_server1 = pd.DataFrame(dict_server)
    # st.write(dict_server1)

    
    #st.sidebar.title("Select Filters")

   # with st.sidebar.form(key='columns_in_form'):
        #st.sidebar.markdown("Select Filters:") 
    #    period_list=data["Endpoint details Resource Device Type"].unique().tolist()
    #    st.sidebar.selectbox("Server Name", period_list, index=0, help='Choose by which server you want to look at the metrics. The default is always the most recent month.')
    #    st.sidebar.date_input("Select the Start Date", datetime.date(2021, 1, 1), help='Choose the start time period you want to look at the metrics. The default is always the most start of the year.')
    #    st.sidebar.date_input("Select the End Date", datetime.date(2021, 12, 31), help='Choose the end time period you want to look at the metrics. The default is always the most end of the year.')