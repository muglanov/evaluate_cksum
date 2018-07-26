#!/usr/bin/python3
# coding: utf-8

import sys
import os
from subprocess import check_output

result_file_path = os.path.join(os.getcwd(), 'cksum.txt')
args_count = len(sys.argv)
args = sys.argv[1:]
if ':' not in args:
    eval_dirs = args
    exclude_dirs = []
else:
    eval_dir_args, exclude_dir_args = ' '.join(args).split(':')
    eval_dirs = eval_dir_args.split()
    exclude_dirs = exclude_dir_args.split()
if not exclude_dirs:
    print('Не указаны исключенные дииректории')

result = []
for path in eval_dirs:
    if not path:
        print('Каталог не указан!'.format(path))
        continue
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            if dirpath in exclude_dirs:
                continue
            ls_res = str(check_output('ls -l {}'.format(dirpath), shell=True), 'utf-8')
            for filename in filenames:
                full_file_path = os.path.join(dirpath, filename)
                if str(check_output('ls -l {}'.format(full_file_path), shell=True), 'utf-8').startswith('l'):
                    print('{} - символьная ссылка'.format(full_file_path))
                else:
                    cksum_eval_res = str(check_output('cksum {}'.format(full_file_path), shell=True), 'utf-8')
                    cksum = cksum_eval_res if 'Отказано в доступе' in cksum_eval_res else cksum_eval_res.split()[0]
                    result_line = '{} {}'.format(full_file_path, cksum)
                    print(result_line)
                    result.append(result_line + '\n')
    elif os.path.isfile(path):
        if str(check_output('ls -l {}'.format(path), shell=True), 'utf-8').startswith('l'):
            print('{} - символьная ссылка'.format(path))
        else:
            cksum_eval_res = str(check_output('cksum {}'.format(path), shell=True), 'utf-8')
            cksum = cksum_eval_res if 'Отказано в доступе' in cksum_eval_res else cksum_eval_res.split()[0]
            result_line = '{} {}'.format(path, cksum)
            print(result_line)
            result.append(result_line + '\n')
    else:
        print('Путь {} не существует'.format(path))

with open(result_file_path, 'w') as cksum_txt:
    cksum_txt.writelines(result)
    print('Создан', result_file_path)
