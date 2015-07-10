from flask.ext.wtf import Form
from wtforms import TextField, validators
from wtforms.validators import InputRequired


class RedditPostForm(Form):
    """Form to submit daily inspiration on /r/chadev..."""

    title = TextField(label=u'Title', validators=[InputRequired()])
    link = TextField(label=u'Link', validators=[InputRequired()])
