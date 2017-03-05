from elasticsearch import Elasticsearch
import feedparser
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def index_news():
	
	companiesList = load_input(sys.argv[2])
	posWords = load_input(sys.argv[3])
	negWords = load_input(sys.argv[4])

	feeds = feedparser.parse(sys.argv[1])

	es = Elasticsearch()
	es.indices.create(index='stock-news', ignore=400)

	indexUpdate = datetime.now()
	print("Starting index: "+str(indexUpdate))

	for item in feeds["items"]:
		
		guid = item["guid"]
		published = item['published']
		description = item['description']
		link = item['link']
		guid = item['id']
		title = item['title']
		source = 'infomoney'
		stock = 'N/A'
		sentiment = 'NEUTRO'
		# TODO dicionario de quantidade de referencias positivas e negativas
		for company in companiesList:
			if(company in title):
				stock = company
		for positive in posWords:
			if positive in title:
				sentiment = 'POSITIVO'
		for negative in negWords:
			if negative in title:
				sentiment = 'NEGATIVO'			

		es.index(index="stock-news", id=guid,  doc_type="news", \
			body={"title": title, "indexUpdate": indexUpdate, "description": description, "link":link, "published":published, "stock": stock, "source": source, "sentiment": sentiment}\
		)

	print("End of index.\n")

def load_input(filename):
	companies = [line.strip() for line in open(filename, 'r')]
	return companies

def main():
    scheduler = BlockingScheduler()

    print("Scheduling Tasks")
    scheduler.add_job(index_news, 'interval', minutes=1, id="stock_job")
    print("Tasks Scheduled")
    print("Running Tasks")
    scheduler.start()
    print("Good Bye")
    return 0


if __name__ == "__main__":
    main()

