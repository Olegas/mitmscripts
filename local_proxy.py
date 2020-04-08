from mitmproxy import http
from mitmproxy import ctx
import os
import mimetypes

# Proxy Configuration

mimetypes.add_type('text/vnd.wap.wml; charset=utf-8', '.wml')

# Add hosts from which you want to replace files
hosts = ['pre-test-online.sbis.ru', 'online.sbis.ru']

# Add replacement points. Key is a URL part (URL must begin with a given key), values is a path
# Path can be relative (from current working dir) or absolute
# Longest path will be checked first
replacements = {
    '/resources/WorkTimeManagementLite/': '../no_backup/core/client/WorkTimeManagementLite/',
    '/resources/WorkTimeManagementLite/DayInfo': '/Users/oleg/work/no_backup/core/client/WorkTimeManagementLite/DayInfo'
}

# Just change settings above and save script - MITM will reload it automatically
replacement_locations = sorted(replacements.keys(), reverse=True)

# Also, you need not to set debug cookies,
# this script will analyze modules, you are replacing, and add corresponding cookies to request
modules = list(set([i.split('/resources/')[1].split('/')[0] for i in replacement_locations]))


def request(flow):
    request = flow.request
    if request.pretty_host in hosts:
        cookies = request.cookies
        cookies['s3debug'] = ','.join(modules)
        components = request.path_components
        path = '/' + '/'.join(components)
        for prefix in replacement_locations:
            if path.startswith(prefix):
                target = replacements[prefix]
                local_file = path.replace(prefix, target)
                if os.path.exists(local_file):
                    with open(local_file, 'r') as f:
                        content = f.read()
                        mime_type, encoding = mimetypes.guess_type(path)
                        flow.response = http.HTTPResponse.make(200, content, {
                            'Content-type': mime_type or 'text/plain'
                        })
                else:
                    flow.response = http.HTTPResponse.make(404, "File not found: " + local_file)
