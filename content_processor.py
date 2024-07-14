from process_article import process_article
import codecs
from upload_img import ImgUploader
import random
import dashscope
from http import HTTPStatus


class TitleGenerator:
    def __init__(self, content: str):
        self.content = content

    @staticmethod
    def generate_title(content: str):
        print("\n调用通义千问")
        messages = [{
            'role': 'system',
            'content': "以下是一个名为“交错战线”的游戏中的一篇公告，请你提炼出这篇公告的标题，要求十个字以内，\
                            不需要出现“交错战线”游戏名字，不需要包含引号，不需要出现年份。\n\
                            以下为要求：\
                            如果是对某个人物的介绍，那么标题应为 \"角色介绍——\"后跟人物名称。\
                            如果含有 \"维护公告\" 一类的字样，那么这是一篇维护公告，摘取月份、日期、时间点，加上 \"维护公告\" 作为标题即可。\
                            如果这篇公告是由多个部分组成，不需要包含所有细分的副标题，而是应该总结为一个十个字以内的总标题。\n\
                            不需要出现“交错战线”游戏名字，不需要包含引号，不需要出现年份。\n\
                            以下为需要提炼标题的正文：\n\n\n"
        }, {
            'role': 'user',
            'content': content
        }]
        response = dashscope.Generation.call(
            "qwen-turbo",
            messages=messages,
            seed=random.randint(1, 10000),
            result_format='message',
        )
        if response.status_code == HTTPStatus.OK:
            print((response))
            print(response.output.choices[0].message.content)
            return response.output.choices[0].message.content
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message))
            return None


class ContentProcessor:
    def __init__(self, requester):
        self.requester = requester
        self.image_uploader = ImgUploader(requester)
        self.subject = "[搬运] "
        self.content = ""
        self.subject_title = ""
        self.attachments_check = ''
        self.attachments = ''
        self.pics = ''

    def __encode_text(self):
        try:
            self.subject = codecs.encode(self.subject, 'GBK')
            print("标题转换为gbk成功")
        except UnicodeEncodeError as e:
            print(f"标题转换失败: {e}")
            try:
                self.subject = codecs.encode(self.subject, 'GBK', errors='ignore')
            except UnicodeEncodeError as e:
                print(f"标题转换再次失败: {e}")
                self.subject = codecs.encode(self.subject, 'GBK', errors='replace')
        try:
            self.content = codecs.encode(self.content, 'GBK')
            print("内容转换为gbk成功")
        except UnicodeEncodeError as e:
            print(f"内容转换失败: {e}")
            try:
                self.content = codecs.encode(self.content, 'GBK', errors='ignore')
            except UnicodeEncodeError as e:
                print(f"内容转换再次失败: {e}")
                self.content = codecs.encode(self.content, 'GBK', errors='replace')

    def __process_desc(self, content_list: list):
        try:
            self.subject_title = [n for n in content_list if n["type"] == "RICH_TEXT_NODE_TYPE_TOPIC"]
            content_list = [n for n in content_list if n["type"] != "RICH_TEXT_NODE_TYPE_TOPIC"]
            self.subject_title = " ".join(title["text"] for title in self.subject_title) \
                .replace('#', "") \
                .replace('交错战线公测', "") \
                .replace('交错战线', "")

            content_list = [f"[url={item['jump_url']}]{item['text']}[/url]" if "jump_url" in item else item["text"]
                            for item in content_list]

            self.subject_title += ''.join(content_list).split('\n', 1)[0]
            # content_tmp = "\n".join(content_list)
            content_tmp = " ".join(content_list)
            self.content += content_tmp
            if not self.requester.DEBUG:
                if "动态抽奖" not in content_tmp and "互动抽奖" not in content_tmp:
                    return "OK"
                else:
                    return "动态抽奖"
            print("解析desc成功")
        except Exception as e:
            print("未能解析 desc:", e)
            return None

    def __process_draw(self, pic_list):
        pic_list, attachments_check_list, attachments_list = self.image_uploader.upload_img(
            img_list=[f"{item['src']}" for item in pic_list])
        self.pics += "\n".join(pic_list) + "\n"
        self.attachments_check += "\t".join(attachments_check_list) + "\t"
        self.attachments += "\t".join(attachments_list) + "\t"

    def __process_archive(self, video_list):
        self.content += video_list["desc"] + "\n"
        pic_list, attachments_check_list, attachments_list = self.image_uploader.upload_img(
            img_list=[video_list['cover']])
        self.pics += "\n".join(pic_list) + "\n"
        self.content += f"[flash]{video_list['jump_url']}[/flash]" + "\n"
        self.content += f"[url]{video_list['jump_url']}[/url]" + "\n"
        self.subject_title = video_list["title"]
        self.attachments_check += "\t".join(attachments_check_list) + "\t"
        self.attachments += "\t".join(attachments_list) + "\t"

    def __process_article(self, data):
        content_tmp = data["major"]["article"]["desc"]
        self.subject_title = data["major"]["article"]["title"]
        jump_url = data["major"]["article"]["jump_url"]
        self.content += f'[url=https:{jump_url}]{self.subject_title}[/url]\n'
        if not self.requester.DEBUG:
            if "动态抽奖" not in content_tmp:
                self.content += content_tmp
            else:
                return "动态抽奖"
        pic_list = data["major"]["article"]["covers"]
        (pic_list,
         attachments_check_list,
         attachments_list) = self.image_uploader.upload_img(img_list=pic_list)
        self.pics += "\n".join(pic_list) + "\n"
        self.attachments_check += "\t".join(attachments_check_list) + "\t"
        self.attachments += "\t".join(attachments_list) + "\t"

    def __process_subject_and_content(self):
        self.subject_title = self.subject_title.replace("\n", "")
        self.content = self.content.replace("\n\n\n", "\n\n")

        print(self.content)

        self.subject_title += TitleGenerator.generate_title(content=self.content)
        self.subject = "[搬运] " + self.subject_title

        print("\nself.subject = ", self.subject)
        print("\nself.content = ", self.content)

        if len(self.content) < 6:
            self.content = self.subject_title

        print("\nattachments_check", self.attachments_check)
        print("\nattachments", self.attachments)
        self.__encode_text()

    def generate_content(self, data_latest: dict):
        if self.requester.DEBUG:
            print("generating_content")

        url_of_img = self.requester.img_post_url
        opus_id = data_latest["id_str"]
        data_modules = data_latest["modules"]["module_dynamic"]
        try:
            data_orig = data_latest["orig"]["modules"]["module_dynamic"]
            print("为转发动态")
        except:
            data_orig = None
        data_dict = {
            "modules": data_modules,
            "orig": data_orig,
        }
        dynamic_component_list = data_dict.keys()
        if self.requester.DEBUG:
            print("dynamic_component_list = ", dynamic_component_list)

        if (data_modules.get('major') is not None) and (data_modules.get('major').get('article') is not None):
            url_of_article = "https:" + data_modules["major"]["article"]["jump_url"]
            print("url_of_article: ", url_of_article)
            # 说明是长文章
            self.subject_title, self.content, self.attachments_check, self.attachments = process_article(
                url_of_article=url_of_article,
                opus_id=opus_id,
                auth=self.requester.auth,
                url_of_img=self.requester.img_post_url
            )
        else:
            for dynamic_component in dynamic_component_list:
                data = data_dict[dynamic_component]
                if data is None:
                    continue
                if dynamic_component == "orig":
                    print('dynamic_component == "orig"')
                    self.content += "[quote]"
                if "desc" in data:
                    if data["desc"] is not None:
                        content_list = data["desc"]["rich_text_nodes"]
                        process_desc_result = self.__process_desc(content_list)
                        if not self.requester.DEBUG and process_desc_result == "动态抽奖":
                            return "动态抽奖"
                        # self.content += data["desc"]["text"]

                if data["major"] is not None:
                    if "draw" in data["major"]:
                        pic_list = data["major"]["draw"]["items"]
                        self.__process_draw(pic_list)

                    if "archive" in data["major"]:
                        video_list = data["major"]["archive"]
                        self.__process_archive(video_list)

                    if "article" in data["major"]:
                        process_article_result = self.__process_article(data)
                        if not self.requester.DEBUG and process_article_result == "动态抽奖":
                            return "动态抽奖"

                if dynamic_component == "modules":
                    if data["desc"] is not None:
                        if "draw" in data["desc"]:
                            pic_list = data["desc"]["draw"]["items"]
                            self.__process_draw(pic_list)
                        if "archive" in data["desc"]:
                            video_list = data["desc"]["archive"]
                            self.__process_archive(video_list)

                if dynamic_component == "orig":
                    self.content += "[/quote]"
                self.content += "\n\n" + self.pics

        print(self.pics)
        print("\nself.subject title = ", self.subject_title)
        self.__process_subject_and_content()
        return self.subject, self.content, self.attachments_check, self.attachments
