
from distutils.core import setup
setup(
  name = 'InquestLabs',         
  packages = ['InquestLabs'],   
  version = '0.1',      
  license='MIT',        
  description = 'Python Wrapper for the InQuest Labs API',  
  author = 'Adam Musciano',                   
  author_email = 'amusciano@inquest.net',      
  url = 'inquest.net',   
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',   
  keywords = [],   
  install_requires=[            
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)