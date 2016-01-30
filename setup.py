from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# Inspired by the example at https://pytest.org/latest/goodpractises.html
class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests','-w','tests'])


setup(name='SwiftFormat',
      author='Ignacio Calderon',
      description='A Swift parser and formatter',
      url="http://github.com/kronenthaler/swift-format",
      version='1.3',
      license='BSD License',
#      packages=find_packages(exclude=['tests']),
      setup_requires=['nose', 'coverage'],
      cmdclass={'test': NoseTestCommand},
)
