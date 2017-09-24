import feedparser
from flask import render_template
from flask import Flask
from flask import request
import json
import urllib2
import urllib 

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640',
             'news24': 'http://feeds.news24.com/articles/news24/TopStories/rss',
             'voa': 'https://www.voazimbabwe.com/api/zu-goepvji',
             'sports': 'https://www.voazimbabwe.com/api/zm$gpe$vjm'}

DEFAULTS = {'publication':'bbc',
			'city':'London,UK'}

@app.route("/")
def home():
	#get customised headlines based on user input or default
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)
	#get customised weather based on user input or default
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)
	return render_template("home.html", articles=articles,weather=weather)

def get_news(query):
    #query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
        print "satisfied"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']
    # weather = get_weather("London,UK")
    # return render_template("home.html", articles=feed["entries"],weather= weather)
    # print "bye"

def get_weather(query):
	# api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="
	query = urllib.quote(query)
	WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q=" + str(query) + "&appid=7a3510f2bdd7f74ac596f94aa03cb4be"
	url = WEATHER_URL.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = {"description":parsed["weather"][0]["description"],
					"temperature":parsed["main"]["temp"]-273.15,
					"city":parsed["name"]
					}
	return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)
