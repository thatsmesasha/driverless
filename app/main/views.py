from flask import render_template, redirect, request, flash, session
from . import main

@main.route('/', methods=['GET'])
def index():
    return render_template('/index.html')
