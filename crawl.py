# 설치가 필요한 패키지
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import os
import time
from tqdm import tqdm

import argparse
import time 
import urllib

def save_image_from_url(urls, save_dir, count=0):
    print("... download images")
    os.makedirs(save_dir, exist_ok=True)
    # 이미지 URL수 만큼 반복
    for image_url in tqdm(urls):
        # 카운트 증가
        save_name = os.path.join(save_dir,  '{}.png'.format(count))
        try:
            urllib.request.urlretrieve(image_url, save_name)
            count += 1
        except:
            print("[Error] %s(은)는 저장에 실패했습니다." % image_url)


def _login_instagram(driver, login_option, user_id=None, user_passwd=None):
    instagram_id_name="username"
    instagram_pw_name="password"
    instagram_login_btn=".sqdOP.L3NKy.y3zKF     "
    facebook_login_page_css=".sqdOP.L3NKy.y3zKF     "
    facebook_login_page_css2=".sqdOP.yWX7d.y3zKF     "
    facebook_id_form_name="email"
    facebook_pw_form_name="pass"
    facebook_login_btn_name="login"

    print(f"login start - option {login_option}")
    login_url = "https://www.instagram.com/accounts/login/" 
    driver.get(login_url) 
    time.sleep(10)
    if login_option == "instagram":
        try:
            instagram_id_form = driver.find_element_by_name(instagram_id_name) 
            instagram_id_form.send_keys(user_id) 
            time.sleep(5) 

            instagram_pw_form = driver.find_element_by_name(instagram_pw_name)
            instagram_pw_form.send_keys(user_passwd) 
            time.sleep(7) 

            login_ok_button = driver.find_element_by_css_selector(instagram_login_btn) 
            login_ok_button.click() 
            is_login_success = True
        except:
            print("instagram login fail") 
            is_login_success = False
    else:
        is_facebook_btn_click = False 
        try: 
            print("try click facebook login button 1") 
            facebook_login_btn = driver.find_element_by_css_selector(facebook_login_page_css) 
            time.sleep(5) 
            facebook_login_btn.click() 
            is_facebook_btn_click = True 
            is_login_success = True 
            print("... succeeded !")
        except: 
            print("click facebook login button 1 fail") 
            is_facebook_btn_click = False 
            is_login_success = False 
        time.sleep(10) 
        if not is_facebook_btn_click: 
            print("try click facebook login button 2") 
            try: 
                facebook_login_btn = driver.find_element_by_css_selector(facebook_login_page_css2) 
                time.sleep(5) 
                facebook_login_btn.click() 
                is_facebook_btn_click = True 
                is_login_success = True 
            except: 
                print("click facebook login button 2 fail") 
                is_login_success = False 
                time.sleep(10)
    if is_facebook_btn_click:
        id_input_form = driver.find_element_by_name(facebook_id_form_name) 
        pw_input_form = driver.find_element_by_name(facebook_pw_form_name) 
        id_input_form.send_keys(user_id) 
        pw_input_form.send_keys(user_passwd) 

        time.sleep(10) 

        login_btn = driver.find_element_by_name(facebook_login_btn_name) 
        login_btn.click()
    else:
        print("Cannot click FACEBOOK login button !")
        exit()


def get_url_instagram_with_login(keyword, num_scroll=5, 
                                 login_option="facebook", 
                                 login_id=None, login_pw=None):

    # open CHROME
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Nexus 5"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # 맥이나 리눅스의 경우 파일 확장자가 없다. 윈도우의 경우 exe 확장자까지 명시해야 한다.
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    # 모든 동작마다 크롬브라우저가 준비될 때 까지 최대 5초씩 대기
    driver.implicitly_wait(5)

    _login_instagram(driver, login_option=login_option, 
                     user_id=login_id, user_passwd=login_pw)

    url = 'https://www.instagram.com/explore/tags/{}'
    url = url.format(keyword)

    time.sleep(10)
    driver.get(url)
    # 브라우저가 표시될 때 까지 프로그램 대기
    time.sleep(10)

    # 이미지 URL 목록을 저장할 빈 리스트
    urls = []
    # 지정된 회차 동안 반복하면서 스크롤을 화면 맨 아래로 이동한다.
    for i in range(0, num_scroll):
        # 현재 브라우저에 표시되고 있는 소스코드 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(type(soup))
        # INSTAGRAM에서 이미지 source는 FFVAD class에 저장되어있음
        # <img class="FFVAD" src="PATH/TO/IMAGE">
        img_css_all = soup.find_all(attrs={'class':'FFVAD'})
        for img_css in img_css_all:
            if 'src' not in img_css.attrs: continue
            url = img_css.attrs['src']
            urls.append(url)
            print("---" * 20)
            print(url)
        # 동일한 항목에 대한 중복제거
        urls = list(set(urls))
        # 수집 과정을 출력한다.
        print("%04d번째 페이지에서 %02d건 수집함 >> 누적 데이터수: %05d" % (i + 1, len(img_css_all), len(urls)))
        # 스크롤을 맨 아래로 이동
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 다음 컨텐츠가 로딩되는 동안 1초씩 대기
        time.sleep(1)
    # 동일한 항목에 대한 중복제거
    urls = list(set(urls))
    # close CHROME
    driver.close()
    return urls


def get_url_instagram(keyword, num_scroll=5):
    # open CHROME
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Nexus 5"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # 맥이나 리눅스의 경우 파일 확장자가 없다. 윈도우의 경우 exe 확장자까지 명시해야 한다.
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    # 모든 동작마다 크롬브라우저가 준비될 때 까지 최대 5초씩 대기
    driver.implicitly_wait(5)

    url = 'https://www.instagram.com/explore/tags/{}'
    url = url.format(keyword)

    driver.get(url)
    # 브라우저가 표시될 때 까지 프로그램 대기
    time.sleep(10)

    # 이미지 목록을 저장할 빈 리스트
    img_list = []
    # 지정된 회차 동안 반복하면서 스크롤을 화면 맨 아래로 이동한다.
    for i in range(0, num_scroll):
        # 현재 브라우저에 표시되고 있는 소스코드 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # srcset이라는 속성을 포함하는 모든 이미지 태그 가져오기 --> 리스트형으로 반환됨
        img = soup.select("img[srcset]")
        # 미리 준비한 리스트에 결합시킴
        img_list += img
        # 동일한 항목에 대한 중복제거
        img_list = list(set(img_list))
        # 수집 과정을 출력한다.
        print("%04d번째 페이지에서 %02d건 수집함 >> 누적 데이터수: %05d" % (i + 1, len(img), len(img_list)))
        # 스크롤을 맨 아래로 이동
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 다음 컨텐츠가 로딩되는 동안 1초씩 대기
        time.sleep(1)
    # 이미지의 주소만을 담기
    src_list = []
    for t in img_list:
        srcset = t.attrs['srcset']  # srcset 속성 가져오기
        srcset_list = srcset.split(",")  # 쉼표 단위로 추출
        item = srcset_list[len(srcset_list) - 1]  # 이미지 해상도가 가장 큰 마지막 원소를 선택
        url = item[:item.find(" ")]  # 첫 번째 글자부터 마지막 공백문자 전까지 잘라냄
        src_list.append(url)  # 준비한 리스트에 추출결과 넣기
    # 중복제거를 위해 집합으로 변경 후 리스트로 다시 변환
    src_list = list(set(src_list))
    # close CHROME
    driver.close()
    return src_list

def scroll_down_google(element, driver, num_scroll):
    for i in range(num_scroll):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
    try:
        driver.find_element_by_id('smb').click()
        for i in range(num_scroll):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

def get_url_google(keyword, num_scroll=50):
    url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'
    url = url.format(keyword)

    # open CHROME
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Nexus 5"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # 맥이나 리눅스의 경우 파일 확장자가 없다. 윈도우의 경우 exe 확장자까지 명시해야 한다.
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    # 모든 동작마다 크롬브라우저가 준비될 때 까지 최대 5초씩 대기
    driver.implicitly_wait(5)
    driver.get(url)

    element = driver.find_element_by_tag_name('body')

    # Scroll down
    scroll_down_google(element, driver, num_scroll)

    print('Reached end of page.')
    time.sleep(0.5)
    print('Retry')
    time.sleep(0.5)

    try:
        # Below is in japanese "show more result" sentences. Change this word to your lanaguage if you require.
        driver.find_element_by_xpath('//input[@value="결과 더보기"]').click()
    except:
        pass

    # Scroll again
    scroll_down_google(element, driver, num_scroll)

    # get urls
    page_source = driver.page_source 

    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('img')

    urls = []
    for image in tqdm(images):
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                # print(f'No found image sources.')
                print(e)
    urls = list(set(urls))
    # close CHROME
    driver.close()
    return urls


# def only_get_urls_instagram(driver, keyword, num_scroll=5):
def only_get_urls_instagram(keyword, num_scroll=5):
    url = 'https://www.instagram.com/explore/tags/{}'
    url = url.format(keyword)

    # open CHROME
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Nexus 5"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # 맥이나 리눅스의 경우 파일 확장자가 없다. 윈도우의 경우 exe 확장자까지 명시해야 한다.
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    # 모든 동작마다 크롬브라우저가 준비될 때 까지 최대 5초씩 대기
    driver.implicitly_wait(5)
    driver.get(url)

    time.sleep(10)
    driver.get(url)
    # 브라우저가 표시될 때 까지 프로그램 대기
    time.sleep(10)

    # 이미지 URL 목록을 저장할 빈 리스트
    urls = []
    num_url_last = []
    # 지정된 회차 동안 반복하면서 스크롤을 화면 맨 아래로 이동한다.
    for i in tqdm(range(0, num_scroll)):
        # 현재 브라우저에 표시되고 있는 소스코드 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # INSTAGRAM에서 이미지 source는 FFVAD class에 저장되어있음
        # <img class="FFVAD" src="PATH/TO/IMAGE">
        img_css_all = soup.find_all(attrs={'class':'FFVAD'})
        for img_css in img_css_all:
            if 'src' not in img_css.attrs: continue
            url = img_css.attrs['src']
            urls.append(url)
        # 동일한 항목에 대한 중복제거
        urls = list(set(urls))
        # 수집 과정을 출력한다.
        # print("%04d번째 페이지에서 %02d건 수집함 >> 누적 데이터수: %05d" % (i + 1, len(img_css_all), len(urls)))
        # 스크롤을 맨 아래로 이동
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 다음 컨텐츠가 로딩되는 동안 1초씩 대기
        time.sleep(1)
        # 최근 5번 스크롤 동안 더 이상 새로운 항목이 없으면 제거
        num_url_last.append(len(urls))
        if (len(num_url_last) > 10) and len(list(set(num_url_last[-5:]))) == 1:
            print("... no more new items are collected during 5 times recently. stop scrolling down")
            break
    # 동일한 항목에 대한 중복제거
    urls = list(set(urls))
    return urls



def get_parser():
    parser = argparse.ArgumentParser(description="Image Crawler")
    parser.add_argument("--web", default="google", choices=["google", "instagram"], 
                        help="website to search keywords (google or instagram).")
    parser.add_argument("--keyword", type=str, help="keyword to search images.")
    parser.add_argument("--num_scroll", type=int, default=50, 
                        help="the number of scrolling on website during searching")
    parser.add_argument("--save_path", type=str, default="./img",
                        help="path to save crawled images")
    parser.add_argument("--login_option", type=str, default=None, choices=["facebook", "instagram"],
                        help="login option for instagram (facebook or instagram)")
    parser.add_argument("--login_id", type=str, help="login ID")
    parser.add_argument("--login_pw", type=str, help="login Password")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    # search with keyword and collect URL of images
    keyword = args.keyword
    web_type = args.web
    if web_type == "google":
        urls = get_url_google(keyword, num_scroll=args.num_scroll)
    elif web_type == "instagram":
        if args.login_option is None:
            urls = only_get_urls_instagram(keyword, num_scroll=args.num_scroll)
        else:
            urls = get_url_instagram_with_login(keyword, num_scroll=args.num_scroll,
                                                login_option=args.login_option,
                                                login_id=args.login_id, login_pw=args.login_pw)

    # save images with URL
    save_image_from_url(urls, args.save_path)
