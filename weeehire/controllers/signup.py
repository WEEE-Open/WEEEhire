# -*- coding: utf-8 -*-
"""Signup controller module"""

from datetime import datetime
from tg import expose, redirect, validate, flash, url, lurl, request, abort
from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User
from tw2.core import RegexValidator, EmailValidator, Required, _
import tw2.forms as twf
from tgext.mailer import get_mailer, Message
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


class SignupForm(twf.Form):
    class child(twf.widgets.BaseLayout):
        sn = twf.TextField(css_class="form-control mt-10",
                           placeholder="s123456")

    action = lurl('/signup/verify')
    submit = twf.SubmitButton(value='Invia', css_class="btn btn-success mt-10")


class SignupController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    # allow_only = predicates.not_anonymous()

    @expose('weeehire.templates.signup')
    def index(self, status=None, **kw):
        if status == 'badsn':
            flash(_('Caro utonto, inserisci il tuo numero di matricola nel formato indicato.'), 'error')
        if status == 'login':
            flash(_('Questa matricola è già in uso, fai il login!'), 'error')
        if status == 'success':
            flash(_('Apri il link di conferma che hai ricevuto sulla tua mail del poli'))
        return dict(page='signup-index', form=SignupForm)

    @expose()
    def verify(self, **kw):
        if len(kw) < 1:
            abort(404)
        matricola = kw['sn']
        matricola.lower()
        if is_valid_sn(matricola):
            if matricola.isdigit():
                email = matricola + '@studenti.polito.it'
            else:
                email = matricola + '@studenti.polito.it'
            user = User.by_email_address(email)
            if not user:
                confirm_link = url('/signup/register?email=', None, True) + email
                token = generate_password()
                confirm_link += '&auth=' + token
                password = generate_password()

                u = User()
                u.user_name = matricola
                u.display_name = matricola
                u.email_address = email
                u.token = token
                u.password = password
                DBSession.add(u)
                DBSession.flush()

                mailer = get_mailer(request)
                message = Message(subject="Reclutamento WEEE Open",
                                  sender="weeeopen@yandex.ru",
                                  recipients=[email],
                                  body=("Ciawa! asd\nClicca qua per attivare l'account " + confirm_link +
                                        "\n\n------------------CREDENZIALI-DI-ACCESSO------------------" +
                                        "\nIl tuo username: " + matricola +
                                        "\nLa tua password: " + password +
                                        "\n----------------------------------------------------------" +
                                        "\n\nCiawa di nuovo! asd" +
                                        "\n\n\nPS: Ciao, sono il developer di questo ameno sito web,\n" +
                                        "volevo solo avvisarti del fatto che non ho intenzione di implementare\n" +
                                        "un sistema per permetterti di cambiare la password, quindi se la perdi\n" +
                                        "sono cazzi tuoi. Ti consiglio di non cancellare questa mail, o se proprio\n" +
                                        "vuoi essere scartato ancor prima che leggiamo il tuo form, stampa questa\n" +
                                        "mail, tanto gli alberi ricrescono in fretta e amano essere abbattuti :)\n" +
                                        "SEEEH!! Fanculo l'ambiente! Viva il consumismo spropositato! :O"
                                        )
                                  )
                mailer.send(message)
            else:
                return redirect("/signup?status=login")
            return redirect("/signup?status=success")
        else:
            return redirect("/signup?status=badsn")

    @expose('weeehire.templates.post_signup')
    def register(self, email, auth, **kw):
        if not email or not auth:
            abort(404)
        user = User.by_email_address(email)
        if user:
            if user.created:
                flash(_('Utente già verificato'), 'warning')
                return dict()
            if user.token == auth:
                user.created = datetime.now()
                flash(_('Autenticazione riuscita'))
            else:
                flash(_('Autenticazione fallita'), 'error')
        else:
            flash(_('Utente non registrato'), 'error')
        DBSession.flush()
        return dict()