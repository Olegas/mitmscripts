import mimetypes
import os

from mitmproxy import http

# Proxy Configuration

mimetypes.add_type('text/vnd.wap.wml; charset=utf-8', '.wml')

# Add hosts from which you want to replace files
hosts = [
    'online.sbis.ru',
    'cdn.sbis.ru',
    'cdn2.sbis.ru'
]


class ReplacementBuilder:
    def __init__(self):
        self.replacements = {}
        self.target_folder = ""

    def set_target_folder(self, folder_path):
        if not os.path.isdir(folder_path):
            raise ValueError("Provided path is not a valid directory.")
        if folder_path[-1] == '/':
            folder_path = folder_path[:-1]
        self.target_folder = folder_path
        return self

    def add_debug_module(self, module_name):
        if not self.target_folder:
            raise ValueError("Target folder must be set first.")
        key = f'/static/resources/{module_name}/'
        value = None
        self.replacements[key] = value
        return self

    def add_module_replacement(self, module_name):
        if not self.target_folder:
            raise ValueError("Target folder must be set first.")
        key = f'/static/resources/{module_name}/'
        value = f'{self.target_folder}/{module_name}/'
        self.replacements[key] = value
        return self

    def add_library_replacement(self, module_name, library_name):
        if not self.target_folder:
            raise ValueError("Target folder must be set before adding library replacements.")

        lower_lib_name = library_name[0].lower() + library_name[1:]

        key1 = f'/static/resources/{module_name}/_{library_name}/'
        value1 = f'{self.target_folder}/{module_name}/_{library_name}/'
        self.replacements[key1] = value1

        key2 = f'/static/resources/{module_name}/{lower_lib_name}.js'
        value2 = f'{self.target_folder}/{module_name}/{lower_lib_name}.js'
        self.replacements[key2] = value2

        key3 = f'/static/resources/{module_name}/{lower_lib_name}.css'
        value3 = f'{self.target_folder}/{module_name}/{lower_lib_name}.css'
        self.replacements[key3] = value3

        return self

    def add_file_replacement(self, relative_path):
        key = f'/static/resources/{relative_path}'
        value = f'{self.target_folder}/{relative_path}'
        self.replacements[key] = value

    def build(self):
        if not self.target_folder:
            raise ValueError("Target folder must be set before building the replacements.")
        return self.replacements


replacements = dict()

b = ReplacementBuilder()
b.set_target_folder('/Users/olegelifantiev/work/event-calendar/application/')
# b.add_module_replacement('EmployeeWorkplace')
b.add_module_replacement('CoreUserCalendar')
b.add_module_replacement('TodayCalendar')
b.add_module_replacement('MainUserCalendar')
b.add_module_replacement('UserCalendarCommon')
# b.add_library_replacement('CoreUserCalendar', 'usersCalendars')
# b.add_module_replacement('ServiceAgreementIntegration')

# b.add_debug_module('Events')
# b.add_debug_module('PEControls')
# b.add_debug_module('Controls-DataEnv')
# b.add_debug_module('React')
# b.add_debug_module('Controls')
# b.add_debug_module('ExtControls')
# b.add_debug_module('Controls-Lists')
# b.add_debug_module('Presto')
b.add_debug_module('Types')
b.add_debug_module('EventsMiniCard')
replacements.update(b.build())

b2 = ReplacementBuilder()
b2.set_target_folder('/Users/olegelifantiev/work/work-time-mgmt_core/application/')
# b2.add_library_replacement('WorkTimeManagementBase', 'workDay')
# b2.add_library_replacement('WorkTimeManagementLite', 'DayTypeChangeMenu')
# b2.add_library_replacement('WorkTimeManagementLite', 'DayInfo')
# b2.add_module_replacement('PlanningVacations')
replacements.update(b2.build())


b3 = ReplacementBuilder()
b3.set_target_folder('/Users/olegelifantiev/work/work-time-mgmt_work-time-planning/application/')
# b3.add_library_replacement('WorkPlanning', 'workSchedule')
replacements.update(b3.build())

b4 = ReplacementBuilder()
b4.set_target_folder('/Users/olegelifantiev/work/wtrules/application')
b4.add_module_replacement('WTRules')
replacements.update(b4.build())

b5 = ReplacementBuilder()
b5.set_target_folder('/Users/olegelifantiev/work/engine_work-time-mgmt/application')
# b5.add_module_replacement('WTMControls')
replacements.update(b5.build())

b6 = ReplacementBuilder()
b6.set_target_folder('/Users/olegelifantiev/work/sbis3-presto/application')
# b6.add_module_replacement('Presto')
replacements.update(b6.build())

b7 = ReplacementBuilder()
b7.set_target_folder('/Users/olegelifantiev/work/booking_core/application')
# b7.add_module_replacement('EQueueBooking')
replacements.update(b7.build())

b8 = ReplacementBuilder()
b8.set_target_folder('/Users/olegelifantiev/work/work-time-mgmt_activity/application')
# b8.add_module_replacement('WorkTimeRule')
replacements.update(b8.build())


# Set this to True to unpack ALL modules
full_debug = False

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
                        origin = request.headers.get('Origin')
                        headers = {
                            b'Content-type': (mime_type or 'text/plain').encode('utf-8'),
                            b'Access-Control-Allow-Credentials': 'true'.encode('utf-8'),
                            b'X-Source': local_file.encode('utf-8')
                        }
                        if origin is not None:
                            headers.update({
                                b'Access-Control-Allow-Origin': origin.encode('utf-8'),
                            })
                        flow.response = http.Response.make(200, content, headers)
                    else:
                        flow.response = http.Response.make(404, "File not found: " + local_file)


def response(flow):
    request = flow.request
    if request.pretty_host in hosts:
        response = flow.response
        headers = response.headers
        all_headers = headers.get_all('set-cookie')
        all_headers.append('s3debug={}; path=/'.format('true' if full_debug else ','.join(modules)))
        headers.set_all('set-cookie', all_headers)
        response.headers = headers
    pass
