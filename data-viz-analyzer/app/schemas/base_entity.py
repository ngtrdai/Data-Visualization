from sqlalchemy import Column, Integer, Time


class BaseEntity:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)
