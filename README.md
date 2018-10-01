# WEEEhire

Form di reclutamento

## How to install/run/do things

You'll need a `developement.ini` file, which contains billions upon billions of settings more than `test.ini`,  
so just ask [Hyd3L](https://github.com/Hyd3L) for one.

Once you've obtained a `development.ini` file, check these lines and edit them:
```INI
#tgext.mailer data:
mail.host = mail.example.com
mail.username = yourtestemail@example.com
mail.password = yourtestemailultrasecurepassword(yourbirthdate)
mail.tls = true
```

Open a shell and type these arcane commands:

```Shell
# First of, clone this repository
git clone https://github.com/WEEE-Open/WEEEhire

# Put the development.ini file in the cloned repository
mv /path/to/development.ini /path/to/weeehire

# Create a Python virtual environment within the cloned repository (minimum version required: 3.6)
python3 -m venv venv

# Edit the venv/bin/activate script and append these lines
# Do this only in developement, they're necessary to initially seed the database
export ADMIN_USERNAME='admin'
export ADMIN_EMAIL='admin@example.com'
export ADMIN_PASS='ultrasecurepassword'
export NO_REPLY_EMAIL='yourtestemail@example.com'

# Activate the virtual environment
source venv/bin/activate

# Install the application dependencies
pip install -e .

# Setup the web application
gearbox setup-app

# Start the testing web-server (accessible at http://127.0.0.1:8080)
gearbox serve --reload --debug
```

This web-application is powered by the [TurboGears](http://www.turbogears.org) Python web framework.

## Translations

To generate a new .po file, use:

```Shell
xgettext --from-code=UTF-8 -o weeehire/i18n/en/LC_MESSAGES/weeehire_new.po weeehire/controllers/*.py weeehire/model/*.py weeehire/templates/*.xhtml*
msgmerge --backup=off --update weeehire/i18n/en/LC_MESSAGES/weeehire.po weeehire/i18n/en/LC_MESSAGES/weeehire_new.po
mv weeehire/i18n/en/LC_MESSAGES/weeehire_new.po weeehire/i18n/en/LC_MESSAGES/weeehire.po
```
