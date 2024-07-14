import requests
from bs4 import BeautifulSoup
from upload_img import ImgUploader


def process_article(
        auth,
        url_of_img,
        url_of_article,
        opus_id,
):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    }
    url = url_of_article
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    nga_code = ""
    attachments_check = ""
    attachments = ""
    subject_title = ""
    nga_code += "[quote]"
    try:
        normal_article_holder = soup.find('div',class_ = "normal-article-holder")
        subject_title = soup.find('h1',class_='title').text
        print("article")
        for element in normal_article_holder.descendants:
            if element.name == 'p':
                if element.text.__len__() <= 1:
                    print("element.text.__len__() <= 1", element.text, element.text.__len__())
                    nga_code += "\n"
                elif "、" in element.text[0:2] and element.text[0] in ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]:
                    print(element.text)
                    nga_code += "[/quote]\n[quote][h][size=130%]" + element.text + "[/size][/h]\n"
                else:
                    nga_code += element.text + "\n"
            elif element.name == 'figure':
                img_tag = element.find('img')
                data_src_value = "https:" + img_tag.get('data-src')
                pic_list, attachments_check_list, attachments_list = upload_img(auth=auth, url_of_img=url_of_img, img_list=[data_src_value])
                attachments_check += "\t".join(attachments_check_list)+"\t"
                attachments += "\t".join(attachments_list)+"\t"
                nga_code += "\n".join(pic_list)+"\n"
    except Exception as e:
        print(e)
        if "/read/cv" in url_of_article:
            url = "https://www.bilibili.com/opus/" + opus_id
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
    try:
        opus_module_content = soup.find('div',class_ = "opus-module-content")
        opus_module_title__text = soup.find('span',class_='opus-module-title__text').text
        if opus_module_content != None:
            subject_title = opus_module_title__text
            print("article")
            for element in opus_module_content.descendants:
                if element.name == 'p':
                    if element.text.__len__() <= 1:
                        print("element.text.__len__() <= 1", element.text, element.text.__len__())
                        nga_code += "\n"
                    elif "、" in element.text[0:2] and element.text[0] in ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]:
                        print(element.text)
                        nga_code += "[/quote]\n[quote][h][size=130%]" + element.text + "[/size][/h]\n"
                    else:
                        nga_code += element.text + "\n"
                elif element.name == 'div' and "opus-para-pic" in element.get('class'):
                    img_tag = element.find('img')
                    data_src_value = "https:" + img_tag.get('src')
                    data_src_value = data_src_value[:(data_src_value.find(".jpg") + 4)]
                    pic_list, attachments_check_list, attachments_list = upload_img(auth=auth, url_of_img=url_of_img, img_list=[data_src_value])
                    attachments_check += "\t".join(attachments_check_list)+"\t"
                    attachments += "\t".join(attachments_list)+"\t"
                    nga_code += "\n".join(pic_list)+"\n"
    except Exception as e:
        print(e)
    
    nga_code += "[/quote]"
    print(nga_code)
    return subject_title, nga_code, attachments_check, attachments


if __name__ == "__main__":
    pass