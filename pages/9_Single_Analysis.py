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

if emotion == "Frustrasi":

    if confidence >= 90:

        segment = "🔴 High Risk Customer"

        description = """
Pelanggan mengalami frustrasi tinggi terhadap aplikasi.
Memerlukan perhatian dan penanganan segera.
"""

    else:

        segment = "🟠 At Risk Customer"

        description = """
Pelanggan mulai menunjukkan frustrasi,
namun tingkat keyakinan model belum terlalu tinggi.
"""

elif emotion == "Marah":

    segment = "🟠 At Risk Customer"

    description = """
Pelanggan menunjukkan kemarahan terhadap layanan.
Perlu dilakukan evaluasi terhadap penyebab keluhan.
"""

elif emotion == "Netral":

    segment = "🟡 Passive Customer"

    description = """
Pelanggan memberikan ulasan yang bersifat informatif
tanpa menunjukkan emosi yang dominan.
"""

else:

    segment = "🟢 Loyal Customer"

    description = """
Pelanggan merasa puas terhadap aplikasi
dan berpotensi menjadi pengguna loyal.
"""

# =====================================================
# DISPLAY
# =====================================================

c1, c2 = st.columns(2)

c1.metric(
    "Customer Segment",
    segment
)

c2.metric(
    "Confidence",
    f"{confidence:.2f}%"
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

if segment == "🔴 High Risk Customer":

    priority = "🔴 High"

    objective = "Mengurangi risiko churn dan meningkatkan kepuasan pelanggan."

    actions = [
        "Prioritaskan penanganan keluhan pelanggan.",
        "Lakukan investigasi terhadap penyebab masalah.",
        "Koordinasikan dengan tim pengembang apabila ditemukan bug.",
        "Berikan informasi apabila perbaikan telah dilakukan.",
        "Monitor review pelanggan setelah update aplikasi."
    ]

elif segment == "🟠 At Risk Customer":

    priority = "🟠 Medium"

    objective = "Mencegah pelanggan menjadi tidak puas."

    actions = [
        "Analisis penyebab utama keluhan.",
        "Berikan edukasi penggunaan fitur apabila diperlukan.",
        "Pastikan kendala pelanggan dapat direproduksi.",
        "Monitor feedback pelanggan berikutnya."
    ]

elif segment == "🟡 Passive Customer":

    priority = "🟡 Low"

    objective = "Meningkatkan engagement pelanggan."

    actions = [
        "Dorong pelanggan mencoba fitur baru.",
        "Berikan informasi mengenai update aplikasi.",
        "Pantau perubahan sentimen pelanggan."
    ]

else:

    priority = "🟢 Normal"

    objective = "Mempertahankan kepuasan pelanggan."

    actions = [
        "Pertahankan kualitas layanan aplikasi.",
        "Terus tingkatkan performa aplikasi.",
        "Dorong pelanggan memberikan rating positif.",
        "Jadikan review positif sebagai insight."
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
