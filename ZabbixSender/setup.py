from setuptools import setup, find_packages

setup(name='ZabbixSender',
      version=__import__('ZabbixSender').__version__,
      description='Send data to Zabbix',
      author='Takanori Suzuki',
      url='https://github.com/BlueSkyDetector/code-snippet/tree/master/ZabbixSender',
      py_modules=['ZabbixSender'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: Do What The Fuck You Want To Public License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ]
)
