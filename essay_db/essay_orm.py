from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, Float, Text, String, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class Essay(Base):
    __tablename__ = "essay"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    added_on = Column(DateTime, default=datetime.utcnow)
    final_score = Column(Integer, nullable=False)
    criteria_score_1 = Column(Integer, nullable=False)
    criteria_score_2 = Column(Integer, nullable=False)
    criteria_score_3 = Column(Integer, nullable=False)
    criteria_score_4 = Column(Integer, nullable=False)
    criteria_score_5 = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    comments = Column(Text, nullable=False)

    prompt: Mapped["Prompt"] = relationship(back_populates="essays")
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompt.id"))


class Prompt(Base):
    __tablename__ = "prompt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    info = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    added_on = Column(DateTime, default=datetime.utcnow)
    url = Column(String, nullable=False)

    essays: Mapped[List["Essay"]] = relationship(back_populates="prompt")


metadata = Base.metadata
