import os
import requests as r
import json
from datetime import datetime

SUPABASE_URL  = 'https://api.supabase.com'
SUPABASE_PAT  = os.environ.get('SUPABASE_PAT',None)
SUPABASE_KEY  = os.environ.get('SUPABASE_KEY',None)

class ManagementClient:

    def __init__(self, project_url, supabase_key, supabase_pat):

        if not SUPABASE_KEY:
          print("Please set up your SUPABASE_KEY environment variable")
          return

        self.project_url  = project_url
        self.supabase_key = supabase_key
        self.supabase_pat = supabase_pat
        self.base_path    = self.project_url
        self.headers_pat      = {
                'Authorization': f'Bearer {self.supabase_pat}'
        }
        self.headers_jwt = {
                'Authorization': f'Bearer {self.supabase_key}'
        }


    def get(self, path):
        res = r.get(path, headers = self.headers_pat)
        return (res.status_code, json.dumps(res.json(), indent = 4))

    def post(self, path, data):
        res = r.post(path, headers = self.headers_jwt, json = data)
        return (res.status_code, json.dumps(res.json(), indent = 4))

    def projects(self):
        path = f'{self.base_path}/v1/projects'
        res_code, data = self.get(path)
        return data

    def secrets(self, ref):
        path = f'{self.base_path}/v1/projects/{ref}/secrets'
        res_code, data = self.get(path)
        return data


    def functions(self, ref):
        path = f'{self.base_path}/v1/projects/{ref}/functions'
        res_code, data = self.get(path)
        return data


    def network_restrictions(self, ref):
        path = f'{self.base_path}/v1/projects/{ref}/network-restrictions'
        res_code, data = self.get(path)
        return data

    def organizations(self):
        path = f'{self.base_path}/v1/organizations'
        res_code, data = self.get(path)
        return data

    def create_project(self, data):
        path = f'{self.base_path}/platform/projects'
        res_code, data = self.post(path, data)
        return data



def main():
    management = ManagementClient(SUPABASE_URL, SUPABASE_KEY, SUPABASE_PAT)
    projects   = json.loads(management.projects())
    new_project = {
           "id": projects[0]['id'],
           "organization_id": projects[0]['organization_id'],
           "name": "supadev_clone",
           "region": projects[0]['region'],
           "created_at": str(datetime.now())
    }
    print(projects)

    project = projects[0]['id']
    print(management.organizations())
    print(management.secrets(project))
    print(management.functions(project))
    print(management.network_restrictions(project))


if __name__ == '__main__':
    main()
