# -*- coding: utf-8 -*-
"""Form controller module"""

from tg import expose, redirect, response, request, flash, url, abort
from tg.i18n import ugettext as _
from tg.i18n import get_lang

from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User, Option
from tgext.mailer import get_mailer, Message
from datetime import datetime
from string import ascii_letters, digits
from random import randint
from json import dumps


def generate_password():
    alphabet = ascii_letters + digits
    password = ""
    for c in range(32):
        password += str(alphabet[randint(0, len(alphabet) - 1)])
    return password


def is_valid_sn(sn):
    if len(sn) != 7:
        return False
    if sn[0].lower() not in ['s', 'd']:
        return False
    sn = sn[1:7]
    if not sn.isdigit():
        return False
    return True


class FormController(BaseController):
    @expose('weeehire.templates.form-index')
    def index(self, **kw):
        recruiting = Option.get_value('recruiting');
        if not recruiting:
            flash(_("Siamo spiacenti, attualmente siamo al completo."), 'error')
        return dict(page='form-index', recruiting=recruiting)

    @expose('weeehire.templates.form')
    def edit(self, **kw):
        if not Option.get_value('recruiting'):
            return redirect('/')
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
            {"value": "", "text": ""},
            {"value": "1 Triennale", "text": _("1 Triennale")},
            {"value": "2 Triennale", "text": _("2 Triennale")},
            {"value": "3 Triennale", "text": _("3 Triennale")},
            {"value": "1 Magistrale", "text": _("1 Magistrale")},
            {"value": "2 Magistrale", "text": _("2 Magistrale")},
            {"value": "Dottorato", "text": _("Dottorato")}
        ]

        interests = [
            {"value": "", "text": ""},
            {"value": "Riparazione Hardware", "text": _("Riparazione Hardware")},
            {"value": "Elettronica", "text": _("Elettronica")},
            {"value": "Sviluppo Software", "text": _("Sviluppo Software")},
            {"value": "Sysadmin", "text": _("Sysadmin")},
            {"value": "Design e comunicazione visiva", "text": _("Design e comunicazione visiva")},
            {"value": "Design per il riuso", "text": _("Design per il riuso")},
            {"value": "Pubbliche relazioni", "text": _("Pubbliche relazioni")},
            {"value": "Altro", "text": _("Altro")}
        ]
        return dict(page='form-edit', courses=courses, years=years, interests=interests)

    @expose()
    def save(self, **kw):
        if not is_valid_sn(kw['user_name']):
            flash(_('Inserisci il tuo numero di matricola nel formato indicato.'), 'error')
            return redirect('/form/edit')
        user = User.by_user_name(kw['user_name'])
        if user:
            flash(_('Matricola già in uso!'), 'error')
            return redirect('/form/edit')

        token = generate_password()
        passwd = generate_password()

        user = User()
        user.user_name = kw['user_name'].lower()
        user.email_address = user.user_name + \
                             ('@studenti.polito.it' if user.user_name[0] == 's' else '@polito.it')
        user.display_name = user.user_name
        user.first_name = kw['first_name']
        user.last_name = kw['last_name']
        user.study_course = kw['cdl']
        user.year = kw['year']
        user.interest = kw['interest']
        user.lang = ('it' if not get_lang(all=False)[0] else get_lang(all=False)[0])
        user.letter = kw['letter']
        user.token = token
        user.password = passwd
        user.created = datetime.now()
        DBSession.add(user)
        DBSession.flush()

        status_link = url('/form/status?m=', None, True) + user.user_name
        status_link += '&auth=' + token

        noreply_email = Option.get_value('no_reply_email')
        mailer = get_mailer(request)
        message = Message(subject=_("Reclutamento WEEE Open"),
                          sender=noreply_email,
                          recipients=[user.email_address],
                          body=(_("""Ciao!
Abbiamo ricevuto la tua candidatura per il team WEEE Open, questa è la pagina da cui potrai verificare lo stato della tua domanda:

%s

Se la domanda sarà approvata, riceverai un'email sempre a questo indirizzo con scritto chi contattare per passare al colloquio. Le stesse informazioni saranno visibili anche alla pagina di cui sopra.

Buona fortuna ;)
Il software WEEEHire per conto del team WEEE Open
""") % status_link
                                )
                          )
        mailer.send(message)

        if Option.get_value('new_request_notify'):
            admin_email = User.by_user_id(1).email_address
            message = Message(subject="WEEEhire - Nuova richiesta ricevuta",
                              sender=noreply_email,
                              recipients=[admin_email],
                              body=(url('/soviet/read?uid=', None, True) + str(user.user_id))
                              )
            mailer.send(message)
        flash(_(
            "Candidatura inviata con successo!\nSalva questa pagina nei preferiti per controllare lo stato. Ti abbiamo inviato lo stesso link anche a %s") % user.email_address)
        return redirect(status_link)

    @expose('weeehire.templates.form-status')
    def status(self, m, auth, **kw):
        if not m or not auth:
            abort(404)
        user = User.by_user_name(m)
        if user:
            if user.token == auth:
                deletion_link = url("/form/delete?m=") + user.user_name + "&auth=" + user.token
                gdpr_link = url("/form/gdpr_data?m=") + user.user_name + "&auth=" + user.token
                return dict(page='form-status', user=user, deletion_link=deletion_link, gdpr_link=gdpr_link)
        abort(404)

    @expose('json', content_type="application/json")
    def gdpr_data(self, m, auth, **kw):
        if not m or not auth:
            abort(404)
        user = User.by_user_name(m)
        if user:
            if user.token == auth:
                response.headerlist.append(('Content-Disposition',
                                            str('attachment;filename=%s-data.json' % user.user_name)))
                user_dict = dict(
                    id=user.user_id,
                    username=user.user_name,
                    auth_token=user.token,
                    email=user.email_address,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    study_course=user.study_course,
                    study_year=user.year,
                    interest=user.interest,
                    language=user.lang,
                    motivation_letter=user.letter,
                    date_compiled=user.created
                )
                return dumps(user_dict, indent=2)
        abort(404)

    @expose()
    def delete(self, m, auth, **kw):
        if not m or not auth:
            abort(404)
        user = User.by_user_name(m)
        if user:
            if user.token == auth:
                DBSession.delete(user)
                flash(_('Tutti i tuoi dati sono stati cancellati!'))
                return redirect('/')
        abort(404)
