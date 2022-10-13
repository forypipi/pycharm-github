from setuptools import setup, find_packages

setup(
    name='BloomFilter',
    packages=find_packages(),
    version='0.0.3',
    install_requires=[          # 添加了依赖的 package
        'mmh3==3.0.0',
        'math',
        'bitarray',
        'copy'
    ],
    author="FOR",
    author_email="forypipi@163.com",
    description="This is a package for bloom filter. "
                "A Bloom filter is a space-efficient probabilistic data structure, "
                "conceived by Burton Howard Bloom in 1970, "
                "that is used to test whether an element is a member of a set.",
    keywords="bloom filter, bitarray",
    url="https://github.com/forypipi/Big-Data-Algorithm-Application.git",   # project home page, if any
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)