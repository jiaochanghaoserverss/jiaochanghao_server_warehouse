# -*- coding: utf-8 -*-

'''
@brief: 脚本配置默认环境
'''

class ConfigClass(object):
    def __init__(self, config):
        self._conf = config

    def __getattr__(self, key):
        return self._conf.get(key, None)
        # try:
        #     return self._conf[key]
        # except KeyError:
        #     return super(ConfigClass, self).__getattr__(key)

    def __setattr__(self, key, value):
        raise Exception('Cannot set value into config')


def init_venv(usage, parser_options=None):
    '''
    parser_options: (
        (['-v', '--venv'], {'dest': 'venv'}),
        (['-c', '--config'], dict(dest='config')),
    )
    '''
    import os
    from optparse import OptionParser

    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--venv", dest="venv", help="python virtual enviroment path", default="")

    parser_options = parser_options or []
    for opt in parser_options:
        args = opt[0]
        kwargs = opt[1]
        parser.add_option(*args, **kwargs)

    (options, args) = parser.parse_args()

    os.system('source ~/.bashrc')
    if options.venv:
        # use python in virtual env
        activate_file = os.path.join(options.venv, 'bin/activate_this.py')
        exec(compile(open(activate_file).read(), activate_file, 'exec'), dict(__file__=activate_file))
    else:
        print('python virtual environment not provided')

    return options


def init_django_venv(usage, parser_options=None):
    '''
    例子: /usr/local/bin/python /home/webui/scripts/stats/lesson_stats.py -c conf.scripts.prd
    '''

    import os
    import sys
    import importlib
    from optparse import OptionParser

    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="config", help="django脚本配置", default="")

    parser_options = parser_options or []
    for opt in parser_options:
        args = opt[0]
        kwargs = opt[1]
        parser.add_option(*args, **kwargs)

    (options, args) = parser.parse_args()
    if not options.config:
        print('缺少配置文件')
        exit(-1)

    configModule = importlib.import_module(options.config)
    conf = configModule.Config

    if not conf.get('settings'):
        print('缺少django配置')
        exit(-1)

    os.system('source ~/.bashrc')
    if conf.get('venv'):
        # 设置python venv
        activate_file = os.path.join(conf['venv'], 'bin/activate_this.py')
        exec(compile(open(activate_file).read(), activate_file, 'exec'), dict(__file__=activate_file))
    if conf.get('root'):
        # 设置django根目录
        sys.path.append(conf['root'])

    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", conf['settings'])

    import django
    django.setup()

    return options, conf


