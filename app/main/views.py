from flask import render_template, redirect, request, flash, session
from . import main

@main.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@main.route('/manual', methods=['GET'])
def manual():
    return render_template('/manual.html')

@main.route('/training', methods=['GET'])
def training():
    return render_template('/training.html')

@main.route('/self-driving', methods=['GET'])
def self_driving():
    return render_template('/self-driving.html')
