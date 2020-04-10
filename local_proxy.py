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
# If you want to turn on debugging for specified module but do not want to replace it, set replacement as None
modules = list(set([i.split('/resources/')[1].split('/')[0] for i in replacement_locations]))


# This script will automagically "create" .json.js files on-the-fly from raw .json i18n dictionaries
def lang_handler(flow, path, local_file):
    local_json = local_file.replace('.json.js', '.json')
    if os.path.exists(local_json):
        with open(local_json, 'r') as f:
            module = path.split('/resources/')[1].replace('.json.js', '.json')
            content = f.read()
            content = "define('" + module + "',[],function(){return " + content + ";});"
            mime_type = 'text/javascript; encoding=utf-8'
            return content, mime_type

    return None, None


def default_handler(flow, path, local_file):
    if os.path.exists(local_file):
        with open(local_file, 'r') as f:
            return f.read(), None

    return None, None


def full_ext(path):
    filename = path.split('/')[-1]
    return '.' + '.'.join(filename.split('.')[1:])


handlers = {
    '.json.js': lang_handler
}


def request(flow):
    request = flow.request
    if request.pretty_host in hosts:
        components = request.path_components
        path = '/' + '/'.join(components)
        for prefix in replacement_locations:
            if path.startswith(prefix):
                target = replacements[prefix]
                if target:
                    local_file = path.replace(prefix, target)
                    extension = full_ext(local_file)
                    handler = handlers[extension] if extension in handlers else default_handler
                    content, mime_type = handler(flow, path, local_file)

                    if content is not None:
                        if mime_type is None:
                            mime_type, encoding = mimetypes.guess_type(path)
                        flow.response = http.HTTPResponse.make(200, content, {
                            'Content-type': mime_type or 'text/plain'
                        })
                    else:
                        flow.response = http.HTTPResponse.make(404, "File not found: " + local_file)


def response(flow):
    request = flow.request
    if request.pretty_host in hosts:
        response = flow.response
        headers = response.headers
        all_headers = headers.get_all('set-cookie')
        all_headers.append('s3debug={}, path=/'.format(','.join(modules)))
        headers.set_all('set-cookie', all_headers)
        response.headers = headers
    pass