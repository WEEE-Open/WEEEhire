# -*- coding: utf-8 -*-
"""Form controller module"""

from tg import expose, redirect, request, flash, url, abort
from tg.i18n import ugettext as _

from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User
from tgext.mailer import get_mailer, Message
from datetime import datetime
from string import ascii_letters, digits
from random import randint
from os import environ as env


def generate_password():
    alphabet = ascii_letters + digits
    password = ""
    for c in range(32):
        password += str(alphabet[randint(0, len(alphabet) - 1)])
    return password


def is_valid_sn(sn):
    if len(sn) != 7:
        return False
    if sn[0] not in ['s', 'd']:
        return False
    sn = sn[1:7]
    if not sn.isdigit():
        return False
    return True


class FormController(BaseController):
    @expose('weeehire.templates.form-index')
    def index(self, status=None, **kw):
        if status == 'success':
            flash(_('Candidatura inviata con successo! Controlla la tua mail del poli.'))
        return dict(page='form-index')

    @expose('weeehire.templates.form')
    def edit(self, error=None, **kw):
        if error == 'm_invalid':
            flash(_('Caro utonto, inserisci il tuo numero di matricola nel formato indicato.'), 'error')
        elif error == 'm_used':
            flash(_('Matricola già in uso!'), 'error')
        courses = [
            "",
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
            "",
            "1",
            "2",
            "3",
            "LM1",
            "LM2"
        ]

        interests = [
            "",
            "Elettronica",
            "Programmazione",
            "Design",
            "Amministrazione",
            "Pubbliche relazioni",
            "Altro"
        ]
        return dict(page='form-edit', courses=courses, years=years, interests=interests)

    @expose()
    def save(self, **kw):
        if not is_valid_sn(kw['user_name']):
            return redirect('/form/edit?error=m_invalid')
        user = User.by_user_name(kw['user_name'])
        if user:
            return redirect('/form/edit?error=m_used')

        token = generate_password()
        passwd = generate_password()

        user = User()
        user.user_name = kw['user_name']
        user.email_address = kw['user_name'] + '@studenti.polito.it'
        user.display_name = kw['user_name']
        user.first_name = kw['first_name']
        user.last_name = kw['last_name']
        user.study_course = kw['cdl']
        user.year = kw['year']
        user.interest = kw['interest']
        user.letter = kw['letter']
        user.compiled = datetime.now()
        user.token = token
        user.password = passwd
        user.created = datetime.now()
        DBSession.add(user)
        DBSession.flush()

        status_link = url('/form/status?m=', None, True) + user.user_name
        status_link += '&auth=' + token

        mailer = get_mailer(request)
        message = Message(subject="Reclutamento WEEE Open",
                          sender=env['ADMIN_EMAIL'],
                          recipients=[user.email_address],
                          body=("Ciao!\n\nAbbiamo ricevuto la tua candidatura, di seguito troverai\n" +
                                "il link che ti permetterà di verificare lo stato della tua domanda.\n\n" +
                                status_link +
                                "\n\nNon è necessario refreshare la pagina come un forsennato!\n" +
                                "Una mail automatica ti avviserà quando avremo preso una decisione.\n" +
                                "Ciawa! asd\n\nTeam WEEE Open"
                                )
                          )
        mailer.send(message)
        return redirect('/form?status=success')

    @expose('weeehire.templates.form-status')
    def status(self, m, auth, **kw):
        if not m or not auth:
            abort(404)
        user = User.by_user_name(m)
        if user:
            if user.token == auth:
                return dict(page='form-status', user=user)
        abort(404)
