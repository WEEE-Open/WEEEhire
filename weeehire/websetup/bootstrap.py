# -*- coding: utf-8 -*-
"""Setup the weeehire application"""
from __future__ import print_function, unicode_literals
import transaction
from weeehire import model


def bootstrap(command, conf, vars):
    """Place any commands to setup weeehire here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = 'admin'
        u.display_name = 'admin'
        u.email_address = 'weeeopen@yandex.ru'
        u.password = 'open'

        model.DBSession.add(u)

        g = model.Group()
        g.group_name = 'managers'
        g.display_name = 'Managers Group'

        g.users.append(u)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = 'manage'
        p.description = 'This permission gives an administrative right'
        p.groups.append(g)

        model.DBSession.add(p)

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
