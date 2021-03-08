import selenium
from selenium import webdriver
import pandas as pd
import os
# import openpyxl
import time
import requests
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

#selenium.common.exceptions.StaleElementReferenceException:
def get_prd_amazon(search):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    search = "+".join(search.split(" "))
    if "+" in search:
        search_url="https://www.amazon.in/s?k={k}&crid=2PT07K1CUD2LT&sprefix=earphone%2Caps%2C294&ref=nb_sb_ss_ts-doa-p_1_8"
        driver.get(search_url.format(k=search))
    else:
        search_url = "https://www.amazon.in/s?k={k}&ref=nb_sb_noss_2"
        driver.get(search_url.format(k=search))
    driver.implicitly_wait(2)
    prds_likns = driver.find_elements_by_class_name('sg-col-inner') #InvalidSelectorException:
    # prds_likns=prds_likns.find_element_by_class_name('sg-row')
    # prds_likns = prds_likns.find_element_by_class_name('sg-col-inner')
    # prds_likns = prds_likns.find_element_by_class_name('a-section a-spacing-none')
    # prds_likns = prds_likns.find_element_by_class_name('a-link-normal a-text-normal')
    # print("x: ",prds_likns.text)
    # for i in prds_likns:
    #     print(i.text)
    #     break
    # time.sleep(2)

    cnt = 0
    x = 0
    parent = driver.current_window_handle
    for lnk in prds_likns:
        prd_details={"url": [],"name":[], "source": [], "price": [], "model no": []}
        lnk.click()
        x += 1
        handles = driver.window_handles
        for handle in handles:
            # print(handle)
            driver.switch_to.window(handle)
            print(driver.title)
            if x == 2:
                time.sleep(3)
                prd_details["url"].append(lnk.text)
                prd_details["source"].append("Amazon")
                print("name:", driver.find_element_by_class_name('a-size-large product-title-word-break').text)
                prd_details["name"].append(driver.find_element_by_class_name('a-size-large product-title-word-break').text)
                model_num = driver.find_elements_by_class_name('a-size-base prodDetAttrValue')

                print("model_no", model_num[4].text)
                prd_details["model no"].append(model_num[4].text)
                print("prize:", driver.find_element_by_class_name('a-size-medium a-color-price priceBlockDealPriceString').text)
                prd_details["price"].append(driver.find_element_by_class_name('a-size-medium a-color-price priceBlockDealPriceString').text)
                driver.close()
                driver.switch_to.window(parent)
                time.sleep(5)
                x = 0
                break
            x += 1
        if cnt == 10:
            break
        cnt += 1
        time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # sleep_between_interactions
    driver.close()
    print(prd_details)
    return

def get_prd_flpkrt(search,feature):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    prd_dtl={"name:"}

    search = "+".join(search.split(" "))
    print("search:",search)
    # url="https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    # driver.get(url)
    # driver.find_element_by_class_name('_3704LK').clear()
    #
    # driver.find_element_by_class_name('_3704LK').send_keys(search)
    # driver.find_element_by_class_name('L0Z3Pu').click()

    search_url="https://www.flipkart.com/search?q={q}&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_na&as-pos=1&as-type=RECENT&suggestionId=poco+m3%7CMobiles&requestId=95ef28c9-955b-46ef-b7c3-8330d79e2900&as-backfill=on"

    driver.get(search_url.format(q=search))
    prds_likns=driver.find_elements_by_class_name('_4rR01T')
    time.sleep(1)
    cnt=0
    x=0
    parent = driver.current_window_handle
    prd_details = {"name": [], "source": [], "price": [], "model no": []}
    for lnk in prds_likns:

        lnk.click()
        x+=1
        handles=driver.window_handles
        for handle in handles:
            # print(handle)
            driver.switch_to.window(handle)
            print(driver.title)
            if x==2:

                time.sleep(3)
                # prd_details["url"].append(lnk.text)
                print("name:", driver.find_element_by_class_name('B_NuCI').text)
                prd_details["name"].append(driver.find_element_by_class_name('B_NuCI').text)
                prd_details["source"].append("flipkart")
                model_num=driver.find_elements_by_class_name('_21lJbe')

                print("model_no",model_num[1].text)
                prd_details["model no"].append(model_num[1].text)
                print("price:",driver.find_element_by_class_name('_30jeq3').text)
                prd_details["price"].append(driver.find_element_by_class_name('_30jeq3').text)
                driver.close()
                driver.switch_to.window(parent)
                time.sleep(5)
                x=0
                break
            x+=1
        if cnt==5:
            break
        cnt+=1
        time.sleep(5)



    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # sleep_between_interactions
    driver.close()
    # traverse list
    print(prd_details)
    # if feature==1:
    #     srt=sorted(prd_details["price"].values)
    # else:
    #     srt = sorted(prd_details["price"].values,reverse=True)
    product_details=pd.DataFrame(prd_details)
    if feature == 1:
        product_details.sort_values(by='price', ascending=False)
    else:
        product_details.sort_values(by=['price'])
    data_to_xl=pd.ExcelWriter('product_details.xlsx')
    # file_name='product_details.xlsx'
    product_details.to_excel(data_to_xl)
    data_to_xl.save()
    return
search=input("Enter want you want to search:")
feature=int(input("1:price high to low\n2:price low to high\n =>"))
if isinstance(feature, int):
    pass
else:
    print("please enter a right choise")
# get_prd_flpkrt(search)
get_prd_flpkrt(search,feature)

