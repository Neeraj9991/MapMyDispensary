import streamlit as st
import pandas as pd
from geopy.distance import geodesic
from streamlit_javascript import st_javascript

st.set_page_config(page_title="Map My Dispensaryr", layout="wide")
st.title("Map My Dispensary")

# Upload dispensary Excel
uploaded_file = st.file_uploader("Upload Dispensary Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("All Dispensaries")
    st.dataframe(df)

    st.markdown("---")
    st.subheader("Finding Nearest Dispensary Automatically...")

    # Step 1: Get user location via browser
    user_loc = st_javascript("navigator.geolocation.getCurrentPosition(pos => [pos.coords.latitude, pos.coords.longitude]);", key="gps")
    
    if user_loc:
        user_lat, user_lon = user_loc
        st.success(f"Your location detected: {user_lat:.6f}, {user_lon:.6f}")

        # Step 2: Find nearest dispensary
        nearest = None
        min_distance = float('inf')
        for index, row in df.iterrows():
            facility_loc = (row['Lattitude'], row['Longitude'])
            distance = geodesic((user_lat, user_lon), facility_loc).km
            if distance < min_distance:
                min_distance = distance
                nearest = row

        if nearest is not None:
            st.subheader("Nearest Dispensary")
            st.write(f"**{nearest['Facility Name']} ({nearest['Facility Type']})**")
            st.write(f"Distance: {min_distance:.2f} km")

            # Step 3: Button to open Google Maps
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={nearest['Lattitude']},{nearest['Longitude']}"
            st.markdown(f"[Open in Google Maps]({maps_url})", unsafe_allow_html=True)
    else:
        st.warning("Waiting for location detection... Please allow location access in your browser.")
