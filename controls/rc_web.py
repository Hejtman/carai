from http.server import BaseHTTPRequestHandler
from lib.utils import who


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
    actions_kwargs = {'duration': 1, 'priority': 1000, 'justification': 'Direct Web Action.', 'same_actions_limit': 5, 'abort_previous': True}

    def _send_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html;charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self._send_headers()
        self.wfile.write(bytes(self.page, 'utf-8'))

    def do_POST(self):
        post_data = self.rfile.read(int(self.headers.get('Content-Length'))).decode('utf-8')
        data = post_data.split('=', 1)[0]

        try:
            self._control.perform_action(action=data, origin=self, **self.actions_kwargs)
        except ValueError:
            try:
                self._control.reverse_component_state(component=data)
            except ValueError:
                self._control.rc.logger.error(f'{who(self)}: Do not know what this is about: {data}')

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
{''.join([f'<tr>'
          f'<td><input type="submit" id="{c.__class__.__name__}" onmousedown="mousedown(id)" value="{c.__class__.__name__}"/></td><td>{c.state}</td>' + 
          "".join([f'<td><input type="submit" id="{value}" onmousedown="mousedown(id)" value="{key}"/></td>' for key, value in c.actions.items()]) + 
          f'</tr>' for c in self._control.components])}
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
        pages = {
            '': self.home_page,
            'COMPONENTS': f'<html><head>{self.META}<title>COMPONENTS</title></head><body>{self.JS}{self.components}</body></html>',
            'RC': f'<html><head>{self.CSS}{self.META}<title>RC</title></head><body>{self.JS}{self.rc}</body></html>',
        }
        return pages.get(sub_page, f'<html><head><title>ERROR</title></head><body>404 PAGE "{self.path}" NOT FOUND!</body></html>')

# TODO: buttons
