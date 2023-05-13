from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_payment_gateways/__init__.py
from frappe_payment_gateways import __version__ as version

setup(
	name="frappe_payment_gateways",
	version=version,
	description="Frappe/ERPNext payment gateways for Paystack, Flutter, Okra  and Many more.",
	author="Anthony C. Emmanuel",
	author_email="mymi14s@hotmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
