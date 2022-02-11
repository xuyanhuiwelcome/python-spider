from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import lxml
import pymysql

browser = webdriver.Chrome()
def run(page):
    url = 'https://search.bilibili.com/upuser?keyword=%E5%A1%94%E7%BD%97&page={page}'.format(
        page=page)
    browser.get(url)
    WebDriverWait(browser,30)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_data(soup)

def save_data(soup):
    lsts = soup.find(class_="body-contain").find_all(class_="user-item")
    for item in lsts:
        username = item.find(class_="title").get('title')
        level = item.find(class_="title").find("i")
        desc = item.find(class_="desc").text
        spans = item.find(class_="up-info clearfix").find_all("span")
        funs = spans[0].text.strip("稿件：")
        work = spans[1].text.strip("粉丝：")
        if work.count('万') > 0:
            work = float(work.strip('万')) * 10000
        centerUrl = item.find("a").get('href').strip("//")
        save_mysql(username,level,desc,funs,work,centerUrl)

def save_mysql(useranme,level,desc,funs,work,contenturl):
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         database='tesst')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO `tarotuser`(`userName`,`funs`,`work`,`desc`,`centerUrl`) VALUES('"+useranme+"','"+funs+"','"+str(work)+"','"+desc+"','"+contenturl+"')"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
def main():
    for page in range(1,50):
        run(page)

if __name__=='__main__':
    main()
