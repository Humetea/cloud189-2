import requests


class Cloud:

    def __init__(self, cookies):
        self.files = {
            '/': {'id': '-11', 'is_folder': True}
        }

        self.s = requests.Session()
        self.s.cookies = requests.utils.cookiejar_from_dict(dict(p.split('=') for p in cookies.split('; ')))

    def cache_files(self, path):
        cur = ''
        prev = {}

        for p in path.split('/'):
            cur = Cloud.path_format(cur + '/' + p)

            if cur in self.files and self.files[cur]['is_folder']:
                prev = self.files[cur]
                continue

            try:
                print('Fetching %s' % cur)
                r = self.s.get(
                    'https://cloud.189.cn/v2/listFiles.action?fileId=%s&mediaType=&keyword=&inGroupSpace=false&orderBy=1&order=ASC&pageNum=1&pageSize=60&noCache=1' %
                    prev['id']).json()

                file = next(i for i in r['data'] if i['fileName'] == p)
            except:
                break

            prev = self.files[cur] = {
                'id': file['fileId'],
                'digest': file['fileIdDigest'],
                'is_folder': file['isFolder'],
            }

    def download(self, path):
        r = self.s.get(
            'https://cloud.189.cn/downloadFile.action?fileStr=%s&downloadType=1' % self.files[path]['digest'],
            allow_redirects=False)
        r = self.s.get(r.headers['Location'], allow_redirects=False)

        return r.headers['Location']

    @staticmethod
    def path_format(path):
        while '//' in path:
            path = path.replace('//', '/')

        return '/' + path.strip('/')
