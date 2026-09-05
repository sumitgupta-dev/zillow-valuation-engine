# 🏠 The Algorithmic Valuation Engine
🚀 LIVE API DEMO: https://zillow-valuation-engine.onrender.com/docs

(Click the link above to test the API live in your browser!)

A production-ready Machine Learning microservice that predicts house prices and instantly finds comparable properties (Zillow-style "comps"). 

Instead of just returning a single price prediction, this API uses a custom **K-Nearest Neighbors (KNN) algorithm powered by a Max-Heap Priority Queue** to search through 21,000 records and return the 3 most similar houses in milliseconds.

---

### 🧠 The Problem vs. The Solution

**The Problem:** Standard ML models output a single price, acting as a "black box." Users don't trust a price if they can't see *why* the model predicted it. Furthermore, finding similar houses using standard sorting algorithms is computationally expensive and slow.


**The Solution:** 
1. **Trust:** The API returns the predicted price *alongside* the 3 closest comparable houses, providing immediate mathematical proof for the valuation.
2. **Efficiency:** Instead of sorting all 21,000 houses to find the closest ones, I engineered a custom KNN algorithm using a **Max-Heap**.This reduces time complexity from O(N log N) to O(N log K), keeping memory usage extremely low and response times instant.

---

### ⚙️ Tech Stack
* **Machine Learning:** Scikit-Learn (RandomForestRegressor, StandardScaler)
* **Data Engineering:** Pandas, NumPy
* **DSA / Algorithm:** Custom KNN built with Python's `heapq` (Max-Heap)
* **Backend API:** FastAPI, Uvicorn
* **Deployment:** Docker

---

### 🚀 API Endpoints

#### `POST /predict`
Accepts house features and returns the predicted price along with 3 comparable properties.

**Request Body:**
```json
{
  "sqft_living": 1000,
  "bedrooms": 1,
  "bathrooms": 2
}
```

**Response Body:**
```json
{
  "predicted_price": 348874.74,
  "comparable_houses": [
    {
      "id": 6821101827,
      "date": "20141105T000000",
      "price": 340000,
      "bedrooms": 2,
      "bathrooms": 1.75,
      "sqft_living": 1010,
      "sqft_lot": 1461,
      "floors": 1,
      "waterfront": 0,
      "view": 0,
      "condition": 3,
      "grade": 7,
      "sqft_above": 670,
      "sqft_basement": 340,
      "yr_built": 2003,
      "yr_renovated": 0,
      "zipcode": 98199,
      "lat": 47.6515,
      "long": -122.4,
      "sqft_living15": 1500,
      "sqft_lot15": 2499
    },
    {
      "id": 3335000050,
      "date": "20140714T000000",
      "price": 397000,
      "bedrooms": 2,
      "bathrooms": 1.75,
      "sqft_living": 1610,
      "sqft_lot": 4104,
      "floors": 1,
      "waterfront": 0,
      "view": 0,
      "condition": 3,
      "grade": 7,
      "sqft_above": 950,
      "sqft_basement": 660,
      "yr_built": 1996,
      "yr_renovated": 0,
      "zipcode": 98118,
      "lat": 47.5565,
      "long": -122.275,
      "sqft_living15": 1510,
      "sqft_lot15": 5284
    }
  ]
}
```
*(Note: one column are truncated in this example for readability).*

---

### 🐳 Installation & Local Deployment

This project is fully containerized using Docker. To run the API locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sumitgupta-dev/zillow-valuation-engine.git
   cd zillow-valuation-engine
   ```

2. **Build the Docker image:**
   ```bash
   docker build -t zillow-engine .
   ```

3. **Run the Docker container:**
   ```bash
   docker run -p 8000:8000 zillow-engine
   ```

4. **Access the API:**
   Open your browser and go to `http://127.0.0.1:8000/docs` to access the interactive FastAPI Swagger UI.

---

### 🏗️ Architecture Notes
* **Smart Defaults:** To keep the user experience simple, the API only asks for 5 inputs (Sqft, Beds, Baths, Lat, Long). The remaining 6 features required by the model (waterfront, view, condition, grade, etc.) are injected automatically as "average" smart defaults on the backend.
* **Global Loading:** The ML model, Scaler, and Database are loaded into memory *once* when the server starts, ensuring every API request is processed instantly without file I/O bottlenecks.

---