from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from classes import Job
import urllib.parse
import time
import csv

# + get more skills
skills = [
    "HTML",
    "CSS",
    "Javascript",
    "Python",
    "Java",
    "C++",
    "C",
    "C#",
    "Go",
    "Rust",
    "Swift",
    "Kotlin",
    "Scala",
    "Rust",
    "flutter",
    "Ruby"
]

# +++++++++++++++++++++ Page url reference
PAGE_DOMAIN = "https://www.wanted.co.kr/"
PAGE_PREFIX = "search?query="
PAGE_SUFIX = "&tab=position"
# +++++++++++++++++++++ Page Select Target Classes
PSTC = {
    "master" : "search_tabpanel_position",
    "wrap" : "JobCard_container__FqChn",
    "t" : "JobCard_title__ddkwM",
    "cn" : "JobCard_companyName__vZMqJ" ,
    "l" : "JobCard_location__2EOr5",
    "r" : "JobCard_reward__sdyHn"
}

# +++++++++++++++++++++ playwright -> content -> beautifulsoup -> dataset
def content_get_jobs(sk, c):
    result = []
    su = BeautifulSoup(c, "html.parser")
    master = su.find("div", id = PSTC["master"])
    wrap = master.find_all("div", class_ = PSTC["wrap"])
    for job in wrap:
        result.append(Job(
            sk
            ,f"{PAGE_DOMAIN}{job.find('a')['href']}"
            ,job.find("strong", class_ = PSTC["t"]).text
            ,job.find("span", class_ = PSTC["cn"]).text
            ,job.find("span", class_ = PSTC["l"]).text
            ,job.find("span", class_ = PSTC["r"]).text
        ))
    return result

# +++++++++++++++++++++ Write to csv file
def make_csv(skill, export_list):
    file = open(f"{skill}_jobs.csv", mode="w", encoding="utf-8")
    wr = csv.writer(file)
    wr.writerow(["포지션","링크","타이틀","회사명","근무지","보상"]) # header
    wr.writerows(export_list)
    file.close()

# +++++++++++ start sync_playwright and beautifulsoup parsing jobs
p = sync_playwright().start()
# launch chrome browser driver with chromium headless mode(we don't see browser)
# if you want show browser, call "launch()" method with "headless=False"
br = p.chromium.launch(headless=False)
page = br.new_page()
jobs = {} # list of jobs
all_export_list = []
scroll = 2 # scroll counter / 동적으로 처리되는 무한 스크롤을 몇번 반복할지 지정

for skill in skills:
    page.goto(f"{PAGE_DOMAIN}{PAGE_PREFIX}{skill if skill != "C++" and skill != "C#" else urllib.parse.quote(skill)}{PAGE_SUFIX}")
    time.sleep(2)
    for i in range(scroll):
        page.keyboard.down("End")
        time.sleep(2)
    content = page.content()
    jobs[skill] = content_get_jobs(skill, content)
    export_list = []
    for job in jobs[skill]:
        export_list.append(job.to_export_list())
    # all job 
    all_export_list.extend(export_list)
    make_csv(skill, export_list)

make_csv("all", all_export_list)
# stop sync_playwright
p.stop()

