# backend/models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('elderly', 'caregiver'), nullable=False)
    pairing_code = Column(String(6), index=True)
    paired_with_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(DateTime, server_default=func.now())

    paired_with = relationship('User', remote_side=[id], uselist=False)
    prescriptions = relationship('Prescription', back_populates='user', cascade='all, delete-orphan')
    voice_clips = relationship('VoiceClip', back_populates='caregiver', cascade='all, delete-orphan')


class Prescription(Base):
    __tablename__ = 'prescriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    image_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship('User', back_populates='prescriptions')
    medicines = relationship('Medicine', back_populates='prescription', cascade='all, delete-orphan')


class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer, ForeignKey('prescriptions.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    dosage = Column(String(50))
    frequency = Column(String(50))
    times = Column(JSON)

    prescription = relationship('Prescription', back_populates='medicines')
    dose_logs = relationship('DoseLog', back_populates='medicine', cascade='all, delete-orphan')


class DoseLog(Base):
    __tablename__ = 'dose_logs'
    id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, ForeignKey('medicines.id', ondelete='CASCADE'), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(Enum('taken', 'missed', 'delayed'), server_default='missed')
    taken_at = Column(DateTime)
    notified_caregiver = Column(Boolean, default=False)

    medicine = relationship('Medicine', back_populates='dose_logs')


class VoiceClip(Base):
    __tablename__ = 'voice_clips'
    id = Column(Integer, primary_key=True)
    caregiver_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    file_path = Column(String(255), nullable=False)
    message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    caregiver = relationship('User', back_populates='voice_clips')