from content_processor import ContentProcessor


class PostGenerator:
    def __init__(self, requester):
        self.requester = requester

    def post(self,
             subject,
             content,
             attachments_check,
             attachments):
        data_dict = {
            "post_subject": subject,
            "post_content": content,
            "attachments_check": attachments_check,
            "attachments": attachments,
        }
        response = self.requester.post_nga(data_dict)
        print(response.text)

    def generate_content(self, data_latest: dict):
        content_processor = ContentProcessor(requester=self.requester)
        return content_processor.generate_content(data_latest)

    def generate_post(self, data_latest):
        subject, content, attachments_check, attachments = self.generate_content(data_latest)
        if [subject, content, attachments_check, attachments] == ["动", "态", "抽", "奖"]:
            return
        data_dict = {
            "post_subject": subject,
            "post_content": content,
            "attachments_check": attachments_check,
            "attachments": attachments
        }
        print(data_dict)
        print(self.requester.post_nga(data_dict=data_dict).text)
        return


if __name__ == "__main__":
    pass
