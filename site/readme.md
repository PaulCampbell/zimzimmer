# The website

We have a website that does a couple of things:

1) Allows you to collect people saying a variety of things. Navigate to
localhost:5000/get_voice, and follow the instructions.  When you get to the end and
submit the data, it will be sent up to the server where it will be turned into .wav files
and saved to disk.

2) Loads a tensorflow model for data evaluation.  Navigate to
localhost:5000/whos_that and follow the instructions. When you submit the data it will
send the recorded speech to the server. The server extracts relevant features from the sound and submits it
to the tensorflow model for evaluation. The server should respond with the name of the person who was speaking.


## Server App

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


## Browser App

It's a javascript app. you can find it in the [browser](./browser) directory.

Build it before you run up your website

```
cd browser
yarn
yarn build
```
