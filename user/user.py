import streamlit as st
import firebase_admin
from firebase_admin import firestore
import pandas as pd
import numpy as np
from datetime import datetime

front_balance_data , side_balance_data, star_data = {}, {}, {}
scissors_data, arabesque_data, passé_data = {}, {}, {}
firebase_admin.get_app()
db = firestore.client()
doc_ref = db.collection("users").document(st.session_state.user_id)
collec_ref = doc_ref.collection("scores")

if collec_ref:
    for doc in collec_ref.stream():
        if doc.id == "front balance":
            front_balance_data = doc.to_dict()

        elif doc.id == "side balance":
            side_balance_data = doc.to_dict()
        
        elif doc.id == "star jump":
            star_data = doc.to_dict()

        elif doc.id == "scissors leap":
            scissors_data = doc.to_dict()

        elif doc.id == "pivot arabesque":
            arabesque_data = doc.to_dict()

        elif doc.id == "pivot passé":
            passé_data = doc.to_dict()

data = st.session_state.user
st.header(f'Welcome {data["name"]}')

def format_time(time_key):
    """Format time to exclude seconds - shows date, hour, and minutes only"""
    try:
        # Try parsing as datetime string if it's a string
        if isinstance(time_key, str):
            # Try common datetime formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
                try:
                    dt = datetime.strptime(time_key, fmt)
                    return dt.strftime('%Y-%m-%d %H:%M')
                except ValueError:
                    continue
            # If parsing fails, return as is
            return time_key
        elif isinstance(time_key, datetime):
            return time_key.strftime('%Y-%m-%d %H:%M')
        else:
            return str(time_key)
    except:
        return str(time_key)

st.title("Performance Graphs")

# Row 1: Front Balance and Side Balance
col1, col2 = st.columns(2)

with col1:
    st.subheader("Front Balance")
    if front_balance_data:
        df = pd.DataFrame({
            'time': [format_time(key) for key in front_balance_data.keys()],
            'score': [inner["Scroe"] for inner in front_balance_data.values()]
        })
        st.line_chart(df, x='time', y='score')
    else:
        st.info("No data available")

with col2:
    st.subheader("Side Balance")
    if side_balance_data:
        df = pd.DataFrame({
            'time': [format_time(key) for key in side_balance_data.keys()],
            'score': [inner["Scroe"] for inner in side_balance_data.values()]
        })
        st.line_chart(df, x='time', y='score')
    else:
        st.info("No data available")

# Row 2: Star Jump and Scissors Leap
col3, col4 = st.columns(2)

with col3:
    st.subheader("Star Jump")
    if star_data:
        df = pd.DataFrame({
            'time': [format_time(key) for key in star_data.keys()],
            'score': [inner["Scroe"] for inner in star_data.values()]
        })
        st.line_chart(df, x='time', y='score')
    else:
        st.info("No data available")

with col4:
    st.subheader("Scissors Leap")
    if scissors_data:
        df = pd.DataFrame({
            'time': [format_time(key) for key in scissors_data.keys()],
            'score': [inner["Scroe"] for inner in scissors_data.values()]
        })
        st.line_chart(df, x='time', y='score')
    else:
        st.info("No data available")

# Row 3: Pivot Arabesque and Pivot Passé
col5, col6 = st.columns(2)

with col5:
    st.subheader("Pivot Arabesque")
    if arabesque_data:
        df = pd.DataFrame({
            'time': [format_time(key) for key in arabesque_data.keys()],
            'score': [inner["Scroe"] for inner in arabesque_data.values()]
        })
        st.line_chart(df, x='time', y='score')
    else:
        st.info("No data available")

with col6:
    st.subheader("Pivot Passé")
    if passé_data:
        df = pd.DataFrame({
            'time': [format_time(key) for key in passé_data.keys()],
            'score': [inner["Scroe"] for inner in passé_data.values()]
        })
        st.line_chart(df, x='time', y='score')
    else:
        st.info("No data available")