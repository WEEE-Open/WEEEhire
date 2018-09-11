# -*- coding: utf-8 -*-
"""Form controller module"""

from tg import expose, redirect, validate, flash, url
# from tg.i18n import ugettext as _
# from tg import predicates

from weeehire.lib.base import BaseController
# from weeehire.model import DBSession


class FormController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    # allow_only = predicates.not_anonymous()
    
    @expose('weeehire.templates.form')
    def index(self, **kw):
        return dict(page='form-index')
