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

        s = model.User()
        s.user_name = 's000000'
        s.display_name = s.user_name
        s.first_name = 'Aspirante'
        s.last_name = 'Svitabulloni'
        s.email_address = 'aspirante_svitabulloni@fatmax.com'
        s.study_course = 'FISICA DELLE VITI'
        s.year = 'LM1'
        s.letter = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        s.compiled = datetime.now()
        s.password = 'asd'
        s.token = 'asd'
        s.created = datetime.now()

        model.DBSession.add(s)


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
