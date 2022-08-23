from http.server import BaseHTTPRequestHandler


class Web(BaseHTTPRequestHandler):
    _control = None  # set externally before instantiation
    # FIXME: suppress double-click behaviour
    CSS = '''<style>
    table { border: 1px solid black; }
    tr, input {-webkit-user-select: none;}
    </style>'''
    META = '<meta http-equiv="refresh" content="10">'  # FIXME: reload only img from camera + status or iframe it on different page than RC keyboard!
    JS = '''<script>
      function mousedown(id) {{ var xhr = new XMLHttpRequest(); xhr.open("POST", "", true); xhr.send(id+"=PRESSED"); }}
      function mouseup(id)   {{ var xhr = new XMLHttpRequest(); xhr.open("POST", "", true); xhr.send(id+"=RELEASED"); }}
    </script>'''

    def _send_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html;charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self._send_headers()
        self.wfile.write(bytes(self.page, 'utf-8'))

    def do_POST(self):
        post_data = self.rfile.read(int(self.headers.get('Content-Length'))).decode('utf-8')
        print(post_data.split('=', 1))
        self._send_headers()
        self.wfile.write(bytes(self.page, 'utf-8'))

    def log_request(self, code='-', size='-'):
        pass  # to not pollute terminal with each http request (happens every second - see META)

    @property
    def components(self) -> str:
        # TODO: turn on/off component
        return f'''
<table>
<tr><th colspan="2"><a href="{'COMPONENTS' if self.path == '/' else '/'}">COMPONENTS</a></th></tr>
{''.join([f'<tr><td>{c.__class__.__name__}</td><td>{c.state}</td></tr>' for c in self._control.components])}
<tr><td>{self._control.__class__.__name__}</td><td>{self._control.state}</td></tr>
</table>'''

    @property
    def rc(self) -> str:
        return f'''
<table>
  <tr><th colspan="7"><a href="{'RC' if self.path == '/' else '/'}">RC</a></th></tr>
  <tr><td><input type='submit' id="MOVE_FORWARD"  onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="▲"/></td>
      <td>                                                                                                       </td>
      <td><input type='submit' id="MOVE_FORWARD"  onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="▲"/></td></tr>

  <tr><td><input type='submit' id="MOVE_LEFT"     onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="◀"/></td>
      <td><input type='submit' id="MOVE_STOP"     onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="⏹"/></td>
      <td><input type='submit' id="MOVE_RIGHT"    onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="▶"/></td></tr>

  <tr><td><input type='submit' id="MOVE_BACKWARD" onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="▼"/></td>
      <td>                                                                                                       </td>
      <td><input type='submit' id="MOVE_BACKWARD" onmousedown="mousedown(id)" onmouseup="mouseup(id)" value="▼"/></td></tr>
</table>
'''

    @property
    def home_page(self) -> str:
        return f"""
<html><head>{self.CSS}{self.META}<title>Remote Control</title></head>
<body>
{self.JS}
{self.components}
{self.rc}
TODO: CAMERA IMAGE
TODO: CONSOLE LOG
</body></html>
"""

    @property
    def page(self) -> str:
        sub_page = self.path.rsplit('/', maxsplit=1)[-1]
        match sub_page:
            case '':
                return self.home_page
            case 'COMPONENTS':
                return f'<html><head>{self.META}<title>COMPONENTS</title></head><body>{self.JS}{self.components}</body></html>'
            case 'RC':
                return f'<html><head>{self.CSS}{self.META}<title>RC</title></head><body>{self.JS}{self.rc}</body></html>'
            case _:
                return f'<html><head><title>ERROR</title></head><body>404 PAGE "{self.path}" NOT FOUND!</body></html>'

# TODO: buttons
