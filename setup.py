from distutils.core import setup

setup(
    name='studyFlash',
    data_files = [
        ('man/man1', ['STUDYFLASH.1'])
    ],
    version='1.1.0',
    description="Learning flashcards inside your terminal",
    author="Alone2",
    author_email="contact@asinz.ch",
    url="https://github.com/Alone2/studyFlash",
    packages=['studyFlash'],
    scripts=['scripts/studyflash', 'scripts/studyflash-quizlet']
)
