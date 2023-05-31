import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.barcode_service import Barcode_Service
from service.json_service_imp import Json_Service_Imp
import secret_key.config as config
import requests
from flask import jsonify 

# 크롤링
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
        
    # 크롤링
    def crawling_search(self, barcode):

        result_list = []


        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome('D:\파일 찾기\chromedriver.exe', options=chrome_options)

        # 해당 URL을 연다 (의약 검색 페이지)
        driver.get('https://nedrug.mfds.go.kr/searchDrug')

        # 검색창에 검색어를 입력합니다.
        input_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "stdrCodeName"))
            )
        # 바코드가 13자리가 아닐 경우 13자리로 만들어준다.
        input_elem.send_keys(f"{barcode[-13:]}")

        # 검색 버튼을 누릅니다.
        button_elem = driver.find_element(By.CSS_SELECTOR, ".btn_search100")
        button_elem.click()

        try:
            print(barcode[-13:])
            # 요소가 보이도록 화면을 스크롤합니다.
            scroll = driver.find_element(By.CSS_SELECTOR, ".table_scroll")
            driver.execute_script("arguments[0].scrollBy(1300, 0)", scroll)

            # 요소 클릭(의약 상세 페이지)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr td:nth-child(16) span:nth-child(2)")))
            element.click()

            # 새로운 탭으로 전환
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[1])

            # 이름 크롤링
            itemName = driver.find_element(By.CSS_SELECTOR, "h2.popupConTitle a:nth-child(1) strong").text.split(":")[1].strip()
            result_list.append(itemName)

            # 업체명 크롤링
            entpName = driver.find_element(By.CSS_SELECTOR, "h2.popupConTitle a:nth-child(3) strong").text.split(":")[1].strip()
            result_list.append(entpName)

            # 제품이미지 크롤링
            itemImage = driver.find_element(By.CSS_SELECTOR, "div.explan_right img").get_attribute("src")
            result_list.append(itemImage)

            # 제품정보 크롤링
            efcyQesitm = driver.find_element(By.ID, "_ee_doc1").text
            result_list.append(efcyQesitm)

            useMethodQesitm = driver.find_element(By.ID, "_ee_doc2").text
            result_list.append(useMethodQesitm)

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


            for i in result_list:
                print(i)

            # 작업이 완료되면 새 창을 닫습니다.
            driver.close()

            # 기존 창으로 전환합니다.
            driver.switch_to.window(window_handles[0])

            # 작업이 완료되면 창을 닫습니다.
            driver.close()

            data = {
                "data_type": "medicine",
                "data": result_list 
            }

            return jsonify(data)    # 크롤링 결과 반환

        except Exception as e:
            print(e)
            return 'false'