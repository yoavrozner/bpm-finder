import requests
import json
import youtube_dl


ACCESS_TOKEN = 'access_token=UOmQ5JLigMe6w1hJbxuMr3Y6QaCaeNzk3GC2r5M3rMoigl14X87h5RacUdhGUiPy'
BASE_SEARCH_BY_NAME = 'https://api.genius.com/search?q='


def url_finder():
    try:
        search_string = raw_input('What song are you looking for?')
        response = requests.get(BASE_SEARCH_BY_NAME + str(search_string) + "&" + ACCESS_TOKEN)
        response = response.json()
        index = 0
        result = response
        id_item = (result['response']['hits'][index]['result']['id'])
        id_item = requests.get('https://api.genius.com/songs/' + str(id_item) + '?' + ACCESS_TOKEN)
        id_item = id_item.json()
        place = 0
        my_url = str(unicode(id_item['response']['song']['media'][place]['url']))
        while "youtube" not in my_url:
            if place > 4:
                break
            place += 1
            my_url = str(unicode(id_item['response']['song']['media'][place]['url']))
        return my_url
    except IndexError:
        return False


def download_np4(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def mp4_to_wav():
    pass


def main():
    url = url_finder()
    print url
    download_np4(url)


if __name__ == '__main__':
    main()
