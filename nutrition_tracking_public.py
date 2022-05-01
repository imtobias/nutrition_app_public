import numpy as np
import pandas as pd
import streamlit as st

st.header('Track calories and macros')
st.write("""The calculator below provides daily targets for calories and macros (grams of protein, fat, carb) to achieve your target weekly weight loss, given
your baseline calories and body weight. To find your baseline daily calorie amount, follow the procedure described on this [fat loss page](https://share.streamlit.io/imtobias/fat_loss/main/fat_loss.py).

This [Wolfram app](https://www.wolframalpha.com/widgets/gallery/view.jsp?id=a9eaa1e9113c865b755f4c9aa0675d3c) identifies your food's calories and macros: Enter
something like \"1/2 cup rice + 1 lb chicken breast boneless skinless\" to get the desired information.""")
#have to change this to csv to make it work after deploying
df = pd.read_csv('nutrition_template.csv')
df['Date'] = df['Date'].astype(str).str[:10]
st.subheader('Inputs')
baseline_calories = st.number_input('Baseline calories', value=3000, min_value=0)
body_weight = st.number_input('Body weight (lb)', value=193, min_value=0)
target_loss_percent = float(st.selectbox(label='Target weekly weight loss, as a percent of bodyweight',\
    options=['0.5%','0.75%','1%'])[:-1]) / 100
target_loss_pounds = body_weight * target_loss_percent
calories_to_cut = target_loss_pounds * 500
target_calories = int(baseline_calories - calories_to_cut)
fat_grams = int(0.4 * body_weight)
protein_grams = body_weight
carb_grams = int((target_calories - 9 * fat_grams - 4 * protein_grams) / 4)

st.subheader('Daily targets')
df_target = pd.DataFrame([[target_calories,fat_grams,protein_grams,carb_grams]])
df_target = df_target.rename(columns={0:'Calories',1:'Fat',2:'Protein',3:'Carbs'})
st.write(df_target)

st.subheader('Adherence to target')
st.write("""Upload data to track daily adherence to suggested daily targets. Update your data as formatted in the template (provide link to Github). The Meal and Food
columns are for your personal use, and do not affect aggregation into daily data. Keep data
as CSV; Streamlit is currently not processing .xlsx files.""")
user_data = st.file_uploader('Upload food data')

if user_data is not None:
    user_data = pd.read_csv(user_data)
    df = user_data

distances = df.groupby(['Date']).sum()
distances = distances.sort_values('Date',ascending=False)
distances['Calories'] -= target_calories
distances['Fat'] -= fat_grams
distances['Protein'] -= protein_grams
distances['Carbs'] -= carb_grams

st.write(distances)
st.write('A negative number means we need more; a positive number means we had an excess. For example, -500 calories means we need 500 more calories to reach the\
    daily target.')

st.subheader('Daily data')
st.write(df.groupby(['Date']).sum().sort_values('Date',ascending=False))


st.subheader('Full data')
st.write(df.sort_values('Date',ascending=False))
