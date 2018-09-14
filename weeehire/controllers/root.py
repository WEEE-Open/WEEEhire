# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import predicates, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from weeehire import model
from weeehire.controllers.secure import SecureController
from weeehire.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from weeehire.lib.base import BaseController
from weeehire.controllers.error import ErrorController
from weeehire.controllers.signup import SignupController
from weeehire.controllers.form import FormController
from weeehire.controllers.soviet import SovietController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the weeehire application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    soviet = SovietController()
    signup = SignupController()
    form = FormController()

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "weeehire"

    @expose('weeehire.templates.index')
    def index(self):
        """Handle the front-page."""
        if not request.identity:
            return redirect('/signup')
        else:
            if request.identity['user'].user_id == 1:
                return redirect('/soviet')
            else:
                return redirect('/form')

    @expose('weeehire.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if request.identity:
            return redirect('/')
        if failure is not None:
            if failure == 'user-not-found' or failure == 'invalid-password':
                flash(_('Username o password non validi'), 'error')
            elif failure == 'user-not-verified':
                flash(_('Utente non verificato'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Bentornato, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('Ciawa asd!'))
        return HTTPFound(location=came_from)
