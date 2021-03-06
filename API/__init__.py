from API import HttpUtil, UrlConstants, ahttp


def get(api_url: str, params: dict = None, max_retry: int = 3, **kwargs):
    for retry in range(max_retry):
        try:
            api_url = UrlConstants.WEB_SITE + api_url.replace(UrlConstants.WEB_SITE, '')
            return HttpUtil.get(api_url=api_url, params=params, **kwargs).json()
        except Exception as error:
            print(error)


class Book:

    @staticmethod
    def novel_info(novel_id: int):
        response = get(UrlConstants.BOOK_INFO_API.format(novel_id))
        if response.get('_id') is not None:
            return response

    @staticmethod
    def catalogue(novel_id: int, max_retry=5):
        for retry in range(max_retry):
            response = get(UrlConstants.BOOK_CATALOGUE.format(novel_id))
            if response.get('mixToc').get('chapters') is not None:
                return response.get('mixToc').get('chapters')

    @staticmethod
    def search_book(novel_name: str):
        return get(UrlConstants.SEARCH_API.format(novel_name)).get('books')


class Chapter:
    @staticmethod
    def download_chapter(chapter_id: str):
        api_url = UrlConstants.WEB_SITE + UrlConstants.CHAPTER_API.format(chapter_id)
        response = get(api_url)['chapter']
        return response['title'], response['body']


class Cover:
    @staticmethod
    def download_cover(max_retry=10) -> str:
        for retry in range(max_retry):
            params = {'type': 'moe', 'size': '1920x1080'}
            response = HttpUtil.get('https://api.yimian.xyz/img', params=params)
            if response.status_code == 200:
                return HttpUtil.get(response.url).content
            else:
                print("msg:", response.text)


class Tag:
    @staticmethod
    def get_type():
        type_dict = {}
        response = get(UrlConstants.GET_TYPE_INFO)
        for number, sort in enumerate(response['male']):
            number += 1
            major = sort.get('major')
            type_dict[number] = major
        return type_dict

    @staticmethod
    def tag_info(tag_id, tag_name, page):
        book_list = get(UrlConstants.TAG_API.format(tag_id, tag_name, page))
        if book_list['books']:
            return book_list['books']

    @staticmethod
    def ranking(ranking_num):
        return get(UrlConstants.RANKING_API.format(ranking_num))
