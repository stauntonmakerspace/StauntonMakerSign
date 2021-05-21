from setuptools import setup

setup(name='makersign',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/stauntonmakerspace/StauntonMakerSign',
      author='Nile Walker',
      author_email='nilezwalker@gmail.com',
      license='MIT',
      packages=['makersign'],
      install_requires=[
          'pygame',
          'pyserial'
      ],
      zip_safe=False)