import requests


def post_video(video,
             fid = 823,
             num = 1,
             file_type = 'mp4',
             attachment_file1_auto_size = '',
             filename = 'image.mp4',
             attachment_file1_url_utf8_name = "image%2emp4",
             Content_Type = 'video/mp4',
             cookie='',
             auth='',
             url_of_video='',
             ):
    round_num = 0
    num = str(num) 
    url_of_video_json = str(url_of_video) + "?__output=11"

    while 1:
        payload = {'attachment_file1_dscp': '',
            'attachment_file1_video': '1',
            # 'attachment_file1_auto_size': '1',
            'attachment_file1_auto_size': attachment_file1_auto_size,
            'attachment_file1_watermark': '',
            'func': 'upload',
            'v2': '1',
            'origin_domain': 'ngabbs.com',
            '__output': '1',
            'auth': auth,
            'fid': '823',
            'attachment_file1_url_utf8_name': attachment_file1_url_utf8_name,
            'filename': filename,
            'Content-Type': Content_Type}
        print("\n",payload,"\n")
        
        files=[
        ('attachment_file1',(filename,video,Content_Type))
        ]

        headers = {'Cookie': cookie,}

        response = requests.request("POST", url_of_video_json, headers=headers, data=payload, files=files)
        print(response.text)
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
                else: break
            else: break
        except:
            break

    attachments = response.json()['attachments']
    attachments_check = response.json()['attachments_check']
    url_of_video_uploaded = response.json()['url']

    return attachments_check, url_of_video_uploaded, attachments


def upload_one_video(num, file_type='png', fid = 823, video = '', auth='', url_of_video=''):
    response = requests.get(video)
    # response.content 已经是 bytes 数据
    attachments_check, url_of_video_uploaded, attachments = post_video(video = response.content,
                                                                   fid=fid,num=num,
                                                                   file_type=file_type,
                                                                   auth=auth,
                                                                   url_of_video=url_of_video);
    url_of_video_uploaded = '[flash=video]./'+ str(url_of_video_uploaded) + '[/flash]'
    return attachments_check, url_of_video_uploaded, attachments


def upload_video(
        auth='',
        url_of_video='',
        video_list=None):
    # url_of_video 是要把图片传上去的地址，也就是nga的图片服务器
    # video_list 是要上传的图片的 url 列表
    if video_list is None:
        video_list = []
    video_uploaded_list = []
    attachments_check_list = []
    attachments_list = []
    num = 0
    for video in video_list:
        num += 1
        print(video)
        attachments_check, url_of_video_uploaded, attachments = upload_one_video(num=num, video=video, auth=auth, url_of_video=url_of_video)
        video_uploaded_list.append(url_of_video_uploaded)
        attachments_check_list.append(attachments_check)
        attachments_list.append(attachments)
    print('video_uploaded_list=',video_uploaded_list.__str__())
    return video_uploaded_list, attachments_check_list, attachments_list


if __name__ == "__main__":
    pass