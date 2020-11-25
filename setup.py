from setuptools import setup

package_name = 'raspi_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rok',
    maintainer_email='r.pahic@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['service = raspi_ros.service_tool_manager:main',
        'tool_service = raspi_ros.service_tool:main',
        'client = raspi_ros.client_member_function:main',
        ],
    },
)
