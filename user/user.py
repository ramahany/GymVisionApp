import streamlit as st
import firebase_admin
from firebase_admin import firestore
import pandas as pd
import numpy as np

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


# Front balance graph and data
st.title("Front Balance Graph")
df = pd.DataFrame({
    'time': front_balance_data.keys(),
    'score': [inner["Scroe"] for inner in front_balance_data.values()]
})
# df['time'] = pd.to_datetime(df['time'])  # Convert to datetime if needed

st.line_chart(df, x='time', y='score')

# side balance graph and data
st.title("Side Balance Graph")

df = pd.DataFrame({
    'time': side_balance_data.keys(),
    'score': [inner["Scroe"] for inner in side_balance_data.values()]
})

# df['time'] = pd.to_datetime(df['time'])  # Convert to datetime if needed

st.line_chart(df, x='time', y='score')

# star graph and data
st.title("Star Jump Graph")
df = pd.DataFrame({
    'time': star_data.keys(),
    'score': [inner["Scroe"] for inner in star_data.values()]
})
# df['time'] = pd.to_datetime(df['time'])  # Convert to datetime if needed

st.line_chart(df, x='time', y='score')

# scissors leap graph and data
st.title("Scissors Leap Graph")
df = pd.DataFrame({
    'time': scissors_data.keys(),
    'score': [inner["Scroe"] for inner in scissors_data.values()]
})
# df['time'] = pd.to_datetime(df['time'])  # Convert to datetime if needed

st.line_chart(df, x='time', y='score')

# pivot arabesque graph and data
st.title("Pivot Arabesque Graph")
df = pd.DataFrame({
    'time': arabesque_data.keys(),
    'score': [inner["Scroe"] for inner in arabesque_data.values()]
})
# df['time'] = pd.to_datetime(df['time'])  # Convert to datetime if needed

st.line_chart(df, x='time', y='score')

# pivot passé graph and data
st.title("Pivot Passé Graph")
df = pd.DataFrame({
    'time': passé_data.keys(),
    'score': [inner["Scroe"] for inner in passé_data.values()]
})
# df['time'] = pd.to_datetime(df['time'])  # Convert to datetime if needed

st.line_chart(df, x='time', y='score')