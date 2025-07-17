from rapidfuzz import fuzz

# === Configuration ===
FUZZY_THRESHOLD = 85  # Change this to test different thresholds

# Example strings — you can modify these
generated_response = "I don't have enough reliable information to answer this question accurately."
fallback_phrase = "I don't have enough reliable information to answer this question accurately."

# === Fuzzy Matching Test ===
similarity = fuzz.ratio(generated_response.lower(), fallback_phrase.lower())

print("🔍 Comparing:")
print(f"Generated Response: {generated_response}")
print(f"Fallback Phrase:    {fallback_phrase}")
print(f"\n🧠 Similarity Score: {similarity}")

if similarity >= FUZZY_THRESHOLD:
    print(f"✅ Match! (Threshold: {FUZZY_THRESHOLD})")
else:
    print(f"❌ No Match. (Threshold: {FUZZY_THRESHOLD})")
