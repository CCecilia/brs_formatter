from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='brs-formatter',
      version='0.1',
      description='Formats brightsript files for Roku development.',
      long_description=readme(),
      classifiers=[
            'Intended Audience :: Developers'
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Zope',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Utilities'
      ],
      keywords='brightscript brs Roku',
      url='http://github.com/storborg/funniest',
      author='Christian Cecilia',
      author_email='christian@fubo.tv',
      license='MIT',
      packages=[],
      include_package_data=True,
      zip_safe=False)
