import requests
from bs4 import BeautifulSoup as bs
import re


def _get_pages(query, page=0, search_img=False):
    # 任意の1ページ分を対象にGoogle検索実施
    # https://www.google.com/search?q=justin+bieber&start=20
    base_url = "https://www.google.com/search"
    query = query.replace(" ","+")
    query = query.replace("　","+")

    search_url = base_url + "?q="+ query + "&start=" + str(page*10)
    if (search_img):
        search_url = search_url + "&tbm=isch"    
    print(search_url) 

    response = requests.get(search_url)
    
    return response


def _get_num_of_hits(response):
# responseからヒット件数を抽出
    soup = bs(response.text, "html.parser")
    result_stats = soup.find("div", id="resultStats")
    num_of_hits = int(result_stats.text[1:-1].replace(",",""))
    
    return num_of_hits


def _extract_link_info(response):
# 任意の1ページ分を対象に見出しとURLを取得
    soup = bs(response.text, "html.parser")
    headings = soup.find_all("div", class_="g")

    result = []
    for i in range(len(headings)):
        if(headings[i].a== None or headings[i].h3.a == None):
            break
        title = headings[i].a.text
        tmp_url = headings[i].h3.a['href']
        url = re.sub(r'/url\?q=|&sa.*','', tmp_url)
        
        if(headings[i].span!=None):
            description = headings[i].find("span", class_="st").text
        else:
            description = "No description"

        dic = {"title": title, "url": url, "description": description}
        result.append(dic)
    
    return result


def get_any_pages(query, page=0, search_img=False):
# 検索対象数指定(default page:0, ヒット数を上限とする)

    # ヒット件数
    response = _get_pages(query, page=0, search_img=search_img)        
    num_of_hits = _get_num_of_hits(response)
    print("Num of hits: {}".format(num_of_hits))
    
    # 検索結果
    result = _extract_link_info(response)
    for i in range(1,page):
        if(page > float(num_of_hits/10)):
            break
        response = _get_pages(query, page=i, search_img=search_img)    
        next_page_result = _extract_link_info(response)
        result.extend(next_page_result)
    
    return result


if __name__ == "__main__":
    # init()
    query = "東京　観光"
    max_target_page = 2
    search_img = False

    result = get_any_pages(query, page=max_target_page, search_img=search_img)
    print(result)

