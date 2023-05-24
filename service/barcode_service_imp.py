import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.barcode_service import Barcode_Service
from service.json_service_imp import Json_Service_Imp
import secret_key.config as config
import requests
from flask import jsonify 

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

json_service = Json_Service_Imp()

class Barcode_Service_IMP(Barcode_Service):

    def search(self, barcode): # 바코드를 받아서 검색
        # api 호출
        response = requests.get(
            f'http://openapi.foodsafetykorea.go.kr/api/{config.BARCODE_KEY}/C005/json/1/5/BAR_CD={barcode}')
        
        if json_service.json_key_check(response.json()["C005"], "row"):
            # 바코드 정보가 존재할 경우

            data = {
                "data_type":"food",
                "data": response.json()["C005"]["row"]
            }
            return data
        else:
            # 바코드 정보가 존재하지 않을 경우
            return "false"
        
    def crawling_search(self, barcode):
        need_list = ["entpName", #업체명
                    "itemName", #제품명
                    "itemSeq",   #품목기준코드
                    "efcyQesitm",    #효능
                    "useMethodQesitm",   #사용법
                    "atpnWarnQesitm",    #주의사항경고
                    "atpnQesitm",    #주의사항
                    "intrcQesitm",   #상호작용
                    "seQesitm",  #부작용
                    "depositMethodQesitm",   #보관방법
                    "openDe",    #공개일자
                    "updateDe",  #수정일자
                    "itemImage"  #낱알 이미지
                    ]

        result_list = []


        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome('D:\파일 찾기\chromedriver.exe', options=chrome_options)

        driver.get('https://nedrug.mfds.go.kr/searchDrug')

        input_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "stdrCodeName"))
            )
        input_elem.send_keys(f"{barcode}")

        button_elem = driver.find_element(By.CSS_SELECTOR, ".btn_search100")
        button_elem.click()

        try:
            print(barcode)
            # 요소가 보이도록 화면을 스크롤합니다.
            scroll = driver.find_element(By.CSS_SELECTOR, ".table_scroll")
            driver.execute_script("arguments[0].scrollBy(1300, 0)", scroll)

            element = driver.find_element(By.CSS_SELECTOR, "tr.cancel td:nth-child(16) span:nth-child(2)")

            element.click()

            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[1])



            itemName = driver.find_element(By.CSS_SELECTOR, "h2.popupConTitle a:nth-child(1) strong").text.split(":")[1].strip()
            result_list.append(itemName)

            entpName = driver.find_element(By.CSS_SELECTOR, "h2.popupConTitle a:nth-child(3) strong").text.split(":")[1].strip()
            result_list.append(entpName)

            itemImage = driver.find_element(By.CSS_SELECTOR, "div.explan_right img").get_attribute("src")
            result_list.append(itemImage)

            efcyQesitm = driver.find_element(By.ID, "_ee_doc1").text
            result_list.append(efcyQesitm)

            # driver.execute_script("window.scrollTo(0, 600)")
            

            useMethodQesitm = driver.find_element(By.ID, "_ee_doc2").text
            result_list.append(useMethodQesitm)

            # driver.execute_script("window.scrollTo(0, 600)")

            atpnWarnQesitm = driver.find_element(By.ID, "_ee_doc3").text
            result_list.append(atpnWarnQesitm)


            atpnQesitm = driver.find_element(By.ID, "_ee_doc4").text
            result_list.append(atpnQesitm)

            intrcQesitm = driver.find_element(By.ID, "_ee_doc5").text
            result_list.append(intrcQesitm)


            seQesitm = driver.find_element(By.ID, "_ee_doc6").text
            result_list.append(seQesitm)

            depositMethodQesitm = driver.find_element(By.ID, "_ee_doc7").text
            result_list.append(depositMethodQesitm)


            # print(result_list)

            for i in result_list:
                print(i)


            # 작업이 완료되면 새 창을 닫습니다.
            driver.close()

            # 기존 창으로 전환합니다.
            driver.switch_to.window(window_handles[0])

            driver.close()

            data = {
                "data_type": "medicine",
                "data": result_list 
            }

            return jsonify(data)

        except Exception as e:
            print(e)
            return 'false'