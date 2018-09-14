# WEEEhire

Form di reclutamento

## How to install/run/do things

Type these arcane commands:

```Shell
	virtualenv -p /usr/bin/python3 venv  # or just "virtualenv venv", but this project requires Python 3
	source venv/bin/activate
	pip install tg.devtools tgext.pluggable tgext.mailer
	pip install -e .
	export ADMIN_USERNAME='admin'
	export ADMIN_EMAIL='something@example.com'
	export ADMIN_PASS='p4ssw0rd'
	gearbox setup-app
	gearbox serve
```

You'll also need a `developement.ini` file, which contains billions upon billions of settings more than `test.ini`, so just ask @Hyd3L for one.

