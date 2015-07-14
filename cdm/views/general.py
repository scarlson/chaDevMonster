# -*- coding: utf-8 -*-

import os
import arrow
import hmac
import hashlib
import subprocess
from flask import Blueprint, render_template, flash
from flask import Flask, request
from cdm.forms.forms import RedditPostForm
from cdm.models.submission import Submission
from cdm import db

mod = Blueprint('general', __name__)


@mod.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@mod.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@mod.route('/', methods=['POST', 'GET'])
def index():
    """Landing page."""
    form = RedditPostForm()
    if form.validate_on_submit():
        title = form.title.data
        link = form.link.data
        if link_in_db(link):
            flash(
                u'This link has already been submitted, please submit another', 'danger')
            return render_template('index.html', form=form)
        save_to_db(title, link)
        flash(u'Your information has been submitted and will be posted to reddit soon. Thank you.', 'success')
        return render_template('success.html')

    return render_template('index.html', form=form)


@mod.route('/about', methods=['GET'])
def about():
    """About page."""
    return render_template('about.html')


@mod.route('/queue', methods=['GET'])
def queue():
    """List links and titles that are waiting to be submitted to reddit."""
    queue = Submission.query.filter_by(submitted=False).order_by(Submission.created_on)

    return render_template('queue.html', queue=queue)


@mod.route('/reddit_callback')
def reddit_callback():
    from flask import abort, request
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    # We'll change this next line in just a moment
    return "got a code! %s" % code

@mod.route("/payload", methods=['POST'])
def github_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            if payload['commits'][0]['distinct'] == True:
                try:
                    cmd_output = subprocess.check_output(
                        ['git', 'pull', 'origin', 'master'],)
                    cmd_output = cmd_output + subprocess.check_output(
                        ['sudo', 'supervisorctl', 'restart', 'gunicorn'],)

                    return jsonify({'msg': str(cmd_output)})
                except subprocess.CalledProcessError as error:
                    return jsonify({'msg': str(error.output)})

    else:
        return jsonify({'msg': 'invalid hash'})


def verify_hmac_hash(data, signature):
    github_secret = config.GITHUB_SECRET
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return ('sha1='+mac.hexdigest()) == signature


def link_in_db(link):
    """Check if a link is in the db."""

    query = Submission.query.filter_by(link=link).first()
    if query:
        return True
    return False


def save_to_db(title, link):
    """Save title and link to db if it doesn't already exists."""

    utc = arrow.utcnow()
    est = utc.to('US/Eastern')
    submission = Submission(title=title, link=link, created_on=est)
    db.session.add(submission)
    db.session.commit()

