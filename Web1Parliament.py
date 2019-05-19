import os
import time
import datetime

from driver_builder import DriverBuilder
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import shutil


class Web1Parliament:

	def __init__(self):
		self.download_dir = os.path.join(
			os.path.dirname(os.path.abspath(__file__)), 'NewsPapers')
		driver_builder = DriverBuilder()
		self.driver = driver_builder.get_driver(download_location=self.download_dir)
		self.start_url = 'https://srv-web1.parliament.gr/library.asp?item=40200&seg='

	def get_newspaper_titles(self):
		self.driver.get(self.start_url)
		container = self.driver.find_elements_by_tag_name('option')#'//*[@name="seg"]')
		values, titles = [], []
		for option in container[1:]:
			value = option.get_attribute('value')
			title = option.get_attribute('innerHTML')
			title = title.replace('/', '-')
			values.append(value)
			titles.append(title)
		return values, titles

	def open_newspaper(self, value):
		#self.select_option(xpath=menu_xpath, by=value, value_or_text=value)
		#print (value)
		#time.sleep(10)
		submit_btn = self.driver.find_element_by_xpath('//*[@type="submit"]')
		doc_base_url = self.start_url.replace('library', 'display_doc')
		#time.sleep(10)
		#submit_btn.click()
		newspaper_url = doc_base_url + value
		self.driver.get(newspaper_url)
		#self.switch_to_tab(tabnum=1)

	def select_option(self, xpath, by, value_or_text):
		select = Select(self.driver.find_element_by_xpath(xpath))
		if by == 'text':
			select.select_by_visible_text(value_or_text)
		elif by == 'value':
			select.select_by_value(value_or_text)

	def switch2frame(self, xpath):
		self.driver.switch_to.frame(self.driver.find_element_by_xpath(xpath))

	def wait_for_pageload(self, keywords, timeout=20, msg=True):
		starttime = datetime.datetime.now()
		timeout = datetime.timedelta(seconds=timeout)
		while True:
			try:
				html = self.driver.find_element_by_xpath('/html').get_attribute('outerHTML')
				if any(kwd in html for kwd in keywords):
					break
				elif datetime.datetime.now() > starttime + timeout:
					if msg == True:
						print ('timed out')
					break
			except Exception as e:
				pass

	def switch_to_tab(self, tabnum):
		self.driver.switch_to.window(self.driver.window_handles[tabnum])

	def download_newspapers(self, title):
		#self.wait_for_pageload(keywords=['open-button'])
		self.switch2frame('/html/frameset/frame[1]')
		pages = self.driver.find_elements_by_tag_name('option')
		values = [x.get_attribute('value') for x in pages]
		current_url = self.driver.current_url
		counter = 1
		for value in values:
			self.download_page(title, value, counter)
			self.restart_driver(current_url)
			self.switch2frame('/html/frameset/frame[1]')
			counter += 1
		self.driver.close()

	def download_page(self, title, value, counter):	
		self.select_option(xpath='//*[@id="lpages"]', by='value', value_or_text=value)
		self.driver.switch_to.default_content()
		self.switch2frame('//*[@id="middle"]')
		self.wait_for_pageload(keywords=['Open', 'open-button'])
		download_btn = self.driver.find_element_by_xpath('//*[@id="open-button"]')
		download_btn.click()
		self.wait4download(directory=self.download_dir)
		self.move_file(move_to=title, counter=counter)
		self.driver.switch_to.default_content()
		self.switch2frame('/html/frameset/frame[1]')

	def wait4download(self, directory, timeout=30):
		starttime = datetime.datetime.now()
		timeout = datetime.timedelta(seconds=timeout)
		while True:
			current_filecount = len(os.listdir(directory))
			folder = os.listdir(directory)
			str_folder = ''.join(folder)
			if 'crdownload' not in str_folder and '.pdf' in str_folder:
				return True
			elif datetime.datetime.now() > starttime + timeout:
				if msg == True:
					print ('timed out')
				return False

	def move_file(self, move_to, counter):
		filename = [x for x in os.listdir(self.download_dir) if '.pdf' in x][0]
		new_filename = '{}.pdf'.format(counter)
		os.rename(filename, new_filename)
		inpath = os.path.join(self.download_dir, new_filename)
		outpath = os.path.join(self.download_dir, move_to)
		shutil.move(inpath, outpath)


	def restart_driver(self, url):
		self.driver.quit()
		self.driver = self.driver_builder.get_driver(self.download_dir, headless=False)
		self.driver.get(url)

	def make_dirs(self, titles):
		try:
			os.chdir(self.download_dir)
			for title in titles:
				os.mkdir(title)
		except FileExistsError:
			pass

	def main(self):
		values, titles = self.get_newspaper_titles()
		self.make_dirs(titles)
		for i in range(1, len(values)):
			print (titles[i])
			self.open_newspaper(values[i])
			self.download_newspapers(titles[i])
			self.restart_driver(url=self.start_url)


if __name__ == "__main__":
	scraper = Web1Parliament()
	scraper.main()