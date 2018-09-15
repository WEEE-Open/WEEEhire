# -*- coding: utf-8 -*-
"""Soviet controller module"""

from tg import expose, flash, redirect, abort
from tg import predicates, request
from tgext.mailer import get_mailer, Message
from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User


class SovietController(BaseController):
    allow_only = predicates.has_permission('manage')
    
    @expose('weeehire.templates.soviet')
    def index(self, filter=None, **kw):
        if filter == 'awaiting':
            users = DBSession.query(User).filter(User.user_id != 1).filter_by(status=None).all()
        elif filter == 'approved':
            users = DBSession.query(User).filter(User.user_id != 1).filter_by(status=True).all()
        elif filter == 'rejected':
            users = DBSession.query(User).filter(User.user_id != 1).filter_by(status=False).all()
        else:
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
        user.status = True
        return redirect('/soviet')

    @expose()
    def reject(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        user.status = False
        return redirect('/soviet')

    @expose()
    def clear(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        user.status = None
        return redirect('/soviet')

    @expose()
    def publish(self, **kw):
        approved_users = DBSession.query(User).filter_by(published=False).filter_by(status=True).all()
        rejected_users = DBSession.query(User).filter_by(published=False).filter_by(status=False).all()

        for i in range(len(approved_users)):
            approved_users[i].published = True
            approved_users[i] = approved_users[i].email_address

        for i in range(len(rejected_users)):
            rejected_users[i].published = True
            rejected_users[i] = rejected_users[i].email_address

        mailer = get_mailer(request)
        if approved_users:
            message = Message(subject="Reclutamento WEEE Open",
                              sender="weeeopen@yandex.ru",
                              bcc=approved_users,
                              body="Ciao, sei ammesso al colloquio!\n\nTeam WEEE Open"
                              )
            mailer.send(message)
        if rejected_users:
            message = Message(subject="Reclutamento WEEE Open",
                              sender="weeeopen@yandex.ru",
                              bcc=rejected_users,
                              body="Ciao, sei stato scartato!\n\nTeam WEEE Open"
                              )
            mailer.send(message)

        flash('Risultati pubblicati correttamente')
        return redirect('/soviet')

    @expose()
    def delete(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        DBSession.delete(user)
        return redirect('/soviet')
