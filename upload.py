oauth_token="773ab19df1116df1623d5effd07fcab6571b42c8"

import urllib2, json

c=1
while c != 949:
	print "Adding bug "+str(c)+"/949"
	bug=json.load(open("bugs/"+str(c)))
	openClosed='open'
	body=""
	if bug["status"]=='resolved':
		openClosed='closed'
	
	if bug["history"]!=[]:
		for i in bug["history"]:
			body+="<b>Comment by "+i["author"]+":</b><i>\n"
			body+=i["message"]
			body+="</i><hr/>\n\n"
	else:
		body+="No Messages!"
	if bug["files"]!=[]:
		for i in bug["files"]:
			body+="<b>File at "+i["url"]+" by "+i["author"]+"</b>\n"
	else:
		body+="No Files!\n"
	body+="\n"
	body+="Status : <b>"+bug["status"]+"</b>\n"
	body+="Nosy List : <b>"
	for i in bug["nosylist"]:
		body += "  "+i+" "
	body+="</b>\n"
	labels=bug["keywords"]
	labels.append("imported")
	labels.append(bug["priority"])
	labels.append(bug["status"])
	if bug["milestone"]!="":
		labels.append("milestone:"+bug["milestone"])
	body+="Superceder : <b>"+bug["superceder"]+"</b>\n"
	body+="Priority : <b>"+bug["priority"]+"</b>\n"
	body+="Waiting On : <b>"+bug["waitingon"]+"</b>\n"
	body+="Roundup ID : <b>"+bug["id"]+"</b>\n"

	req = urllib2.Request('https://api.github.com/repos/602p/oh-issues/issues?access_token='+oauth_token,
			json.dumps({
				'title':bug["title"],
				'body':body,
				'asignee':bug["assigned"],
				'labels':labels
			})
		)
	resp = json.load(urllib2.urlopen(req))
	req = urllib2.Request('https://api.github.com/repos/602p/oh-issues/issues/'+str(resp["number"])+'?access_token='+oauth_token,
			json.dumps({
				'state':openClosed
			})
		)
	resp = urllib2.urlopen(req)
	#print str(json.load(resp))
	c+=1