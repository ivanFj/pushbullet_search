import requests

def get_pushes(token):
	
	pushesList = ""
	    
	##url = urllib2.Request("https://api.pushbullet.com/v2/pushes?active=true", headers=token)
	url = requests.get("https://api.pushbullet.com/v2/pushes?active=true", headers = token)
	##response = urllib2.urlopen(url)
	pushes = url.json()

	for push in pushes["pushes"]:
		container = u"<div class='push'>{}</div>"
		title = push.get("title", u"")
		link = push.get("url", u"")
		body = push.get("body", u"")
		
		if title:
			title = u"<span>{}</span>".format(title)
		if link:
			link = u"<span><a href='{0}'>{0}</a></span>".format(link)
		if body:
			body = u"<span>{}</span>".format(body)
			
		newPush = container.format(title + link + body)
		pushesList += newPush
	
	return pushesList