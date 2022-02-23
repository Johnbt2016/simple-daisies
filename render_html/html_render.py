import base64
import markdown as md
import pickle

class HTMLDoc:
	def __init__(self):
		self.markdown = ''
		self.html = None

	def add_text(self, text):
		self.markdown += text
		self.markdown += '\n'

	def add_bytestring_image(self, bytestring, alt_text = 'alt_text'):
		image_string = '![' + alt_text + '](data:image/png;base64,' + bytestring + ')'
		self.markdown += image_string
		self.markdown += '\n'

	def add_image(self, image, alt_text = 'alt_text'):
		image_string = '![' + alt_text + '](' + image + ')'
		self.markdown += image_string
		self.markdown += '\n'

	def add_css(self, css_file):
		css_string = '<html>\n<head>\n<link rel=\"stylesheet\" href=\"' + css_file + '\">\n</head>'
		self.html = css_string + self.html
		self.html += '</html>'

	def to_html(self):
		self.html = md.markdown(self.markdown)

def format_output(bytestring_image, text):


	style = '''<html><head>
			<style>
				* {
				font-family: 'Roboto', sans-serif;
				}
				h1 {
				text-align: center;
				}
				p {
				text-align: left;
				}
			</style>
			</head>
			'''

	doc = HTMLDoc()
	doc.add_text(text)
	doc.add_bytestring_image(bytestring_image)
	doc.to_html()
	doc.html = style + doc.html
	doc.html += '</html'
	# doc.add_css("styling.css")

	return pickle.dumps(doc.html)
