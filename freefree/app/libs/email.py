# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/7
from threading import Thread
from flask import current_app, render_template
from freefree.app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e('Failure to send this email.')


def send_email(to, subject, template, **kwargs):
    msg = Message('[FreeFree]' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return msg
