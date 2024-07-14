import json

class DataFetcher:
    def __init__(self, requester):
        self.requester = requester

    @staticmethod
    def data_dict_get(requester):
        response = requester.get_bilibili()
        data_dict = response.json()
        if response.status_code == 200:
            with open("./data_got.json",'w',encoding='utf-8') as data_file:
                json.dump(data_dict, data_file)
        else:
            data_file=open("./data_got.json",'r',encoding='utf-8')
            data_dict=json.loads(data_file.read())
            data_file.close()
        return data_dict


if __name__ == "__main__":
    pass