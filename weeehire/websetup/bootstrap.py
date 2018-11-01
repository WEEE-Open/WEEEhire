# -*- coding: utf-8 -*-
"""Setup the weeehire application"""
from __future__ import print_function, unicode_literals
import transaction
from weeehire import model
from datetime import datetime
from os import environ as env


def bootstrap(command, conf, vars):
    """Place any commands to setup weeehire here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        a = model.User()
        a.user_name = env['ADMIN_USERNAME']
        a.display_name = env['ADMIN_USERNAME']
        a.email_address = env['ADMIN_EMAIL']
        a.password = env['ADMIN_PASS']
        a.created = datetime.now()

        model.DBSession.add(a)

        g = model.Group()
        g.group_name = 'managers'
        g.display_name = 'Managers Group'

        g.users.append(a)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = 'manage'
        p.description = 'This permission gives an administrative right'
        p.groups.append(g)

        model.DBSession.add(p)

        o = model.Option()
        o.key = "no_reply_email"
        o.value = env['NO_REPLY_EMAIL']
        model.DBSession.add(o)

        o = model.Option()
        o.key = "new_request_notify"
        o.value = "true"
        model.DBSession.add(o)

        o = model.Option()
        o.key = "recruiting"
        o.value = "true"
        model.DBSession.add(o)
       
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
