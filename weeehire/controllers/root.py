# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _
from tg.i18n import get_lang, set_lang
from tg.exceptions import HTTPFound

from weeehire.lib.base import BaseController
from weeehire.controllers.error import ErrorController
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
    soviet = SovietController()
    form = FormController()

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "weeehire"

    @expose('weeehire.templates.index')
    def index(self):
        """Handle the front-page."""
        if request.identity:
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
                flash(_('Username e/o password non validi'), 'error')
            elif failure == 'user-not-verified':
                flash(_('Utente non verificato'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Username e/o password non validi'), 'error')

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
        flash('Ciawa asd!')
        return HTTPFound(location=came_from)

    @expose('weeehire.templates.privacy')
    def privacy(self):
        """Shows the privacy policy page"""
        return dict(page='privacy-page')

    @expose('weeehire.templates.server')
    def server(self):
        """Uovo di Pasqua"""
        return dict(page='server-img')

    @expose()
    def lang(self, l, came_from=lurl('/')):
        """Changes the language for the current session"""
        set_lang(l)
        return redirect(came_from)

