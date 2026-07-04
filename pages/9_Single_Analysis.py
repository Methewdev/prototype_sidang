"""
=========================================================
SINGLE REVIEW ANALYSIS
=========================================================
"""

import streamlit as st
import streamlit as st
import pandas as pd

from modules.preprocessing import (
    preprocess_single_review
)

from modules.prediction import (
    predict_text
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Single Review Analysis",
    page_icon="📝",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📝 Single Review Analysis")

st.markdown(
    """
Analisis satu review menggunakan model **Fine-Tuned IndoBERT**
dengan tahapan preprocessing yang sama seperti proses Batch Analysis.
"""
)

st.divider()

# =====================================================
# INPUT REVIEW
# =====================================================

review = st.text_area(
    label="Masukkan Review",
    placeholder="Contoh:\nLivin sering logout sendiri ketika akan transfer.",
    height=180
)

analyze = st.button(
    "🚀 Analyze Review",
    use_container_width=True
)

# =====================================================
# ANALYSIS
# =====================================================

if analyze:

    if review.strip() == "":

        st.warning(
            "Silakan masukkan review terlebih dahulu."
        )

        st.stop()

    with st.spinner(
        "Melakukan preprocessing dan prediksi..."
    ):

        preprocess = preprocess_single_review(
            review
        )

        prediction = predict_text(
            preprocess["final_text"]
        )

    st.success(
        "Analisis berhasil dilakukan."
    )

    st.session_state.single_preprocess = preprocess
    st.session_state.single_prediction = prediction
    # =====================================================
# LOAD RESULT
# =====================================================

if "single_preprocess" not in st.session_state:
    st.info("Silakan masukkan review kemudian klik **Analyze Review**.")
    st.stop()

preprocess = st.session_state.single_preprocess
prediction = st.session_state.single_prediction
    # =====================================================
# DATA UNDERSTANDING
# =====================================================

st.divider()

st.subheader("📊 Data Understanding")

review_text = preprocess["original_text"]

# ==========================================
# STATISTICS
# ==========================================

character_count = len(review_text)

word_count = len(review_text.split())

sentence_count = len(
    [s for s in review_text.split(".") if s.strip()]
)

average_word_length = round(

    sum(len(word) for word in review_text.split())

    / max(word_count, 1),

    2

)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Characters",
    character_count
)

c2.metric(
    "Words",
    word_count
)

c3.metric(
    "Sentences",
    sentence_count
)

c4.metric(
    "Avg Word Length",
    average_word_length
)

st.markdown("### 📝 Original Review")

st.info(review_text)
# =====================================================
# PREPROCESSING PIPELINE
# =====================================================

st.divider()

st.subheader("🧹 Text Preprocessing")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([

    "🧹 Cleaning",

    "🔡 Case Folding",

    "🔄 Normalization",

    "🚫 Stopword",

    "🌱 Stemming",

    "🔠 Tokenization"

])

# =====================================================
# CLEANING
# =====================================================

with tab1:

    st.markdown("### Cleaning")

    st.markdown("**Sebelum Cleaning**")

    st.code(
        preprocess["original_text"],
        language="text"
    )

    st.markdown("**Sesudah Cleaning**")

    st.code(
        preprocess["cleaning"],
        language="text"
    )

# =====================================================
# CASE FOLDING
# =====================================================

with tab2:

    st.markdown("### Case Folding")

    st.code(
        preprocess["case_folding"],
        language="text"
    )

# =====================================================
# NORMALIZATION
# =====================================================

with tab3:

    st.markdown("### Normalization")

    st.code(
        preprocess["normalization"],
        language="text"
    )

# =====================================================
# STOPWORD
# =====================================================

with tab4:

    st.markdown("### Stopword Removal")

    st.code(
        preprocess["stopword"],
        language="text"
    )

# =====================================================
# STEMMING
# =====================================================

with tab5:

    st.markdown("### Stemming")

    st.code(
        preprocess["stemming"],
        language="text"
    )

    st.markdown("### Final Text")

    st.success(
        preprocess["final_text"]
    )

# =====================================================
# TOKENIZATION
# =====================================================

with tab6:

    st.markdown("### Tokenization")

    token_df = pd.DataFrame({

        "No": range(
            1,
            len(preprocess["token"]) + 1
        ),

        "Token": preprocess["token"]

    })

    st.dataframe(
        token_df,
        width="stretch",
        hide_index=True
    )
    # =====================================================
# EMOTION PREDICTION
# =====================================================

st.divider()

st.subheader("🤖 Emotion Prediction")

emotion = prediction["emotion"]
confidence = prediction["confidence"] * 100


# =====================================================
# CUSTOMER SEGMENT
# =====================================================

if emotion == "Frustrasi":

    segment = "😠 Nasabah Frustasi"

    risk = "Very High"

    description = """
Pelanggan mengalami frustrasi tinggi terhadap aplikasi
dan memerlukan penanganan segera.
"""

elif emotion == "Sedih":

    segment = "😟 Nasabah Tidak Puas"

    risk = "High"

    description = """
Pelanggan merasa kecewa terhadap layanan aplikasi
dan berpotensi menurunkan loyalitas.
"""

elif emotion == "Netral":

    segment = "😐 Nasabah Passive"

    risk = "Medium"

    description = """
Pelanggan belum menunjukkan emosi dominan.
Perlu dilakukan engagement lebih lanjut.
"""

else:

    segment = "😊 Nasabah Puas"

    risk = "Low"

    description = """
Pelanggan merasa puas terhadap aplikasi
dan berpotensi menjadi pengguna loyal.
"""
# =====================================================
# EMOTION ICON
# =====================================================

emotion_icon = {
    "Senang": "😊",
    "Netral": "😐",
    "Marah": "😠",
    "Frustrasi": "😫"
}

icon = emotion_icon.get(
    emotion,
    "🤖"
)

# =====================================================
# CONFIDENCE STATUS
# =====================================================

if confidence >= 90:

    status = "High Confidence"

elif confidence >= 70:

    status = "Medium Confidence"

else:

    status = "Low Confidence"

# =====================================================
# RESULT CARD
# =====================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Detected Emotion",
    f"{icon} {emotion}"
)

c2.metric(
    "Confidence",
    f"{confidence:.2f}%"
)

c3.metric(
    "Prediction Status",
    status
)
# =====================================================
# INTERPRETATION
# =====================================================

description = {

    "Senang":
    "Review menunjukkan kepuasan pengguna terhadap layanan aplikasi.",

    "Netral":
    "Review bersifat informatif dan tidak menunjukkan emosi yang dominan.",

    "Marah":
    "Review menunjukkan kemarahan terhadap layanan atau fitur aplikasi.",

    "Frustrasi":
    "Review menunjukkan pengguna mengalami kendala yang menyebabkan frustrasi."

}

st.info(
    description.get(
        emotion,
        "-"
    )
)
# =====================================================
# EMOTION PROBABILITY
# =====================================================

st.divider()

st.subheader("📈 Emotion Probability")

probability = prediction["probability"]

emotion_icon = {
    "Senang": "😊",
    "Netral": "😐",
    "Marah": "😠",
    "Frustrasi": "😫"
}

# urutan tampilan
emotion_order = [
    "Senang",
    "Netral",
    "Marah",
    "Frustrasi"
]

probability_table = []

for emotion in emotion_order:

    value = probability.get(emotion, 0)

    st.markdown(
        f"**{emotion_icon.get(emotion,'')} {emotion}**"
    )

    st.progress(
        float(value)
    )

    st.caption(
        f"{value*100:.2f}%"
    )

    probability_table.append({

        "Emotion": emotion,

        "Probability (%)": round(
            value * 100,
            2
        )

    })

st.divider()

st.subheader("📋 Probability Detail")

probability_df = pd.DataFrame(
    probability_table
)

st.dataframe(

    probability_df,

    width="stretch",

    hide_index=True

)
# =====================================================
# CUSTOMER SEGMENTATION
# =====================================================

st.divider()

st.subheader("👥 Customer Segmentation")

emotion = prediction["emotion"]
confidence = prediction["confidence"] * 100

# =====================================================
# SEGMENTATION RULE
# =====================================================

# =====================================================
# RETENTION RULE
# =====================================================

if segment == "😠 Nasabah Frustasi":

    priority = "Very High"

    objective = "Mengurangi risiko churn dan menyelesaikan keluhan pelanggan."

    actions = [
        "Prioritaskan penyelesaian masalah.",
        "Lakukan eskalasi ke tim teknis.",
        "Hubungi pelanggan secara proaktif.",
        "Berikan kompensasi bila diperlukan.",
        "Lakukan monitoring hingga pelanggan kembali puas."
    ]

elif segment == "😟 Nasabah Tidak Puas":

    priority = "High"

    objective = "Meningkatkan kepuasan pelanggan."

    actions = [
        "Tindak lanjuti keluhan pelanggan.",
        "Identifikasi penyebab utama masalah.",
        "Lakukan follow-up setelah perbaikan.",
        "Pastikan layanan kembali normal."
    ]

elif segment == "😐 Nasabah Passive":

    priority = "Medium"

    objective = "Meningkatkan engagement pelanggan."

    actions = [
        "Edukasi penggunaan fitur.",
        "Berikan promo yang relevan.",
        "Dorong penggunaan fitur baru."
    ]

elif segment == "😊 Nasabah Puas":

    priority = "Low"

    objective = "Mempertahankan loyalitas pelanggan."

    actions = [
        "Pertahankan kualitas layanan.",
        "Berikan reward dan cashback.",
        "Dorong pelanggan memberikan ulasan positif."
    ]

else:

    priority = "-"

    objective = "-"

    actions = [
        "Belum ada rekomendasi."
    ]
# =====================================================
# DISPLAY
# =====================================================

c1, c2 = st.columns(2)

c1.metric(
    "Customer Segment",
    segment
)

c2.metric(
    "Risk Level",
    risk
)

st.info(description)
# =====================================================
# CUSTOMER RETENTION STRATEGY
# =====================================================

st.divider()

st.subheader("❤️ Customer Retention Strategy")

# =====================================================
# RETENTION RULE
# =====================================================
# =====================================================
# RETENTION RULE
# =====================================================

# =====================================================
# RETENTION RULE
# =====================================================

if segment == "😠 Nasabah Frustasi":

    priority = "Very High"

    objective = "Mengurangi risiko churn dan menyelesaikan keluhan pelanggan."

    actions = [
        "Prioritaskan penyelesaian masalah.",
        "Lakukan eskalasi ke tim teknis.",
        "Hubungi pelanggan secara proaktif.",
        "Berikan kompensasi bila diperlukan.",
        "Lakukan monitoring hingga pelanggan kembali puas."
    ]

elif segment == "😟 Nasabah Tidak Puas":

    priority = "High"

    objective = "Meningkatkan kepuasan pelanggan."

    actions = [
        "Tindak lanjuti keluhan pelanggan.",
        "Identifikasi penyebab utama masalah.",
        "Lakukan follow-up setelah perbaikan.",
        "Pastikan layanan kembali normal."
    ]

elif segment == "😐 Nasabah Passive":

    priority = "Medium"

    objective = "Meningkatkan engagement pelanggan."

    actions = [
        "Edukasi penggunaan fitur.",
        "Berikan promo yang relevan.",
        "Dorong penggunaan fitur baru."
    ]

elif segment == "😊 Nasabah Puas":

    priority = "Low"

    objective = "Mempertahankan loyalitas pelanggan."

    actions = [
        "Pertahankan kualitas layanan.",
        "Berikan reward dan cashback.",
        "Dorong pelanggan memberikan ulasan positif."
    ]

else:

    priority = "-"

    objective = "-"

    actions = [
        "Belum ada rekomendasi."
    ]

# =====================================================
# METRIC
# =====================================================

c1, c2 = st.columns(2)

c1.metric(
    "Retention Priority",
    priority
)

c2.metric(
    "Business Objective",
    objective
)

st.markdown("### 📌 Recommended Actions")

for i, action in enumerate(actions, start=1):

    st.write(f"{i}. {action}")

st.success("Retention strategy berhasil dibuat berdasarkan hasil analisis emosi.")
