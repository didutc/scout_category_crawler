import requests as r
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import json  # json import하기
import urllib.request
import warnings
from alive_progress import alive_bar
import os


class category:  # 카테고리에서 서브 카테고리 없으면 출력 불가
    def __init__(self):
        self.id_array = []
        self.name_array = []
        self.num = input('카테고리넘버: ')

    def Run(self):  # 파일 실행 함수
        filename_list = self.Input()
        name_list_list, id_list_list = self.Scoutcategory(filename_list)
        reverseCategory_list = self.Reversecategory(filename_list)

        self.Makecsv(reverseCategory_list, name_list_list, id_list_list)
        return reverseCategory_list
    # //////////////////////////////// 모든 카테고리가 될수 있도록 바꾸었음 ////////////////////////

    def Input(self):
        word = self.num.split(',')
        filename_list = self.Categorytargeting(word)
        return filename_list

    def Categorytargeting(self, Input_word_list):
        category_list = []
        for Input_word in Input_word_list:
            Input_word = Input_word.replace(" ", "")
            if Input_word == "패션의류":
                category_list.append(1)
            if Input_word == "패션잡화":
                category_list.append(2)
            if Input_word == "화장품":
                category_list.append(3)
            if Input_word == "디지털":
                category_list.append(4)
            if Input_word == "인테리어":
                category_list.append(5)
            if Input_word == "출산":
                category_list.append(6)
            if Input_word == "식품":
                category_list.append(7)
            if Input_word == "스포츠":
                category_list.append(8)
            if Input_word == "생활":
                category_list.append(9)
            if Input_word.isdigit() == True:
                category_list.append(Input_word)

        return category_list

    def Reversecategory(self, Categorytargeting_category_list):
        reverseCategory_list = []

        for Categorytargeting_category in Categorytargeting_category_list:

            if int(Categorytargeting_category) == 1:
                category = "패션의류"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 2:
                category = "패션잡화"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 3:
                category = "화장품"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 4:
                category = "디지털"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 5:
                category = "인테리어"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 6:
                category = "출산"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 7:
                category = "식품"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 8:
                category = "스포츠"
                reverseCategory_list.append(category)
            elif int(Categorytargeting_category) == 9:
                category = "생활"
                reverseCategory_list.append(category)
            else:
                category = Categorytargeting_category
                reverseCategory_list.append(category)

        return reverseCategory_list

    def Scoutcategory(self, categoryNumber_list):  # 아이템 스카우트 카테고리 찾는 함수
        name_list_list = []
        id_list_list = []
        for categoryNumber in categoryNumber_list:

            name_list2 = []
            id_list2 = []
            subcategoryUrl = (
                "https://api.itemscout.io/api/category/"
                + str(categoryNumber)
                + "/subcategories"
            )
            time.sleep(0.4)
            subcategoryUrl_rep = r.get(subcategoryUrl)

            subcategoryUrl_rep_json = json.loads(subcategoryUrl_rep.text)
            subcategoryUrl_datajson_list = subcategoryUrl_rep_json["data"]

            with alive_bar(len(subcategoryUrl_datajson_list)) as bar:

                for subcategoryUrl_datajson in subcategoryUrl_datajson_list:
                    # continue  # skip test
                    bar()

                    # 상위 개체가 있다면 subcategoryUrl_datajson은 여러가지 카테고리가 나온다 그리고 id로 리스폰스를 다시 해보실 또 하위 카테고리가 뜬다 만약 한개만 떴다는 것은 더이상 하위 카테고리가 없다는 뜻이다
                    idNum = subcategoryUrl_datajson["id"]

                    level = subcategoryUrl_datajson["level"]
                    name = subcategoryUrl_datajson["name"]
                    # print(id_data)
                    # print(level_data)

                    subcategoryUrl2 = (
                        "https://api.itemscout.io/api/category/"
                        + str(idNum)
                        + "/subcategories"
                    )
                    time.sleep(0.4)
                    subcategoryUrl_rep2 = r.get(subcategoryUrl2)

                    subcategoryUrl_rep2_json = json.loads(
                        subcategoryUrl_rep2.text)
                    subcategoryUrl_datajson2_list = subcategoryUrl_rep2_json["data"]

                    if len(subcategoryUrl_datajson2_list) == 0:

                        name_list2.append(name)
                        id_list2.append(idNum)
                        continue
                    for subcategoryUrl_datajson2 in subcategoryUrl_datajson2_list:

                        idNum2 = subcategoryUrl_datajson2["id"]
                        level2 = subcategoryUrl_datajson2["level"]
                        name2 = subcategoryUrl_datajson2["name"]
                        # print(id_data2)
                        # print(level_data2)

                        subcategoryUrl3 = (
                            "https://api.itemscout.io/api/category/"
                            + str(idNum2)
                            + "/subcategories"
                        )
                        time.sleep(0.4)
                        subcategoryUrl_rep3 = r.get(subcategoryUrl3)

                        subcategoryUrl_rep3_json = json.loads(
                            subcategoryUrl_rep3.text)

                        subcategoryUrl_datajson3_list = subcategoryUrl_rep3_json["data"]
                        if len(subcategoryUrl_datajson3_list) == 0:
                            name_list2.append(name + ">" + name2)
                            id_list2.append(idNum2)
                            continue
                        for subcategoryUrl_datajson3 in subcategoryUrl_datajson3_list:

                            idNum3 = subcategoryUrl_datajson3["id"]
                            level3 = subcategoryUrl_datajson3["level"]
                            name3 = subcategoryUrl_datajson3["name"]
                            # print(id_data2)
                            # print(level_data2)

                            name_list2.append(name + ">" + name2 + ">" + name3)
                            id_list2.append(idNum3)
            name_list_list.append(name_list2)
            id_list_list.append(id_list2)

        return name_list_list, id_list_list

    # ////////////////////////////// 패스 데이터 베이스 파일로 바꾸기 ///////////////////////
    def Makecsv(self, filename_list, name_list_list, id_list_list):  # Csv만드는 함수
        path = "./"
        try:
            os.mkdir(path)
        except:
            pass
        finalname_list = []
        finalid_list = []
        for filename, name_list, id_list in zip(filename_list, name_list_list, id_list_list):
            #

            data = pd.DataFrame({"이름": name_list, "id": id_list})

            data.to_csv(
                path + "\\" + filename + "_category.csv",
                mode="w",
                encoding="utf-8-sig",
                index=False,
            )


category = category()
category.Run()
######## 마지막카테고리만 입력  ########################
# ### 고쳐야 할것 기존 카테고리 입력체제, CSV 저장 체제###
