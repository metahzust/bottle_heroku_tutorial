import os
    
import requests

from bottle import route, template, redirect, static_file, error, run

###########

from bs4 import BeautifulSoup

stophs = {'268765953|268766977': "Bois de l'Epine RER (1022)",
 '268765954|268766978': 'Aunettes L.E.P. (1086)',
 '268765955|268766979': 'Camille Guerin (1078)',
 '268765956|268766980': 'Lyc\xc3\xa9e Parc des Loges (1057)',
 '268765957|268766981': 'Clinique (1053)',
 '268765958|268766982': 'Maurice Genevoix (1082)',
 '268765959|268766983': 'Jacques Prevert (1190)',
 '268765960|268766984': 'Les Miroirs (1004)',
 '268765961|268766985': 'Agora (1011)',
 '268765962|268766986': 'Evry Courcouronnes Centre RER (1640)',
 '268765963|268766987': 'Monseigneur Rom\xc3\xa9ro (1064)',
 '268765964|268766988': 'Les Estudines (1056)',
 '268765965|268766989': 'JM.Djibaou (1059)',
 '268765966|268766990': 'Gasp\xc3\xa9ri (1115)',
 '268765967|268766991': 'Petite Montagne (1521)',
 '268765968|268766992': 'Dame du Lac (1364)',
 '268765969|268766993': 'Chemin de la Joute (1146)',
 '268765970|268766994': 'Les Peupliers (1478)',
 '268765971|268766995': 'Champagne (1336)',
 '268765972|268766996': 'Les Malines (1142)',
 '268765973|268766997': 'Complexe Sportif (1613)',
 '268765974|268766998': 'Mairie (1657)',
 '268765975|268766999': "Maison de l'Enfance (1496)",
 '268765976|268767000': "L'Eglantier (1449)",
 '268765977|268767001': 'Les Hauts Cornuts (1400)',
 '268765978|268767002': 'Les Longaines (1470)',
 '268765979|268767003': 'Exona (1028)',
 '268765980|268767004': 'Marques Avenue (1015)',
 '268765981|268767005': '8 mai 1945 (1300)',
 '268765982|268767006': 'Lyc\xc3\xa9e (2279)',
 '268765983|268767007': 'Pablo Picasso (2288)',
 '268765984|268767008': 'Henri Matisse (1402)',
 '268765985|268767009': 'L\xc3\xa9on Blum (2275)',
 '268765986|268767010': 'G\xc3\xa9n\xc3\xa9ral de Gaulle (2256)',
 '268765987|268767011': 'Gustave Courbet (1396)',
 '268767012': 'Gare RER (2261)',
 '268767013': 'Cimetiere (1349)',
 '268767014': 'Sous-Pr\xc3\xa9fecture (2283)',
 '268767015': 'Parking Cr\xc3\xaat\xc3\xa9 (2284)',
 '268767016': 'F\xc3\xa9licien Rops (1246)',
 '268767017': 'MJC (1504)',
 '268767018': 'Parc Chantemerle (1512)',
 '268767019': 'Centre Commercial (2276)',
 '268767020': 'L\xc3\xa9on Cass\xc3\xa9 (1242)',
 '268767021': 'Cottage (1360)',
 '268767022': 'Louis Drevet (1488)',
 '268767023': 'Salvador Allende (1658)',
 '268767024': 'Les Tours (1620)',
 '268767025': 'Square (1586)',
 '268767026': 'Henri Dunant (1216)'}
stops = {
    '268765962|268766986': 'Evry Courcouronnes Centre RER (1640)',
    '268799246|268800028': 'Mairie (1656)',
    "268765969|268766993": "Chemin de la Joute (1146)
}
moman = {
    '268799246|268800028': 'Mairie (1656)',
    "268765969|268766993": "Chemin de la Joute (1146)",
}
url = "https://dev.actigraph.fr/actipages/tice/pivk/relais.html.php"

def get_form(refs = "268765962|268766986"):
    r_parameters = {
            "a":"refresh",
            "refs":refs,
            "ran":"807306871",
            }
    return r_parameters

##########
@route('/ref/:no')
def show_times(no):
    r_parameters = get_form(no)
    r  = requests.post(url,data = r_parameters)
    soup = BeautifulSoup(r.text)
    time_list = soup.findAll('li')
    profile_data = {'line': time_list[0].text, 'first': time_list[1].text, 'second': time_list[2].text}
    return template('details', data=profile_data)

@route('/table')
def stops_list():
    return template('make_table', dic = stops)

@route('/home')
def show_home():
    return template('home')


@route('/')
def handle_root_url():
    redirect('/home')


@route('/profile')
def make_request():
    # make an API request here
    r  = requests.post(url, data = get_form)
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

