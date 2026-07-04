# =====================================================
# PREDICT SINGLE TEXT
# =====================================================

def predict_text(text):

    if text is None:
        text = ""

    text = str(text).strip()

    encoding = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

    encoding = {
        key: value.to(device)
        for key, value in encoding.items()
    }

    with torch.no_grad():
        output = model(**encoding)

    probability = torch.softmax(
        output.logits,
        dim=1
    ).cpu().numpy()[0]

    prediction = int(np.argmax(probability))

    return {
        "emotion": EMOTION_LABELS[prediction],
        "confidence": float(probability[prediction]),
        "probability": {
            label: float(prob)
            for label, prob in zip(
                EMOTION_LABELS,
                probability
            )
        }
    }
