import time
import os
import json

from basic import BasicRequest
from data_dict_get import DataFetcher
from generate_post import PostGenerator

class Poster:
    def __init__(self, site: str, DEBUG=False):
        self.DEBUG = DEBUG
        self.get_sites()
        self.site = site
        self.requester = BasicRequest(site=site, DEBUG=DEBUG)

    @staticmethod
    def get_sites():
        with open(os.path.join("src", "data.json"), "r", encoding="utf-8") as fr:
            data_json = json.load(fr)
        return data_json["site"].keys()

    def get_data_list(self, site: str):
        try:
            data_dict = DataFetcher.data_dict_get(self.requester)
            return data_dict["data"]["items"]
        except Exception as e:
            print("bilibili api 请求故障")
            print(e)
            time.sleep(5)
            try:
                data_dict = DataFetcher.data_dict_get(self.requester)
                return data_dict["data"]["items"]
            except Exception as e:
                print("bilibili api 请求再次故障")
                print(e)
                return

    def post_data(self, data_list, post_num):
        for data in data_list:
            current_time = int(time.time())
            data_time = data["modules"]["module_author"]["pub_ts"]
            time_diff = (current_time - data_time) / 60
            if time_diff < 30:
                if post_num >=1:
                    time.sleep(180)
                gen = PostGenerator(requester=self.requester).generate_post(data)
                print(gen)
                if gen == "动态抽奖": continue
                post_num += 1
        return post_num

    def post_data_test(self, data_list, post_num):
        data = data_list[6]
        with open(os.path.join("src", "data_list_tmp.txt"), "w", encoding="utf-8") as fr:
            fr.write(str(data_list))
        # with open(os.path.join("src", "data_list_tmp_1_desc_rich_text_nodes.json"), "w", encoding="utf-8") as fr:
        #     fr.write(str(data_list[1]["modules"]["desc"]["rich_text_nodes"]))
        # with open(os.path.join("src", "data_list_tmp_1_orig.json"), "w", encoding="utf-8") as fr:
        #     fr.write(str(data_list[1]["orig"]))
        gen = PostGenerator(requester=self.requester).generate_post(data)
        print(gen)
        return 1


site_list = Poster.get_sites()

###########

item = "test"
poster = Poster(site=item, DEBUG=True)
data_list = poster.get_data_list(site=item)
post_num = 0
if data_list != None:
    post_num += poster.post_data_test(data_list, post_num)
    if post_num == 0:
        print("No Post Detected!!")
    else:
        print(f"{post_num} Post is sent!!")
else:
    print("API Wrong!!")

###########

# for item in site_list:
#     if item == "test":
#         continue
#     poster = Poster(site=item)
#     data_list = poster.get_data_list(site=item)
#     post_num = 0
#     if data_list != None:
#         post_num += poster.post_data(data_list, post_num)
#         if post_num == 0:
#             print("No Post Detected!!")
#         else:
#             print(f"{post_num} Post is sent!!")
#     else:
#         print("API Wrong!!")

