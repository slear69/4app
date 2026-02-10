import streamlit as st

st.title("zdravei test po mat")
age = st.number_input("ваведи години",min_value=0 , max_value=120)
name = st.text_input("ваведи име")
point= 0 
if st.button("краи"):
  st.success('готово')
  st.write("ти си",name,"на",age)

st.title("1 задача - 1т.")
answere=st.number_input("колко е 4^3")
if st.button('предаи'):
    if answere >= 64:
       st.success('правилно :D 1 т.')
       point = point + 1
    st.title("da / ne - 1т.")
    answer = st.radio("молната маса равна ли е на Mm = m/n ",("да","не"))
    if answer == "да":
       st.success('браво 1т.')
       point = point + 1
    else:
       st.warning('грешно имаш',point)
 
