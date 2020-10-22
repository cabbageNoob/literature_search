'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-22 09:49:59
'''
import sys, os
sys.path.insert(0, os.getcwd())

from flask import Flask, render_template, redirect, request
from search import filter_msg


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def search():
    """
    URL : /
    Query engine to find a list of relevant URLs.
    Method : POST or GET (no query)
    Form data :
        - query : the search query
        - hits : the number of hits returned by query
        - start : the start of hits
    Return a template view with the list of relevant URLs.
    """
    # GET data
    query_term = request.args.get("query", None)
    page_num = request.args.get("page_num", 1, type=int)
    page_len = request.args.get("page_len", 10, type=int)
    sort_type = request.args.get("sort", 1, type=int)
    similar = request.args.get("similar", False, type=bool)
    if page_num < 0 or page_len < 0:
        return "Error, start or hits cannot be negative numbers"

    if similar:
        url = request.args.get("url", 1, type=str)
        data = query_engine.search_more_like_this(
            url=url, fieldname="content", top=10)
        range_pages = [1]

        # show the list of matching results
        return render_template('spatial/index.html', query=query_term,
                               # response_time=r.elapsed.total_seconds(),
                               response_time=0.1,
                               total=data["total"],
                               page_len=page_len,
                               page_num=page_num,
                               range_pages=range_pages,
                               results=data["results"],
                               maxpage=1,
                               similar=True)
    elif query_term:
        # query search engine

        data  = filter_msg(query_term)

        # recom_search = query_engine.get_recommend_query(query_term)

        i = page_num
        maxi = 1+int(data["total"]/page_len)
        range_pages = range(
            i-5, i+5 if i+5 < maxi else maxi) if i >= 6 else range(1, maxi+1 if maxi < 10 else 10)

        # show the list of matching results
        return render_template('spatial/index.html', query=query_term,
                               # response_time=r.elapsed.total_seconds(),
                            #    response_time=time,
                               total=data["total"],
                               page_len=page_len,
                               page_num=page_num,
                               range_pages=range_pages,
                               results=data['hits'],
                               maxpage=maxi,
                            #    recommends=recom_search,
                               sort_type=sort_type)
    else:  # retrun home page with hot news
        
        # data = query_engine.recommend_news()

        # show the list of matching results
        return render_template('spatial/index.html',
                               # response_time=r.elapsed.total_seconds(),
                            #    results=data["results"]
                               )





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8003)