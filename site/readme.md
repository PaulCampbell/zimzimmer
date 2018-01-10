# The website



## Server

It's a flask app

Use some virtual env:

```
virtualenv .
source bin/activate
```

Cool - You're now running a python virtual env.  If you wanna stop that thing type `deactivate`.

Restore your dependencies

```
pip install -r requirements.txt
```

to run up the app

`python app.py`

oh - you'll want to build the javascripts first by the way.

```
cd browser
yarn
yarn build
```

## Browser

It's a javascript app. you can find it in the `browser` directory.

