import requests

class ImgUploader:
    def __init__(self, requester):
        self.requester = requester

    def post_img(self, img):
        round_num = 0
        data_dict = {}
        while 1:
            response = self.requester.post_nga_img(img, data_dict)
            try:
                if response.json()["error_code"] == 9:
                    if round_num == 0:
                        print(round_num)
                        data_dict = {
                            "filename": 'image_gif.gif',
                            "attachment_file1_url_utf8_name": "image_gif%2egif",
                            "Content_Type": 'image/gif',
                            "file_type": 'gif',
                        }
                        round_num += 1
                        continue
                    elif round_num == 1:
                        print(round_num)
                        data_dict = {"attachment_file1_auto_size": '1'}
                        continue
                    else: break
                else: break
            except:
                break

        # print(response.text)
        attachments = response.json()['attachments']
        attachments_check = response.json()['attachments_check']
        url_of_img_uploaded = response.json()['url']

        return attachments_check, url_of_img_uploaded, attachments

    def post_img_ori(self,
                 img,
                 fid=823,
                 num=1,
                 attachment_file1_auto_size='',
                 filename='image.png',
                 attachment_file1_url_utf8_name="image%2epng",
                 file_type='png',
                 Content_Type='image/png',
                 cookie='',
                 auth='',
                 url_of_img='',
                 ):

        fid=self.requester.fid
        cookie=self.requester.cookie_nga
        auth=self.requester.auth
        url_of_img=self.requester.img_post_url
        round_num = 0
        num = str(num)
        url_of_img_json = str(url_of_img) + "?__output=11"

        while 1:
            payload = {'attachment_file1_dscp': '',
                       'attachment_file1_img': '1',
                       # 'attachment_file1_auto_size': '1',
                       'attachment_file1_auto_size': attachment_file1_auto_size,
                       'attachment_file1_watermark': '',
                       'func': 'upload',
                       'v2': '1',
                       'origin_domain': 'ngabbs.com',
                       'auth': auth,
                       'fid': fid,
                       'attachment_file1_url_utf8_name': attachment_file1_url_utf8_name,
                       'filename': filename,
                       'Content-Type': Content_Type}

            files = [
                ('attachment_file1', (filename, img, Content_Type))
            ]

            headers = {
                'Cookie': cookie
            }

            response = requests.request("POST", url_of_img_json, headers=headers, data=payload, files=files)
            # print(response.text)
            try:
                if response.json()["error_code"] == 9:
                    if round_num == 0:
                        print(round_num)
                        filename = 'image_gif.gif'
                        attachment_file1_url_utf8_name = "image_gif%2egif"
                        Content_Type = 'image/gif'
                        file_type = 'gif'
                        round_num += 1
                        continue
                    elif round_num == 1:
                        print(round_num)
                        attachment_file1_auto_size = '1'
                        continue
                    else:
                        break
                # elif response.json()["error_code"] == 4:
                # # {"error_code":4,"error":"upload file error 1"}
                # # 搞不懂为什么会是这个问题. 按理来说图片过大应该是9的.
                #     break
                else:
                    print(round_num)
                    attachment_file1_auto_size = '1'
                    continue
            except:
                break

        attachments = response.json()['attachments']
        attachments_check = response.json()['attachments_check']
        url_of_img_uploaded = response.json()['url']

        return attachments_check, url_of_img_uploaded, attachments


    def upload_one_img(self, num, file_type='png', img = ''):
        response = requests.get(img)
        # if self.requester.DEBUG:
            # print(response)
        # attachments_check, url_of_img_uploaded, attachments = self.post_img(img = response.content)
        attachments_check, url_of_img_uploaded, attachments = self.post_img_ori(img = response.content)
        url_of_img_uploaded = '[img]./'+ str(url_of_img_uploaded) + '.medium.jpg' + '[/img]'
        return attachments_check, url_of_img_uploaded, attachments


    def upload_img(self, img_list=None):
        if img_list is None:
            img_list = list()
        img_uploaded_list = []
        attachments_check_list = []
        attachments_list = []
        num = 0
        for img in img_list:
            num += 1
            # print(img)
            attachments_check, url_of_img_uploaded, attachments = self.upload_one_img(num=num, img=img)
            img_uploaded_list.append(url_of_img_uploaded)
            attachments_check_list.append(attachments_check)
            attachments_list.append(attachments)
        # print('img_uploaded_list=',img_uploaded_list.__str__())
        return img_uploaded_list, attachments_check_list, attachments_list


if __name__ == "__main__":
    from basic import BasicRequest

    requester = BasicRequest("crosscore", DEBUG=True)
    image_uploader = ImgUploader(requester)
    img = "https://img.nga.178.com/attachments/mon_202407/14/7nQk9e-cbz2K1oT3cSnj-cp.jpg"
    pic_list, attachments_check_list, attachments_list = image_uploader.upload_img([img])
    print(pic_list)
    print(attachments_list)
    print(attachments_check_list)