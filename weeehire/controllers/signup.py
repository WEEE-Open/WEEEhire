# -*- coding: utf-8 -*-
"""Signup controller module"""

from tg import expose, redirect, validate, flash, lurl
# from tg.i18n import ugettext as _
# from tg import predicates

from weeehire.lib.base import BaseController
# from weeehire.model import DBSession
from tw2.core import RegexValidator, _
import tw2.forms as twf
import re


class PolitoMailVaildator(RegexValidator):
    msgs = {
        'badregex': ('bademail', _('Must be your polito mail address')),
    }
    regex = re.compile('^[\w\-.]+@[\w\-.]+polito.it')


class SignupForm(twf.Form):
    class child(twf.widgets.TableLayout):
        email = twf.TextField(validator=PolitoMailVaildator)
    action = lurl('/signup/verify')
    submit = twf.SubmitButton(value='Submit')


class SignupController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    # allow_only = predicates.not_anonymous()
    
    @expose('weeehire.templates.signup')
    def index(self, **kw):
        return dict(page='signup-index', form=SignupForm)

    @expose()
    @validate(SignupForm, error_handler=index)
    def verify(self, **kw):
        email = kw['email']
        print(email)
        return redirect("/")
