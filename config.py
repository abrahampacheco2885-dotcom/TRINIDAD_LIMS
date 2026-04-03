import os
from datetime import timedelta

class Config:
    # Prioriza la clave de entorno de Render, si no, usa una de desarrollo
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-nexus-2026')
    
    # Base de datos: Usa DATABASE_URL de Render (PostgreSQL) o SQLite local para pruebas
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///trinidad_lims.db')
    
    # Si la URL de Render empieza con "postgres://", la corregimos a "postgresql://" (Requisito de SQLAlchemy 1.4+)
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Configuración de PDF: En Render no usamos la ruta de Windows C:\
    # Si estamos en Render, intentamos usar el binario del sistema
    WKHTMLTOPDF_PATH = os.environ.get('WKHTMLTOPDF_PATH', '/usr/local/bin/wkhtmltopdf')

# Esto permite que app.config.from_object(Config) funcione directamente
