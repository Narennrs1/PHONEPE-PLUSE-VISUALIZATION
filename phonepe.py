import streamlit as st
import os
import pandas as pd
import json
import psycopg2
import requests
import plotly.express as px
import numpy as np

#SQL TABLE TO DATA FRAME

mydb=psycopg2.connect(host='localhost',user='postgres',password='Sql0991',database='phonepe',port=5432)
cursor=mydb.cursor()

query1='''select * from aggregated_transaction'''
cursor.execute(query1)
mydb.commit()
d1=cursor.fetchall()
agre_tran=pd.DataFrame(d1,columns=("States",
                        "year",
                        'quater',
                        'transaction_type',
                        'transaction_count',
                        'transaction_amount'))
#REPLACE THE SPELLING FOR MAP AND FOR OTHE VISUALISATION
agre_tran.States=agre_tran.States.str.title()
agre_tran['States']=agre_tran['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
agre_tran['States']=agre_tran['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
agre_tran['States']=agre_tran['States'].str.replace('-',' ')

query2='''select * from aggregated_user'''
cursor.execute(query2)
mydb.commit()
d2=cursor.fetchall()
agre_use=pd.DataFrame(d2,columns=('States',
                                          'year',
                                          'quater',
                                          'brand',
                                          'transaction_count',
                                          'percentage'))

agre_use.States=agre_use.States.str.title()
agre_use['States']=agre_use['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
agre_use['States']=agre_use['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
agre_use['States']=agre_use['States'].str.replace('-',' ')

query3='''select * from map_transaction'''
cursor.execute(query3)
mydb.commit()
d3=cursor.fetchall()
map_tran=pd.DataFrame(d3,columns=('States',
                                    'year',
                                    'quater',
                                    'district',
                                    'transaction_count',
                                    'transaction_amount'))

map_tran.States=map_tran.States.str.title()
map_tran['States']=map_tran['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
map_tran['States']=map_tran['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
map_tran['States']=map_tran['States'].str.replace('-',' ')

query4='''select * from map_user'''
cursor.execute(query4)
mydb.commit()
d4=cursor.fetchall()
map_use=pd.DataFrame(d4,columns=('States',
                                   'year',
                                   'quater',
                                   'districts',
                                   'registeredUsers',
                                   'appOpens'))

map_use.States=map_use.States.str.title()
map_use['States']=map_use['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
map_use['States']=map_use['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
map_use['States']=map_use['States'].str.replace('-',' ')

query5='''select * from top_transaction'''
cursor.execute(query5)
mydb.commit()
d5=cursor.fetchall()
top_tran=pd.DataFrame(d5,columns=('States',
                                        'year',
                                        'quater',
                                        'pincodes',
                                        'transaction_count',
                                        'transaction_amount'))

top_tran.States=top_tran.States.str.title()
top_tran['States']=top_tran['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
top_tran['States']=top_tran['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
top_tran['States']=top_tran['States'].str.replace('-',' ')

query6='''select * from top_user'''
cursor.execute(query6)
mydb.commit()
d6=cursor.fetchall()
top_use=pd.DataFrame(d6,columns=('States',
                                        'year',
                                        'quater',
                                        'pincodes',
                                        'registeredUsers'))


top_use.States=top_use.States.str.title()
top_use['States']=top_use['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
top_use['States']=top_use['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
top_use['States']=top_use['States'].str.replace('-',' ')

#INDIA MAP PLOTTING
def geo_ta():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    Gdata1=json.loads(response.content)

    fig = px.choropleth(
                    agre_tran,
                    geojson=Gdata1,
                    locations= "States",
                    featureidkey= "properties.ST_NM",
                    color= "transaction_amount", 
                    color_continuous_scale="Sunsetdark", 
                    range_color= (0,3000000),
                    title="TRANSACTION AMOUNT", 
                    hover_name= "States", 
                    animation_frame= "year", 
                    animation_group= "quater")

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600,width=700)
    return st.plotly_chart(fig)

#BAR PLOT FOR TC
def transaction_count():
    agcn=agre_tran[["transaction_type","transaction_count"]]
    agcn1=agcn.groupby('transaction_type')['transaction_count'].sum()
    dfagcn=pd.DataFrame(agcn1).reset_index()
    fig_ty=px.bar(dfagcn,x='transaction_type',y='transaction_count',title="TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Blackbody_r)
    fig_ty.update_layout(width=600,height=400)
    return st.plotly_chart(fig_ty)

#INDAI MAP 2
def geo_tc():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    Gdata1=json.loads(response.content)

    map2=agre_tran[['States','transaction_count','quater','year']]
    
    fig = px.choropleth(
                    map2,
                    geojson=Gdata1,
                    locations= "States",
                    featureidkey= "properties.ST_NM",
                    color= "transaction_count", 
                    color_continuous_scale="solar", 
                    range_color= (0,3000000),
                    title="TRANSACTION COUNT", 
                    hover_name= "States", 
                    animation_frame= "year", 
                    animation_group= "quater")

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600,width=700)
    return st.plotly_chart(fig)

#BAT PLOT FOR TA
def transaction_amt():
    agty=agre_tran[["transaction_type","transaction_amount"]]
    agty1=agty.groupby('transaction_type')['transaction_amount'].sum()
    dfagty=pd.DataFrame(agty1).reset_index()
    fig_ty=px.bar(dfagty,x='transaction_type',y='transaction_amount',title="TRANSACTION TYPE",color_discrete_sequence=px.colors.sequential.Blackbody_r)
    fig_ty.update_layout(width=600,height=400)
    return st.plotly_chart(fig_ty)

def trans_amt_yr(yr):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tra.sort()

    agre_tran.States=agre_tran.States.str.title()
    agre_tran['States']=agre_tran['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
    agre_tran['States']=agre_tran['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
    agre_tran['States']=agre_tran['States'].str.replace('-',' ')
    
    year= int(yr)
    yr1= agre_tran[["States","year","transaction_amount"]]
    yr2= yr1.loc[(agre_tran["year"]==year)]
    yr3= yr2.groupby("States")["transaction_amount"].sum()
    yrby= pd.DataFrame(yr3).reset_index()

    fig_yr= px.choropleth(yrby, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "transaction_amount", color_continuous_scale="RdBu", range_color=(0,800000000000),
                            title="TRANSACTION AMOUNT BY YEAR", hover_name= "States")

    fig_yr.update_geos(fitbounds= "locations", visible= False)
    fig_yr.update_layout(width=600,height=700)
    return st.plotly_chart(fig_yr)

def trans_countby_yr(yr):
    year= int(yr)
    cu1= agre_tran[["transaction_type", "year", "transaction_count"]]
    cu2= cu1.loc[(agre_tran["year"]==year)]
    cu3= cu2.groupby("transaction_type")["transaction_count"].sum()
    cuyr= pd.DataFrame(cu3).reset_index()

    fig_cuyr= px.bar(cuyr,x= "transaction_type", y= "transaction_count", title= "TRANSACTION COUNT BY TYPE",
                    color_discrete_sequence=px.colors.sequential.BuPu_r)
    fig_cuyr.update_layout(width=600, height=500)
    return st.plotly_chart(fig_cuyr)

def trans_cnt_yr(yr):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)

    agre_tran.States=agre_tran.States.str.title()
    agre_tran['States']=agre_tran['States'].replace(['Andaman-&-Nicobar-Islands'],'Andaman & Nicobar')
    agre_tran['States']=agre_tran['States'].replace(['Dadra-&-Nagar-Haveli-&-Daman-&-Diu'],'Dadra and Nagar Haveli and Daman and Diu')
    agre_tran['States']=agre_tran['States'].str.replace('-',' ')
    
    year= int(yr)
    yr1= agre_tran[["States","year","transaction_count"]]
    yr2= yr1.loc[(agre_tran["year"]==year)]
    yr3= yr2.groupby("States")["transaction_count"].sum()
    yrby= pd.DataFrame(yr3).reset_index()

    fig_yr= px.choropleth(yrby, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "transaction_count", color_continuous_scale="RdBu", range_color=(0,800000000000),
                            title="TRANSACTION COUNT BY YEAR", hover_name= "States")

    fig_yr.update_geos(fitbounds= "locations", visible= False)
    fig_yr.update_layout(width=600,height=700)
    return st.plotly_chart(fig_yr)

def trans_amtby_yr(yr):
    year= int(yr)
    cu1= agre_tran[["year", "transaction_type", "transaction_amount"]]
    cu2= cu1.loc[(agre_tran["year"]==year)]
    cu3= cu2.groupby("transaction_type")["transaction_amount"].sum()
    cuyr= pd.DataFrame(cu3).reset_index()

    fig_cuyr= px.bar(cuyr,x= "transaction_type", y= "transaction_amount", title= "TRANSACTION COUNT BY TYPE",
                    color_discrete_sequence=px.colors.sequential.BuPu_r)
    fig_cuyr.update_layout(width=600, height=500)
    return st.plotly_chart(fig_cuyr)

# TOP QUESTION
def qus1():
    brand= map_tran[["district","transaction_amount"]]
    brand1= brand.groupby("district")["transaction_amount"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index().head(10)

    fig_brd= px.pie(brand2, values= "transaction_amount", names= "district", color_discrete_sequence=px.colors.sequential.algae_r,
                       title= "TOP 10 DISTRICTS OF HIGHEST TRANSACTION")
    return st.plotly_chart(fig_brd)

def qus2():
    brand= map_tran[["district","transaction_amount"]]
    brand1= brand.groupby("district")["transaction_amount"].sum().sort_values(ascending=True)
    brand2= pd.DataFrame(brand1).reset_index().head(10)

    fig_brd= px.pie(brand2, values= "transaction_amount", names= "district", color_discrete_sequence=px.colors.sequential.algae_r,
                       title= "TOP 10 DISTRICTS OF LOWEST TRANSACTION")
    return st.plotly_chart(fig_brd)

def qus3():
    lowt= agre_tran[["States","transaction_amount"]]
    lowt1= lowt.groupby("States")["transaction_amount"].sum().sort_values(ascending=False)
    lowt2= pd.DataFrame(lowt1).reset_index().head(15)

    fig_lt= px.bar(lowt2, x= "States", y= "transaction_amount", title= "HIGHTEST TRANSACTION and STATES",
                color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_lt.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_lt)

def qus4():
    lowt= agre_tran[["States","transaction_amount"]]
    lowt1= lowt.groupby("States")["transaction_amount"].sum().sort_values(ascending=True)
    lowt2= pd.DataFrame(lowt1).reset_index().head(15)

    fig_lt= px.bar(lowt2, x= "States", y= "transaction_amount", title= "LOWEST TRANSACTION and STATES",
                color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_lt.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_lt)
def qus5():
    lowt= map_use[["States","appOpens"]]
    lowt1= lowt.groupby("States")["appOpens"].sum().sort_values(ascending=False)
    lowt2= pd.DataFrame(lowt1).reset_index().head(10)

    fig_lt= px.bar(lowt2, x= "States", y= "appOpens", title= "HIGHTEST STATES WITH APPOPENS",
                color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_lt.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_lt)
def qus6():
    lowt= map_use[["States","appOpens"]]
    lowt1= lowt.groupby("States")["appOpens"].sum().sort_values(ascending=True)
    lowt2= pd.DataFrame(lowt1).reset_index().head(10)

    fig_lt= px.bar(lowt2, x= "States", y= "appOpens", title= "LOWEST STATES WITH APPOPENS",
                color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_lt.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_lt)

def qus7():
    lowt= agre_tran[["States","transaction_count"]]
    lowt1= lowt.groupby("States")["transaction_count"].sum().sort_values(ascending=False)
    lowt2= pd.DataFrame(lowt1).reset_index()

    fig_lt= px.bar(lowt2, x= "States", y= "transaction_count", title= "HIGHEST COUNT and STATES",
                color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_lt.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_lt)

def qus8():
    lowt= agre_tran[["States","transaction_count"]]
    lowt1= lowt.groupby("States")["transaction_count"].sum().sort_values(ascending=True)
    lowt2= pd.DataFrame(lowt1).reset_index()

    fig_lt= px.bar(lowt2, x= "States", y= "transaction_count", title= "LOWEST COUNT and STATES",
                color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_lt.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_lt)

def qus9():
    brand= map_tran[["district","transaction_amount"]]
    brand1= brand.groupby("district")["transaction_amount"].sum().sort_values(ascending=True)
    brand2= pd.DataFrame(brand1).reset_index().head(20)

    fig_brd= px.bar(brand2, x= "district", y= "transaction_amount", color_discrete_sequence=px.colors.sequential.Oranges_r,
                       title= "DISTRICTS TO LOWEST TRANSACTION")
    return st.plotly_chart(fig_brd)

def qus10():
    brand= agre_use[["brand","transaction_count"]]
    brand1= brand.groupby("brand")["transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brd= px.pie(brand2, values= "transaction_count", names= "brand", color_discrete_sequence=px.colors.sequential.algae_r,
                       title= "Top Mobile Brands and Transaction_count")
    return st.plotly_chart(fig_brd)

st.set_page_config(layout="wide")

st.header(":violet[PHONEPE DATA VISUALIZATION AND EXPLORAION]")
st.caption(":violet[India's Leading Digital Payment And Banking Service Provider]")
tab1,tab2,tab3=st.tabs(["***HOME***","***DATA VISUALIZATION***","***TOP DATA***"])

with tab1:
    cl1,cl2,cl3=st.columns(3)

    with cl1:
        on=st.toggle(":violet[ABOUT]")
        if on:
            st.write('''The narrative of Indian digital payments has definitely captivated the world's attention. From the greatest cities to the most distant villages, mobile phone and data penetration is driving a payments revolution''')
            st.write(""
                     "")
            st.write('''When PhonePe first launched five years ago, we were continuously on the lookout for authoritative data sources on digital payments in India. We were looking for answers to queries such,How are consumers truly using digital payments? What are the most notable cases? Is the penetration of QR codes giving kiranas in Tier 2 and 3 a facelift?
We resolved to demystify the what, why, and how of digital payments in India this year, as we became India's largest digital payments platform with a 46% UPI market share.''')
    
    with cl2:
        on=st.toggle(":violet[FEATURE]")
        if on:
            st.selectbox(
                    "",
                    ("Easy Interface", "Payment To Merchant", "Fund Transfer","Recharge and Bill Payments",
                        "Buy & Sell Gold","PhonePe ATM"),
                    index=None,
                    placeholder="Explore The Feature"
                    )

    with st.container():
        videofile=open("D:\\DTM9\\CAPSTONE PROJECT 2\\Phonepvideo.mp4",'rb')
        vid=videofile.read()
        st.video(vid)

with tab2:
    yr1=st.selectbox(":violet[SELECT THE DESIRED OPTION]",
                    ("ALL","2018","2019","2020","2021","2022","2023"),index=None,placeholder="SELECT THE YEAR")
    if yr1=="ALL":
        cl1,cl2=st.columns(2)
        with cl1:
            geo_ta()
            transaction_count()
            geo_tc()
            transaction_amt()
        with cl2:
            st.write(" ")
    elif yr1=="2018":
        cl1,cl2=st.columns(2)
        with cl1:
            trans_amt_yr(yr1)
            trans_cnt_yr(yr1)
        with cl2:
            st.write(" ")
    elif yr1=="2019":
        cl1,cl2=st.columns(2)
        with cl1:
            trans_amt_yr(yr1)
            trans_cnt_yr(yr1)
        with cl2:
            st.write(" ")
    elif yr1=="2020":
        cl1,cl2=st.columns(2)
        with cl1:
            trans_amt_yr(yr1)
            trans_cnt_yr(yr1)
        with cl2:
            st.write(" ")
    elif yr1=="2021":
        cl1,cl2=st.columns(2)
        with cl1:
            trans_amt_yr(yr1)
            trans_cnt_yr(yr1)
        with cl2:
            st.write(" ")
    elif yr1=="2022":
        cl1,cl2=st.columns(2)
        with cl1:
            trans_amt_yr(yr1)
            trans_cnt_yr(yr1)
        with cl2:
            st.write(" ")
    elif yr1=="2023":
        cl1,cl2=st.columns(2)
        with cl1:
            trans_amt_yr(yr1)
            trans_cnt_yr(yr1)
        with cl2:
            st.write(" ")

with tab3:
    on=st.toggle("TOP 10 DISTRICTS AND THIER TRANSACTION AMOUNT")
    if on:
        qus1()
        qus2()

    on1=st.toggle("STATES BY TRANSACTION AMOUNT")
    if on1:
        qus3()
        qus4()

    on2=st.toggle("STATES BY APP OPENING")
    if on2:
        qus5()
        qus6()
    on3=st.toggle("STATES BY TRANSACTION COUNT")
    if on3:
        qus7()
        qus8()
    on4=st.toggle("DISTRICTS HAVING LOWEST TRANSACTION AMOUNT")
    if on4:
        qus9()
    on5=st.toggle("TOP MOBILE AND THIER TRANSACTION")
    if on5:
        qus10()
        
