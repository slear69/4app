import streamlit as st

st.title("zdravei test po mat")
age = st.number_input("ваведи години",min_value=0 , max_value=120)
name = st.text_input("ваведи име")
point= 0 
if st.button("краи"):
  st.success('готово')
  st.write("ти си",name,"на",age)

st.title("1 задача - 1т.")
answer=st.number_input("колко е 4^3")
if answer >= 64:
  st.success('правилно :D 1 т.')
  point = point + 1
elif answer != 64:
  st.warning('грешен отговор 0 т. >:(')

st.title("da / ne")
answer = st.radio("обичаш ли програмиранет ",("да","не"))

if answer == "да":
  st.success('peak python the best')
  st.write('fuck zlati')
else:
  st.warning('no such answer aloud')
 
