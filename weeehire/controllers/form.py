# -*- coding: utf-8 -*-
"""Form controller module"""

from tg import expose, redirect, request, validate, flash, url, predicates
# from tg.i18n import ugettext as _
# from tg import predicates

from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User
from datetime import datetime


class FormController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    allow_only = predicates.not_anonymous()
    
    @expose('weeehire.templates.form-index')
    def index(self, **kw):
        uid = request.identity['user'].user_id
        user = User.by_user_id(uid)
        if user.compiled:
            return redirect('/form/status')
        return dict(page='form-index')

    @expose('weeehire.templates.form')
    def edit(self, **kw):
        courses = [
            "INGEGNERIA ELETTRONICA E DELLE COMUNICAZIONI",
            "ELECTRONIC AND COMMUNICATIONS ENGINEERING",
            "INGEGNERIA AEROSPAZIALE",
            "INGEGNERIA BIOMEDICA",
            "INGEGNERIA CHIMICA E ALIMENTARE",
            "INGEGNERIA CIVILE",
            "INGEGNERIA DEI MATERIALI",
            "INGEGNERIA DEL CINEMA E DEI MEZZI DI COMUNICAZIONE",
            "INGEGNERIA DELL'AUTOVEICOLO",
            "AUTOMOTIVE ENGINEERING",
            "INGEGNERIA DELLA PRODUZIONE INDUSTRIALE",
            "INGEGNERIA EDILE",
            "INGEGNERIA ELETTRICA",
            "INGEGNERIA ELETTRONICA",
            "INGEGNERIA ENERGETICA",
            "INGEGNERIA FISICA",
            "INGEGNERIA GESTIONALE",
            "INGEGNERIA INFORMATICA",
            "COMPUTER ENGINEERING",
            "INGEGNERIA MECCANICA",
            "MECHANICAL ENGINEERING",
            "INGEGNERIA PER L'AMBIENTE E IL TERRITORIO",
            "MATEMATICA PER L'INGEGNERIA"
        ]

        years = [
            "1",
            "2",
            "3",
            "LM1",
            "LM2"
        ]
        return dict(page='form-edit', courses=courses, years=years)

    @expose()
    def save(self, **kw):
        uid = request.identity['user'].user_id
        user = User.by_user_id(uid)
        user.first_name = kw['first_name']
        user.last_name = kw['last_name']
        user.study_course = kw['cdl']
        user.year = kw['year']
        user.letter = kw['letter']
        user.compiled = datetime.now()
        return redirect('/')

    @expose('weeehire.templates.form-status')
    def status(self, **kw):
        return dict(page='form-status')
