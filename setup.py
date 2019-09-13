from setuptools import setup,find_packages

setup(
    name='x2t',
    version='0.0.1.dev1',
    description="convert xls table to tex code",
    url='https://github.com/sailist/LatexTool',
    author='sailist',
    author_email='sailist@outlook.com',
    license='MIT',
    include_package_data = True,
    install_requires = [
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='xlsx tex table',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'x2t = LatexTool.totable:main'
        ]
      },
)