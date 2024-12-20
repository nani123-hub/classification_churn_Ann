import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import sklearn

model =load_model('model.h5')

with open('onehot_encoder.pkl','rb') as file:
  onehot_encoder=pickle.load(file)

with open('label_encoder_gender.pkl','rb') as file:
  label_encoder_gender=pickle.load(file)

with open('scaler.pkl','rb') as file:
  scaler=pickle.load(file)

st.title('Customer Churn Prediction')
geography =st.selectbox('Geography',onehot_encoder.categories_[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age= st.slider('Age',18,92)
balance= st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products =st.slider('Number of Products',1,4)
has_cr_card =st.selectbox('Has Credit Card', [0,1])
is_active_member =st.selectbox('Is Active Member',[0,1])
  
input_data={
    'CreditScore':[credit_score],
    'Gender': [gender],
    'Age': [age],
    'Geography': [geography],
    'Tenure' : [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
}
geo_encoded = onehot_encoder.transform([[geography]])
geo_encoded_df = pd.DataFrame(geo_encoded,columns=onehot_encoder.get_feature_names_out(['Geography']))

input_data=pd.DataFrame(input_data)

input_data =pd.concat([input_data.drop('Geography',axis=1),geo_encoded_df],axis=1)
input_data['Gender']=label_encoder_gender.transform(input_data['Gender'])

input_data_scaled=scaler.transform(input_data)

prediction=model.predict(input_data_scaled)
prediction_prob=prediction[0][0]
st.write('churn probability',prediction_prob)
if prediction_prob>0.5:
  st.write('customer likely to churn')
else:
  st.write('customer not likely to churn')
