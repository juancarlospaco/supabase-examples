import os
import requests as r
import json


PROJECT_URL  = os.environ.get('SUPABASE_URL',None)
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', None)


class Client:

    def __init__(self, project_url, supabase_key):

        if not SUPABASE_KEY:
            print("Please set up your SUPABASE_KEY environment variable")
            return

        self.project_url  = project_url
        self.supabase_key = supabase_key
        self.base_path    = self.project_url + "/rest/v1"
        self.pg_range     = None
        self.headers      = {'apiKey': self.supabase_key}


    def connect(self, path):
        res = r.get(path, headers = self.headers)
        return (res.status_code, json.dumps(res.json(), indent = 4))


    def pagination(self, start, end):
        self.pg_range = range(start, end)


    def paginationRequested(self):
        self.headers["Range"] = f'{self.pg_range.start}-{self.pg_range.stop}'


    def resultSet(self, path, pagination=False):
        if pagination:
            self.paginationRequested()

        response_code, response_data = self.connect(path)

        #if response_code == 200:
        print(response_data)


    def selectAll(self, table_name, pagination=False):
        path = f'{self.base_path}/{table_name}?select=*'
        self.headers["Authorization"] = f'Bearer {self.supabase_key}'
        self.resultSet(path, pagination)


    def selectColumns(self, table_name, pagination=False, cols=[]):
        csc  = ",".join(cols)
        path = f'{self.base_path}/{table_name}?select={csc}'
        self.headers["Authorization"] = f'Bearer {self.supabase_key}'
        self.resultSet(path, pagination)


def main():
    client = Client(PROJECT_URL, SUPABASE_KEY)
    #client.pagination(0,0)
    client.selectAll("products")
    #client.selectColumns("products", ["id"])


if __name__ == '__main__':
    main()
