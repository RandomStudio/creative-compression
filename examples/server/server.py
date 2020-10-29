from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
	def do_OPTIONS(self):
		self.send_response(200, "ok")
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()

	def do_GET(self):
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET')
		self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
		return super(CORSRequestHandler, self).end_headers()


httpd = HTTPServer(('127.0.0.1', 8000), CORSRequestHandler)
httpd.serve_forever()