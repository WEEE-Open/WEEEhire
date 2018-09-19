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
    def index(self, **kw):
        return dict(page='form-index')

    @expose('weeehire.templates.form')
    def edit(self, error=None, **kw):
        if error == 'm_invalid':
            flash(_('Caro utonto, inserisci il tuo numero di matricola nel formato indicato.'), 'error')
        elif error == 'm_used':
            flash(_('Matricola già in uso!'), 'error')
        courses = [
            "",
			"Automotive Engineering",
			"Communications And Computer Networks Engineering",
			"Design E Comunicazione Visiva",
			"Design Sistemico",
			"Electronic And Communications Engineering",
			"Ict For Smart Societies",
			"Ingegneria Aerospaziale",
			"Ingegneria Biomedica",
			"Ingegneria Chimica E Alimentare",
			"Ingegneria Chimica E Dei Processi Sostenibili",
			"Ingegneria Civile / Civil Engineering",
			"Ingegneria Dei Materiali",
			"Ingegneria Del Cinema E Dei Mezzi Di Comunicazione",
			"Ingegneria Del Petrolio E Mineraria",
			"Ingegneria Dell'Autoveicolo",
			"Ingegneria Della Produzione Industriale E Dell'Innovazione Tecnologica",
			"Ingegneria Della Produzione Industriale",
			"Ingegneria Edile",
			"Ingegneria Elettrica",
			"Ingegneria Elettronica / Electronic Engineering",
			"Ingegneria Elettronica E Delle Comunicazioni",
			"Ingegneria Energetica E Nucleare",
			"Ingegneria Energetica",
			"Ingegneria Fisica",
			"Ingegneria Gestionale / Engineering And Management",
			"Ingegneria Informatica / Computer Engineering",
			"Ingegneria Matematica",
			"Ingegneria Meccanica / Mechanical Engineering",
			"Ingegneria Meccatronica / Mechatronic Engineering",
			"Ingegneria Per L'Ambiente E Il Territorio",
			"Matematica Per L'Ingegneria",
			"Nanotechnologies For Icts / Nanotecnologie Per Le Ict",
			"Petroleum And Mining Engineering",
			"Physics Of Complex Systems / Fisica Dei Sistemi Complessi",
			"Pianificazione Territoriale, Urbanistica E Paesaggistico-Ambientale",
			"Architettura"
        ]

        years = [
            "",
            "1 Triennale",
            "2 Triennale",
            "3 Triennale",
            "1 Magistrale",
            "2 Magistrale",
            "Dottorato"
        ]

        interests = [
            "",
            "Elettronica",
            "Sviluppo Software",
            "Sysadmin",
            "Design e comunicazione visiva",
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
                          sender="weeeopen@yandex.ru",
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
        flash(_("Candidatura inviata con successo!\nSalvati questo link (che per scaramanzia ti abbiamo anche inviato sulla mail del poli) tra i preferiti."))
        return redirect(status_link)

    @expose('weeehire.templates.form-status')
    def status(self, m, auth, **kw):
        if not m or not auth:
            abort(404)
        user = User.by_user_name(m)
        if user:
            if user.token == auth:
                return dict(page='form-status', user=user)
        abort(404)
