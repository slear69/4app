import streamlit as st

st.title("zdravei")
age = st.number_input("ваведи години")
name = st.text_input("ваведи име")

if st.button("краи"):
  st.success('готово')
  st.write("ти си",name,"на",age)

st.title("godini")

if age >= 18:
  st.success('ти си пулнолетен')
  st.write('ти си на',age,'заповядаи в p didy party')
else:
  sr.warning('няма да отивам в затвора')

st.title("da / ne")
answer = st.radio("обичаш ли програмиранет ",("да","не"))

if answer == "da":
  st.success('peak python the best')
  st.write('fuck zlati')
else:
  sr.warning('no such answer aloud')
  break
