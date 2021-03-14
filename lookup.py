#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import properties
import json
import urllib2

def getByName(sn, apiKey, reg):
    url = "https://{2}.api.pvp.net/api/lol/{2}/v1.4/summoner/by-name/{0}?api_key={1}".format(sn.lower().replace(" ", ""), apiKey, reg)
    result = urllib2.urlopen(url)

    return result

def getRecentMatches(id, apiKey, reg):
    url = "https://na.api.pvp.net/api/lol/{2}/v1.3/game/by-summoner/{0}/recent?api_key={1}".format(id, apiKey, reg)
    recent_matches = urllib2.urlopen(url)

    return recent_matches

def getChamps(apiKey, reg):
    url = "https://global.api.pvp.net/api/lol/static-data/{1}/v1.2/champion?dataById=true&champData=image&api_key={0}".format(apiKey, reg)
    champs = urllib2.urlopen(url)

    return champs

def getSpells(apiKey, reg):
    url = "https://global.api.pvp.net/api/lol/static-data/{1}/v1.2/summoner-spell?dataById=true&spellData=image&api_key={0}".format(apiKey, reg)
    spells = urllib2.urlopen(url)

    return spells

def check_response(response):
    message = ""
    statusMssg = ""
    result = ""

    urlInfo = response.info()
    code = response.getcode()

    if code == 200:
        result = json.load(response)

    elif code == 429:
        delay = urlInfo.getheader("Retry-After")
        message = "Too many request. Try again in " + str(delay) + " second(s)."
        self.response.headers["Delay"] = delay

    elif code == 404:
        message = "Are you sure you spelled the summoner name correctly or chose the right region?"

    elif code != 200:
        message = "Something went wrong. Try again in a little bit."

    return {"mssg" : message, "result" : result, "code" : code}

class MainHandler(webapp2.RequestHandler):
    def post(self):
        summoner = self.request.get("sn")
        region = self.request.get("reg", "na")

        matches = ""
        champinfo = ""
        id = None
        spells = ""

        try:
            result = getByName(summoner, properties.API_KEY, region)
        except urllib2.URLError, e:
            result = e

        info = check_response(result)

        if info["code"] == 200:
            summonerResp = info["result"]
            id = summonerResp[summoner.lower().replace(" ", "")]["id"]

            #possibly add this to response instead of headers
            self.response.headers["Name"] = str(summonerResp[summoner.lower().replace(" ", "")]["name"])
            self.response.headers["Icon"] = str(summonerResp[summoner.lower().replace(" ", "")]["profileIconId"])

            try:
                matchesResp = getRecentMatches(id, properties.API_KEY, region)
            except urllib2.URLError, e:
                matchesResp = e

            info = check_response(matchesResp)

            if info["code"] == 200:
                matches = info["result"]

                try:
                    champResp = getChamps(properties.API_KEY, region)
                except urllib2.URLError, e:
                    ChampResp = e

                info = check_response(champResp)

                if info['code'] == 200:
                    champinfo = info["result"]

                    try:
                        spellResp = getSpells(properties.API_KEY, region)
                    except urllib2.URLError, e:
                        spellResp = e

                    info = check_response(spellResp)

                    if info['code'] == 200:
                        spells = info["result"]

        if info['code'] != 200:
            self.response.headers["Mssg"] = info["mssg"]

        self.response.headers["Code"] = str(info["code"]);
        self.response.out.write(json.dumps([matches, champinfo, spells, id]))

app = webapp2.WSGIApplication([("/lookup", MainHandler)])
