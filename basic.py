import json
import os
import requests
import dashscope
from urllib import parse


class BasicRequest:
    def __init__(self, site: str, DEBUG: bool) -> None:
        self.DEBUG = DEBUG
        self.site = site
        self.__read_data()
        self.__create_session()
        self.img_post_url, self.auth = self.__get_url_and_auth_to_post()
        self.__session_nga.headers.update({"auth": self.auth})

    def __read_data(self):
        with open(os.path.join("src", "data.json"), "r", encoding="utf-8") as fr:
            self.__data_json = json.load(fr)
        self.site_dict: dict = self.__data_json["site"]
        self.url_dict: dict = self.__data_json["url"]
        self.dashscope_api_key_dict: dict = self.__data_json["dashscope_api_key"]
        self.bilibili_cookie_dict: dict = self.__data_json["bilibili_cookie"]
        self.nga_cookie_dict: dict = self.__data_json["nga_cookie"]
        self.header_dict: dict = self.__data_json["header"]
        ########
        self.fid = self.site_dict[self.site]["fid"]
        self.tid = self.site_dict[self.site]["tid"]
        self.stid = self.site_dict[self.site]["stid"]
        self.action = self.site_dict[self.site]["action"]
        ########
        try:
            dashscope.api_key = self.dashscope_api_key_dict["default"]
            self.url_nga = self.url_dict["nga"]["default"]
            self.url_bilibili = self.url_dict["bilibili"]["default"]
            self.header_nga: dict = self.header_dict["nga"]
            self.header_bilibili: dict = self.header_dict["bilibili"]
            self.cookie_nga = self.nga_cookie_dict["default"]
            self.cookie_bilibili = self.bilibili_cookie_dict["default"]
            # self.dashscope_api_key = self.dashscope_api_key_dict["default"]
        except Exception as e:
            print(e)

    def __create_session(self) -> None:
        self.__session_bilibili = requests.Session()
        self.__session_bilibili.cookies.update({"SESSION": self.cookie_bilibili})
        self.__session_bilibili.headers.update(self.header_bilibili)
        ##########
        self.__session_nga = requests.Session()
        self.__session_nga.cookies.update({"SESSION": self.cookie_nga})
        self.__session_nga.headers.update(self.header_nga)

    def post_nga(self, data_dict: dict):
        return self.__request(
            url=self.url_nga,
            session=self.__session_nga,
            # data_dict, 包含subject、content等信息，并不是 payload，还是需要 params（只是之后拼接到payload）
            params={
                "fid": self.fid,
                "tid": self.tid,
                "stid": self.stid,
                "action": self.action,
            },
            method="post",
            data_dict=data_dict)

    def get_nga(self):
        return self.__request(
            url=self.url_nga,
            session=self.__session_nga,
            params={
                "fid": self.fid,
                "tid": self.tid,
                "stid": self.stid,
                "action": self.action,
            },
            method="get",
            data_dict=None)

    def post_nga_img(self, img, data_dict: dict):
        payload = {
            'attachment_file1_dscp': '',
            'attachment_file1_img': '1',
            'attachment_file1_auto_size': '',
            'attachment_file1_watermark': '',
            'func': 'upload',
            'v2': '1',
            'origin_domain': 'ngabbs.com',
            '__output': '1',
            'fid': self,
            'attachment_file1_url_utf8_name': "image%2epng",
            'filename': "image.png",
            'Content-Type': "image/png"}

        payload = {**payload, **data_dict}
        if self.DEBUG:
            print(payload)

        if "filename" in data_dict and "Content-Type" in data_dict:
            filename = data_dict["filename"]
            content_type = data_dict["Content-Type"]
        else:
            filename = "image.png"
            content_type = "image/png"
        files = [('attachment_file1', (filename, img, content_type))]
        response = self.__request(url=str(self.img_post_url) + "?__output=11",
                                  session=self.__session_nga,
                                  method="post",
                                  data_dict=dict(),
                                  params=payload,
                                  files=files)
        print(response.text)
        return response

    def get_bilibili(self):
        return self.__request(
            # url=self.url_bilibili,
            url=self.url_bilibili + '?host_mid=' + str(self.site_dict[self.site]["user_id_dict"]),
            session=self.__session_bilibili,
            # params={
            #     "host_mid": self.site_dict[self.site]["user_id_dict"]
            # },
            params={},
            method="get",
            data_dict=None)

    def __request(self, url: str,
                  session: requests.Session,
                  params: dict,
                  method: str,
                  data_dict,
                  files=None) -> requests.Response:
        if method == "post":
            payload_dict = {**params,
                            **data_dict,
                            "nojump": 1,
                            "lite": 'htmljs',
                            "step": 2}
            data = parse.urlencode(payload_dict)
            data = payload_dict
            return session.request(
                url=url,
                method=method,
                params={**params, **{"__output": 11}},
                data=data,
                files=files)
        elif method == "get":
            return session.request(
                url=url,
                params={**params, **{"__output": 14}},
                method=method)

    # 名字带了__的方法基本可以视作是私有方法

    def __get_url_and_auth_to_post(self):
        response = self.get_nga().json()
        print(str(response))
        data_dict = response['result'][0]
        url = data_dict['attach_url']
        auth = data_dict['auth']
        print("url = ", url)
        print("auth = ", auth)
        return url, auth
