import os
import sys
import datetime
import json
from zipfile import ZipFile
from pytz import timezone
import ast

# Defaults
domains = []
saz_file_path = ''
output_folder = ''
my_timezone = 'GMT'
time_sent_format = '%Y-%m-%d-%H:%M:%S'
date_format = '%a, %d %b %Y %H:%M:%S ' + my_timezone


def parse_headers(content):
    # Get rid of the body
    headers = content.split(b'\x0d\x0a\x0d\x0a')[0]
    # Split by lines without the first one (eg. 'HTTP/1.1 200')
    headers_lines = headers.splitlines()[1:]

    parsed_headers = []
    time_sent = ''

    for line in headers_lines:
        if b': ' in line:
            line = line.decode('utf-8')
            split_header = line.split(': ')
            parsed_headers.append(split_header)

            # Retrieve time from relevant header
            if split_header[0] == 'Time-Sent':
                time_sent = datetime.datetime.fromtimestamp(int(split_header[1]) / 1000, tz=timezone(my_timezone))\
                    .strftime(time_sent_format)
            elif split_header[0] == 'Date':
                time_sent = datetime.datetime.strptime(split_header[1], date_format)
                time_sent = time_sent.strftime(time_sent_format)

    return parsed_headers, time_sent


def get_body(content):
    # Get rid of the headers
    body = content.split(b'\x0d\x0a\x0d\x0a')[1:]
    body = b'\x0d\x0a\x0d\x0a'.join(body)

    return body


# Add your own implementation for parsing the body for your own needs
def request_custom_parse_body(body):
    return ''


# Add your own implementation for parsing the body for your own needs
def response_custom_parse_body(body):
    return ''


def parse_saz_file(file_path, output_folder_name):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    with ZipFile(file_path, 'r') as saz_zip:
        # Extract the sessions files from the .saz archive
        session_files = [f for f in saz_zip.namelist() if f.endswith('.txt')]
        session_files.reverse()
        session_tuples = []
        while len(session_files) > 1:
            session_tuples.append({'request': session_files.pop(), 'response': session_files.pop()})

        for session_tuple in session_tuples:
            session_data = {'domain': '', 'path': '', 'time': '', 'parsed_request': {}, 'parsed_response': {}}

            # Parse request
            with saz_zip.open(session_tuple['request']) as req:
                content = req.read()
                session_data['request_hex'] = content.hex()
                session_data['parsed_request']['req_type'] = content.split(b'\r\n')[0].split(b' ')[0].decode('utf-8')
                if session_data['parsed_request']['req_type'] == 'CONNECT':
                    continue
                path = content.split(b'\r\n')[0].split(b' ')[1]
                session_data['domain'] = path.split(b'://')[1].split(b'/')[0].decode('utf-8')
                path = path.split(b'://')[1].split(b'/')[1:]
                session_data['path'] = (b'/' + b'/'.join(path)).decode('utf-8')
                if len(domains) > 0 and session_data['domain'] not in domains:
                    continue

                session_data['parsed_request']['headers'], time_sent = parse_headers(content)
                if time_sent != '':
                    session_data['time'] = time_sent
                body = get_body(content)
                session_data['parsed_request']['body_hex'] = body.hex()
                session_data['parsed_request']['custom_parsed_body'] = request_custom_parse_body(body)

            # Parse response
            with saz_zip.open(session_tuple['response']) as res:
                content = res.read()
                session_data['response_hex'] = content.hex()

                session_data['parsed_response']['code'] = int(content.split(b'\r\n')[0].split(b' ')[1])

                session_data['parsed_response']['headers'], time_sent = parse_headers(content)
                if time_sent != '' and session_data['time'] == '':
                    session_data['time'] = time_sent
                body = get_body(content)
                session_data['parsed_response']['body_hex'] = body.hex()
                session_data['parsed_response']['custom_parsed_body'] = response_custom_parse_body(body)

            # Dump session data to a file
            filename = 'session' + res.name.split('raw/')[1].split('_')[0] + '.json'
            file_path = os.path.join(output_folder_name, filename)

            json_object = json.dumps(session_data, indent=4)
            with open(file_path, 'w') as json_file:
                json_file.write(json_object)


# Check if all arguments are provided
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("[!] Usage: python " + sys.argv[0] + " <saz_file_path> <output_folder> [<list of domains>]")
    exit()

else:
    saz_file_path = sys.argv[1]
    output_folder = sys.argv[2]
    if len(sys.argv) == 4:
        domains = ast.literal_eval(sys.argv[3])

parse_saz_file(saz_file_path, output_folder)
