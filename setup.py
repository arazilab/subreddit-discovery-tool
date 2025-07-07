from setuptools import setup, find_packages

setup(
    name='subreddit_finder',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'openai',  # if needed
    ],
    description='Tool to find and filter Reddit subreddits using Arctic Shift and OpenAI relevance agent.',
    author='Your Name',
    author_email='your@email.com',
    python_requires='>=3.7',
)
