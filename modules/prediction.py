# =====================================================
# PREDICT DATAFRAME
# =====================================================

def predict_dataframe(
    df,
    text_column="final_text",
    batch_size=32
):

    data = df.copy()

    # Validasi kolom
    if text_column not in data.columns:
        raise ValueError(
            f"Kolom '{text_column}' tidak ditemukan."
        )

    # Validasi dataframe kosong
    if data.empty:
        return data

    # Ambil text
    texts = (
        data[text_column]
        .fillna("")
        .astype(str)
        .tolist()
    )

    emotion_result = []
    confidence_result = []
    probability_result = []

    # Batch prediction
    for start in range(0, len(texts), batch_size):

        batch = texts[start:start + batch_size]

        probs = predict_batch(batch)

        if len(probs) == 0:
            continue

        predictions = np.argmax(
            probs,
            axis=1
        )

        for pred, prob in zip(predictions, probs):

            emotion_result.append(
                EMOTION_LABELS[pred]
            )

            confidence_result.append(
                round(float(prob[pred]), 4)
            )

            probability_result.append(prob)

    probability_result = np.array(probability_result)

    # Hasil prediksi
    data["emotion"] = emotion_result
    data["confidence"] = confidence_result

    # Probability tiap kelas
    for i, label in enumerate(EMOTION_LABELS):
        data[label] = probability_result[:, i]

    # Nomor urut prediksi
    data.insert(
        0,
        "prediction_id",
        range(1, len(data) + 1)
    )

    return data
