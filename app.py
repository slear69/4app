import streamlit as st
import easyocr
import numpy as np
import re
from PIL import Image, ImageEnhance

# ---------------------------
# STREAMLIT UI
# ---------------------------

st.set_page_config(page_title="Скенер за добавки", page_icon="⚠️")

st.title("⚠️ Скенер за вредни добавки")
st.write("Качи снимка или използвай камера.")

# ---------------------------
# OCR READER
# ---------------------------

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])


# ---------------------------
# IMAGE PREPROCESSING
# ---------------------------

def preprocess_image(image):

    image = image.convert("RGB")

    # increase contrast
    image = ImageEnhance.Contrast(image).enhance(2)

    # sharpen
    image = ImageEnhance.Sharpness(image).enhance(2)

    return image


# ---------------------------
# FIX OCR TEXT (VERY IMPORTANT)
# ---------------------------

def clean_ocr_text(text):

    text = text.upper()

    # OCR fixes
    text = text.replace("G", "E")
    text = text.replace("[", "E")
    text = text.replace("O", "0")

    text = re.sub(r"\s+", " ", text)

    return text


# ---------------------------
# OCR FUNCTION
# ---------------------------

def extract_text(image):

    reader = load_reader()

    img_array = np.array(image)

    results = reader.readtext(img_array)

    text = " ".join([r[1] for r in results])

    return clean_ocr_text(text)


# ---------------------------
# DETECTOR (FIXED + ROBUST)
# ---------------------------

def find_harmful_ingredients(text):

    harmful = {

        # COLORANTS
        "E102": "Оцветител",
        "E104": "Оцветител",
        "E110": "Оцветител",
        "E122": "Оцветител",
        "E123": "Оцветител",
        "E127": "Оцветител",
        "E131": "Оцветител",
        "E133": "Оцветител",
        "E151": "Оцветител",

        # PRESERVATIVES
        "E211": "Консервант",
        "E220": "Консервант",
        "E250": "Консервант",

        # FLAVOR
        "E621": "Овкусител",
        "E631": "Овкусител",
        "E635": "Овкусител",

        # SWEETENERS
        "E950": "Подсладител",
        "E951": "Аспартам",
        "E952": "Подсладител",
        "E954": "Подсладител",

        # STABILIZERS
        "E407": "Стабилизатор",
        "E410": "Стабилизатор",
        "E412": "Стабилизатор",
        "E415": "Стабилизатор",
        "E450": "Стабилизатор",

        # OTHER
        "E300": "Антиоксидант",
        "E330": "Киселинен регулатор",
        "E262": "Консервант",
    }

    found = []

    text = text.upper()

    # FIX OCR BROKEN NUMBERS
    text = text.replace("G", "E")
    text = text.replace("[", "E")

    # extract ALL E numbers even broken ones
    matches = re.findall(r"E\s*\d{2,3}", text)

    normalized = []

    for m in matches:
        num = re.sub(r"\D", "", m)
        normalized.append(f"E{num}")

    # check matches
    for item in normalized:
        if item in harmful:
            found.append((item, harmful[item]))

    return found


# ---------------------------
# INPUTS
# ---------------------------

uploaded = st.file_uploader("📤 Качи снимка", type=["png", "jpg", "jpeg"])
camera = st.camera_input("📷 Камера")

image = None

if uploaded:
    image = Image.open(uploaded)

elif camera:
    image = Image.open(camera)


# ---------------------------
# MAIN LOGIC
# ---------------------------

if image:

    st.image(image, caption="Снимка", use_container_width=True)

    processed = preprocess_image(image)

    with st.spinner("🔍 Сканиране..."):

        text = extract_text(processed)

        results = find_harmful_ingredients(text)

    st.subheader("📝 Разпознат текст")

    with st.expander("Покажи текста"):
        st.write(text)

    st.subheader("⚠️ Резултати")

    if results:

        st.error("Открити са вредни добавки!")

        for e, name in results:
            st.warning(f"❌ {e} → {name}")

    else:
        st.success("✅ Няма открити вредни добавки")
