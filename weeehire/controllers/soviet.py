# -*- coding: utf-8 -*-
"""Soviet controller module"""

from tg import expose, redirect, abort, validate, flash, url
# from tg.i18n import ugettext as _
from tg import predicates

from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User


class SovietController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    allow_only = predicates.has_permission('manage')
    
    @expose('weeehire.templates.soviet')
    def index(self, **kw):
        users = DBSession.query(User).filter(User.user_id != 1).all()
        return dict(page='soviet-index', users=users)

    @expose('weeehire.templates.soviet-read')
    def read(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        return dict(page='soviet-read', user=user)

    @expose()
    def accept(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        return redirect('/soviet')

    @expose()
    def reject(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        return redirect('/soviet')
