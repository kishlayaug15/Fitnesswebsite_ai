from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from langchain.llms import Ollama
from reportlab.lib.utils import simpleSplit
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
import variables
import io
#from navfile import diet_type, calories


def create_workout_plan_pdf() -> bytes:
    # plan_type = str(input())
    # duration = int(input())
    # intensity = str(input())

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 40
    max_line_width = width - 2 * margin
    olla = Ollama(base_url=variables.url,model= variables.model_name)
    
    text = f"""
    {olla(f'Generate a detailed workout plan for a {variables.intensity} intensity {variables.plan_type} plan with {variables.duration} minutes per day.')}
    """
    
    text_lines = text.split("\n")
    
    y_position = height - 40
    for line in text_lines:
        wrapped_lines = simpleSplit(line, c._fontname, c._fontsize, max_line_width)
        for wrapped_line in wrapped_lines:
            if y_position < margin:
                c.showPage()
                y_position = height - margin
            c.drawString(margin, y_position, wrapped_line.strip())
            y_position -= 20
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def create_meal_plan_pdf() -> bytes:
    # diet_type = str(input())
    # calories = int(input())
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 40
    max_line_width = width - 2 * margin
    olla = Ollama(base_url=variables.url,model= variables.model_name)
    
    text = f"""
    {olla(f'Generate a detailed meal plan for a {variables.diet_type} diet with {variables.calories} calories per day.')}
    """
    
    text_lines = text.split("\n")
    
    y_position = height - 40
    for line in text_lines:
        wrapped_lines = simpleSplit(line, c._fontname, c._fontsize, max_line_width)
        for wrapped_line in wrapped_lines:
            if y_position < margin:
                c.showPage()
                y_position = height - margin
            c.drawString(margin, y_position, wrapped_line.strip())
            y_position -= 20
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def create_health_plan_pdf() -> bytes:
    # user_data = {}
    # health_params = int(input("Enter the User Health Information: "))
    # for i in range(health_params):
    #     key = input(f"Enter health parameter {i+1}: ")
    #     value = input(f"Enter {key} value: ")
    #     user_data[key] = value
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 40
    max_line_width = width - 2 * margin
    olla = Ollama(base_url=variables.url,model= variables.model_name)
    
    text = f"""
    {olla(f'Generate a detailed health plan for a {variables.user_data} data per day.')}
    """
    
    text_lines = text.split("\n")
    
    y_position = height - 40
    for line in text_lines:
        wrapped_lines = simpleSplit(line, c._fontname, c._fontsize, max_line_width)
        for wrapped_line in wrapped_lines:
            if y_position < margin:
                c.showPage()
                y_position = height - margin
            c.drawString(margin, y_position, wrapped_line.strip())
            y_position -= 20
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
