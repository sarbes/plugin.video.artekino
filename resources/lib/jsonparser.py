# -*- coding: utf-8 -*-
import requests
import resources.lib.oauth as oauth
import json
import libmediathek4utils as lm4utils
import time
baseApi = 'https://www.artekinofestival.com/api'

username = lm4utils.getSetting('username')
password = lm4utils.getSetting('password')

if len(username) == 0 or len(password) == 0:
	lm4utils.displayMsg(lm4utils.getTranslation(31000),lm4utils.getTranslation(31001))


def getMovies():
	#token = oauth.getToken('artekino%3A%2F%2Fapi%2Ffoobar',username,password)
	token = oauth.getToken('artekino%3A%2F%2Fapi%2Ffoobar','','')
	j = requests.get(f'{baseApi}/film?access_token={token}&locale={_getLang()}').json()
	l = []
	i = 0
	for item in j['hydra:member']:
		d = {'params':{'mode':'playVideo'}, 'metadata':{'art':{}}, 'type':'video'}
		d['metadata']['name'] = item['international_title']
		if 'synopsis' in item:
			d['metadata']['plot'] = item['synopsis']
		if item['thumbnail_large'] != None:
			d['metadata']['art']['thumb'] = item['thumbnail_large']['file_location']
		else: continue #hack for faulty api
		try: d['metadata']['art']['fanart'] = item['background_media']['']['file_location']
		except: pass
		if item['poster_medium'] != None:
			d['metadata']['art']['poster'] = item['poster_medium']['file_location']
		if item['thumbnail_square'] != None:
			d['metadata']['art']['icon'] = item['thumbnail_square']['file_location']
		if item['length'] != None:
			d['metadata']['duration'] = item['length']*60
		d['params']['id'] = str(item['movie_medium']['id'])
		#if item['availability']['dates_availability']['is_available']:
		if item['availability']['dates_availability']['start_date'] != None and item['availability']['dates_availability']['end_date'] != None:
			now = time.gmtime()
			start_date = time.strptime(item['availability']['dates_availability']['start_date'][:19],'%Y-%m-%dT%H:%M:%S')
			end_date   = time.strptime(item['availability']['dates_availability']['end_date'][:19],'%Y-%m-%dT%H:%M:%S')
			if start_date < now and now < end_date:
				l.append(d)

	return {'items':l,'pagination':{'currentPage':0}}

def getMovie():
	token = oauth.getToken('artekino%3A%2F%2Fapi%2Ffoobar',username,password)
	j = requests.get(baseApi+'/film?access_token='+token+'&parent_list=film-event-16&locale=en').json()
	l = []
	for item in j['hydra:member']:
		d = {'params':{'mode':'playVideo'}, 'metadata':{'art':{}}, 'type':'video'}
		d['metadata']['name'] = item['international_title']
		if 'synopsis' in item:
			d['metadata']['plot'] = item['synopsis']
		d['metadata']['art']['thumb'] = item['thumbnail_large']['file_location']
		d['metadata']['art']['fanart'] = item['background_media']['']['file_location']
		d['metadata']['art']['poster'] = item['poster_medium']['file_location']
		d['metadata']['art']['icon'] = item['thumbnail_square']['file_location']
		d['metadata']['duration'] = item['length']*60
		d['params']['id'] = str(item['movie_medium']['id'])
		l.append(d)
	return {'items':l,'pagination':{'currentPage':0}}

def getVideo(id):
	pl = oauth.getPlaylist(username,password,id)
	j = json.loads(pl)
	vtt = ''
	lang = ''
	for stream in j['items'][0]['locations']['adaptive']:
		if stream['drm']['drmtype'] == 'widevine':
			url = stream['src']
			licenseserverurl = stream['drm']['licenseserverurl']+'||R{SSM}|'
	l = _getLang()
	for subtitle in j['items'][0]['tracks']['subtitles']:
		if subtitle['srclang'] == l:
			vtt = subtitle['src']
			lang = l
		if vtt == '' and subtitle['srclang'] == 'en':
			vtt = subtitle['src']
			lang = 'en'

	d = {}
	d['media'] = [{'url':url, 'licenseserverurl':licenseserverurl, 'type': 'video', 'stream':'DASH'}]
	d['subtitle'] = [{'url':vtt, 'type':'webvtt', 'lang':lang, 'colour':False}]
	return d
	
def _getLang():
	availableLanguages = ['en','de','es','fr','hu','it','pl','pt','ro','ua']
	s = lm4utils.getSetting('language')
	if s == 'system':
		l = lm4utils.getISO6391()
		if l in availableLanguages:
			return l
		else:
			return 'en'
	else:
		return s

