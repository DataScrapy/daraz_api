from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
from bs4 import BeautifulSoup as soup
import time
from database_crud import page_url_status_post



def get_driver(driver, url, depth_level):
    try:
        driver.get(url)
        time.sleep(5)

        req = requests.get(url)
        status = req.status_code

        old_position = 0
        new_position = 500

        for i in range(16):
            try:
                driver.find_elements_by_xpath('//a[@id="acc-alert-close"]')[0].click()
                time.sleep(2)
            except:
                pass
            driver.execute_script("window.scrollTo(" + str(old_position) + "," + str(new_position) + ");")
            time.sleep(2)

            driver.execute_script("window.scrollTo(" + str(new_position) + "," + str(old_position) + ");")
            time.sleep(2)
            driver.execute_script("window.scrollTo(" + str(old_position) + "," + str(new_position) + ");")
            old_position = new_position
            new_position = new_position + 500
            time.sleep(4)

        driver.execute_script("window.scrollTo(" + str(new_position) + "," + str(0) + ");")
        time.sleep(3)

        page_soup = soup(driver.page_source, "html.parser")

        page_url_status_post(url, depth_level, status)

        return page_soup

    except:
        pass


def html_parser(url, depth_level):
    try:
        req = requests.get(url)
        status = req.status_code

        page_url_status_post(url, depth_level, status)

    except:
        pass




def scrap_url(all_url_lst, driver, main_url):
    try:
        depth_level = "0"

        all_url_lst.append(main_url)

        page_soup = get_driver(driver, main_url, depth_level)


        root_ul = page_soup.find("ul", {"class": "lzd-site-menu-root"})
        root_lst = root_ul.findAll("li", {"class": "lzd-site-menu-root-item"})

        main_menu_lst = []

        # Getting list of all root-level items
        for i in range(len(root_lst)):
            try:
                sub_menu = root_ul.find("ul", {"class": "lzd-site-menu-sub Level_1_Category_No"+str(i+1)})
                sub_menu_lst_1 = sub_menu.findAll("li", {"class": "lzd-site-menu-sub-item"})
                sub_menu_lst_2 = sub_menu.findAll("li", {"class": "sub-item-remove-arrow"})

                sub_menu_lst = sub_menu_lst_1 + sub_menu_lst_2

                [main_menu_lst.append(li) for li in sub_menu_lst]

            except:
               pass

        depth_one_lst = []

        # getting content of all depth-level-1 items & list of depth-level-2 items
        for sub_menu in main_menu_lst:
            try:
                sub_menu_url = sub_menu.find("a")["href"]

                if sub_menu_url.startswith("http"):
                    pass
                else:
                    sub_menu_url = "https:" + sub_menu_url
                if sub_menu_url in all_url_lst:
                    continue

                all_url_lst.append(sub_menu_url)

                depth_level = "1"
                page_soup = html_parser(sub_menu_url, depth_level)

                # Getting list of depth-level-2 items
                grand_item = sub_menu.find("ul", {"class": "lzd-site-menu-grand"})
                grand_item_lst = grand_item.findAll("li", {"class": "lzd-site-menu-grand-item"})

                [depth_one_lst.append(li) for li in grand_item_lst]

            except:
                pass

        # getting content of all depth-level-2 items
        for sub_menu in main_menu_lst:
            try:
                sub_menu_url = sub_menu.find("a")["href"]

                if sub_menu_url.startswith("http"):
                    pass
                else:
                    sub_menu_url = "https:" + sub_menu_url
                if sub_menu_url in all_url_lst:
                    continue

                all_url_lst.append(sub_menu_url)

                depth_level = "2"
                page_soup = html_parser(sub_menu_url, depth_level)

            except:
                pass

    except:
        pass


def scrap(main_url):
    try:
        options = Options()
        options.add_argument("--headless")
        all_url_lst = []

        root_dir = os.path.dirname(os.path.abspath(__file__))

        driver = webdriver.Chrome(options=options, executable_path=root_dir + '/chromedriver.exe')

        driver.maximize_window()

        scrap_url(all_url_lst, driver, main_url)

        return {"status: success"}

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return {"status": "error", "data": str(e)}

        pass