from distutils.core import setup

setup(
    name='studyFlash',
    version='1.0.1',
    description="Learning flashcards inside your terminal",
    author="Alone2",
    author_email="contact@asinz.ch",
    url="https://github.com/Alone2/studyFlash",
    packages=['studyFlash'],
    scripts=['scripts/studyflash', 'scripts/studyflash-quizlet']
)
