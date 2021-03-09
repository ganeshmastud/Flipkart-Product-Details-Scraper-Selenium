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
def get_prd_amazon(search,no_of_products):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    search = "+".join(search.split(" "))
    # if "+" in search:
    #     search_url="https://www.amazon.in/s?k={k}&crid=2PT07K1CUD2LT&sprefix=earphone%2Caps%2C294&ref=nb_sb_ss_ts-doa-p_1_8"
    #     driver.get(search_url.format(k=search))
    # else:
    #     search_url = "https://www.amazon.in/s?k={k}&ref=nb_sb_noss_2"
    #     driver.get(search_url.format(k=search))
    driver.implicitly_wait(2)
    driver.get('https://www.amazon.in')
    time.sleep(2)
    driver.find_element_by_id('twotabsearchtextbox').send_keys(search)
    driver.find_element_by_id('nav-search-submit-button').click()
    time.sleep(5)
    prds_likns = driver.find_elements_by_xpath("//a[@class='a-size-base a-link-normal s-no-hover a-text-normal']") #InvalidSelectorException:

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
    prd_details = {"name": [], "source": [], "price": [], "model no": [], "category": []}
    for lnk in prds_likns:

        lnk.click()
        x += 1
        handles = driver.window_handles
        for handle in handles:
            # print(handle)
            driver.switch_to.window(handle)
            print(driver.title)
            if x == 2:
                time.sleep(3)
                # prd_details["url"].append(lnk.text)
                prd_details["source"].append("Amazon")
                print("name:", driver.find_element_by_id('productTitle').text)
                prd_details["name"].append(driver.find_element_by_id('productTitle').text)
                model_num = driver.find_element_by_id('productDetails_techSpec_section_1')
                row=model_num.find_elements_by_tag_name('tr')[4]
                col=row.find_element_by_tag_name('td')
                print(col.text)

                prd_details["model no"].append(col.text)
                table = driver.find_element_by_id('productDetails_detailBullets_sections1')
                try:
                    row = table.find_elements_by_tag_name('tr')[6]

                    try:
                        category = row.find_element_by_tag_name('td')
                        category=category.text
                        # prd_details["category"].append(category.text)
                    except Exception as e:
                        category="Not available"
                except Exception as e:
                    category = "Not available"
                print("category",category)
                prd_details["category"].append(category)
                price=""
                if len(price)==0:
                    try:
                        price=driver.find_element_by_id("priceblock_dealprice").text
                    except Exception as e:
                        price=""
                if len(price)==0:
                    try:
                        price= driver.find_element_by_id('priceblock_saleprice').text
                    except Exception as e:
                        price = ""
                if len(price)==0:
                    price = driver.find_element_by_id("priceblock_ourprice").text
                print("prize:", price)
                prd_details["price"].append(price)
                driver.close()
                driver.switch_to.window(parent)
                time.sleep(5)
                x = 0
                break
            x += 1
        if cnt == no_of_products-1:
            break
        cnt += 1
        time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # sleep_between_interactions
    driver.close()
    print(prd_details)
    return prd_details

def get_prd_flpkrt(search, no_of_products):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    driver.get('https://www.flipkart.com')
    button = driver.find_element_by_xpath("/html/body/div[2]/div/div/button")
    button.click()
    search = "+".join(search.split(" "))
    print("search:", search)
    driver.find_element_by_class_name("_3704LK").send_keys(search)
    time.sleep(2)
    driver.find_element_by_class_name('L0Z3Pu').click()
    time.sleep(8)
    prds_likns=driver.find_elements_by_class_name('_4rR01T')
    time.sleep(1)
    cnt=0
    x=0
    parent = driver.current_window_handle
    prd_details = {"name": [], "source": [], "price": [], "model no": [],"category":[]}
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
                category=model_num[4].text
                prd_details["category"].append(category)
                print("category",category)
                driver.close()
                driver.switch_to.window(parent)
                time.sleep(5)
                x=0
                break
            x+=1
        if cnt==no_of_products-1:
            break
        cnt+=1
        time.sleep(5)



    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # sleep_between_interactions
    driver.close()
    print(prd_details)


    return prd_details
def main():

    search=input("Enter what you want to search:")
    flag=True
    while flag:
        try:
            feature=int(input("1:price high to low\n2:price low to high\n =>"))
            if isinstance(feature, int) and feature == 1 or feature == 2:
                flag=False
            else:
                print("please enter a right choise")
        except Exception as e:
            print("Enter the number between [1,2] only.")

    no_of_products=input("Enter the no. of products you want to scrap:")
    if len(no_of_products)==0:
        no_of_products=10
    prd_details=get_prd_amazon(search, int(no_of_products))
    prd_details1=get_prd_flpkrt(search, int(no_of_products))
    for key in prd_details1:
        prd_details[key].extend(prd_details1[key])
    product_details = pd.DataFrame(prd_details)

    if feature == 1:
        product_details.sort_values(by='price', ascending=False)
    elif feature==2:
        product_details.sort_values(by=['price'])
    data_to_xl = pd.ExcelWriter('product_details.xlsx')
    product_details.to_excel(data_to_xl)
    data_to_xl.save()

if __name__=="__main__":
    main()