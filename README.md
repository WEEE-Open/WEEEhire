# WEEEhire

Form di reclutamento

## How to install/run/do things

Open a shell and type these arcane commands:

```Shell
# First of, clone this repository
git clone https://github.com/WEEE-Open/WEEEhire

# Go to the cloned repository
cd WEEEHire

# You could review the settings in this file after copying it, but probably you won't
cp development.ini.example development.ini

# Create a Python virtual environment within the cloned repository (minimum version required: 3.6)
python3 -m venv venv

# Edit the venv/bin/activate script and append these lines beginning with "export"
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

## Translations

To update .po files with new strings:

```Shell
python setup.py extract_messages
python setup.py update_catalog
```

Compile the new translation:

```Shell
python setup.py compile_catalog
```

To add an entirely new language (japanese in this example):

```Shell
python setup.py extract_messages
python setup.py init_catalog -l jp
```

This web-application is powered by the [TurboGears](http://www.turbogears.org) Python web framework.

## Container

You're better off figuring out how to configure Apache to proxy requests to Turbogears directly. Seriously.

The Dockerfile is badly written and uwsgi goes into instant segmentation fault when starting up for no apparent reason.
There are only a handful of Stack Overflow questions with 0 answers and 0 upvotes mentioning the problem.

Also the `RUN gearbox setup-app` and ENV stuff is probably wrong, since env vars are needed only when building but you
shouldn't leave a plaintext password in the Dockerfile and for some reason Turbogears wants the development.ini file.

You may or may not need this:

```
docker run ... \
-e ADMIN_USERNAME='admin' \
-e ADMIN_EMAIL='admin@example.com' \
-e ADMIN_PASS='ultrasecurepassword' \
-e NO_REPLY_EMAIL='yourtestemail@example.com'
```

But seriously, if you can coerce that flaming wreckage of a container into something that barely even works,
please send a pull request. It will be greatly appreciated.
