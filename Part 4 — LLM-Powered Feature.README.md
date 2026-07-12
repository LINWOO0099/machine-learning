# README.md - Part 4

```markdown
# Part 4: LLM-Powered Feature

## Track Choice
**Track C: Model Prediction Explanation Pipeline**
- Load best model from Part 3
- Generate human-readable explanations for predictions
- Validate JSON output with schema

---

## 1. LLM API Setup

### Environment Variable
```python
import os
API_KEY = os.environ.get('LLM_API_KEY')
```

> ⚠️ **Never hardcode API keys** - use environment variables

### API Call Function
```python
def call_llm(system_prompt, user_prompt, temperature=0.0, max_tokens=512):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']
```

### Test Call
```python
response = call_llm("You are helpful", "Reply with: hello", temperature=0)
print(response)  # Output: hello
```

---

## 2. System Prompt

### System Prompt (Verbatum)
```
You are a model prediction explainer. Your role is to explain why a machine learning model made a specific prediction.

Given feature values, a predicted class (0 or 1), and a probability score, provide a structured JSON explanation.

Follow these rules:
1. Output ONLY valid JSON with these fields:
   - prediction_label: "High price" if class=1, "Low price" if class=0
   - confidence_level: "high" if probability > 0.8, "medium" if 0.5-0.8, "low" if < 0.5
   - top_reason: The single most important factor driving this prediction
   - second_reason: The second most important factor
   - next_step: Recommended action based on the prediction

2. Base your explanation on the feature values provided.
3. Use domain knowledge about housing prices.
4. Be specific and data-driven.
5. Do not include any text outside the JSON object.
```

### User Prompt Template
```
Please explain the following prediction:

Feature values:
  sqft_living: {value}
  waterfront: {value}
  condition: {value}
  grade: {value}
  yr_built: {value}

Predicted class: {0 or 1} ({"High price" if class=1 else "Low price"})
Prediction probability: {probability:.3f}

Provide a JSON explanation with the required fields.
```

### Why Temperature = 0?
> Temperature=0 ensures deterministic, reproducible outputs. Model always selects highest-probability token, making it reliable for structured data tasks.

---

## 3. JSON Schema Validation

### Schema (5 Required Fields)
```python
SCHEMA = {
    "type": "object",
    "properties": {
        "prediction_label": {"type": "string"},
        "confidence_level": {"type": "string", "enum": ["low", "medium", "high"]},
        "top_reason": {"type": "string"},
        "second_reason": {"type": "string"},
        "next_step": {"type": "string"}
    },
    "required": ["prediction_label", "confidence_level", "top_reason", "second_reason", "next_step"]
}
```

### Validation Function
```python
def validate_response(response):
    try:
        parsed = json.loads(response.strip())
        jsonschema.validate(parsed, SCHEMA)
        return parsed
    except:
        return {"prediction_label": "unknown", "confidence_level": "low", 
                "top_reason": "unable to generate", "second_reason": "unable", 
                "next_step": "human review"}
```

---

## 4. PII Guardrail

### Guardrail Function
```python
def has_pii(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b'
    return bool(re.search(email_pattern, text) or re.search(phone_pattern, text))
```

### Test Results

| Input | Contains PII? | Action |
|-------|---------------|--------|
| "Clean text with no PII" | ❌ No | ✅ Proceed |
| "Email: test@example.com" | ✅ Yes | 🛑 Blocked |
| "Phone: 555-123-4567" | ✅ Yes | 🛑 Blocked |

---

## 5. End-to-End Pipeline

### Three Test Inputs

**Input 1: Luxury Home**
```python
features = {
    'sqft_living': 5000,
    'waterfront': 1,
    'condition': 5,
    'grade': 12,
    'yr_built': 2010
}
# Predicted: Class 1 (High), Probability: 0.978
```

**Input 2: Small Home**
```python
features = {
    'sqft_living': 1000,
    'waterfront': 0,
    'condition': 2,
    'grade': 6,
    'yr_built': 1960
}
# Predicted: Class 0 (Low), Probability: 0.156
```

**Input 3: Average Home**
```python
features = {
    'sqft_living': 2500,
    'waterfront': 0,
    'condition': 4,
    'grade': 9,
    'yr_built': 2005
}
# Predicted: Class 1 (High), Probability: 0.723
```

### Pipeline Steps
1. Check for PII → Block if found
2. Encode features using model preprocessor
3. Get prediction & probability
4. Build user prompt
5. Call LLM API
6. Validate JSON response
7. Return explanation

---

## 6. Results

### Three-Row Demonstration Table

| Input | Predicted Class | Probability | LLM Explanation | Valid JSON |
|-------|----------------|-------------|-----------------|------------|
| **Input 1**: Luxury (5000 sqft, waterfront) | 1 (High) | 0.978 | `{"prediction_label":"High price","confidence_level":"high","top_reason":"Very large living area","second_reason":"Waterfront location","next_step":"Premium pricing"}` | ✅ Pass |
| **Input 2**: Small (1000 sqft, old) | 0 (Low) | 0.156 | `{"prediction_label":"Low price","confidence_level":"high","top_reason":"Small living area","second_reason":"Older construction","next_step":"Consider renovations"}` | ✅ Pass |
| **Input 3**: Average (2500 sqft, modern) | 1 (High) | 0.723 | `{"prediction_label":"High price","confidence_level":"medium","top_reason":"Above-average size","second_reason":"Good grade","next_step":"Monitor market"}` | ✅ Pass |

### Guardrail Results

| Input | PII Check | Action |
|-------|-----------|--------|
| Input 1 | ✅ Pass | Proceeded |
| Input 2 | ✅ Pass | Proceeded |
| Input 3 | ✅ Pass | Proceeded |

---

## 7. Temperature Comparison

| Temperature | Output Snippet | Key Difference |
|-------------|----------------|----------------|
| **0.0** | `{"prediction_label":"High price","confidence_level":"high","top_reason":"Large living area","second_reason":"Waterfront","next_step":"Premium pricing"}` | Consistent, deterministic |
| **0.7** | `{"prediction_label":"High price","confidence_level":"high","top_reason":"Exceptional square footage","second_reason":"Prime waterfront setting","next_step":"List at premium"}` | Varied wording, same meaning |

> **Explanation**: Temperature=0 always picks highest-probability token (deterministic). Temperature=0.7 samples from broader distribution (varied but equivalent outputs).

---

## 8. Code Example

### Full Pipeline
```python
# Load model
model = joblib.load('best_model.pkl')

# Define features
features = {'sqft_living': 2500, 'waterfront': 0, 'condition': 4, 'grade': 9, 'yr_built': 2005}

# Check PII
if not has_pii(str(features)):
    # Encode & predict
    encoded = encode_record(features)
    pred = model.predict(encoded)[0]
    proba = model.predict_proba(encoded)[0][1]
    
    # Get explanation
    user_prompt = construct_prompt(features, pred, proba)
    response = call_llm(SYSTEM_PROMPT, user_prompt, temperature=0)
    
    # Validate
    explanation = validate_response(response)
    print(explanation)
else:
    print("Blocked: PII detected")
```

---

## 9. Key Takeaways

| Aspect | Finding |
|--------|---------|
| **Track** | C - Model Prediction Explanation |
| **Best Model** | Gradient Boosting (AUC = 0.921) |
| **LLM Provider** | OpenRouter / GPT-3.5-turbo |
| **Temperature** | 0.0 (deterministic) |
| **Validation** | ✅ All 3 responses valid JSON |
| **Guardrail** | ✅ Blocks emails & phone numbers |
| **Fallback** | ✅ Works when validation fails |

---

## ✅ Checklist

- [x] API key in environment variable
- [x] `call_llm()` function implemented
- [x] Test prompt returns "hello"
- [x] System prompt defined
- [x] User prompt template defined
- [x] Temperature=0 explained
- [x] JSON schema with 5 required fields
- [x] Validation function implemented
- [x] PII guardrail implemented
- [x] Guardrail tested (block email, allow clean)
- [x] 3 inputs processed end-to-end
- [x] Temperature comparison done
- [x] Results table in README

---

## Files

| File | Description |
|------|-------------|
| `part4_track_c.py` | Full Python code |
| `best_model.pkl` | Loaded from Part 3 |

---

## How to Run

```bash
export LLM_API_KEY="your-api-key-here"
python part4_track_c.py
```

---

**Status**: ✅ Complete  
**Track**: C - Model Prediction Explanation

---
```
