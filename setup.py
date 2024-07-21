from setuptools import setup, find_packages

setup(
    name='GitFollowBot',
    version='1.0.3',
    author='Errahum',
    description='A bot to follow and unfollow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Errahum/GitFollowBot',
    packages=find_packages(),
    install_requires=[
        'time',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'GitFollowBot=main_console_follow_unfollow:main_console_follow_unfollow',
        ],
    },
    include_package_data=True,
    license='MIT',
)
