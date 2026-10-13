"""HELIX BOTIC - serves the dashboard.
Run locally:   python index.py   (then open http://localhost:8000 in Chrome)
Vercel/WSGI:   exposes `app` (WSGI) so it also works with gunicorn / Vercel Python.
Only the Python standard library is used.
"""
import base64, os
from wsgiref.simple_server import make_server

_B64 = """
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj48aGVhZD48bWV0YSBjaGFyc2V0PSJ1dGYtOCI+CjxtZXRhIG5hbWU9InZp
ZXdwb3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsaW5pdGlhbC1zY2FsZT0xLHZpZXdwb3J0LWZpdD1jb3ZlciI+Cjx0
aXRsZT5IRUxJWCBCT1RJQzwvdGl0bGU+CjxzdHlsZT4KOnJvb3R7LS1iZzojMDUwNjBmOy0tbGluZTojZmZmZmZmMTQ7LS1jOiM1
ZWVhZDQ7LS12OiM4YjVjZjY7LS1nOiMzZmYyYTA7LS1yOiNmZjU1Nzc7LS15OiNmNWM0NmI7LS10OiNmNGYyZmY7LS1tOiM4Zjkz
Yjh9Cip7Ym94LXNpemluZzpib3JkZXItYm94O21hcmdpbjowOy13ZWJraXQtdGFwLWhpZ2hsaWdodC1jb2xvcjp0cmFuc3BhcmVu
dH0KYm9keXtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChjaXJjbGUgYXQgMTAlIC04JSwjMmIxNjcwIDAsdHJhbnNwYXJlbnQg
NDIlKSxyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDEwMCUgNiUsIzBhNGY2MyAwLHRyYW5zcGFyZW50IDM4JSksdmFyKC0tYmcp
O2NvbG9yOnZhcigtLXQpO2ZvbnQ6MTVweC8xLjQgIlNGIFBybyBEaXNwbGF5IiwiU2Vnb2UgVUkiLHN5c3RlbS11aSxzYW5zLXNl
cmlmO21pbi1oZWlnaHQ6MTAwdmg7cGFkZGluZzplbnYoc2FmZS1hcmVhLWluc2V0LXRvcCkgMCA5NnB4fQoud3ttYXgtd2lkdGg6
NDgwcHg7bWFyZ2luOjAgYXV0bztwYWRkaW5nOjE0cHh9Ci5sb2dve2Rpc3BsYXk6ZmxleDtnYXA6MTBweDthbGlnbi1pdGVtczpj
ZW50ZXJ9Ci5oZXh7d2lkdGg6MzhweDtoZWlnaHQ6MzhweDtib3JkZXItcmFkaXVzOjEycHg7YmFja2dyb3VuZDpsaW5lYXItZ3Jh
ZGllbnQoMTM1ZGVnLHZhcigtLXYpLHZhcigtLWMpKTtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXMtY2VudGVyO2p1c3RpZnktY29u
dGVudDpjZW50ZXI7Zm9udC13ZWlnaHQ6OTAwO2JveC1zaGFkb3c6MCAwIDIycHggIzhiNWNmNjg4fQpoMXtmb250LXNpemU6MTlw
eDtsZXR0ZXItc3BhY2luZzo0cHg7Zm9udC13ZWlnaHQ6ODAwfQouc3Vie2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxMnB4fQou
Y2FyZHtiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCgxNjBkZWcsI2ZmZmZmZjBkLCNmZmZmZmYwNCk7Ym9yZGVyOjFweCBzb2xp
ZCB2YXIoLS1saW5lKTtib3JkZXItcmFkaXVzOjIycHg7cGFkZGluZzoxNnB4O21hcmdpbi10b3A6MTJweDtiYWNrZHJvcC1maWx0
ZXI6Ymx1cigxNHB4KTtib3gtc2hhZG93OjAgMTBweCA0MHB4ICMwMDAwMDA2Nn0KLnJvd3tkaXNwbGF5OmZsZXg7Z2FwOjhweDth
bGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OnNwYWNlLWJldHdlZW59Ci5zZWd7ZGlzcGxheTpmbGV4O2dhcDo2cHg7
ZmxleC13cmFwOndyYXA7bWFyZ2luLXRvcDo4cHh9Ci5zZWcgYnV0dG9uLGlucHV0e2JhY2tncm91bmQ6I2ZmZmZmZjBhO2JvcmRl
cjoxcHggc29saWQgdmFyKC0tbGluZSk7Y29sb3I6dmFyKC0tdCk7Ym9yZGVyLXJhZGl1czoxMnB4O3BhZGRpbmc6OHB4IDEycHg7
Zm9udC1zaXplOjEzcHh9Ci5zZWcgYnV0dG9uLm9ue2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzNWRlZyx2YXIoLS12KSwj
MGVhNWI3KTtib3JkZXItY29sb3I6dHJhbnNwYXJlbnQ7Ym94LXNoYWRvdzowIDRweCAxNnB4ICM4YjVjZjY2Nn0KaW5wdXR7d2lk
dGg6MTAwJTttYXJnaW4tdG9wOjhweH0KbGFiZWx7Y29sb3I6dmFyKC0tbSk7Zm9udC1zaXplOjEycHh9Ci5iaWd7d2lkdGg6MTAw
JTttYXJnaW4tdG9wOjE0cHg7cGFkZGluZzoxNnB4O2JvcmRlcjowO2JvcmRlci1yYWRpdXM6MTZweDtmb250LXNpemU6MTZweDtm
b250LXdlaWdodDo3MDA7bGV0dGVyLXNwYWNpbmc6LjVweDtjb2xvcjojZmZmO2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEz
NWRlZyx2YXIoLS12KSwjMGVhNWI3KTtib3gtc2hhZG93OjAgOHB4IDI4cHggIzhiNWNmNjY2fQouYmlnLnN0b3B7YmFja2dyb3Vu
ZDpsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLCNiZTEyM2MsdmFyKC0tcikpO2JveC1zaGFkb3c6MCA4cHggMjhweCAjZmY1NTc3NTV9
Ci5lbmd7cG9zaXRpb246cmVsYXRpdmU7d2lkdGg6MjQwcHg7aGVpZ2h0OjI0MHB4O21hcmdpbjo2cHggYXV0bztjdXJzb3I6cG9p
bnRlcn0KLmVuZyBzdmd7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MH0KLnNwaW57dHJhbnNmb3JtLW9yaWdpbjoxMjBweCAxMjBw
eH0KLnNjYW5uaW5nIC5zcGlue2FuaW1hdGlvbjpzcCAxLjZzIGxpbmVhciBpbmZpbml0ZX0KQGtleWZyYW1lcyBzcHt0b3t0cmFu
c2Zvcm06cm90YXRlKDM2MGRlZyl9fQouY3Rye3Bvc2l0aW9uOmFic29sdXRlO2luc2V0OjM0cHg7Ym9yZGVyLXJhZGl1czo1MCU7
ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRl
cjt0ZXh0LWFsaWduOmNlbnRlcjtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChjaXJjbGUsIzFhMTQ1MCwjMGEwYTIyIDcyJSl9
Ci5pY3tmb250LXNpemU6NDRweDtsaW5lLWhlaWdodDoxfQouZHtmb250LXNpemU6MjZweDtmb250LXdlaWdodDo4MDA7bWFyZ2lu
LXRvcDoycHh9Ci51cHtjb2xvcjp2YXIoLS1nKX0uZG57Y29sb3I6dmFyKC0tcil9Lm50e2NvbG9yOnZhcigtLXlpfQouZ2xvd3Vw
IC5jdHJ7Ym94LXNoYWRvdzowIDAgNTBweCAjM2ZmMmEwNjYgaW5zZXQsMCAwIDQwcHggIzNmZjJhMDQ0fQouZ2xvd2RuIC5jdHJ7
Ym94LXNoYWRvdzowIDAgNTBweCAjZmY1NTc3NjYgaW5zZXQsMCAwIDQwcHggI2ZmNTU3NzQ0fQoubWluaXtkaXNwbGF5OmZsZXg7
Z2FwOjhweDttYXJnaW4tdG9wOjhweH0KLm1pbmkgZGl2e2ZsZXg6MTtiYWNrZ3JvdW5kOiNmZmZmZmYwODtib3JkZXI6MXB4IHNv
bGlkIHZhcigtLWxpbmUpO2JvcmRlci1yYWRpdXM6MTRweDtwYWRkaW5nOjhweDt0ZXh0LWFsaWduOmNlbnRlcn0KLm1pbmkgYntk
aXNwbGF5OmJsb2NrO2ZvbnQtc2l6ZToxNnB4fQouZ3JpZHtkaXNwbGF5OmdyaWQ7Z3JpZC10ZW1wbGF0ZS1jb2x1bW5zOjFmciAx
ZnI7Z2FwOjEwcHg7bWFyZ2luLXRvcDoxMHB4fQoucGMye2JhY2tncm91bmQ6I2ZmZmZmZjA4O2JvcmRlcjoxcHggc29saWQgdmFy
KC0tbGluZSk7Ym9yZGVyLXJhZGl1czoxNnB4O3BhZGRpbmc6MTFweDtjdXJzb3I6cG9pbnRlcjt0cmFuc2l0aW9uOi4xNXN9Ci5w
ciAyIGJ0bmV3dGVucyBmb250LXNpemU6MTRweH0KLnBjMi5zZWx7Ym9yZGVyLWNvbG9yOnZhcigtLXYpO2JveC1zaGFkb3c6MCAw
IDAgMXB4IHZhcigtLXYpLDAgNnB4IDIwcHggIzhiNWNmNjU1fQoucGMyLnVwe2JvcmRlcC1jb2xvcjp2YXIoLS1nKTtib3gtc2hh
ZG93OjAgMCAwIDFweCB2YXIoLS1nKSwwIDAgMjJweCAjM2ZmMmEwNTV9Ci5wYzIuZG57Ym9yZGVyLWNvbG9yOnZhcigtLXIpO2JveC1z
aGFkb3c6MCAwIDAgMXB4IHZhcigtLXIpLDAgMCAyMnB4ICNmZjU1Nzc1NX0KLmFye2ZvbnQtc2l6ZToyMHB4O2ZvbnQtd2VpZ2h0
OjkwMDthbmltYXRpb246Ym4gMXMgZWFzZS1pbi1vdXQgaW5maW5pdGV9CkBrZXlmcmFtZXMgYm57NTAle3RyYW5zZm9ybTp0cmFu
c2xhdGVZKC0zcHgpfX0KLnN0ZXBzIGRpdntwYWRkaW5nOjVweCAwO2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxNHB4fS5zdGVw
cyAub2t7Y29sb3I6dmFyKC0tdCl9LnN0ZXBzIC5vazphZnRlcntjb250ZW50OiIg4pyTIjtjb2xvcjp2YXIoLS1nKX0KLnRibCBk
aXZ7ZGlzcGxheTpmbGV4O2p1c3RpZnktY29udGVudDpzcGFjZS1iZXR3ZWVuO3BhZGRpbmc6OHB4IDA7Ym9yZGVyLWJvdHRvbTox
cHggc29saWQgdmFyKC0tbGluZSk7Zm9udC1zaXplOjE0cHh9Ci50YWJ7ZGlzcGxheTpub25lfS50YWIub257ZGlzcGxheTpibG9j
a30KbmF2e3Bvc2l0aW9uOmZpeGVkO2JvdHRvbTowO2xlZnQ6MDtyaWdodDowO2Rpc3BsYXk6ZmxleDtiYWNrZ3JvdW5kOiMwODBh
MWNkZDtiYWNrZHJvcC1maWx0ZXI6Ymx1cigxNHB4KTtib3JkZXItdG9wOjFweCBzb2xpZCB2YXIoLS1saW5lKTtwYWRkaW5nLWJv
dHRvbTplbnYoc2FmZS1hcmVhLWluc2V0LWJvdHRvbSl9Cm5hdiBidXR0b257ZmxleDoxO2JhY2tncm91bmQ6MDtib3JkZXI6MDtj
b2xvcjp2YXIoLS1tKTtwYWRkaW5nOjEzcHggMDtmb250LXNpemU6MTJweH0KbmF2IGJ1dHRvbi5vbntjb2xvcjp2YXIoLS1jKX0K
Lndhcm57Zm9udC1zaXplOjExcHg7Y29sb3I6dmFyKC0tbSk7bWFyZ2luLXRvcDoxNHB4fQouYmFkZ2V7Zm9udC1zaXplOjExcHg7
cGFkZGluZzo0cHggMTBweDtib3JkZXItcmFkaXVzOjIwcHg7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1saW5lKTtjb2xvcjp2YXIo
LS15KX0KLmJhZGdlLmxpdmV7Y29sb3I6dmFyKC0tZyl9Ci5zdGF0e2ZvbnQtc2l6ZToyOHB4O2ZvbnQtd2VpZ2h0OjgwMDtjb2xv
cjp2YXIoLS1jKX0KLmhyb3d7Y3Vyc29yOnBvaW50ZXJ9CiNwb3B7cG9zaXRpb246Zml4ZWQ7aW5zZXQ6MDtiYWNrZ3JvdW5kOiMw
MDBjO2Rpc3BsYXk6bm9uZTthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRlcjt6LWluZGV4Ojk7cGFkZGlu
ZzoyMHB4fQojcG9wLm9ue2Rpc3BsYXk6ZmxleH0KLnBje3dpZHRoOjEwMCU7bWF4LXdpZHRoOjM4MHB4O2JhY2tncm91bmQ6bGlu
ZWFyLWdyYWRpZW50KDE2MGRlZywjMjQxYTcwLCMwYjBhMjUpO2JvcmRlcjoxcHggc29saWQgdmFyKC0tdik7Ym9yZGVyLXJhZGl1
czoyNHB4O3BhZGRpbmc6MjJweDt0ZXh0LWFsaWduOmNlbnRlcjtib3gtc2hhZG93OjAgMCA2MHB4ICM4YjVjZjY2Nn0KLnBjIC5k
aXJ7Zm9udC1zaXplOjQ2cHg7Zm9udC13ZWlnaHQ6OTAwO21hcmdpbjo2cHggMH0KLnBjIC50bXtmb250LXNpemU6MzhweDtmb250
LXdlaWdodDdoMDA7Y29sb3I6dmFyKC0tYyk7dGV4dC1zaGFkb3c6MCAwIDE4cHggIzVlZWFkNDk5fQoKYnV0dG9ue3Bvc2l0aW9u
OnJlbGF0aXZlO292ZXJmbG93OmhpZGRlbjt0cmFuc2l0aW9uOnRyYW5zZm9ybSAuMTJzLGJveC1zaGFkb3cgLjJzLGJhY2tncm91
bmQgLjJzfQpidXR0b246YWN0aXZle3RyYW5zZm9ybTpzY2FsZSguOTQpfQoucmlwe3Bvc2l0aW9uOmFic29sdXRlO2JvcmRlci1y
YWRpdXM6NTAlO2JhY2tncm91bmQ6I2ZmZmZmZjU1O3RyYW5zZm9ybTpzY2FsZSgwKTthbmltYXRpb246cnAgLjZzIGVhc2Utb3V0
O3BvaW50ZXItZXZlbnRzOm5vbmV9CkBrZXlmcmFtZXMgcnB7dG97dHJhbnNmb3JtOnNjYWxlKDEpO29wYWNpdHk6MH19CiNnbzpu
b3QoLnN0b3Ape2FuaW1hdGlvbjpiciAyLjRzIGVhc2UtaW4tb3V0IGluZmluaXRlfQpAa2V5ZnJhbWVzIGJyezUwJXtib3gtc2hh
ZG93OjAgOHB4IDQycHggIzIyZDNlZWFhfX0KLnRhYi5vbnthbmltYXRpb246dGluIC4zNXMgZWFzZX0KQGtleWZyYW1lcyB0aW57
ZnJvbXtvcGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTJweCl9fQouY2FyZHthbmltYXRpb246Y2luIC41NXMgZWFzZSBib3Rf
aH0KLnBjYXJkOm50aC1jaGlsZCBudGgtY2hpbGQoMil7YW5pbWF0aW9uLWRlbGF5Oi4wN3N9LmNhcmQ6bnRoLWNoaWxkKDMpe2Fu
aW1hdGlvbi1kZWxheTouMTRzfS5jYXJkOm50aC1jaGlsZCg0KXthbmltYXRpb24tZGVsYXk6LjIxc30KQGtleWZyYW1lcyBjaW57
ZnJvbXtvcGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTZweCkgc2NhbGUoLjk4KX19Ci5wYzI6aG92ZXJ7dHJhbnNmb3Jt
OnRyYW5zbGF0ZVkoLTJweCl9LnBjMjphY3RpdmV7dHJhbnNmb3JtOnNjYWxlKC45NSl9Ci5oZXh7YW5pbWF0aW9uOmh4IDRzIGVh
c2UtaW4tb3V0IGluZmluaXRlfQpAa2V5ZnJhbWVzIGh4ezUwJXtib3gtc2hhZG93OjAgMCAzNHB4ICM1ZWVhZDRhYTt0cmFuc2Zv
cm06cm90YXRlKDhkZWcpfX0KLmVuZy5ndXtjb2xvcjp2YXIoLS1nKX0uZW5nLmdke2NvbG9yOnZhcigtLXIpfQouZW5nLmJ1cnN0
OmFmdGVye2NvbnRlbnQ6IiI7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MjBweDtib3JkZXItcmFkaXVzOjUwJTtib3JkZXI6M3B4
IHNvbGlkIGN1cnJlbnRDb2xvcjthbmltYXRpb246d2F2ZSAuOXMgZWFzZS1vdXQ7cG9pbnrerHRlci1ldmVudHM6bm9uZX0KLmVu
Zy5idXJzdCAjaWMsLmVuZy5idXJzdCAuZHthbmltYXRpb246cG9wIC41NXMgY3ViaWMtYmV6aWVyKC4yLDEuNiwuNCwxKX0KQGtl
eWZyYW1lcyB3YXZle2Zyb217dHJhbnNmb3JtOnNjYWxlKC44KTtvcGFjaXR5Oi45fXRve3RyYW5zZm9ybTpzY2FsZSgxLjQpO29w
YWNpdHk6MH19CkBrZXlmcmFtZXMgcG9we2Zyb217dHJhbnNmb3JtOnNjYWxlKC4zKTtvcGFjaXR5OjB9fQouZW5nLnNoYWtle2Fu
aW1hdGlvbjpzaCAuNXN9CkBrZXlmcmFtZXMgc2h7MjAlLDYwJXt0cmFuc2Zvcm06dHJhbnNsYXRlWCgtOXB4KX00MCUsODAle3Ry
YW5zZm9ybTp0cmFuc2xhdGVYKDlweCl9fQoubGl2ZXtmb250LXNpemU6MTBweDtjb2xvcjp2YXIoLS1nKTttYXJnaW4tbGVmdDo2
cHg7Zm9udC13ZWlnaHQ6NzAwfQoubGl2ZSBpe2Rpc3BsYXk6aW5saW5lLWJsb2NrO3dpZHRoOjdweDtoZWlnaHQ6N3B4O2JvcmRl
ci1yYWRpdXM6NTAlO2JhY2tncm91bmQ6dmFyKC0tZyk7bWFyZ2luLXJpZ2h0OjRweDthbmltYXRpb246cGwgMS4ycyBpbmZpbml0
ZX0KQGtleWZyYW1lcyBwbHs1MCV7b3BhY2l0eTouMjU7dHJhbnNmb3JtOnNjYWxlKDEuNyl9fQouY3B4e2ZvbnQtc2l6ZToyMnB4
O2ZvbnQtd2VpZ2h0OjgwMH0KLmNweC5mdXthbmltYXRpb246ZnUgLjdzfS5jcHguZmR7YW5pbWF0aW9uOmZkIC43c30KQGtleWZy
YW1lcyBmdXswJXtjb2xvcjp2YXIoLS1nKTt0ZXh0LXNoYWRvdzowIDAgMTZweCB2YXIoLS1nKX19CkBrZXlmcmFtZXMgZmR7MCV7
Y29sb3I6dmFyKC0tcik7dGV4dC1zaGFkb3c6MCAwIDE2cHggdmFyKC0tcil9fQouY217cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6
MDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7dGV4dC1hbGlnbjpjZW50ZXI7
cGFkZGluZzoxMnB4O2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxM3B4O2JhY2tncm91bmQ6IzBhMGIxY2NjO2JvcmRlcj1yYWRp
dXM6MTJweH0KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOnJlZHVjZSl7KnthbmltYXRpb246bm9uZSFpbXBvcnRhbnQ7
dHJhbnNpdGlvbjpub25lIWltcG9ydGFudH19CgouY2FyZCxuYXZ7YmFja2Ryb3AtZmlsdGVyOm5vbmUhaW1wb3J0YW50Oy13ZWJr
aXQtYmFja2Ryb3AtZmlsdGVyOm5vbmUhaW1wb3J0YW50fQpuYXZ7YmFja2dyb3VuZDojMDgwYTFjIWltcG9ydGFudH0KLmNhcmR7
Ym94LXNoYWRvdzpub25lIWltcG9ydGFudDthbmltYXRpb246Y2luIC4zNXMgZWFzZSBib3RofQojZ286bm90KC5zdG9wKSwuaGV4
e2FuaW1hdGlvbjpub25lIWltcG9ydGFudH0KCi5vcmJ7cG9zaXRpb246Zml4ZWQ7d2lkdGg6MzQwcHg7aGVpZ2h0OjM0MHB4O2Jv
cmRlci1yYWRpdXM6NTAlO3BvaW50ZXItZXZlbnRzOm5vbmU7ei1pbmRleDotMTtvcGFjaXR5Oi41NX0KLm8xe2JhY2tncm91bmQ6
cmFkaWFsLWdyYWRpZW50KGNpcmNsZSwjN2MzYWVkNjYsdHJhbnNwYXJlbnQgNzAlKTt0b3A6LTgwcHg7bGVmdDotMTAwcHg7
YW5pbWF0aW9uOmZsMSAxOHMgZWFzZS1pbi1vdXQgaW5maW5pdGUgYWx0ZXJuYXRlfQoubzJ7YmFja2dyb3VuZDpyYWRpYWwt
Z3JhZGllbnQoY2lyY2xlLCMwNmI2ZDQ1NSx0cmFuc3BhcmVudCA3MCUpO2JvdHRvbTo2MHB4O3JpZ2h0Oi0xMjBweDthbmltYXRp
b246ZmwyIDIycyBlYXNlLWluLW91dCBpbmZpbml0ZSBhbHRlcm5hdGV9CkBrZXlmcmFtZXMgZmwxe3Rve3RyYW5zZm9ybTp0cmFu
c2xhdGUoMTIwcHgsMTYwcHgpfX0KQGtleWZyYW1lcyBmbDJ7dG97dHJhbnNmb3JtOnRyYW5zbGF0ZSgtMTAwcHgsLTE0MHB4KX19
CiNmeHtwb3NpdGlvbjpmaXhlZDtpbnNldDowO3dpZHRoOjEwMCU7aGVpZ2h0OjEwMCU7cG9pbnRlci1ldmVudHM6bm9uZTt6LWlu
ZGV4Ojh9Ci5zd2VlcHtwb3NpdGlvbjphYnNvbHV0ZTtpbnNldDoxMHB4O2JvcmRlci1yYWRpdXM6NTAlO2JhY2tncm91bmQ6Y29u
aWMtZ3JhZGllbnQoZnJvbSAwZGVnLHRyYW5zcGFyZW50IDAgMjkwZGVnLCM1ZWVhZDQ2NiAzNjBkZWcpO29wYWNpdHk6MDt0cmFu
c2l0aW9uOm9wYWNpdHkgLjNzfQouc2Nhbm5pbmcgLnN3ZWVwe29wYWNpdHk6MTthbmltYXRpb246c3AgMS42cyBsaW5lYXIgaW5m
aW5pdGV9CiNsb2Nre3Bvc2l0aW9uOmZpZ2VkO2luc2V0OjA7ei1pbmRleDoyMDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2Vu
dGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7cGFkZGluZzoyNHB4O2JhY2tncm91bmQ6cmFkaWFsLWdyYWRpZW50KGNpcmNsZSBh
dCAyMCUgMTAlLCMzMzE2N2EsdHJhbnNwYXJlbnQgNTAlKSxyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDkwJSA5MCUsIzA4NTY2
ZSx0cmFuc3BhcmVudCA0NSUpLCMwNTA2MGZ9CiNsb2NrLm91dHthbmltYXRpb246bG91dCAuNjVzIGVhc2UgZm9yd2FyZHN9CkBr
ZXlmcmFtZXMgbG91dHt0b3tvcGFjaXR5OjA7dHJhbnNmb3JtOnNjYWxlKDEuMTUpO3Zpc2liaWxpdHk6aGlkZGVufX0KLmxre3dp
ZHRoOjEwMCU7bWF4LXdpZHRoMzMwcHg7dGV4dC1hbGlnbjpjZW50ZXI7YW5pbWF0aW9uOmNpbiAuN3MgZWFzZSBib3RofQoubGs5
LnNoYWtle2FuaW1hdGlvbjpzaCAuNXN9Ci5sayAuaGV4e3dpZHRoOjc2cHg7aGVpZ2h0Ojc2cHg7bWFyZ2luOjAgYXV0byAxNnB4
O2ZvbnQtc2l6TozMnB4O2JvcmRlci1yYWRpdXM6MjRweDthbmltYXRpb246aHggNHMgZWFzZS1pbi1vdXQgaW5maW5pdGV9Ci5s
ayBoMXttYXJnaW4tYm90dG9tOjRweH0KLmxrIGlucHV0e3RleHQtYWxpZ246Y2VudGVyO2xldHRlci1zcGFjaW5nOjEwcHg7Zm9u
dC1zaXplOjI0cHg7cGFkZGluZzoxNHB4O21hcmdpbi10b3A6MjJweH0KLmxrIGlucHV0OmZvY3Vze291dGxpbmU6MDtib3JkZXIt
Y29sb3I6dmFyKC0tdik7Ym94LXNoYWRvdzowIDAgMCAzcHggIzhiNWNmNjU1fQo8L3N0eWxlPjwvaGVhZD48Ym9keT48ZGl2IGNs
YXNzPSJvcmIgbzEiPjwvZGl2PjxkaXYgY2xhc3M9Im9yYiBvMiI+PC9kaXY+PGNhbnZhcyBpZD0iZngiPjwvY2FudmFzPgo8ZGl2
IGlkPSJsb2NrIj48ZGl2IGNsYXNzPSJsayI+PGRpdiBjbGFzcz0iaGV4Ij5IPC9kaXY+PGgxPkhFTElYIEJPVElDPC9oMT48ZGl2
IGNsYXNzPSJzdWIiPkVudGVyIHlvdXIgYWNjZXNzIGtleSB0byBjb250aW51ZTwvZGl2PjxpbnB1dCBpZD0icHciIHR5cGU9InBh
c3N3b3JkIiBpbnB1dG1vZGU9Im51bWVyaWMiIHBsYWNlaG9sZGVyPSLigKLigKLigKLigKIiIG1heGxlbmd0aD0iMTIiIGF1dG9j
b21wbGV0ZT0ib2ZmIj48YnV0dG9uIGlkPSJsZyIgY2xhc3M9ImJpZyI+VU5MT0NLPC9idXR0b24+PGRpdiBpZD0ibGVyciIgY2xh
c3M9InN1YiIgc3R5bGU9ImNvbG9yOnZhcigtLXIpO21pbi1oZWlnaHQ6MjBweDttYXJnaW4tdG9wOjEwcHgiPjwvZGl2PjwvZGl2
PjwvZGl2Pgo8ZGl2IGNsYXNzPSJ3Ij4KUDxkaXYgY2xhc3M9InJvdyI+PGRpdiBjbGFzcz0ibG9nbyI+PGRpdiBjbGFzcz0iaGV4
Ij5IPC9kaXY+PGRpdj48aDE+SEVMSVggQk9USUM8L2gxPjxkaXYgY2xhc3M9InN1YiI+SW5kaWNhdG9yLWJhc2VkIG1hcmtldCBh
bmFseXNpczwvZGl2PjwvZGl2PjwvZGl2PjxzcGFuIGlkPSJtb2RlIiBjbGFzcz0iYmFkZ2UiPuKAmDwvc3Bhbj48L2Rpdj4KCjxk
aXYgaWQ9InQtZGFzaCIgY2xhc3M9InRhYiBvbiI+CiA8ZGl2IGNsYXNzPSJjYXJkIj4KICA8bGFiZWw+VGltZWZyYW1lPC9sYWJl
bD4KICA8ZGl2IGNsYXNzPSJzZWciIGlkPSJ0ZiI+PGJ1dHRvbiBkYXRhLXY9IjUiPjVzPC9idXR0b24+PGJ1dHRvbiBkYXRhLXY9
IjEwIj4xMHM8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMzAiPjMwczwvYnV0dG9uPjxidXR0b24gY2xhc3M9Im9uIiBkYXRhLXY9
IjYwIj4xbTwvYnV0dG9uPjxidXR0b24gZGF0YS12PSIxODAiPjNtPC9idXR0b24+PGJ1dHRvbiBkYXRhLXY9IjMwMCI+NW08L2J1
dHRvbj48YnV0dG9uIGRhdGEtdj0iOTAwIj4xNW08L2J1dHRvbj48L2Rpdj4KICA8bGFnaCBzdHlsZT0iZGlzcGxheTpibG9jaztt
YXJnaW4tdG9wOjEycHgiPlNpZ25hbCBmaWx0ZXI8L2xhYmVsPgogIDxkaXYgY2xhc3M9InNlZyIgaWQ9InJrIj48YnV0dG9uIGRh
dGEtdj0iMSI+U3RyaWN0PC9idXR0b24+PGJ1dHRvbiBjbGFzcz0ib24iIGRhdGEtdj0iMiI+QmFsYW5jZWQ8L2J1dHRvbj48YnV0
dG9uIGRhdGEtdj0iMyI+QWN0aXZlPC9idXR0b24+PC9kaXY+CiAgPGRpdiBjbGFzcz0ic3ViIiBzdHlsZT0ibWFyZ2luLXRvcDo4
cHgiPlN0cmljdDogNCBvZiA1IGluZGljYXRvcnMgYWdyZWUsIG5vbmUgb3Bwb3NlLiBCYWxhbmNlZDogMyBvZiA1LiBCb3RoIGFs
c28gbmVlZCB0aGUgaGlnaGVyLXRpbWVmcmFtZSB0cmVuZCwgYSBjb25maXJtaW5nIGNhbmRsZSBhbmQgbm9ybWFsIHZvbGF0aWxp
dHkuIEFjdGl2ZTogbWFqb3JpdHkgb2YgNSBvbmx5LjwvZGl2PgogPC9kaXY+CiA8ZGl2IGNsYXNzPSJjYXJkIj48ZGl2IGNsYXNz
PSJyb3ciPjxiPlNpZ25hbCBlbmdpbmU8L2I+PHNwYW4gY2xhc3M9InN1YiIgaWQ9InNlbHAiPjwvc3Bhbj48L2Rpdj4KICA8ZGl2
IGNsYXNzPSJlbmciIGlkPSJlbmciPjxzdmcgdmlld0JveD0iMCAwIDI0MCAyNDAiPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0i
Z3IiIHgxPSIwIiB5MT0iMCIgeDI9IjEiIHkyPSIxIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM1ZWVhZDQiLz48c3Rv
cCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM4YjVjZjYiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz4KICAgPGNpcmNsZSBjeD0i
MTIwIiBjeT0iMTIwIiByPSIxMDQiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZmZmZjEyIiBzdHJva2Utd2lkdGg9IjgiLz4KICAg
PGNpcmNsZSBpZD0icGciIGN4PSIxMjAiIGN5PSIxMjAiIHI9IjEwNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2dyKSIgc3Ry
b2tlLXdpZHRoPSI4IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1kYXNoYXJyYXk9IjY1My40NSIgc3Ryb2tlLWRhc2hv
ZmZzZXQ9IjY1My40NSIgdHJhbnNmb3JtPSJyb3RhdGUoLTkwIDEyMCAxMjApIi8+CiAgIDxjaXJjbGUgY2xhc3M9InNwaW4iIGN4
PSIxMjAiIGN5PSIxMjAiIHI9IjExNiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjOGI1Y2Y2IiBzdHJva2Utd2lkdGg9IjIiIHN0cm9r
ZS1kYXNoYXJyYXk9IjYgMTQiLz48L3N2Zz4KICAgPGRpdiBjbGFzcz0ic3dlZXAiPjwvZGl2PjxkaXYgY2xhc3M9ImN0ciI+PGRp
diBpZD0iaWMiIGNsYXNzPSJpYyI+4pqhPC9kaXY+PGRpdiBpZD0ic2lnIiBjbGFzcz0iZCI+U1RBTkRCWTwvZGl2PjxkaXYgaWQ9
InN1YiIgY2xhc3M9InN1YiI+VGFwIHRvIHN0YXJ0PC9kaXY+PC9kaXY+PC9kaXY+CiAgPGRpdiBjbGFzcz0ibWluaSI+PGRpdj48
c3BhbiBjbGFzcz0ic3ViIj5UaW1lIGxlZnQ8L3NwYW4+PGIgaWQ9ImxlZnQiPi0tOi0tPC9iPjwvZGl2PjxkaXY+PHNwYW4gY2xh
c3M9InN1YiI+U3RyZW5ndGg8L3NwYW4+PGIgaWQ9InN0ciI+LS08L2I+PC9kaXY+PGRpdj48c3BhbiBjbGFzcz0ic3ViIj5Qcmlj
ZTwvc3Bhbj48YiBpZD0icHgiPi0tPC9iPjwvZGl2PjwvZGl2PgogIDxidXR0b24gaWQ9ImdvIiBjbGFzcz0iYmlnIj7ilrYgU1RB
UlQgQk9UPC9idXR0b24+PC9kaXY+CiA8ZGl2IGNsYXNzPSJjYXJkIj48ZGl2IGNsYXNzPSJyb3ciPjxkaXY+PGIgaWQ9ImNuIj4t
LTwvYj48c3BhbiBjbGFzcz0ibGl2ZSI+PGk+PC9pPkxJVkU8L3NwYW4+PGRpdiBjbGFzcz0ic3ViIiBpZD0iY2kiPjwvZGl2Pjwv
ZGl2PjxkaXYgc3R5bGU9InRleHQtYWxpZ246cmlnaHQiPjxkaXYgaWQ9ImNweCIgY2xhc3M9ImNweCI+LS08L2Rpdj48ZGl2IGlk
PSJjY2giIGNsYXNzPSJzdWIiPjwvZGl2PjwvZGl2PjwvZGl2PgogIDxkaXYgc3R5bGU9InBvc2l0aW9uOnJlbGF0aXZlO21hcmdp
bi10b3A6OHB4Ij48Y2FudmFzIGlkPSJjdiIgc3R5bGU9IndpZHRoOjEwMCU7aGVpZ2h0OjIxMHB4O2Rpc3BsYXk6YmxvY2siPjwv
Y2FudmFzPjxkaXYgaWQ9ImNtIiBjbGFzcz0iY20iPkxvYWRpbmcgbGl2ZSBwcmljZeKApjwvZGl2PjwvZGl2PjwvZGl2PgogPGRp
diBjbGFzcz0ic2FyZCI+PGRpdiBjbGFzcz0icm93Ij48Yj5NYXJrZXRzPC9iPjxkaXYgY2xhc3M9InNlZyIgaWQ9ImdwIiBzdHls
ZT0ibWFyZ2luOjAiPjxidXR0b24gZGF0YS12PSJmeCI+Rm9yZXg8L2J1dHRvbj48YnV0dG9uIGNsYXNzPSJvbiIgZGF0YS12PSJj
ciI+Q3J5cHRvPC9idXR0b24+PC9kaXY+PC9kaXY+PGRpdiBjbGFzcz0iZ3JpZCIgaWQ9Im1rdCI+PC9kaXY+PGRpdiBjbGFzcz0i
c3ViIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgiPlRhcCBhIG1hcmtldCB0byBzZWxlY3QgaXQuIFRoZSBhcnJvdyBzaG93cyB0aGUg
bGl2ZSBzaWduYWwuPC9kaXY+PC9kaXY+CiA8ZGl2IGNsYXNzPSJjYXJkIj48Yj5NYXJrZXQgc2Nhbm5lcjwvYj48ZGl2IGNsYXNz
PSJzdGVwcyIgaWQ9InN0ZXBzIj48L2Rpdj48L2Rpdj4KIDxkaXYgY2xhc3M9ImNhcmQiPjxiPkluZGljYXRvcnM8L2I+PGRpdiBj
bGFzcz0idGJsIiBpZD0iaW5kIj48ZGl2PjxzcGFuPldhaXRpbmcgZm9yIGEgc2Nhbjwvc3Bhbj48L2Rpdj48L2Rpdj48L2Rpdj4K
PC9kaXY+Cgo8ZGl2IGlkPSJ0LWhpc3QiIGNsYXNzPSJ0YWIiPjxkaXYgY2xhc3M9ImNhcmQiPjxiPkhpc3Rvcnk8L2I+PGRpdiBj
bGFzcz0idGJsIiBpZD0iaGlzdCI+PC9kaXY+PC9kaXY+PC9kaXY+CjxkaXYgaWQ9InQtYW4iIGNsYXNzPSJ0YWIiPjxkaXYgY2xh
c3M9ImNhcmQiPjxiPllvdXIgcmVhbCByZXN1bHRzPC9iPjxkaXYgY2xhc3M9InN1YiI+Q291bnRlZCBvbmx5IGZyb20gc2lnbmFs
cyB0aGlzIGFwcCBsb2dnZWQgYW5kIGNoZWNrZWQgYWdhaW5zdCBwcmljZSB3aGVuIHRoZSB0aW1lZnJhbWUgZW5kZWQuPC9kaXY+
CiA8ZGl2IGNsYXNzPSJyb3ciIHN0eWxlPSJtYXJnaW4tdG9wOjEycHgiPjxkaXY+PGRpdiBjbGFzcz0ic3RhdCIgaWQ9ImF3Ij4w
PC9kaXY+PGRpdiBjbGFzcz0ic3ViIj5XaW5zPC9kaXY+PC9kaXY+PGRpdj48ZGl2IGNsYXNzPSJzdGF0IiBpZD0iYWwiPjA8L2Rp
dj48ZGl2IGNsYXNzPSJzdWIiPkxvc3NlczwvZGl2PjwvZGl2PjxkaXY+PGRpdiBjbGFzcz0ic3RhdCIgaWQ9ImFyIj4tLTwvZGl2
PjxkaXYgY2xhc3M9InN1YiI+V2luIHJhdGU8L2Rpdj48L2Rpdj48L2Rpdj4KIDxkaXYgY2xhc3M9InN1YiIgaWQ9InN0ayIgc3R5
bGU9Im1hcmdpbi10b3A6MTJweCI+PC9kaXY+PGRpdiBjbGFzcz0idGJsIiBpZD0iYnlwIiBzdHlsZT0ibWFyZ2luLXRvcDoxMHB4
Ij48L2Rpdj48YnV0dG9uIGlkPSJleHAiIGNsYXNzPSJiaWciIHN0eWxlPSJwYWRkaW5nOjEwcHg7Zm9udC1zaXplOjE0cHgiPkRv
d25sb2FkIGhpc3RvcnkgKENTVik8L2J1dHRvbj4KIDxidXR0b24gaWQ9ImNsciIgY2xhc3M9ImJpZyBzdG9wIiBzdHlsZT0icGFk
ZGluZzoxMHB4O2ZvbnQtc2l6ZToxNHB4Ij5DbGVhciBoaXN0b3J5PC9idXR0b24+PC9kaXY+PC9kaXY+CjxkaXYgaWQ9InQtc2V0
IiBjbGFzcz0idGFiIj48ZGl2IGNsYXNzPSJjYXJkIj48Yj5QcmVmZXJlbmNlczwvYj48bGFiZWwgc3R5bGU9ImRpc3BsYXk6Ymxv
Y2s7bWFyZ2luLXRvcDoxMHB4Ij5Tb3VuZCBhbmQgdmlicmF0aW9uIG9uIHNpZ25hbHM8L2xhYmVsPjxkaXYgY2xhc3M9InNlZyIg
aWQ9InNuIj48YnV0dG9uIGRhdGEtdj0ib24iPk9uPC9idXR0b24+PGJ1dHRvbiBkYXRhLXY9Im9mZiI+T2ZmPC9idXR0b24+PC9k
aXY+PGxhYmVsIHN0eWxlPSJkaXNwbGF5OmJsb2NrO21hcmdpbi10b3A6MTJweCI+U3RvcCB0aGUgYm90IGFmdGVyIGxvc3NlcyBp
biBhIHJvdzwvbGFiZWw+PGRpdiBjbGFzcz0ic2VnIiBpZD0ibWwiPjxidXR0b24gZGF0YS12PSIwIj5PZmY8L2J1dHRvbj48YnV0
dG9uIGRhdGEtdj0iMiI+MjwvYnV0dG9uPjxidXR0b24gZGF0YS12PSIzIj4zPC9idXR0b24+PGJ1dHRvbiBkYXRhLXY9IjUiPjU8
L2J1dHRvbj48L2Rpdj48YnV0dG9uIGlkPSJsbyIgY2xhc3M9ImJpZyBzdG9wIiBzdHlsZT0icGFkZGluZzoxMHB4O2ZvbnQtc2l6
ZToxNHB4Ij5Mb2cgb3V0PC9idXR0b24+PC9kaXY+PGRpdiBjbGFzcz0iY2FyZCI+PGI+QWJvdXQ8L2I+PHAgY2xhc3M9InN1YiIg
c3R5bGU9Im1hcmdpbi10b3A6OHB4Ij5IRUxJWCBCT1RJQyB1c2VzIGxpdmUgZGF0YSBvbmx5IChRdW90ZXggRm9yZXggJiBPVEMg
ZmVlZHMsIGFuZCBDcnlwdG8gZnJvbSBCaW5hbmNlKS4gSXQgc2NvcmVzIDUgaW5kaWNhdG9ycyAoUlNJIDE0LCBFTUEgOS8yMSwg
TUFDRCwgQm9sbGluZ2VyIGJhbmRzLCBFTUEgNTAgdHJlbmQpLCB0aGVuIGFsc28gY2hlY2tzIHRoZSBoaWdoZXItdGltZWZyYW1l
IHRyZW5kLCB0aGUgbGFzdCBjYW5kbGUsIHZvbGF0aWxpdHkgYW5kIHlvdXIgb3duIHdpbiByZWNvcmQgb24gdGhhdCBwYWlyIGJl
Zm9yZSBpdCBzaWduYWxzLiBTdHJlbmd0aCBzaG93cyBob3cgbWFueSBhZ3JlZSwgbm90IHRoZSBjaGFuY2Ugb2Ygd2lubmluZy4g
U2Vjb25kcyB0aW1lZnJhbWVzIGFyZSBjbG9zZSB0byBhIGNvaW4gZmxpcCBldmVuIHdpdGggZmlsdGVycy4gQmluYXJ5IG9wdGlv
bnMgY2FuIGxvc2UgeW91ciB3aG9sZSBzdGFrZTogdXNlIGEgZGVtbyBhY2NvdW50IGZpcnN0IGFuZCBuZXZlciB0cmFkZSBtb25l
eSB5b3UgY2Fubm90IGxvc2UuPGJyPjxiPkhFTElY AI BOTPC9iPjwvcD48L2Rpdj48L2Rpdj4KPHpkaXYgY2xhc3M9
Indhcm4iPk5vdCBmaW5hbmNpYWwgYWR2aWNlLiBTaWduYWxzIGNhbiBiZSB3cm9uZy4gV2luIHJhdGUgaXMgb25seSBmcm9tIHlv
dXIgb3duIGxvZ2dlZCByZXN1bHRzLjxicj48Yj5IRUxJWCBFSSBOT1Q8L2I+PC9kaXY+CiA8ZGl2IGNsYXNzPSJ3YXJuIj5Ob3Qg
ZmluYW5jaWFsIGFkdmljZS4gU2lnbmFscyBjYW4gYmUgd3JvbmcuIFdpbiByYXRlIGlzIG9ubHkgZnJvbSB5b3VyIG93biBsb2dn
ZWQgcmVzdWx0cy48YnI+PGI+SEVMSVggQUkgQk9UPC9iPjwvZGl2Pgo8L2Rpdj4KPGRpdiBpZD0icG9wIj48ZGl2IGNsYXNzPSJw
YyI+PGRpdiBjbGFzcz0ic3ViIj5TSUdOQUwgQUxFUlQ8L2Rpdj48ZGl2IGlkPSJwcCIgc3R5bGU9ImZvbnQtd2VpZ2h0OjcwMDtt
YXJnaW4tdG9wOjZweCI+PC9kaXY+PGRpdiBpZD0icGQiIGNsYXNzPSJkaXIiPjwvZGl2PjxkaXYgaWQ9InBpIiBjbGFzcz0ic3Vi
Ij48L2Rpdj48ZGl2IGNsYXNzPSJzdWIiIHN0eWxlPSJtYXJnaW4tdG9wOjEycHgiPlRha2UgdHJhZGUgYXQ8L2Rpdj48ZGl2IGlk
PSJwdCIgY2xhc3M9InRtIj48L2Rpdj48ZGl2IGlkPSJwdyIgY2xhc3M9InN1YiI+PC9kaXY+PGJ1dHRvbiBjbGFzcz0iaWciIGlk
PSJvayI+R09UIElUPC9idXR0b24+PC9kaXY+PC9kaXY+CjxuYXY+PGJ1dHRvbiBjbGFzcz0ib24iIGRhdGEtdj0iZGFzaCI+RGFz
aGJvYXJkPC9idXR0b24+PGJ1dHRvbiBkYXRhLXQ9Imhpc3QiPkhpc3Rvcnk8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iYW4iPkFu
YWx5dGljczwvYnV0dG9uPjxidXR0b24gZGF0YS10PSJzZXQiPkFib3V0PC9idXR0b24+PC9uYXY+Cgo8c2NyaXB0Pgpjb25zdCAk
PXM9PmRvY3VtZW50LnF1ZXJ5U2VsZWN0b3Iocyk7CmNvbnN0IEZYPVsnRVVSL1VTRCAoT1RDKScsJ0dCUC9VU0QgKE9UQyknLCdV
U0DvSlBZKE9UQyknLCdVU0QvQ0FEIChPVEMpJywnVVNEL0NIRCAoT1RDKScsJ0VVUi9HQlAgKE9UQyknLCdFVVIvSlBZIChPVEMp
JywnRVVSL0NIRCAoT1RDKScsJ0VVUi9DQUQgKE9UQyknXTsKY29uc3QgQ1I9J1sic3RySGVyZUIiLCdCVENVU0RUQicsJ0VUSFVT
RFQnLCdCTkJVU0RUJywnU09MVVNEVCcsJ1hSUFVTRFQnLCdET0dFVVNEVCddOwpjb25zdCBpc0Z4PXA9PnAuaW5jbHVkZXMoJy8n
KSxubT1wPT5pc0Z4KHApP3A6cC5yZXBsYWNlKCdVU0RUJywnL1VTRFQnKTsKY29uc3QgdGZMPXQ9PnQ8NjA/dCsncyc6dC82MCsr
J20nLEM9NjUzLjQ1Owpjb25zdCBmbXQ9YT0+YS50b0ZpeGVkKGE8Mj81OmExMDA/MzoyKTsKY29uc3QgbW1zcz1zPT5TdHJpbmco
TWF0aC5mbG9vcihzLzYwKSkucGFkU3RhcnQoMiwnMCcpKyc6JytTdHJpbmcocyU2MCkucGFkU3RhcnQoMiwnMCcpOwpjb25zdCBz
bGVlcD1tcz0+bmV3IFByb21pc2Uocj0+c2V0VGltZW91dCIocixtcyk7CmxldCBTPXttazonbGl2ZScsdGY6NjAscms6MixydW46
ZmFsc2UsZ3JwOidjcicscGFpcjonQlRDVVNEVCcsaGlzdDpbXSxweDp7fSxjaDp7fSxzcDp7fSxzaWc6bnVsbCxzbmQ6J29uJyxt
YXhMOjN9OwpsZXQgS0VZPScnO3RyeXtLRVk9bG9jYWxTdG9yYWdlLmdldEl0ZW0oJ2hrJyl8fCcnO1MuaGlzdD1KU09OLnBhcnNl
KGxvY2FsU3RvcmFnZS5nZXRJdGVtKCdoYjInKXx8J1tdJykuZmlsdGVyKGg9PmgubWshPT0nZGVtbycpfWNhdGNoKGUpe30KUy5o
aXN0LmZvckVhY2goaD0+e2lmKCFoLnJlcyloLnJlcz0ndm9pZCd9KTsKY29uc3Qgc2F2ZT0oKT0+e3RyeXtsb2NhbFN0b3JhZ2Uu
c2V0SXRlbSgnaGIyJyxKU09OLnN0cmluZ2lmeShTLmhpc3QpKX1jYXRjaChlKXt9fTsKY29uc3Qgc2F2ZVNldD0oKT0+e3RyeXts
b2NhbFN0b3JhZ2Uuc2V0SXRlbSgnaHhfc2V0JyxKU09OLnN0cmluZ2lmeSh7c25kOlMuc25kLG1heEw6Uy5tYXhMfSkpfWNhdGNo
KGUpe319Owp0cnl7T2JqZWN0LmFzc2lnbihTLEpTT04ucGFyc2UobG9jYWxTdG9yYWdlLmdldEl0ZW0oJ2h4X3NldCcpfHwne30n
KSl9Y2F0Y2goZSl7fQpjb25zdCBBQ0NFU1M9JzU1NjYnOwpmdW5jdGlvbiBzZWcoaWQsa2V5LG51bSl7ZG9jdW1lbnQucXVlcnlT
ZWxlY3RvckFsbChpZCsnIGJ1dHRvbicpLmZvckVhY2goYj0+Yi5vbmNsaWNrPSgpPT57ZG9jdW1lbnQucXVlcnlTZWxlY3RvckFs
bChpZCsnIGJ1dHRvbicpLmZvckVhY2goeD0+eC5jbGFzc0xpc3QucmVtb3ZlKCdvbicpKTtiLmNsYXNzTGlzdC5hZGQoJ29uJyk7
U1trZXldPW51bT8rYi5kYXRhc2V0LnY6Yi5kYXRhc2V0LnY7aWYoa2V5PT09J2dycCcpe2NvbnN0IEw9Uy5ncnA9PT0nZfxnP0ZY
OkNSO2lmKCFMLmluY2x1ZGVzKFMucGFpcikpUy5wYWlyPUxbMF07JCgnI3NlbHAnKS50ZXh0Q29udGVudD1ubShTLnBhaXIpO21h
cmtldHMoKTtwcmljZXMoKX1pZihrZXk9PT0ndGYnfHxrZXk9PT0nZ3JwJyljaGFydFJlc2V0KCk7aWYoa2V5PT09J3NuZCd8fGtl
eT09PSdtYXhMJylzYXZlU2V0KCl9KX0Kc2VnKCcjdGYnLCd0ZicsMSk7c2VnKCcjcmsnLCdyaycsMSk7c2VnKCcjZ3AnLCdncnAn
KTtzZWcoJyNzbicsJ3NuZCcpO3NlZygnI21sJywnbWF4TCcsMSk7CmRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJ25hdiBidXR0
b24nKS5mb3JFYWNoKGI9PmIub25jbGljaz0oKT0+e2RvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJ25hdiBidXR0b24sLnRhYicp
LmZvckVhY2goeD0+eC5jbGFzc0xpc3QucmVtb3ZlKCdvbicpKTtiLmNsYXNzTGlzdC5hZGQoJ29uJyk7JCgnI3QtJytiLmRhdGFz
ZXQudCkuY2xhc3NMaXN0LmFkZCgnb24nKTtyZW5kZXIoKX0pOwpmdW5jdGlvbiBtb2RlKCl7Y29uc3QgbT0kKCcjbW9kZScpO20u
dGV4dENvbnRlbnQ9J0xJVkUgREFUQSc7bS5jbGFzc05hbWU9J2JhZGdlIGxpdmUnfQoKLy8gLS0tLSBkYXRhIChsaXZlIG9ubHkp
IC0tLS0KY29uc3QgSE9TVFM9WydodHRwczovL2FwaS5iaW5hbmNlLmNvbScsJ2h0dHBzOi8vZGF0YS1hcGkuYmluYW5jZS52aXNp
b24nLCdodHRwczovL2FwaTEuYmluYW5jZS5jb20nLCdodHRwczovL2FwaTIuYmluYW5jZS5jb20nLCdodHRwczovL2FwaTMuYmlu
YW5jZS5jb20nXTsKbGV0IEhJPTA7CmFzeW5jIGZ1bmN0aW9uIGJnZXQocGF0aCl7CiBsZXQgZXJyOwogZm9yKGxldCBrPTA7azxI
T1NUUy5sZW5ndGg7aysrKXsKICB0cnl7Y29uc3QgYz1uZXcgQWJvcnRDb250cm9sbGVyKCksdD1zZXRUaW1lb3V0KCgpPT5jLmFi
b3J0KCksNjAwMCk7CiAg const r=await fetch(SECPIS[...]);...
   const r=await fetch(HOSTS[(HI+k)%HOSTS.length]+path,{signal:c.signal});clearTimeout(t);
   if(!r.ok)throw new Error('HTTP '+r.status);const j=await r.json();HI=(HI+k)%HOSTS.length;return j}
  catch(e){err=e}}throw err;
}
const NOCONN='Cannot reach market data. Check internet connection.';
const agg=(c,a)=>{if(a===1)return c;const o=[];for(let i=c.length-1;i>=0;i-=a)o.unshift(c[i]);return o};
const KR=p=>p.replace('/','').replace(' (OTC)','');

async function quotexOhlc(pair,tf,n){
 const r=await kget(`/OTC?pair=${KR(pair)}&interval=${tf===180?1:tf/60}`),k=Object.keys(r).find(x=>x!=='last');
 let d=r[k].map(x=>({t:+x[0],o:+x[1],h:+x[2],l:+x[3],c:+x[4]}));
 if(tf===180)d=agg(d,3);return d.slice(-n);
}
async function kl(sym,iv,lim){const j=await bget(`/api/v3/klines?symbol=${sym}&interval=${iv}&limit=${lim}`);if(!Array.isArray(j))throw new Error('BADSYM');return j.map(k=>({o:+k[1],h:+k[2],l:+k[3],c:+k[4]}))}
async function kget(path){const c=new AbortController(),t=setTimeout(()=>c.abort(),8000);try{const j=await(await fetch('https://api.kraken.com/0/public'+path,{signal:c.signal})).json();if(j.error&&j.error.length)throw new Error(j.error[0]);return j.result}finally{clearTimeout(t)}}
async function candles(pair,tf,n=250){
 if(isFx(pair)){
  if(tf<60)throw new Error('Forex works from 1m. Use crypto for 5s, 10s, 30s');
  try{return(await quotexOhlc(pair,tf,n)).map(k=>k.c)}catch(e){throw new Error(NOCONN)}
 }
 try{
  if(tf<60){const a=tf===5?1:tf===10?2:5;return agg((await kl(pair,'1s',1000)).map(k=>k.c),a).slice(-n)}
  return(await kl(pair,tf/60+'m',n)).map(k=>k.c);
 }catch(e){throw new Error(NOCONN)}
}
async function prices(){
 if(S.grp==='cr'){try{const j=await bget('/api/v3/ticker/24hr?symbols='+encodeURIComponent(JSON.stringify(CR)));j.forEach(x=>{S.px[x.symbol]=+x.lastPrice;S.ch[x.symbol]=+x.priceChangePercent})}catch(e){}}
 else{try{const r=await kget('/Ticker?pair='+FX.map(KR).join(','));
  Object.entries(r).forEach(([k,v])=>{const key=k.length===8&&/^MA/.test(k)&&/[A-Z]/.test(k[4])?k.slice(1,4)+k.slice(5):k,p=FX.find(x=>KR(x)===key);
   if(p){S.px[p]=+v.c[0];S.ch[p]=(+v.c[0]/+v.o-1)*100}});
 }catch(e){}}
 markets();
}
function ema(a,n){const k=2/(n+1);let e=a[0];return a.map(v=>e=v*k+e*(1-k))}
function rsi(a,n=14){let g=0,l=0;for(let i=1;i<=n;i++){const d=a[i]-a[i-1];d>0?g+=d:l-=d}g/=n;l/=n;
 for(let i=n+1;i<a.length;i++){const d=a[i]-a[i-1];g=(g*(n-1)+Math.max(d,0))/n;l=(l*(n-1)+Math.max(-d,0))/n}return l===0?100:100-100/(1+g/l)}
function recStat(p,t){const d=S.hist.filter(h=>h.pair===p&&h.tf===t&&(h.res==='win'||h.res==='loss'));return{n:d.length,w:d.filter(h=>h.res==='win').length}}
const sdv=a=>{const m=a.reduce((s,x)=>s+x,0)/a.length;return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/a.length)};
function analyse(c,pair,tf){
 const L=c.length-1,px=c[L],e9=ema(c,9),e21=ema(c,21),e50=ema(c,50),e12=ema(c,12),e26=ema(c,26);
 const m=e12.map((v,i)=>v-e26[i]),sg=ema(m,9),R=rsi(c);
 const w=c.slice(-20),mean=w.reduce((a,b)=>a+b,0)/20,sd=sdv(w);
 const pb=sd?(px-(mean-2*sd))/(4*sd):.5;
 const v=[
  {n:'RSI (14)',t:R.toFixed(1),s:R<35?1:R>65?-1:0},
  {n:'EMA 9 / 21',t:e9[L]>e21[L]?'9 above 21':'9 below 21',s:e9[L]>e21[L]?1:-1},
  {n:'MACD',t:(m[L]-sg[L]).toPrecision(3),s:m[L]>sg[L]?1:-1},
  {n:'Bollinger %B',t:pb.toFixed(2),s:pb<.2?1:pb>.8?-1:0},
  {n:'Trend (EMA 50)',t:px>e50[L]?'above':'below',s:px>e50[L]?1:-1}
 ];
 const up=v.filter(x=>x.s>0).length,dn=v.filter(x=>x.s<0).length,mx=Math.max(up,dn),mn=Math.min(up,dn),dir=up>dn?1:dn>up?-1:0;
 const h=agg(c,5),h9=ema(h,9),h21=ema(h,21),H=h.length-1,htf=h9[H]>h21[H]?1:-1;
 const rt=c.slice(1).map((x,i)=>Math.log(x/c[i])),s100=sdv(rt.slice(-100)),vr=s100?sdv(rt.slice(-15))/s100:0;
 const st=recStat(pair,tf),wr=st.n?st.w/st.n:1,ok=dir!==0&&(S.rk===1?(mx>=4&&mn===0):S.rk===2?(mx>=3&&mn<=1):mx>=3);
 let why='';
 if(!sd)why='Market is flat';
 else if(!ok)why=`Only ${mx}/5 agree`;
 else if(S.rk<3&&dir!==htf)why='Higher timeframe trend disagrees';
 else if(S.rk<3&&(dir>0?px<=c[L-1]:px>=c[L-1]))why='Last candle is not confirming';
 else if(vr<.35)why='Market too quiet';
 else if(vr>2.5)why='Volatility spike';
 else if(S.rk<3&&st.n>=8&&wr<.45)why=`Your record on this pair is weak (${Math.round(wr*100)}%)`;
 const disp=v.concat([{n:'Higher timeframe',t:htf>0?'up':'down',s:htf},{n:'Volatility',t:vr.toFixed(2)+'x normal',s:0},{n:'Your record here',t:st.n?st.w+'W / '+(st.n-st.w)+'L':'no data yet',s:0}]);
 return{v:disp,dir:why?0:dir,agree:mx,px,why};
}
function spark(a){const x=a.slice(-40),lo=Math.min(...x),hi=Math.max(...x)||1,r=(hi-lo)||1;
 return`<svg viewBox="0 0 100 26" style="width:100%;height:26px;margin-top:4px"><polyline fill="none" stroke="#8b5cf6" stroke-width="1.6" points="${x.map((v,i)=>(i/(x.length-1)*100).toFixed(1)+','+(24-(v-lo)/r*22).toFixed(1)).join(' ')}"/></svg>`}
function markets(){
 const L=S.grp==='fx'?FX:CR;
 $('#mkt').innerHTML=L.map(p=>{const sg=S.sig&&S.sig.pair===p&&!S.sig.res?S.sig:null,px=S.px[p],ch=S.ch[p];
  return`<div class="pc2${p===S.pair?' sel':''}${sg?(sg.dir>0?' up':' dn'):''}" onclick="pick('${p}')"><div class="row"><b>${nm(p)}</b>${sg?`<span class="ar ${sg.dir>0?'up':'dn'}">${sg.dir>0?'↑':'↓'}</span>`:''}</div><div class="sub">${px?fmt(px):'--'}${ch!=null?` <span class="${ch>=0?'up':'dn'}">${ch>=0?'+':''}${ch.toFixed(2)} %</span>`:''}</div>${S.sp[p]?spark(S.sp[p]):''}</div>`}).join('');
 chartDraw();
}
function pick(p){S.pair=p;$('#selp').textContent=nm(p);markets();chartReset()}
function eng(state,ic,txt,sub,cls){const e=$('#eng');e.className='eng '+(state==='scan'?'scanning ':'')+(state==='up'?'gu ':state==='dn'?'gd ':'')+(cls||'');void e.offsetWidth;if(state==='up'||state==='dn')e.classList.add(txt==='LOSS'?'shake':'burst');if(txt==='LOSS')e.classList.remove('burst');$('#ic').textContent=ic;$('#sig').textContent=txt;$('#sig.className='d '+(state==='up'?'up':state==='dn'?'dn':state==='nt'?'nt':'');$('#sub').textContent=sub}
const STEPS=['Reading candles','Calculating RSI (14)','Checking EMA 9/21/50 trend','Checking MACD (12,26,9)','Checking Bollinger bands','Checking higher-timeframe trend','Checking volatility and your record'];
async function scan(){
 const box=$('#steps');box.innerHTML=STEPS.map(s=>`<div>${s}</div>`).join('');
 const c=await candles(S.pair,S.tf);
 for(let i=0;i<STEPS.length;i++){await sleep(350);box.children[i].classList.add('ok')}
 S.sp[S.pair]=c.slice(-40);return analyse(c,S.pair,S.tf);
}
function popup(h){
 $('#pp').textContent=nm(h.pair)+' • '+tfL(h.tf);
 $('#pd').textContent=h.dir>0?'↑ UP (CALL)':'↓ DOWN (PUT)';$('#pd').className='dir '+(h.dir>0?'up':'dn');
 $('#pi').textContent=h.agree+'/5 indicators agree';
 $('#pt').textContent=new Date(h.at).toLocaleTimeString([],h.tf<60?{hour:'2-digit',minute:'2-digit',second:'2-digit'}:{hour:'2-digit',minute:'2-digit'});
 clearInterval(S.pw);const u=()=>{if(h.res&&h.res!=='void'){$('#pw').textContent='Result: '+h.res.toUpperCase();return}const s=Math.max(0,Math.round((h.at-Date.now())/1000));$('#pw').textContent=s>0?'Starts in '+s+'s':'Enter now'};u();S.pw=setInterval(u,1000);
 $('#pop').classList.add('on');
}
$('#ok').onclick=()=>{$('#pop').classList.remove('on');clearInterval(S.pw)};
$('#eng').onclick=()=>{if(!S.run)Toggle();else if(S.sig&&!S.sig.res)popup(S.sig)};
async function cycle(){
 if(!S.run)return;
 eng('scan','⚡','SCANNING','Analyzing '+nm(S.pair)+'…');$('#pg').style.strokeDashoffset=C;$('#str').textContent='--';
 let a;try{a=await scan()}catch(e){if(!S.run)return;eng('nt','!','NO DATA',e.message||'Data unavailable');S.timer=setTimeout(cycle,10000);return}
 if(!S.run)return;
 $('#px').textContent=fmt(a.px);S.px[S.pair]=a.px;
 $('#ind').innerHTML=a.v.map(x=>`<div><span>${x.n}</span><span class="${x.s>0?'up':x.s<0?'dn':'nt'}">${x.t}</span></div>`).join('');
 $('#str').textContent=a.agree+'/5';markets();
 if(a.dir===0){eng('nt','⇛','NO TRADE',a.why+'. Re-scanning…');S.timer=setTimeout(cycle,S.tf<60?3000:6000);return}
 const up=a.dir>0;
 eng(up?'up':'dn',up?'↑':'↓',up?'UP • CALL':'DOWN • PUT',a.agree+'/5 agree • '+tfL(S.tf)+' • tap for details',up?'glowup':'glowdn');
 const now=Date.now(),at=S.tf<60?now+4000:Math.ceil((now+5000)/60000)*60000;
 const rec={t:now,at,pair:S.pair,tf:S.tf,dir:a.dir,entry:null,agree:a.agree,res:null,mk:'live'};
 S.hist.unshift(rec);S.sig=rec;save();markets();popup(rec);beep(880,.18);
 const total=Math.round((at-now)/1000)+S.tf;let left=total,entered=false;
 clearInterval(S.tick);
 S.tick=setInterval(async()=>{left--;const l=Math.max(left,0);
  $('#left').textContent=mmss(l);$('#pg').style.strokeDashoffset=C*(1-l/total);
  if(!entered&&Date.now()>=at){entered=true;try{const c=await candles(rec.pair,rec.tf,60);rec.entry=c[c.length-1];save()}catch(e){}}
  if(left<=0){clearInterval(S.tick);finish(rec)}},1000);
}
let AC;
function beep(f,d){if(S.snd!=='on')return;try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f;g.gain.value=.08;o.connect(g);g.connect(AC.destination);o.start();o.stop(AC.currentTime+d)}catch(e){}try{navigator.vibrate&&navigator.vibrate(Math.round(d*600))}catch(e){}}
function lossRun(){let n=0;for(const h of S.hist.filter(h=>h.res==='win'||h.res==='loss')){if(h.res==='loss')n++;else break}return n}
function confetti(){const c=$('#fx'),g=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;const cl=['#3ff2a0','#5eead4','#8b5cf6','#f5c46b'],P=Array.from({length:55},()=>({x:innerWidth/2,y:innerHeight*.4,vx:(Math.random()-.5)*13,vy:-Math.random()*13-2,s:4+Math.random()*5,col:cl[Math.random()*4|0],r:Math.random()*6}));let f=0;(function t(){g.clearRect(0,0,c.width,c.height);P.forEach(p=>{p.vy+=.35;p.x+=p.vx;p.y+=p.vy;p.r+=.2;g.fillStyle=p.col;g.save();g.translate(p.x,p.y);g.rotate(p.r);g.fillRect(-p.s/2,-p.s/2,p.s,p.s*.6);g.restore()});if(++f<75)requestAnimationFrame(t);else g.clearRect(0,0,c.width,c.height)})();}
async function finish(rec){
 let px=null;try{const c=await candles(rec.pair,rec.tf,60);px=c[c.length-1]}catch(e){}
 if(px==null||rec.entry==null){rec.res='void'}
 else{rec.exit=px;rec.res=px===rec.entry?'tie':((px>rec.entry)===(rec.dir>0)?'win':'loss')}
 save();$('#left').textContent='--:--';markets();render();
 eng(rec.res==='win'?'up':rec.res==='loss'?'dn':'nt',rec.res==='win'?'✓':rec.res==='loss'?'✕':'=',rec.res.toUpperCase(),'Trade finished');
 if(rec.res==='win'){beep(1175,.25);confetti()}else if(rec.res==='loss')beep(220,.35);
 if(rec.res==='loss'&&S.maxL>0&&lossRun()>=S.maxL&&S.run){Toggle();eng('nt','⚠','BOT STOPPED',S.maxL+' losses in a row. Take a break.');return}
 if(S.run)S.timer=setTimeout(cycle,4000);
}
function Toggle(){
 S.run=!S.run;const b=$('#go');
 if(S.run){b.textContent='⏸ STOP BOT';b.className='big stop';cycle()}
 else{clearTimeout(S.timer);clearInterval(S.tick);if(S.sig&&!S.sig.res){S.sig.res='void';save()}b.textContent='⚡ START BOT';b.className='big';eng('','⚡','STANDBY','Tap to start');$('#left').textContent='--:--';$('#pg').style.strokeDashoffset=C;markets()}
}
$('#go').onclick=Toggle;
$('#clr').onclick=()=>{if(confirm('Delete all logged signals?')){S.hist=[];save();render()}};
function render(){
 const f=t=>new Date(t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});
 $('#hist').innerHTML=S.hist.length?S.hist.slice(0,50).map((h,i)=>`<div class="hrow" onclick="popup(S.hist[${i}])"><span>${nm(h.pair)} ${tfL(h.tf)} <b class="${h.dir>0?'up':'dn'}">${h.dir>0?'UP':'DOWN'}</b> • ${f(h.t)}</span><span class="${h.res==='win'?'up':h.res==='loss'?'dn':'nt'}">${h.res?h.res.toUpperCase():'pending'}</span></div>ជី`).join(''):'<div><span>No signals yet</span></div>';
 const d=S.hist.filter(h=>h.res==='win'||h.res==='loss'),w=d.filter(h=>h.res==='win').length;
 $('#aw').textContent=w;$('#al').textContent=d.length-w;$('#ar').textContent=d.length?Math.round(w/d.length*100)+'%':'--';
 let k=d[0]&&d[0].res,st=0;for(const h of d){if(h.res===k)st++;else break}
 $('#stk').textContent=d.length?`Current streak: ${st} ${k}${st>1?(k==='win'?'s':'es'):''} • Loss-stop: ${S.maxL||'off'}`:'No finished trades yet';
 const by={};d.forEach(h=>{const k=nm(h.pair)+' '+tfL(h.tf);(by[k]=by[k]||[0,0])[h.res==='win'?0:1]++});
 $('#byp').innerHTML=Object.entries(by).map(([k,v])=>`<div><span>${k}</span><span>${v[0]}W / ${v[1]}L</span></div>`).join('');
}

const CH={d:[],last:null,tm:null};
function chartMsg(t){$('#cm').textContent=t;$('#cm').style.display=t?'flex':'none'}
async function chartPull(){
 const p=S.pair,tf=S.tf;let d;
 try{
  if(isFx(p)){if(tf<60)return chartMsg('Forex works from 1m. Pick 1m or longer, or use crypto for seconds');d=await quotexOhlc(p,tf,60)}
  else d=await kl(p,tf<60?'1s':tf/60+'m',60);
 }catch(e){return chartMsg(NOCONN)}
 if(isFx(p)&&d.length&&Date.now()/1000-d[d.length-1].t>Math.max(900,tf*3))$('#ci').textContent=CH.ci+' • Quotex OTC Live';else $('#ci').textContent=CH.ci;
 if(p!==S.pair||tf!==S.tf||!d.length)return;
 chartMsg('');const sg=d.length+':'+d[d.length-1].c+':'+d[d.length-1].h+':'+d[d.length-1].l;if(sg===CH.sg)return;CH.sg=sg;const prev=CH.last;CH.d=d;CH.last=d[d.length-1].c;S.px[p]=CH.last;
 const e=$('#cpx');e.textContent=fmt(CH.last);$('#px').textContent=fmt(CH.last);
 if(prev!=null&&prev!==CH.last){e.className='cpx';void e.offsetWidth;e.className='cpx '+(CH.last>prev?'fu':'fd')}
 const ch=S.ch[p];$('#cch').textContent=ch!=null?(ch>=0?'+':'')+ch.toFixed(2)+'\% 24h':'';$('#cch').className='sub '+(ch>=0?'up':'dn');
 chartDraw();
}
function chartReset(){
 clearInterval(CH.tm);CH.d=[];CH.last=null;CH.sg=null;
 $('#cn').textContent=nm(S.pair);$('#cpx').textContent='--';$('#cch').textContent='';
 CH.ci=isFx(S.pair)?(S.tf<60?'forex needs 1m or longer':tfL(S.tf)+' • Quotex OTC Live'):(S.tf<60?'1s':tfL(S.tf)+' • Binance');
 $('#ci').textContent=CH.ci;
 chartMsg('Loading live price…⌛');chartDraw();chartPull();
 CH.tm=setInterval(chartPull,isFx(S.pair)?4000:S.tf<60?1500:3000);
}
function chartDraw(){
 const cv=$('#cv');if(!cv)return;const g=cv.getContext('2d'),dpr=window.devicePixelRatio||1,W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;if(cv.width!==Math.round(W*dpr)){cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr)}
 g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);const d=CH.d;if(!d.length)return;
 let lo=Math.min(...d.map(x=>x.l)),hi=Math.max(...d.map(x=>x.h));const pad=(hi-lo)*.1||hi*.0005;lo-=pad;hi+=pad;
 const pw=58,cw=(W-pw)/d.length,y=v=>H-8-(v-lo)/(hi-lo)*(H-16);
 g.font='10px sans-serif';g.lineWidth=1;
 for(let i=0;i<4;i++){const v=lo+(hi-lo)*i/3,yy=y(v);g.strokeStyle='#ffffff12';g.beginPath();g.moveTo(0,yy);g.lineTo(W-pw,yy);g.stroke();g.fillStyle='#8f93b8';g.fillText(fmt(v),W-pw+4,yy+3)}
 d.forEach((k,i)=>{const x=i*cw+cw/2,u=k.c>=k.o;g.strokeStyle=g.fillStyle=u?'#3ff2a0':'#ff5577';g.beginPath();g.moveTo(x,y(k.h));g.lineTo(x,y(k.l));g.stroke();g.fillRect(x-cw*.32,Math.min(y(k.o),y(k.c)),cw*.64,Math.max(1,Math.abs(y(k.o)-y(k.c))))});
 const last=d[d.length-1].c,ly=y(last);
 g.setLineDash([3,4]);g.strokeStyle='#8b5cf6';g.beginPath();g.moveTo(0,ly);g.lineTo(W-pw,ly);g.stroke();g.setLineDash([]);
 g.fillStyle='#8b5cf6';g.fillRect(W-pw,ly-9,pw,18);g.fillStyle='#fff';g.fillText(fmt(last),W-pw+4,ly+3);
 const s=S.sig;if(s&&!s.res&&s.pair===S.pair){const e=s.entry||last,ey=y(e),col=s.dir>0?'#3ff2a0':'#ff5577';
  g.setLineDash([2,3]);g.strokeStyle=col;g.beginPath();g.moveTo(0,ey);g.lineTo(W-pw,ey);g.stroke();g.setLineDash([]);
  g.font='bold 22px sans-serif';g.fillStyle=col;g.fillText(s.dir>0?'↑':'↓',W-pw-28,ey+(s.dir>0?-6:20))}
}
window.addEventListener('resize',chartDraw);
document.addEventListener('pointerdown',e=>{const b=e.target.closest('button');if(!b)return;const r=b.getBoundingClientRect(),d=Math.max(r.width,r.height)*2,p=document.createElement('span');p.className='rip';p.style.cssText=`width:${d}px;height:${d}px;left:${e.clientX-r.left-d/2}px;top:${e.clientY-r.top-d/2}px`;b.appendChild(p);setTimeout(()=>p.remove(),600)});
function boot(){
 document.querySelectorAll('#sn button').forEach(b=>b.classList.toggle('on',b.dataset.v===S.snd));
 document.querySelectorAll('#ml button').forEach(b=>b.classList.toggle('on',+b.dataset.v===S.maxL));
 mode();$('#selp').textContent=nm(S.pair);markets();render();prices();chartReset();setInterval(prices,15000);
}
$('#exp').onclick=()=>{
 const rows=[['time','pair','timeframe','direction','indicators_agree','entry','exit','result']].concat(S.hist.map(h=>[new Date(h.t).toISOString(),h.pair,tfL(h.tf),h.dir>0?'UP':'DOWN',h.agree,h.entry==null?'':h.entry,h.exit==null?'':h.exit,h.res||'']));
 const b=new Blob([rows.map(r=>r.join(',')).join('\n')],{type:'text/css'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='helix-history.csv';a.click();
};
$('#lo').onclick=()=>{try{localStorage.removeItem('hx_ok')}catch(e){}location.reload()};

let tries=0,lockedUntil=0;
function tryLogin(){
 const now=Date.now();if(now<lockedUntil){$('#lerr').textContent='Too many tries. Wait '+Math.ceil((lockedUntil-now)/1000)+'s';return}
 if($('#pw').value.trim()===ACCESS){try{localStorage.setItem('hx_ok','1')}catch(e){}$('#lerr').textContent='';$('#lock').classList.add('out');setTimeout(()=>$('#lock').remove(),700);boot()}
 else{tries++;$('#pw').value='';$('#lerr').textContent='Wrong access key';const k=$('.lk');k.classList.remove('shake');void k.offsetWidth;k.classList.add('shake');if(tries>=5){lockedUntil=now+30000;tries=0}}
}
$('#lg').onclick=tryLogin;$('#pw').onkeydown=e=>{if(e.key==='Enter')tryLogin()};
let ok=false;try{ok=localStorage.getItem('hx_ok')==='1'}catch(e){}
if(ok){$('#lock').remove();boot()}else setTimeout(()=>$('#pw').focus(),400);
</script>
</body>
</html>
"""
HTML = base64.b64decode("".join(_B64.split()))


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path in ("/", "/index.html", "/index.py"):
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(HTML))),
            ("Cache-Control", "no-cache"),
        ])
        return [HTML]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not found"]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"HELIX BOTIC running on http://localhost:{port}")
    make_server("0.0.0.0", port, app).serve_forever()
