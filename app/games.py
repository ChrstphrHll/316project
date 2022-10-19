from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from .models.game import Game

