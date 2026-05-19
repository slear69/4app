# app.py

import streamlit as st
import easyocr
import numpy as np
from PIL import Image, ImageEnhance

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="Harmful Ingredients Scanner",
    page_icon="⚠️",
    layout="centered"
)

st.title("⚠️ Harmful Ingredients Scanner")
st.write("Upload a food label image or take a photo.")

# ---------------------------
# HARMFUL INGREDIENTS LIST
# ---------------------------

harmful_ingredients = [
    "e621",
    "e951",
    "palm oil",
    "палмово масло",
    "aspartame",
    "аспартам",
    "monosodium glutamate",
    "sodium nitrate",
    "high fructose corn syrup"
]

# ---------------------------
# IMAGE PREPROCESSING
# ---------------------------

def preprocess_image(image):
    """
    Improve image quality for OCR
    """

    # Increase contrast
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(2)

    # Increase sharpness
    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(2)

    return image


# ---------------------------
# OCR FUNCTION
# ---------------------------

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])


def extract_text(image):
    """
    Extract text using EasyOCR
    """

    reader = load_reader()

    # Convert image to numpy array
    image_array = np.array(image)

    results = reader.readtext(image_array)

    extracted_text = " ".join([result[1] for result in results])

    return extracted_text


# ---------------------------
# FIND HARMFUL INGREDIENTS
# ---------------------------

def find_harmful_ingredients(text):
    """
    Search for harmful ingredients
    """

    found = []

    text = text.lower()

    for ingredient in harmful_ingredients:
        if ingredient.lower() in text:
            found.append(ingredient)

    return found


# ---------------------------
# IMAGE INPUT
# ---------------------------

uploaded_file = st.file_uploader(
    "📤 Upload an image",
    type=["jpg", "jpeg", "png"]
)

camera_image = st.camera_input("📷 Take a photo")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)

elif camera_image is not None:
    image = Image.open(camera_image)

# ---------------------------
# PROCESS IMAGE
# ---------------------------

if image is not None:

    st.image(image, caption="Selected Image", use_container_width=True)

    with st.spinner("🔍 Scanning label..."):

        # Preprocess image
        processed_image = preprocess_image(image)

        # OCR
        extracted_text = extract_text(processed_image)

        # Find ingredients
        detected = find_harmful_ingredients(extracted_text)

    # ---------------------------
    # SHOW RESULTS
    # ---------------------------

    st.subheader("📝 Extracted Text")

    with st.expander("Show OCR Text"):
        st.write(extracted_text)

    st.subheader("⚠️ Analysis Result")

    if detected:

        st.warning("Harmful ingredients detected!")

        for item in detected:
            st.error(f"❌ {item}")

    else:
        st.success("✅ No harmful ingredients found.")
