# encoding: utf-8
#!/usr/bin/env python
import sys
import os
from subprocess import call
import json
import warnings
import six

from django.core.management import execute_from_command_line

#warnings.simplefilter('default', DeprecationWarning)
#warnings.simplefilter('default', PendingDeprecationWarning)

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),  'evalapi_bee')
PROJ_DIR = os.path.dirname(BASE_DIR)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

dump_models = [
    # 通过查询条件配置需要load的数据，查询语法同Django Model

    {'model': 'deal_records.CarDealHistory', 'query': {'model_detail_slug': ['4805_ah'], 'city': '成都', 'price__isnull': False}},
    {'model': 'deal_records.CarDealHistoryStatatics', 'query': {'model_slug__in': ['qirui-qq3'], 'city': '成都'}},
    {'model': 'category.ModelDetail', 'query': {'global_slug__in': ['qirui-qq3']}},
    {'model': 'category.Category', 'query': {'slug__in': ['qirui-qq3']}},
    {'model': 'general.City'},
    # {'model': 'gpj_evaluation.EvaluationBasePrice', 'query': {'city__in': [274], 'model__in': ['audi-a4']}}
]


def dumpdata():
    """
    根据dump_models的配置从生产数据库中load测试数据
    如果已经存在fixture则不再进行loading操作
    """
    target = os.path.join(BASE_DIR, '.dumpdata')
    fixture_path = os.path.join(BASE_DIR, 'dj_fixture.json')

    try:
        os.stat(fixture_path)
    except OSError:
        pass
    else:
        six.print_('[INFO] dj_fixture already exists,dumping data operation was skipped.')
        return

    try:
        os.stat(target)
    except OSError:
        os.mkdir(target)

    manage_file = os.path.join(PROJ_DIR, 'manage.py')
    print(manage_file)
    prefix = ['python', manage_file, 'dump_object']
    for item in dump_models:
        suffix = ['--settings=evalapi_bee.settings.dev', '--no-follow']
        with open(os.path.join(target, 'item_%d.json' % dump_models.index(item)), 'w') as f:
            sub = list()
            model = [item.get('model')]
            query = item.get('query')
            if query:
                sub += ['--query', json.dumps(query)]
            else:
                model.append("*")
            finall_cmd = prefix + model + sub + suffix
            six.print_(' '.join(finall_cmd))
            call(finall_cmd, stdout=f)
    # merge all these data.json to a single file named dj_fixture.json
    merge_cmd = ['python', manage_file, 'merge_fixtures'] + [os.path.join(target, 'item_%d.json' %
                                                                          dump_models.index(item))
                                                                          for item in dump_models]
    with open(fixture_path, 'w') as f:
        call(merge_cmd, stdout=f)


def runtests():
    if sys.argv[1:]:
        argv = sys.argv[:1] + ['test'] + sys.argv[1:] + ['--settings=evalapi_bee.settings.unittest_settings']
    else:
        argv = sys.argv[:1] + ['test'] + ['evalapi', 'deal_records'] + ['--settings=evalapi_bee.settings.unittest_settings']

    execute_from_command_line(argv)


if __name__ == '__main__':
    """清空.dumpdata目录可以重新生成fixture: rm -rf .dumpdata"""
    try:
        dumpdata()
    except Exception:
        sys.exit(1)
    runtests()
