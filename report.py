import json, jsonschema, _json
from flask import Blueprint, render_template, request, redirect, url_for, Flask
from extensions import db
import sqlalchemy as sql
from routes.agBp import agBp
from model.agModel import Agenda, Desktop
from sqlalchemy import func, or_, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker