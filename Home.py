import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import *
import time
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.offline as pyo
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
# import plotly.plotly_chart

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.subheader("Dashboard")
st.markdown("##")

theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#fetch data
#result = view_all_data()
#df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

 
#load excel file
df=pd.read_csv('synthetic_dataset2.csv')


######## function that generate dates ######
# Function to generate dates
def generate_dates(start_date, end_date, frequency):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))

        if frequency == "monthly":
            current_date = current_date.replace(day=1)  # Move to the first day of the next month
            current_date += timedelta(days=32)  # Add 32 days to ensure we're in the next month
        elif frequency == "quarterly":
            current_date = current_date.replace(day=1, month=((current_date.month - 1) // 3 + 1) * 3 + 1)  # Move to the first day of the next quarter
            current_date += timedelta(days=92)  # Add 92 days to ensure we're in the next quarter
        elif frequency == "yearly":
            current_date = current_date.replace(day=1, month=1)  # Move to the first day of the next year
            current_date += timedelta(days=366)  # Add 366 days to ensure we're in the next year (accounting for leap years)
        else:
            raise ValueError("Invalid frequency specified. Use 'monthly', 'quarterly', or 'yearly'.")

    return date_list


#side bar
# st.sidebar.image("data/logo1.png",caption="www.codegnan.com")

# #switcher
# st.sidebar.header("Please filter")
# region=st.sidebar.multiselect(
#     "Select Region",
#      options=df["Region"].unique(),
#      default=df["Region"].unique(),
# )
# location=st.sidebar.multiselect(
#     "Select Location",
#      options=df["Location"].unique(),
#      default=df["Location"].unique(),
# )
# construction=st.sidebar.multiselect(
#     "Select Construction",
#      options=df["Construction"].unique(),
#      default=df["Construction"].unique(),
# )

# df=df.query(
#     "Region==@region & Location==@location & Construction ==@construction"
# )

def Home():
    with st.expander("Company Stats"):
        showData=st.multiselect('Filter: ',df.columns,default=['Sales', 'Total_Income', 'Net_Profit', 'Cash',
       'Operating_Expense_Ratio', 'Net_Profit_Margin', 'Current_Ratio', 'date',
       'id', 'obs_id', 'salinitySurface', 'Quarter', 'Period'], key="multi1")
    st.dataframe(df[showData],use_container_width=True)
    #compute top analytics
    current_total_income = float(df["Total_Income"].tail(1))
    current_net_profit = float(df["Net_Profit"].tail(1))
    current_cash = float(df["Cash"].tail(1))
    current_operating_expense_ratio= float(df['Operating_Expense_Ratio'].tail(1)) 
    current_net_profit_margin= float(df['Net_Profit_Margin'].tail(1)) 
    current_ratio= float(df['Current_Ratio'].tail(1)) 


    total1,total2,total3,total4,total5,total6=st.columns(6,gap='small')
    with total1:
        st.info('Total_Income',icon="📌")
        st.metric(label="current",value=f"{current_total_income:,.0f}")

    with total2:
        st.info('Net_Profit',icon="📌")
        st.metric(label="current",value=f"{current_net_profit:,.0f}")

    with total3:
        st.info('Cash',icon="📌")
        st.metric(label="current",value=f"{current_cash:,.0f}")

    with total4:
        st.info('Operating_Expense_Ratio',icon="📌")
        st.metric(label="current",value=f"{current_operating_expense_ratio:,.0f}")

    with total5:
        st.info('Net_Profit_Margin',icon="📌")
        st.metric(label="current",value=f"{current_net_profit_margin:.0f}")
    
    with total6:
        st.info('Current_Ratio',icon="📌")
        st.metric(label="current",value=f"{current_ratio:.0f}")

    st.markdown("""---""")




def feature_1():

    
    # Streamlit app
    st.title("Select a Column from DataFrame")

    # Sidebar with options
    selected_column = st.sidebar.selectbox("Select a Column:", df.columns)

    # Display the selected column from the DataFrame
    # st.write(f"Selected Column: {selected_column}")
    # st.write(df[selected_column])



    # Streamlit app
    st.title("Date Range Selector ...date should be after 2020...")

    # Sidebar for user input
    start_date = st.sidebar.date_input("Select a Start Date")
    end_date = st.sidebar.date_input("Select an End Date")

    # Check if the start date is before the end date
    if start_date <= end_date:
        st.write(f"Start Date: {start_date}")
        st.write(f"End Date: {end_date}")
        
        # Convert dates to datetime objects for filtering
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        
   
    # Streamlit app
    st.title("Time Period Selector")

    # Sidebar for user input
    time_period = st.sidebar.selectbox("Select a Time Period:", ["monthly", "quarterly", "yearly"])


    # Function to group data by selected time period
    # def group_data_by_time_period(df, time_period):
    
    if time_period == "monthly":
        monthly_dates = generate_dates(start_date, end_date, "monthly")
        monthly_df = df[df['date'].isin(monthly_dates)].copy()
        dates_d=monthly_dates
    elif time_period == "quarterly":
        quarterly_dates = generate_dates(start_date, end_date, "quarterly")
        quarterly_df = df[df['date'].isin(quarterly_dates)].copy()
        dates_d=quarterly_dates
    elif time_period == "yearly":
        yearly_dates = generate_dates(start_date, end_date, "yearly")
        yearly_df = df[df['date'].isin(yearly_dates)].copy()
        dates_d=yearly_dates
        # yearly_df.reset_index(drop=True, inplace=True)

    # Display data based on the selected time period
    
    # st.write(f"Selected Time Period: {selected_option}")
        
    # monthly_df = df[df['date'].isin(monthly_dates)].copy()
    # quarterly_df = df[df['date'].isin(quarterly_dates)].copy()
    # yearly_df = df[df['date'].isin(yearly_dates)].copy()

    # Optionally, reset the index for the new dataframes
    # monthly_df.reset_index(drop=True, inplace=True)
    # quarterly_df.reset_index(drop=True, inplace=True)
    # yearly_df.reset_index(drop=True, inplace=True)

    # Print the new dataframes
    # print("Monthly Dataframe:")
    # print(monthly_df)

    # print("\nQuarterly Dataframe:")
    # print(quarterly_df)

    # print("\nYearly Dataframe:")
    # print(yearly_df)


    st.title("Function Calling on Button Click")

    # Create a button
    if st.button("Plot Graph"):
        # Function to plot a simple graph
        def plot(x1,y1):
            trace1 = go.Scatter(x=x1, y=y1, mode='lines+markers', name='Actual')
            layout = go.Layout(title="Actual")
            fig = go.Figure(data=[trace1], layout=layout)
            # pyo.iplot(fig)
            st.plotly_chart(fig)


        # Call the function

        plot(dates_d,df[selected_column])    


def feature_2():

    
    # Streamlit app
    st.title("Select a Column from DataFrame")

    # Sidebar with options
    selected_column = st.sidebar.selectbox("Select a Column:", df.columns)

    # Display the selected column from the DataFrame
    # st.write(f"Selected Column: {selected_column}")
    # st.write(df[selected_column])


    ###### duration 1 ##############
    # Streamlit app
    st.title("Duration 1 Selector ...date should be after 2020...")

    # Sidebar for user input
    start_date1 = st.sidebar.date_input("Duration 1 : Select a Start Date",key="start_date1")
    end_date1 = st.sidebar.date_input("Duration 1 : Select an End Date",key="end_date1")

    # Check if the start date is before the end date
    if start_date1 <= end_date1:
        st.write(f"Duration 1 : Start Date: {start_date1}")
        st.write(f"Duration 1 : End Date: {end_date1}")
        
        # Convert dates to datetime objects for filtering
        start_date1 = datetime.combine(start_date1, datetime.min.time())
        end_date1 = datetime.combine(end_date1, datetime.max.time())
        
   
    # Streamlit app
    st.title("Duration 1 : Time Period Selector")

    # Sidebar for user input
    time_period1 = st.sidebar.selectbox("Select a Time Period:", ["monthly", "quarterly", "yearly"], key="time_period1")


    # Function to group data by selected time period
    # def group_data_by_time_period(df, time_period):
    
    if time_period1 == "monthly":
        monthly_dates = generate_dates(start_date1, end_date1, "monthly")
        monthly_df = df[df['date'].isin(monthly_dates)].copy()
        dates_d1=monthly_dates
        d1=monthly_df
    elif time_period1 == "quarterly":
        quarterly_dates = generate_dates(start_date1, end_date1, "quarterly")
        quarterly_df = df[df['date'].isin(quarterly_dates)].copy()
        dates_d1=quarterly_dates
        d1=quarterly_df
    elif time_period1 == "yearly":
        yearly_dates = generate_dates(start_date1, end_date1, "yearly")
        yearly_df = df[df['date'].isin(yearly_dates)].copy()
        dates_d1=yearly_dates
        d1=yearly_df
        # yearly_df.reset_index(drop=True, inplace=True)



    ###### duration 2 ##############
    # Streamlit app
    st.title("Duration 2 Selector ...date should be after 2020...")

    # Sidebar for user input
    start_date2 = st.sidebar.date_input("Duration 2 : Select a Start Date",key="start_date2")
    end_date2 = st.sidebar.date_input("Duration 2 : Select an End Date",key="end_date2")

    # Check if the start date is before the end date
    if start_date2 <= end_date2:
        st.write(f"Duration 2 : Start Date: {start_date2}")
        st.write(f"Duration 2 : End Date: {end_date2}")
        
        # Convert dates to datetime objects for filtering
        start_date2 = datetime.combine(start_date2, datetime.min.time())
        end_date2 = datetime.combine(end_date2, datetime.max.time())
        
   
    # Streamlit app
    st.title("Duration 2 : Time Period Selector")

    # Sidebar for user input
    time_period2 = st.sidebar.selectbox("Select a Time Period:", ["monthly", "quarterly", "yearly"], key="time_period2")


    # Function to group data by selected time period
    # def group_data_by_time_period(df, time_period):
    
    if time_period2 == "monthly":
        monthly_dates = generate_dates(start_date2, end_date2, "monthly")
        monthly_df = df[df['date'].isin(monthly_dates)].copy()
        dates_d2=monthly_dates
        d2=monthly_df
    elif time_period2 == "quarterly":
        quarterly_dates = generate_dates(start_date2, end_date2, "quarterly")
        quarterly_df = df[df['date'].isin(quarterly_dates)].copy()
        dates_d2=quarterly_dates
        d2=quarterly_df
    elif time_period2 == "yearly":
        yearly_dates = generate_dates(start_date2, end_date2, "yearly")
        yearly_df = df[df['date'].isin(yearly_dates)].copy()
        dates_d2=yearly_dates 
        d2=yearly_df   





    st.title("Compare two Duration of a Feature")

    # Create a button
    if st.button("Plot Graphs"):
        # Function to plot a simple graph
        def plot(x1,y1):
            trace1 = go.Scatter(x=x1, y=y1, mode='lines+markers', name='Actual')
            layout = go.Layout(title="Actual")
            fig = go.Figure(data=[trace1], layout=layout)
            # pyo.iplot(fig)
            st.plotly_chart(fig)


        # Call the function

        plot(dates_d1,d1[selected_column]) 
        plot(dates_d2,d2[selected_column])   

        


def feature_3():

    
    # Streamlit app
    st.title("Select a Column from DataFrame")

    # Sidebar with options
    selected_column = st.sidebar.selectbox("Select a Column:", df.columns)

    # Display the selected column from the DataFrame
    # st.write(f"Selected Column: {selected_column}")
    # st.write(df[selected_column])



    # Streamlit app
    st.title("Date Range Selector ...date should be after 2020...")

    # Sidebar for user input
    start_date = st.sidebar.date_input("Select a Start Date")
    end_date = st.sidebar.date_input("Select an End Date")

    # Check if the start date is before the end date
    if start_date <= end_date:
        st.write(f"Start Date: {start_date}")
        st.write(f"End Date: {end_date}")
        
        # Convert dates to datetime objects for filtering
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        
   
    # Streamlit app
    st.title("Time Period Selector")

    # Sidebar for user input
    time_period = st.sidebar.selectbox("Select a Time Period:", ["monthly", "quarterly", "yearly"])


    # Function to group data by selected time period
    # def group_data_by_time_period(df, time_period):
    
    if time_period == "monthly":
        monthly_dates = generate_dates(start_date, end_date, "monthly")
        monthly_df = df[df['date'].isin(monthly_dates)].copy()
        dates_d=monthly_dates
        d3=monthly_df 
    elif time_period == "quarterly":
        quarterly_dates = generate_dates(start_date, end_date, "quarterly")
        quarterly_df = df[df['date'].isin(quarterly_dates)].copy()
        dates_d=quarterly_dates
        d3=quarterly_df
    elif time_period == "yearly":
        yearly_dates = generate_dates(start_date, end_date, "yearly")
        yearly_df = df[df['date'].isin(yearly_dates)].copy()
        dates_d=yearly_dates
        d3=yearly_df
        # yearly_df.reset_index(drop=True, inplace=True)



    # Streamlit app
    st.title("Step size : Positive Integer Input (i.e. 30)")

    # User input for a positive integer
    positive_integer = st.number_input("Enter a Positive Integer", min_value=1, value=1, step=1)
    s=positive_integer



    st.title("Click below Button for forecast")

    # Create a button
    if st.button("Plot Forecaste"):

        def compare_forecast(x1,y1,s):

            forecast_dates = pd.date_range(start=x1[-1], periods=s + 1, freq='M')[1:]

            model = ExponentialSmoothing(endog=df[selected_column]).fit()
            predictions = model.forecast(steps=s)
            # print(predictions)
            trace1 = go.Scatter(x=x1, y=y1, mode='lines+markers', name='Actual')
            trace2 = go.Scatter(x=forecast_dates, y=predictions, mode='lines', name='Forecasted',line=dict(color='red'))
            layout = go.Layout(title="Actual vs Forecast")
            fig = go.Figure(data=[trace1, trace2], layout=layout)
            st.plotly_chart(fig)


        compare_forecast(dates_d,d3[selected_column],s) 





def graphs():
    #total_investment=int(df["Investment"]).sum()
    #averageRating=int(round(df["Rating"]).mean(),2)
    
    #simple bar graph
    investment_by_business_type=(
        df.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    fig_investment=px.bar(
       investment_by_business_type,
       x="Investment",
       y=investment_by_business_type.index,
       orientation="h",
       title="<b> Investment by Business Type </b>",
       color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
       template="plotly_white",
    )


    fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
     )

        #simple line graph
    investment_state=df.groupby(by=["State"]).count()[["Investment"]]
    fig_state=px.line(
       investment_state,
       x=investment_state.index,
       y="Investment",
       orientation="v",
       title="<b> Investment by State </b>",
       color_discrete_sequence=["#0083b8"]*len(investment_state),
       template="plotly_white",
    )
    fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
     )

    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df, values='Rating', names='State', title='Regions by Ratings')
      fig.update_layout(legend_title="Regions", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
     
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df["Investment"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Target done !")
    else:
     st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Target Percentage")


def sideBar():

 with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Plot a Feature","Compare Two Durations of a Feature","Forecast a Feature"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    Home()
    # graphs()
 if selected=="Plot a Feature":
    st.subheader(f"Page: {selected}")
    feature_1()
    # Progressbar()
    # graphs()

 if selected=="Compare Two Durations of a Feature":
    st.subheader(f"Page: {selected}")
    feature_2()      

 if selected=="Forecast a Feature":
    st.subheader(f"Page: {selected}")
    feature_3()   

 

sideBar()

# Home()
# feature_1()
# feature_2()
# feature_3()


#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

