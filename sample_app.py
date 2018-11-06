﻿import os
    
import requests

from bottle import route, template, redirect, static_file, error, run

    
url = "https://dev.actigraph.fr/actipages/tice/pivk/relais.html.php"
r_parameters = {
        "a":"refresh",
        "refs":"268765962|268766986",
        "ran":"807306871",
        }
from bs4 import BeautifulSoup

@route('/home')
def show_home():
    return template('home')


@route('/')
def handle_root_url():
    redirect('/home')


@route('/profile')
def make_request():
    # make an API request here
    r  = requests.post(url,data = r_parameters)
    soup = BeautifulSoup(r.text)
    time_list = soup.findAll('li')
    profile_data = {'line': time_list[0].text, 'first': time_list[1].text, 'second': time_list[2].text}
    return template('details', data=profile_data)


@route('/css/<filename>')
def send_css(filename):
    return static_file(filename, root='static/css')


@error(404)
def error404(error):
    return template('error', error_msg='404 error. Nothing to see here')


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)

