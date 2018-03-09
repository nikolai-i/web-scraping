#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import datetime

def collect(url):
    sess = requests.Session()
    def aux(url):
        if url[-1] == '#':
            sess.close()
            return null
        else:
            page = BeautifulSoup(sess.get(url).content)
            img = page.find_all('div', attrs={'id': 'comic'})[0].img
            num = url.split('/')[-2]
            try:
                with open('download.log', 'a') as f:
                    f.write('[{}] Downloading from {}.\n'.format(datetime.datetime.now(), img['src']))
                suffix = img['src'].split('.')[-1]
                stream = sess.get('https:' + img['src'], stream=True)
                if stream.ok:
                    with open('{0:04d} {1}.{2}'.format(int(num), img['alt'], suffix), 'wb') as f:
                        for chunk in stream:
                            f.write(chunk)
                nexturl = page.find_all('a', attrs={'rel':'next'})[0]['href']
            except:
                with open('download.log', 'a') as f:
                    f.write('[{}] Failed download {}.\n'.format(datetime.datetime.now(), img['src']))
            finally:
                aux('https://www.xkcd.com' + nexturl)
    aux(url)

if __name__=='__main__':
    collect('https://www.xkcd.com/1/')
