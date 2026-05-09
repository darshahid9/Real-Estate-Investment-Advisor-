import pandas as pd
import numpy as np
import streamlit as st
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "https://drive.google.com/drive/folders/1OWIOuZXm5c-mctsyvhsLhcW4pBmIoJXP")


@st.cache_data(show_spinner=False)
def load_and_process():
    df = pd.read_csv(DATA_PATH)

    # Recalculate Price_per_SqFt in actual ₹ (original col is lakh/sqft scale)
    df["Price_per_SqFt"] = (df["Price_in_Lakhs"] * 100_000) / df["Size_in_SqFt"]

    # Parse amenities into binary columns
    amenity_items = ["Gym", "Pool", "Garden", "Playground", "Clubhouse"]
    for a in amenity_items:
        df[f"Has_{a}"] = df["Amenities"].str.contains(a, case=False, na=False).astype(int)
    df["Amenity_Count"] = df[[f"Has_{a}" for a in amenity_items]].sum(axis=1)

    # Scores
    transport_map = {"Low": 1, "Medium": 5, "High": 10}
    df["Transport_Score"] = df["Public_Transport_Accessibility"].map(transport_map).fillna(5)
    df["School_Score"] = (df["Nearby_Schools"] / df["Nearby_Schools"].max() * 10).round(2)
    df["Hospital_Score"] = (df["Nearby_Hospitals"] / df["Nearby_Hospitals"].max() * 10).round(2)
    df["Parking_Score"] = df["Parking_Space"].map({"Yes": 10, "No": 0}).fillna(0)
    df["Security_Score"] = df["Security"].map({"Yes": 10, "No": 0}).fillna(0)
    df["Amenity_Score"] = (df["Amenity_Count"] / 5 * 10).round(2)

    df["Infrastructure_Score"] = (
        df["Transport_Score"] * 0.25
        + df["School_Score"] * 0.20
        + df["Hospital_Score"] * 0.20
        + df["Amenity_Score"] * 0.15
        + df["Security_Score"] * 0.10
        + df["Parking_Score"] * 0.10
    ).round(2)

    df["Furnished_Score"] = df["Furnished_Status"].map(
        {"Unfurnished": 0, "Semi-furnished": 5, "Furnished": 10}
    ).fillna(5)

    # City-level value index
    city_median = df.groupby("City")["Price_per_SqFt"].transform("median")
    df["Value_Index"] = (city_median / df["Price_per_SqFt"]).round(3)

    # Growth rate by city
    city_growth = {
        "Mumbai": 0.090, "New Delhi": 0.085, "Noida": 0.085,
        "Gurgaon": 0.085, "Bangalore": 0.100, "Hyderabad": 0.100,
        "Pune": 0.090, "Chennai": 0.080, "Ahmedabad": 0.075,
        "Kolkata": 0.070, "Surat": 0.075, "Jaipur": 0.080,
        "Lucknow": 0.075, "Kochi": 0.080, "Indore": 0.075,
        "Bhubaneswar": 0.080, "Vishakhapatnam": 0.080, "Dehradun": 0.080,
        "Haridwar": 0.075, "Guwahati": 0.075, "Trivandrum": 0.075,
        "Mysore": 0.075, "Coimbatore": 0.075, "Vijayawada": 0.075,
        "Mangalore": 0.070, "Faridabad": 0.075, "Dwarka": 0.080,
        "Amritsar": 0.070, "Ludhiana": 0.070, "Jodhpur": 0.070,
        "Nagpur": 0.075, "Bhopal": 0.075, "Patna": 0.070,
        "Ranchi": 0.070, "Jamshedpur": 0.065, "Raipur": 0.070,
        "Warangal": 0.070, "Bilaspur": 0.065, "Silchar": 0.065,
        "Durgapur": 0.065, "Cuttack": 0.065, "Gaya": 0.065,
    }
    df["Growth_Rate"] = df["City"].map(city_growth).fillna(0.075)

    # Future price (5 years)
    df["Future_Price_5Yr"] = (df["Price_in_Lakhs"] * (1 + df["Growth_Rate"]) ** 5).round(2)
    df["Appreciation_Lakhs"] = (df["Future_Price_5Yr"] - df["Price_in_Lakhs"]).round(2)
    df["Appreciation_Pct"] = ((df["Appreciation_Lakhs"] / df["Price_in_Lakhs"]) * 100).round(2)

    # Good Investment label (rule-based)
    score = (
        (df["Value_Index"] >= 1.0).astype(int) * 2
        + (df["BHK"] >= 3).astype(int)
        + (df["Infrastructure_Score"] >= 5).astype(int)
        + (df["Age_of_Property"] <= 10).astype(int)
        + (df["Availability_Status"] == "Ready_to_Move").astype(int)
        + (df["Growth_Rate"] >= 0.08).astype(int)
        + (df["Security"] == "Yes").astype(int)
        + (df["Parking_Space"] == "Yes").astype(int)
    )
    df["Investment_Score"] = score
    df["Good_Investment"] = (score >= 5).astype(int)

    return df
