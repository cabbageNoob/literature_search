基于 BeautifulSoup 解析 html

config.py : 配置文件，一般不需要修改

spider_store.py : 用于存储数据

spider_main.py : 主函数，单线程

spider_newmain.py : 主函数，多线程

spider_test : 用于测试 main 中的函数

data/ : 存储爬取的数据，以期刊为文件名

journals/ : 存储多线程爬取的数据，以期刊为文件名

删除.bat : 把文件拖过去直接删除

filenames.txt : 记录已经爬取完的期刊

journals.txt : 记录多线程已经爬取完的期刊

跳过.txt : 跳过不想爬的期刊名称