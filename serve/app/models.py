from sqlalchemy import TIMESTAMP, Column, Float, Integer, String
from sqlalchemy.sql import func

from serve.app.database import Base


class PredictionTable(Base):
    """Implement table for storing features with corresponding predictions."""

    __tablename__ = 'prediction'

    ID = Column(String, primary_key=True)
    Delivery_person_ID = Column(String)
    Delivery_person_Age = Column(Integer)
    Delivery_person_Ratings = Column(Float)
    Restaurant_latitude = Column(Float)
    Restaurant_longitude = Column(Float)
    Delivery_location_latitude = Column(Float)
    Delivery_location_longitude = Column(Float)
    Type_of_order = Column(String)
    Type_of_vehicle = Column(String)
    Time_taken = Column(Float)
    prediction = Column(Float)
    createdAt = Column(TIMESTAMP(timezone=True), default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=func.now())
