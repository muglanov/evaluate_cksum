#!/usr/bin/python
# coding: utf-8

import sys
import os
from commands import getoutput

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
    print u"Не указаны исключенные дииректории"

result = []
for path in eval_dirs:
    if not path:
        print u"Каталог не указан!".format(path)
        continue
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            if dirpath in exclude_dirs:
                continue
            for filename in filenames:
                full_file_path = os.path.join(dirpath, filename)
                if getoutput('ls -l {}'.format(full_file_path)).startswith('l'):
                    print('{} - символьная ссылка'.format(full_file_path))
                else:
                    cksum_eval_res = unicode(getoutput('cksum {}'.format(full_file_path)), 'utf-8')
                    cksum = cksum_eval_res if u'Отказано в доступе' in cksum_eval_res else cksum_eval_res.split()[0]
                    result_line = '{} {}'.format(full_file_path, cksum)
                    print result_line
                    result.append(result_line + '\n')
    elif os.path.isfile(path):
        if getoutput('ls -l {}'.format(full_file_path)).startswith('l'):
            print('{} - символьная ссылка'.format(full_file_path))
        else:
            cksum_eval_res = unicode(getoutput('cksum {}'.format(path)), 'utf-8')
            cksum = cksum_eval_res if u'Отказано в доступе' in cksum_eval_res else cksum_eval_res.split()[0]
            result_line = '{} {}'.format(path, cksum)
            print result_line
            result.append(result_line + '\n')
    else:
        print u'Путь {} не существует'.format(path)

with open(result_file_path, 'w') as cksum_txt:
    cksum_txt.writelines(result)
    print u'Создан', result_file_path
