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

    harmful_ingredients = {

        # -------------------
        # COLORANTS / ОЦВЕТИТЕЛИ
        # -------------------
        "E102": "Colorant / Оцветител (Tartrazine)",
        "E104": "Colorant / Оцветител",
        "E110": "Colorant / Оцветител (Sunset Yellow)",
        "E122": "Colorant / Оцветител (Azorubine)",
        "E123": "Colorant / Оцветител",
        "E124": "Colorant / Оцветител (Ponceau 4R)",
        "E127": "Colorant / Оцветител",
        "E129": "Colorant / Оцветител (Allura Red)",
        "E131": "Colorant / Оцветител",
        "E132": "Colorant / Оцветител",
        "E133": "Colorant / Оцветител (Blue)",
        "E142": "Colorant / Оцветител",
        "E151": "Colorant / Оцветител (Black PN)",

        # -------------------
        # PRESERVATIVES / КОНСЕРВАНТИ
        # -------------------
        "E200": "Preservative / Консервант",
        "E202": "Preservative / Консервант",
        "E211": "Preservative / Консервант (Sodium benzoate)",
        "E220": "Preservative / Консервант (Sulphites)",
        "E221": "Preservative / Консервант",
        "E222": "Preservative / Консервант",
        "E223": "Preservative / Консервант",
        "E224": "Preservative / Консервант",
        "E225": "Preservative / Консервант",
        "E226": "Preservative / Консервант",
        "E227": "Preservative / Консервант",
        "E228": "Preservative / Консервант",
        "E250": "Preservative / Консервант (Sodium nitrite)",
        "E251": "Preservative / Консервант (Nitrate)",
        "E252": "Preservative / Консервант",

        # -------------------
        # SWEETENERS / ПОДСЛАДИТЕЛИ
        # -------------------
        "E420": "Sweetener / Подсладител (Sorbitol)",
        "E421": "Sweetener / Подсладител",
        "E950": "Sweetener / Подсладител (Acesulfame K)",
        "E951": "Sweetener / Подсладител (Aspartame)",
        "E952": "Sweetener / Подсладител (Cyclamate)",
        "E954": "Sweetener / Подсладител (Saccharin)",
        "E955": "Sweetener / Подсладител (Sucralose)",

        # -------------------
        # FLAVOR ENHANCERS / ОВКУСИТЕЛИ
        # -------------------
        "E621": "Flavor enhancer / Овкусител (MSG)",
        "E627": "Flavor enhancer / Овкусител",
        "E631": "Flavor enhancer / Овкусител",
        "E635": "Flavor enhancer / Овкусител",

        # -------------------
        # STABILIZERS / СТАБИЛИЗАТОРИ
        # -------------------
        "E320": "Stabilizer / Стабилизатор (BHA)",
        "E321": "Stabilizer / Стабилизатор (BHT)",
        "E407": "Stabilizer / Стабилизатор (Carrageenan)",
        "E410": "Stabilizer / Стабилизатор",
        "E412": "Stabilizer / Стабилизатор",
        "E415": "Stabilizer / Стабилизатор",
        "E440": "Stabilizer / Стабилизатор",
        "E450": "Stabilizer / Стабилизатор (Phosphates)",

        # -------------------
        # OTHER HARMFUL / спорни съставки
        # -------------------
        "palm oil": "Harmful fat / Палмово масло",
        "палмово масло": "Вредна мазнина / Палмово масло",

        "hydrogenated oil": "Trans fat / Хидрогенирано масло",
        "частично хидрогенирано": "Trans fat / Транс мазнини",

        "high fructose corn syrup": "Sweetener / Високо фруктозен сироп",
        "високо фруктозен сироп": "Sweetener / High fructose syrup",

        "monosodium glutamate": "Flavor enhancer / Мононатриев глутамат",
        "мононатриев глутамат": "Flavor enhancer / MSG",

        "aspartame": "Sweetener / Аспартам",
        "аспартам": "Sweetener / Аспартам",

        "glucose-fructose syrup": "Sweetener / Глюкозо-фруктозен сироп",
        "глюкозо-фруктозен сироп": "Sweetener / Glucose-fructose syrup"
    }

    found = []

    text = text.lower()

    for ingredient, category in harmful_ingredients.items():
        if ingredient.lower() in text:
            found.append((ingredient, category))

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
