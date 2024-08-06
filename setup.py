from setuptools import setup, find_packages

setup(
    name='career_counsellor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'openai==1.40.0',
        'gradio==4.40.0',
        'python-dotenv==1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'career-counsellor=career_counsellor.app:create_interface'
        ],
    },
    author='Corey Sullivan',
    author_email='coreypsullivan@gmail.com',
    description='A career counselling application using the OpenAI API and Gradio.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cpsullivan/career-coach.git',  # Update with your repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
