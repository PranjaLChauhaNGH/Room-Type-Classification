from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from typing import Literal

app = FastAPI()

Columns = [
    'neighbourhood_group', 'neighbourhood', 'latitude', 'longitude',
    'price', 'minimum_nights', 'number_of_reviews',
    'reviews_per_month', 'calculated_host_listings_count',
    'availability_365'
]
class Features(BaseModel):
    neighbourhood_group: Literal['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
    neighbourhood: str = Field(..., min_length=1)
    latitude : float = Field(..., ge=-99, le=99)
    longitude : float = Field(..., ge=-180, le=180)
    price : float = Field(..., ge=0, le=999)
    minimum_nights : int = Field(..., ge=0, le=99)
    number_of_reviews : int = Field(..., ge=0, le=999)
    reviews_per_month : int = Field(..., ge=0, le=99)
    calculated_host_listings_count : int = Field(..., ge=0, le=99)
    availability_365 : int = Field(..., ge=0, le=365)

model = joblib.load('Model_Pipeline.pkl')

@app.get('/')
def greet():
    return "hello welcome"

@app.post('/predict')
def predict(features: Features):
    row = pd.DataFrame([features.dict()], columns=Columns)
    prediction = model.predict(row)
    probability = model.predict_proba(row)

    return {
        "Predicted_room_type" : prediction[0],
        "Predicted_room_probability" : probability.tolist()[0]
    }
