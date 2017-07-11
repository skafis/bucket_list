# run.py
from flask import render_template, Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()