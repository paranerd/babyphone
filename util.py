import os
import time
import datetime
import shutil
import hashlib
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def remove(path):
	if os.path.isfile(path):
		os.remove(path)
	else:
		shutil.rmtree(path)

def create_folder(path):
	"""
	Create folder if not exists

	@param string path Absolute path to folder
	@return string
	"""
	if not os.path.exists(path):
		os.makedirs(path)
		return path

def remove_folder(path):
	"""
	Remove folder recursively

	@param string path
	"""
	shutil.rmtree(path)

def md5(string):
	"""
	Calculate MD5-Checksum of string

	@param string string
	@return string
	"""
	m = hashlib.md5()
	m.update(string.encode('utf-8'))
	return m.hexdigest()

def get_project_path():
	"""
	Return absolute path of project folder

	@return string
	"""
	return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))