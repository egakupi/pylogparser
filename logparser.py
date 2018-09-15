import re

"""
Написать функцию-парсер таких log-файлов, который будет находить все такие события и возвращать структуру со следующей информацией (по примеру выше):

PID: 14211
SF_AT: 00000000
SF_TEXT:
EAX=E4399DEC EBX=00000000 ECX=00000000 EDX=00000000
ESI=F6D84000 EDI=F6C16E74 EBP=F6C16E94 EFL=00010246
ESP=F6C16E3C (746E C1F6 0040 D8F6 EC9D 39E4 F45A 3AF7 EC9D 39E4 A222 1E00 1B00 0000 946E C1F6)
EIP=F73A4EBC (8A1A 8A15 7970 06F7 8A9B 586D 06F7 00D3 8A50 0100 DA8D 5802 0FB6 7301 31C0 8A86)

"""


def log_parser(log_file_path, output_file_path):
    infile = open(log_file_path, "r")
    outfile = open(output_file_path, "w")
    regex = '(?<=\[err\]:F-)(\w*).*(Segmentation fault at )(\w*)(.*)'
    lines = infile.readlines()
    line_iter = iter(lines)
    for line in line_iter:
        search = re.search(regex, line)
        if search:
            result = ['PID:' + search.group(1),
                      'SF_AT:' + search.group(3),
                      'SF_TEXT:' + search.group(4)]
            for i in range(0, 4):
                next_line = next(line_iter)
                result.append(re.search('Dump: (.*)', next_line).group(1))
            for result_line in result:
                outfile.write(result_line + '\n')
            outfile.write('\n')
    infile.close()
    outfile.close()
