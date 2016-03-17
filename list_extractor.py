import requests, json


def section(data):
	for i in range(100):
		if not data['title'] == 'External links':
			if '@an'+str(i) in data['content']:
				if data['@type'] == 'section':
					sec = 0
				else:
					sec = 1
				an = data['content']['@an'+str(i)]
				if isinstance(an, dict):
					if an['@type'] == 'list':
						print '    '*data['level']*sec+data['title']
						list(an)
					else:
						pass
			else:
				break

def list(data):
	for i in data['content']:
		if i['@type'] == 'list_item':
			x = 0
			for j in i['content']:
				if j == "# ''":
					print ' '*4,
				elif j == "''":
					continue
				elif 'label' in j:
					print ' '*4*i['level']+j['label'],
					if j['@type'] == 'reference':
						print '<https://en.wikipedia.org/wiki/%s>' % j['label'].replace(' ', '_') , 
					x = 1
				elif isinstance(j, dict):
					if j.has_key('template') or j.has_key('open_tag') or j.has_key('close_tag'):
						continue
				else:
					print ' '*4 + str(j),
			print
		elif i['@type'] == 'list':
			print '*'*20
			list(i)



links = [
		'List_of_works_of_William_Gibson', 
		'Charles_L._Harness',
		'Arthur_C._Clarke'
		]

for link in links:
	while 1:
		r = requests.get('http://jsonpedia.org/annotate/resource/json/en%3A' + '%s?filter=@type:section&procs=-Extractors,Structure' % link)
		if r.status_code == 200:
			break
	data = json.loads(r.text)		
	print '***' + link + '***'
	for i in data['result']:
		if i['@type'] == 'section' and i['title'] == 'Novels':
			section(i)
	print 
