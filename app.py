import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk  # for 3D visuals
import plotly.express as px  # for interactive plots

# first we will import the csv file containing our data
DATA_URL = "./resources/Motor_Vehicle_Collisions.csv"


st.title("Motor Vehicle Collisions in New York City")

st.markdown('''Given the increasing reports of road accidents, this application
was made in order to have a better insight regarding motor vehicle accidents
 specifically. We have collected data from various sources and store them in
 a csv file. This file is used to create this dashboard combined with streamlit. ''')


# function that reads the csv and stores it to a dataframe
@st.cache(persist=True)  # to avoid executing the function at every reload
def load_data(nrows):
    # read csv, perform basic operations
    df = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    df.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True) # drop missing values
    lowercase = lambda x: str(x).lower()  # lambda for renaming columns
    df.rename(lowercase, axis='columns', inplace=True)  # turn all columns to lowercase
    df.rename(columns={'crash_date_crash_time' : 'date/time'}, inplace=True)

    return df  # return the formatted df


SIZE = 100000   # we can change if we want more / less data
data = load_data(SIZE)  # these data will change dynamically later on
original_data = data  # static copy of data fro the last part of the app


#  plot in map accidents based on number of injured people
st.header("Where are the most people injured in NYC?")
injured_people = st.slider(   # injured_people are given from a slider
    "Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query(
    "injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))


# collisions during a specific time space
st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour of day:", 0, 23)  # hour selection
data = data[data['date/time'].dt.hour == hour]  # extract only the specified data

# let's plot the previous results to a 3D map
st.markdown("Motor Vehicle Collisions Between %i:00 and %i:00" % (hour, (hour+1)%24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))  # centered coordinates
st.write(pdk.Deck(  # this creates a 3D map
    map_style="mapbox://styles/mapbox/light-v9",  # style of the map
    initial_view_state={  # default state for the map view
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,  # arbitrary value, it works so it's ok
        "pitch": 50  # degree of freedom
    },
    layers=[  # list with all layers in the map (in our case, only 1)
        pdk.Layer(
            "HexagonLayer",  # how to represent each point
            data=data[['date/time', 'latitude', 'longitude']],  # which data are represented
            get_position=['longitude', 'latitude'],
            radius=100,
            extruded=True,  # if True, points are 3D, else they are 2D
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000]
        )
    ]
))

# more details about the collision in the previously specified Hour
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour+1)%24))
filtered = data[  # for interactive data based on hour given from before
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < hour+1)
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]  # group up data based on minute of collision
chart_data = pd.DataFrame({
    'minute': range(60),
    'crashes': hist
})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)  # actual plot
st.write(fig)  # to display the previous diagram into the browser


# find most dangerous streets in NYC
st.header("Top 5 most dangerous street by affected type")
select = st.selectbox(
    "Affected type of people:",   # detail message
    ['Pedestrians', 'Cyclists', 'Motorists']  # options of the selectbox
)
# show appropriate results based on selected category
if select == 'Pedestrians':
    st.write(data.query(
        "injured_pedestrians >= 1")[['on_street_name', 'injured_pedestrians']].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5]
    )
elif select == 'Cyclists':
    st.write(data.query(
        "injured_cyclists >= 1")[['on_street_name', 'injured_cyclists']].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5]
    )
else:
    st.write(data.query(
        "injured_motorists >= 1")[['on_street_name', 'injured_motorists']].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5]
    )


# show dataframe if the box is checked
if st.checkbox("Display Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)
