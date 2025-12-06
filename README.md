# Natural Language to SQL Query Engine

A lightweight pipeline using **LangChain**, **OpenAI**, and **MySQL (Chinook DB)**.
Users can ask questions in plain English, and the system automatically:

1. Fetches the database schema
2. Generates the correct SQL query
3. Executes it on MySQL
4. Returns a natural language answer

---

### Features

* Automatic SQL generation based on live schema
* Executes queries directly on MySQL
* Natural-language final responses
* Modular LangChain-based pipeline

---

### Example

```python
result = full_chain.invoke({
    "question": "how many albums are there?"
})
```

