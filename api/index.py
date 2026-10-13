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
Yjh9Cip7Ym94LXNpemluZzpib3JkZXItYm94O21hcmdpbjowOy0td2Via2l0LXRhcC1oaWdobGlnaHQtY29sb3I6dHJhbnNwYXJl
bnR9CmJvZHl7YmFja2dyb3VuZDpyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDEwMCUgNiUsIzBhNGY2MyAwLHRyYW5zcGFyZW50
IDM4JSkscmFkaWFsLWdyYWRpZW50KGNpcmNsZSBhdCAxMCUgLTglLCMyYjE2NzAgMCx0cmFuc3BhcmVudCA0MiUpLHZhcigtLWJn
KTtjb2xvcjp2YXIoLS10KTtnb250OjE1cHgvMS40ICJTRiBQcm8gRGlzcGxheSIsIlNlZ29lIFVJIiwzeXN0ZW0tdWksc2Fucy1z
ZXJpZjttaW4taGVpZ2h0OjEwMHZoO3BhZGRpbmc6ZW52KHNhZmUtYXJlYS1pbnNldC10b3ApIDAgOTZweH0KLnd3bWF4LXdpZHRo
OjQ4MHB4O21hcmdpbjowIGF1dG87cGFkZGluZzoxNHB4fQoubG9nb3tkaXNwbGF5OmZsZXg7Z2FwOjEwcHg7YWxpZ24taXRlbXM6
Y2VudGVyfQouaGV4e3dpZHRoOjM4cHg7aGVpZ2h0OjM4cHg7Ym9kZXItcmFkaXVzOjEycHg7YmFja2dyb3VuZDpsaW5lYXItZ3Jh
ZGllbnQoMTM1ZGVnLHZhcigtLXYpLHZhcigtLWMpKTtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29u
dGVudDpjZW50ZXI7Zm9udC13ZWlnaHQ6OTAwO2JveC1zaGFkb3c6MCAwIDIycHggIzhiNWNmNjg4fQpoMXtmb250LXNpemU6MTlw
eDtsZXR0ZXItc3BhY2luZzo0cHg7Zm9udC13ZWlnaHQ6ODAwfQouc3Vie2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxMnB4fQou
Y2FyZHtiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCgxNjBkZWcsI2ZmZmZmZjBkLCNmZmZmZmYwNCk7Ym9kZXI6MXB4IHNv
bGlkIHZhcigtLWxpbmUpO2JvcmRlci1yYWRpdXM6MjJweDtwYWRkaW5nOjE2cHg7bWFyZ2luLXRvcDoxMnB4O2JhY2tkcm9wLWZpbHRl
cjpidWx1cigxNHB4KTtib3gtc2hhZG93OjAgMTBweCA0MHB4ICMwMDAwMDA2Nn0KLnJvd3tkaXNwbGF5OmZsZXg7Z2FwOjhweDth
bGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OnNwYWNlLWJldHdlZW59Ci5zZWd7ZGlzcGxheTpmbGV4O2dhcDo2cHg7
ZmxleC13cmFwOndyYXA7bWFyZ2luLXRvcDo4cHh9Ci5zZWcgYnV0dG9uLGlucHV0e2JhY2tncm91bmQ6I2ZmZmZmZjBhO2JvcmRl
cjoxcHggc29saWQgdmFyKC0tbGluZSk7Y29sb3I6dmFyKC0tdCk7Ym9kZXItcmFkaXVzOjEycHg7cGFkZGluZzohOHB4IDEy
cHg7Zm9udC1zaXplOjEzcHh9Ci5zZWcgYnV0dG9uLm9ue2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzNWRlZyx2YXIoLS12
KSwjMGVhNWI3KTtib3JkZXItY29sb3I6dHJhbnNwYXJlbnQ7Ym94LXNoYWRvdzowIDRweCAxNnB4ICM4YjVjZjY2Nn0KaW5wdXR7
d2lkdGg6MTAwJTttYXJnaW4tdG9wOjhweH0KbGFiZWx7Y29sb3I6dmFyKC0tbSk7Zm9udC1zaXplOjEycHh9Ci5iaWd7d2lkdGg6
MTAwJTttYXJnaW4tdG9wOjE0cHg7cGFkZGluZzoxNnB4O2JvcmRlcjowO2JvcmRlci1yYWRpdXM6MTZweDtmb250LXNpemU6MTZweDtm
b250LXdlaWdodDo3MDA7bGV0dGVyLXNwYWNpbmc6LjVweDtjb2xvcjojZmZmO2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEz
NWRlZyx2YXIoLS12KSwjMGVhNWI3KTtib3gtc2hhZG93OjAgOHB4IDI4cHggIzhiNWNmNjY2fQouYmlnLnN0b3B7YmFja2dyb3Vu
ZDpsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLCNiZTEyM2MsdmFyKC0tcikpO2JveC1zaGFkb3c6MCA4cHggMjhweCAjZmY1NTc3NTV9
Ci5lbmd7cG9zaXRpb246cmVsYXRpdmU7d2lkdGg6MjQwcHg7aGVpZ2h0OjI0MHB4O21hcmdpbjo2cHggYXV0bztjdXJzb3I6cG9p
bnters9wZXJ9Ci5lbmdzdmd7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MH0KLnNwaW57dHJhbnNmb3JtLW9yaWdpbjoxMjBweCAxMjBw
eH0KLnNjYW5uaW5nIC5zcGlue2FuaW1hdGlvbjpzcCAxLjZzIGxpbmVhciBpbmZpbml0ZX0KQGtleWZyYW1lcyBzcHt0b3t0cmFu
c2Zvcm06cm90YXRlKDM2MGRlZyl9fQouY3Rye3Bvc2l0aW9uOmFic29sdXRlO2luc2V0OjM0cHg7Ym9yZGVyLXJhZGl1czo1MCU7
ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRl
cjt0ZXh0LWFsaWduOmNlbnRlcjtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChjaXJjbGUsIzFhMTQ1MCwjMGEwYTIyIDcyJSl9
Ci5pY3tmb250LXNpemU6NDRweDtsaW5lLWhlaWdodDoxfQouZHtmb250LXNpemU6MjZweDtmb250LXdlaWdodDo4MDA7bWFyZ2lu
LXRvcDoycHh9Ci51cHtjb2xvcjp2YXIoLS1nKX0uZG57Y29sb3I6dmFyKC0tcil9Lm50e2NvbG9yOnZhcigtLXkpfQouZ2xvd3Vw
IC5jdHJ7Ym94LXNoYWRvdzowIDAgNTBweCAjM2ZmMmEwNjYgaW5zZXQsMCAwIDQwcHggIzNmZjJhMDQ0fQouZ2xvd2RuIC5jdHJ7
Ym94LXNoYWRvdzowIDAgNTBweCAjZmY1NTc3NjYgaW5zZXQsMCAwIDQwcHggI2ZmNTU3NzQ0fQoubWluaXtkaXNwbGF5OmZsZXg7
Z2FwOjhweDttYXJnaW4tdG9wOjhweH0KLm1pbmkgZGl2e2ZsZXg6MTtiYWNrZ3JvdW5kOiNmZmZmZmYwODtib3JkZXI6MXB4IHNv
bGlkIHZhcigtLWxpbmUpO2JvcmRlci1yYWRpdXM6MTRweDtwYWRkaW5nOjhweDt0ZXh0LWFsaWduOmNlbnRlcn0KLm1pbmkgYntk
aXNwbGF5OmJsb2NrO2ZvbnQtc2l6ZToxNnB4fQouZ3JpZHtkaXNwbGF5OmdyaWQ7Z3JpZC10ZW1wbGF0ZS1jb2x1bW5zOjFmciAx
ZnI7Z2FwOjEwcHg7bWFyZ2luLXRvcDoxMHB4fQoucGMye2JhY2tncm91bmQ6I2ZmZmZmZjA4O2JvcmRlcjoxcHggc29saWQgdmFy
KC0tbGluZSk7Ym9yZGVyLXJhZGl1czoxNnB4O3BhZGRpbmc6MTFweDtjdXJzb3I6cG9pbnRlcjt0cmFuc2l0aW9uOi4xNXN9Ci5w
YzIgYntmb250LXNpemU6MTRweH0KLnBjMi5zZWx7Ym9yZGVyLWNvbG9yOnZhcigtLXYpO2JveC1zaGFkb3c6MCAwIDAgMXB4IHZh
cigtLXYpLDAgNnB4IDIwcHggIzhiNWNmNjU1fQoucGMyLnVwe2JvcmRlci1jb2xvcjp2YXIoLS1nKTtib3gtc2hhZG93IzAgMCAw
IDFweCB2YXIoLS1nKSwwIDAgMjJweCAjM2ZmMmEwNTV9Ci5wYzIuZG57Ym9yZGVyLWNvbG9yOnZhcigtLXIpO2JveC1zaGFkb3c6
MCAwIDAgMXB4IHZhcigtLXIpLDAgMCAyMnB4ICNmZjU1Nzc1NX0KLmFye2ZvbnQtc2l6ZToyMHB4O2ZvbnQtd2VpZ2h0OjkwMDth
bmltYXRpb246Ym4gMXMgZWFzZS1pbi1vdXQgaW5maW5pdGV9CkBrZXlmcmFtZXMgYm57NTAle3RyYW5zZm9ybTp0cmFuc2xhdGVZ
KC0zcHgpfX0KLnN0ZXBzIGRpdntwYWRkaW5nOjVweCAwO2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxNHB4fS5zdGVwcyAub2t7
Y29sb3I6dmFyKC0tdCl9LnN0ZXBzIC5vazphZnRlcntjb250ZW50OiIg4pyTIjtjb2xvcjp2YXIoLS1nKX0KLnRibCBkaXZ7ZGlz
cGxheTpmbGV4O2p1c3RpZnktY29udGVudDpzcGFjZS1iZXR3ZWVuO3BhZGRpbmc6OHB4IDA7Ym9yZGVyLWJvdHRvbToxcHggc29s
aWQgdmFyKC0tbGluZSk7Zm9udC1zaXplOjE0cHh9Ci50YWJ7ZGlzcGxheTpub25lfS50YWIub257ZGlzcGxheTpibG9ja30KbmF2
e3Bvc2l0aW9uOmZpeGVkO2JvdHRvbTowO2xlZnQ6MDtyaWdodDowO2Rpc3BsYXk6ZmxleDtiYWNrZ3JvdW5kOiMwODBhMWNkZDti
YWNrZHJvcC1maWx0ZXI6Ymx1cigxNHB4KTtib3JkZXItdG9wOjFweCBzb2xpZCB2YXIoLS1saW5lKTtwYWRkaW5nLWJvdHRvbTpl
bnYoc2FmZS1hcmVhLWluc2V0LWJvdHRvbSl9Cm5hdiBidXR0b257ZmxleDoxO2JhY2tncm91bmQ6MDtib3JkZXI6MDtjb2xvcjp2
YXIoLS1tKTtwYWRkaW5nOjEzcHggMDtmb250LXNpemU6MTJweH0KbmF2IGJ1dHRvbi5vbntjb2xvcjp2YXIoLS1jKX0KLndhcm57
Zm9udC1zaXplOjExcHg7Y29sb3I6dmFyKC0tbSk7bWFyZ2luLXRvcDoxNHB4fQouYmFkZ2V7Zm9udC1zaXplOjExcHg7cGFkZGlu
Zzo0cHggMTBweDtib3JkZXItcmFkaXVzOjIwcHg7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1saW5lKTtjb25vcjp2YXIoLS15KX0K
LmJhZGdlLmxpdmV7Y29sb3I6dmFyKC0tZyl9Ci5zdGF0e2ZvbnQtc2l6ZToyOHB4O2ZvbnQtd2VpZ2h0OjgwMDtjb2xvcjp2YXIo
LS1jKX0KLmhyb3d7Y3Vyc29yOnBvaW50ZXJ9CiNwb3B7cG9zaXRpb246Zml4ZWQ7aW5zZXQ6MDtiYWNrZ3JvdW5kOiMwMDBjO2Rp
c3BsYXk6bm9uZTthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRlcjt6LWluZGV4Ojk7cGFkZGluZzoyMHB4
fQojcG9wLm9ue2Rpc3BsYXk6ZmxleH0KLnBje3dpZHRoOjEwMCU7bWF4LXdpZHRoOjM4MHB4O2JhY2tncm91bmQ6bGluZWFyLWdy
YWRpZW50KDE2MGRlZywjMjQxYTcwLCMwYjBhMjUpO2JvcmRlcjoxcHggc29saWQgdmFyKC0tdik7Ym9yZGVyLXJhZGl1czoyNHB4
O3BhZGRpbmc6MjJweDt0ZXh0LWFsaWduOmNlbnRlcjtiY3gtc2hhZG93OjAgMCA2MHB4ICM4YjVjZjY2Nn0KLnBjIC5kaXJ7Zm9u
dC1zaXplOjQ2cHg7Zm9udC13ZWlnaHQ6OTAwO21hcmdpbjo2cHggMH0KLnBjIC50bXtmb250LXNpemU6MzhweDtmb250LXdlaWdo
dDo4MDA7Y29sb3I6dmFyKC0tYyk7dGV4dC1zaGFkb3c6MCAwIDE4cHggIzVlZWFkNDk5fQoKYnV0dG9ue3Bvc2l0aW9uOnJlbGF0
aXZlO292ZXJmbG93OmhpZGRlbjt0cmFuc2l0aW9uOnRyYW5zZm9ybSAuMTJzLGJveC1zaGFkb3cgLjJzLGJhY2tncm91bmQgLjJz
fQpidXR0b246YWN0aXZle3RyYW5zZm9ybTpzY2FsZSguOTQpfQoucmlwe3Bvc2l0aW9uOmFic29sdXRlO2JvcmRlci1yYWRpdXM6
NTAlO2JhY2tncm91bmQ6I2ZmZmZmZjU1O3RyYW5zZm9ybTpzY2FsZSgwKTthbmltYXRpb246cnAgLjZzIGVhc2Utb3V0O3BvaW50
ZXItZXZlbnRzOm5vbmV9CkBrZXlmcmFtZXMgcnB7dG97dHJhbnNmb3JtOnNjYWxlKDEpO29wYWNpdHk6MH19CiNnbzpub3QoLnN0
b3Ape2FuaW1hdGlvbjpiciAyLjRzIGVhc2UtaW4tb3V0IGluZmluaXRlfQpAa2V5ZnJhbWVzIGJyezUwJXtib3gtc2hhZG93OjAg
OHB4IDQycHggIzIyZDNlZWFhfX0KLnRhYi5vbnthbmltYXRpb246dGluIC4zNXMgZWFzZX0KQGtleWZyYW1lcyB0aW57ZnJvbXtv
cGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTJweCl9fQouY2FyZHthbmltYXRpb246Y2luIC41NXMgZWFzZSBib3RofQou
Y2FyZDpudGgtY2hpbGQoMil7YW5pbWF0aW9uLWRlbGF5Oi4wN3N9LmNhcmQ6bnRoLWNoaWxkKDMpe2FuaW1hdGlvbi1kZWxheTou
MTRzfS5jYXJkOm50aC1jaGlsZCg0KXthbmltYXRpb24tZGVsYXk6LjIxc30KQGtleWZyYW1lcyBjaW57ZnJvbXtvcGFjaXR5OjA7
dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTZweCkgc2NhbGUoLjk4KX19Ci5wYzI6aG92ZXJ7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoLTJw
eCl9LnBjMjphY3RpdmV7dHJhbnNmb3JtOnNjYWxlKC45NSl9Ci5oZXh7YW5pbWF0aW9uOmh4IDRzIGVhc2UtaW4tb3V0IGluZmlu
aXRlfQpAa2V5ZnJhbWVzIGh4ezUwJXtib3gtc2hhZG93OjAgMCAzNHB4ICM1ZWVhZDRhYTt0cmFuc2Zvcm06cm90YXRlKDhkZWcp
fX0KLmVuZy5ndXtjb2xvcjp2YXIoLS1nKX0uZW5nLmdke2NvbG9yOnZhcigtLXIpfQouZW5nLmJ1cnN0OmFmdGVye2NvbnRlbnQ6
IiI7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MjBweDtib3JkZXItcmFkaXVzOjUwJTtib3JkZXI6M3B4IHNvbGlkIGN1cnJlbnRD
b2xvcjthbmltYXRpb246d2F2ZSAuOXMgZWFzZS1vdXQ7cG9pbnRlci1ldmVudHM6bm9uZX0KLmVuZy5idXJzdCAjaWMsLmVuZy5i
dXJzdCAuZHthbmltYXRpb246cG9wIC41NXMgY3ViaWMtYmV6aWVyKC4yLDEuNiwuNCwxKX0KQGtleWZyYW1lcyB3YXZle2Zyb217
dHJhbnNmb3JtOnNjYWxlKC44KTtvcGFjaXR5Oi45fXRve3RyYW5zZm9ybTpzY2FsZSgxLjQpO29wYWNpdHk6MH19CkBrZXlmcmFt
ZXMgcG9we2Zyb217dHJhbnNmb3JtOnNjYWxlKC4zKTtvcGFjaXR5OjB9fQouZW5nLnNoYWtle2FuaW1hdGlvbjpzaCAuNXN9CkBr
ZXlmcmFtZXMgc2h7MjAlLDYwJXt0cmFuc2Zvcm06dHJhbnNsYXRlWCgtOXB4KX00MCUsODAle3RyYW5zZm9ybTp0cmFuc2xhdGVY
KDlweCl9fQoubGl2ZXtmb250LXNpemU6MTBweDtjb2xvcjp2YXIoLS1nKTttYXJnaW4tbGVmdDo2cHg7Zm9udC13ZWlnaHQ6NzAw
fQoubGl2ZSBpe2Rpc3BsYXk6aW5saW5lLWJsb2NrO3dpZHRoOjdweDtoZWlnaHQ6N3B4O2JvcmRlci1yYWRpdXM6NTAlO2JhY2tn
cm91bmQ6dmFyKC0tZyk7bWFyZ2luLXJpZ2h0OjRweDthbmltYXRpb246cGwgMS4ycyBpbmZpbml0ZX0KQGtleWZyYW1lcyBwbHs1
MCV7b3BhY2l0eTouMjU7dHJhbnNmb3JtOnNjYWxlKDEuNyl9fQouY3B4e2ZvbnQtc2l6ZToyMnB4O2ZvbnQtd2VpZ2h0OjgwMH0K
LmNweC5mdXthbmltYXRpb246ZnUgLjdzfS5jcHguZmR7YW5pbWF0aW9uOmZkIC43c30KQGtleWZyYW1lcyBmdXswJXtjb2xvcjp2
YXIoLS1nKTt0ZXh0LXNoYWRvdzowIDAgMTZweCB2YXIoLS1nKX19CkBrZXlmcmFtZXMgZmR7MCV7Y29sb3I6dmFyKC0tcik7dGV4
dC1zaGFkb3c6MCAwIDE2cHggdmFyKC0tcil9fQouY217cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MDtkaXNwbGF5OmZsZXg7YWxp
Z24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7dGV4dC1hbGlnbjpjZW50ZXI7cGFkZGluZzoxMnB4O2NvbG9y
OnZhcigtLW0pO2ZvbnQtc2l6ZToxM3B4O2JhY2tncm91bmQ6IzBhMGIxY2NjO2JvcmRlci1yYWRpdXM6MTJweH0KQG1lZGlhIChw
cmVmZXJzLXJlZHVjZWQtbW90aW9uOnJlZHVjZSl7KnthbmltYXRpb246bm9uZSFpbXBvcnRhbnQ7dHJhbnNpdGlvbjpub25lIWlt
cG9ydGFudH19CgouY2FyZCxuYXZ7YmFja2Ryb3AtZmlsdGVyOm5vbmUhaW1wb3J0YW50Oy13ZWJraXQtYmFja2Ryb3AtZmlsdGVy
Om5vbmUhaW1wb3J0YW50fQpuYXZ7YmFja2dyb3VuZDojMDgwYTFjIWltcG9ydGFudH0KLmNhcmR7Ym94LXNoYWRvdzpub25lIWlt
cG9ydGFudDthbmltYXRpb246Y2luIC4zNXMgZWFzZSBib3RofQojZ286bm90KC5zdG9wKSwuaGV4e2FuaW1hdGlbjpub25lIWlt
cG9ydGFudH0KCi5vcmJ7cG9zaXRpb246Zml4ZWQ7d2lkdGg6MzQwcHg7aGVpZ2h0OjM0MHB4O2JvcmRlci1yYWRpdXM6NTAlO3Bv
aW50ZXItZXZlbnRzOm5vbmU7ei1pbmRleDotMTtvcGFjaXR5Oi41NX0KLm8xe2JhY2tncm91bmQ6cmFkaWFsLWdyYWRpZW50KGNp
cmNsZSwjN2MzYWVkNjYsdHJhbnNwYXJlbnQgNzAlKTt0b3A6LTgwcHg7bGVmdDotMTAwcHg7YW5pbWF0aW9uOmZsMSAxOHMgZWFz
ZS1pbi1vdXQgaW5maW5pdGUgYWx0ZXJuYXRlfQoubzJ7YmFja2dyb3VuZDpyYWRpYWwtZ3JhZGllbnQoY2lyY2xlLCMwNmI2ZDQ1
NSx0cmFuc3BhcmVudCA3MCUpO2JvdHRvbTo2MHB4O3JpZ2h0Oi0xMjBweDthbmltYXRpb246ZmwyIDIycyBlYXNlLWluLW91dCBp
bmZpbml0ZSBhbHRlcm5hdGV9CkBrZXlmcmFtZXMgZmwxe3Rve3RyYW5zZm9ybTp0cmFuc2xhdGUoMTIwcHgsMTYwcHgpfX0KQGtl
eWZyYW1lcyBmbDJ7dG97dHJhbnNmb3JtOnRyYW5zbGF0ZSgtMTAwcHgsLTE0MHB4KX19CiNmeHtwb3NpdGlvbjpmaXhlZDtpbnNl
dDowO3dpZHRoOjEwMCU7aGVpZ2h0OjEwMCU7cG9pbnRlci1ldmVudHM6bm9uZTt6LWluZGV4Ojh9Ci5zd2VlcHtwb3NpdGlvbjph
YnNvbHV0ZTtpbnNldDoxMHB4O2JvcmRlci1yYWRpdXM6NTAlO2JhY2tncm91bmQ6Y29uaWMtZ3JhZGllbnQoZnJvbSAwZGVnLHRy
YW5zcGFyZW50IDAgMjkwZGVnLCM1ZWVhZDQ2JiAzNjBkZWcpO29wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNpdHkgLjNzfQouc2Nh
bm5pbmcgLnN3ZWVwe29wYWNpdHk6MTthbmltYXRpb246c3AgMS42cyBsaW5lYXIgaW5maW5pdGV9CiNsb2Nre3Bvc2l0aW9uOmZp
eGVkO2luc2V0OjA7ei1pbmRleDoyMDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50
ZXI7cGFkZGluZzoyNHB4O2JhY2tncm91bmQ6cmFkaWFsLWdyYWRpZW50KGNpcmNsZSBhdCAyMCUgMTAlLCMzMzE2N2EsdHJhbnNw
YXJlbnQgNTAlKSxyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDkwJSA5MCUsIzA4NTY2ZSx0cmFuc3BhcmVudCA0NSUpLCMwNTA2
MGZ9CiNsb2NrLm91dHthbmltYXRpb246bG91dCAuNjVzIGVhc2UgZm9yd2FyZHN9CkBrZXlmcmFtZXMgbG91dHt0b3tvcGFjaXR5
OjA7dHJhbnNmb3JtOnNjYWxlKDEuMTUpO3Zpc2liaWxpdHk6aGlkZGVufX0KLmxre3dpZHRoOjEwMCU7bWF4LXdpZHRoOjMzMHB4
O3RleHQtYWxpZ246Y2VudGVyO2FuaW1hdGlvbjpjaW4gLjdzIGVhc2UgYm90aH0KLmxrLnNoYWtle2FuaW1hdGlvbjpzaCAuNXN9
Ci5sayAuaGV4e3dpZHRoOjc2cHg7aGVpZ2h0Ojc2cHg7bWFyZ2luOjAgYXV0byAxNnB4O2ZvbnQtc2l6ZTozMnB4O2JvcmRlci1y
YWRpdXM6MjRweDthbmltYXRpb246aHggNHMgZWFzZS1pbi1vdXQgaW5maW5pdGV9Ci5sayBoMXttYXJnaW4tYm90dG9tOjRweH0K
LmxrIGlucHV0e3RleHQtYWxpZ246Y2VudGVyO2xldHRlci1zcGFjaW5nOjEwcHg7Zm9udC1zaXplOjI0cHg7cGFkZGluZzoxNHB4
O21hcmdpbi10aW9jOjIycHh9Ci5sayBpbnB1dDpmb2N1c3tvdXRsaW5lOjA7Ym9yZGVyLWNvbG9yOnZhcigtLW0pO2JveC1zaGFkb3c6
MCAwIDAgM3B4ICM4YjVjZjY1NX0KPC9zdHlsZT48L2hlYWQ+PGJvZHk+PGRpdiBjbGFzcz0ib3JiIG8xIj48L2Rpdj48ZGl2IGNs

YXNzPSJvcmIgbzIiPjwvZGl2PjxjYW52YXMgaWQ9ImZ4Ij48L2NhbnZhcj4KPGRpdiBpZD0ibG9jayI+PGRpdiBjbGFzcz0ibGsi
PjxkaXYgY2xhc3M9ImhleCI+SDwvZGl2PjxoMT5IRUxJWCBCT1RJQzwvaDE+PGRpdiBjbGFzcz0ic3ViIj5FbnRlciB5b3VyIGFj
Y2VzcyBrZXkgdG8gY29udGludWU8L2Rpdj48aW5wdXQgaWQ9InB3IiB0eXBlPSJwYXNzd29yZCIgaW5wdXRtb2RlPSJudW1lcmlj
IiBwbGFjZWhvbGRlcj0i4oCi4oCi4oCi4iIG1heGxlbmd0aD0iMTIiIGF1dG9jb21wbGV0ZT0ib2ZmIj48YnV0dG9uIGlkPSJs
ZyIgY2xhc3M9ImJpZyI+VU5MT0NLPC9idXR0b24+PGRpdiBpZD0ibGVyciIgY2xhc3M9InN1YiIgc3R5bGU9ImNvbG9yOnZhcigt
LXIpO21pbi1oZWlnaHQ6MjBweDttYXJnaW4tdG9wOjEwcHgiPjwvZGl2PjwvZGl2PjwvZGl2Pgo8ZGl2IGNsYXNzPSJ3Ij4K
PGRpdiBjbGFzcz0icm93Ij48ZGl2IGNsYXNzPSJsb2dvIj48ZGl2IGNsYXNzPSJoZXgiPkg8L2Rpdj48ZGl2PjxoMT5IRUxJWCBC
T1RJQzwvaDE+PGRpdiBjbGFzcz0ic3ViIj5JbmRpY2F0b3ItYmFzZWQgbWFya2V0IGFuYWx5c2lzPC9kaXY+PC9kaXY+PC9kaXY+
PHNwYW4gaWQ9Im1vZGUiIGNsYXNzPSJiYWRnZSI+4oCmPC9zcGFuPjwvZGl2PgoKPGRpdiBpZD0idC1kYXNoIiBjbGFzcz0idGFi
IG9uIj4KIDxkaXYgY2xhc3M9ImNhcmQiPgogIDxsYWJlbD5UaW1lZnJhbWU8L2xhYmVsPgogIDxkaXYgY2xhc3M9InNlZyIgaWQ9
InRmIj48YnV0dG9uIGRhdGEtdj0iNSI+NXM8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMTAiPjEwczwvYnV0dG9uPjxidXR0b24g
ZGF0YS12PSIzMCI+MzBzPC9idXR0b24+PGJ1dHRvbiBjbGFzcz0ib24iIGRhdGEtdj0iNjAiPjFtPC9idXR0b24+PGJ1dHRvbiBk
YXRhLXY9IjE4MCI+M208L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMzAwIj5JbTwvYnV0dG9uPjxidXR0b24gZGF0YS12PSI5MDAi
PjE1bTwvYnV0dG9uPjwvZGl2PgogIDxsYWJlbCBzdHlsZT0iZGlzcGxheTpibG9jazttYXJnaW4tdG9wOjEycHgiPlNpZ25hbCBm
aWx0ZXI8L2xhYmVsPgogIDxkaXYgY2xhc3M9InNlZyIgaWQ9InJrIj48YnV0dG9uIGRhdGEtdj0iMSI+U3RyaWN0PC9idXR0b24+
PGJ1dHRvbiBjbGFzcz0ib24iIGRhdGEtdj0iMiI+QmFsYW5jZWQ8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMyI+QWN0aXZlPC9i
dXR0b24+PC9kaXY+CiAgPGRpdiBjbGFzcz0ic3ViIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgiPlN0cmljdDogNCBvZiA1IGluZGlj
YXRvcnMgYWdyZWUsIG5vbmUgb3Bwb3NlLiBCYWxhbmNlZDogMyBvZiA1LiBCb3RoIGFsc28gbmVlZCB0aGUgaGlnaGVyLXRpbWVm
cmFtZSB0cmVuZCwgYSBjb25maXJtaW5nIGNhbmRsZSBhbmQgbm9ybWFsIHZvbGF0aWxpdHkuIEFjdGl2ZTogbWFqb3JpdHkgb2Yg
NSBvbmx5LjwvZGl2Pgr9CiA8L2Rpdi4KIDxkaXYgY2xhc3M9ImNhcmQiPjxkaXYgY2xhc3M9InJvdyI+PGI+U2lnbmFsIGVuZ2luZTwv
Yj48c3BhbiBjbGFzcz0ic3ViIiBpZD0ic2VscCI+PC9zcGFuPjwvZGl2PgogIDxkaXYgY2xhc3M9ImVuZyIgaWQ9ImVuZyI+PHN2
ZyB2aWV3Qm94PSIwIDAgMjQwIDI0MCI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJnciIgdDE9IjAiIHkxPSIwIiB4Mj0iMSIg
eTI9IjEiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVlZWFkNCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0i
IzhiNWNmNiIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPgogICA8Y2lyY2xlIGN4PSIxMjAiIGN5PSIxMjAiIHI9IjEwNCIgZmlsbD0i
bm9uZSIgc3Ryb2tlPSIjZmZmZmZmMTIiIHN0cm9rZS13aWR0aD0iOCIvPgogICA8Y2lyY2xlIGlkPSJwZyIgY3g9IjEyMCIgY3k9
IjEyMCIgcj0iMTA0IiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjZ3IpIiBzdHJva2Utd2lkdGg9IjgiIHN0cm9rZS1saW5lY2Fw
PSJyb3VuZCIgc3Ryb2tlLWRhc2hhcnJheT0iNjUzLjQ1IiBzdHJva2UtZGFzaG9mZnNldD0iNjUzLjQ1IiB0cmFuc2Zvcm09InJv
dGF0ZSgtOTAgMTIwIDEyMCkiLz4KICAgPGNpcmNsZSBjbGFzcz0ic3BpbiIgY3g9IjEyMCIgY3k9IjEyMCIgcj0iMTE2IiBmaWxs
PSJub25lIiBzdHJva2U9IiM4YjVjZjYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWRhc2hhcnJheT0iNiAxNCIvPjwvc3ZnPgog
ICA8ZGl2IGNsYXNzPSJzd2VlcCI+PC9kaXY+PjxkaXYgY2xhc3M9ImN0ciI+PGRpdiBpZD0iaWMiIGNsYXNzPSJpYyI+4pqhPC9k
aXY+PGRpdiBpZD0ic2lnIiBjbGFzcz0iZCI+U1RBTkRCWTwvZGl2PjxkaXYgaWQ9InN1YiIgY2xhc3M9InN1YiI+VGFwIHRvIHN0
YXJ0PC9kaXY+PC9kaXY+PC9kaXY+CiAgPGRpdiBjbGFzcz0ibWluaSI+PGRpdj48c3BhbiBjbGFzcz0ic3ViIj5UaW1lIGxlZnQ8
L3NwYW4+PGIgaWQ9ImxlZnQiPi0tOi0tPC9iPjwvZGl2PjxkaXY+PHNwYW4gY2xhc3M9InN1YiI+U3RyZW5ndGg8L3NwYW4+PGIg
aWQ9InN0ciI+LS08L2I+PC9kaXY+PGRpdj48c3BhbiBjbGFzcz0ic3ViIj5QcmljZTwvc3Bhbj48YiBpZD0icHgiPi0tPC9iPjwv
ZGl2PjwvZGl2PgogIDxidXR0b24gaWQ9ImdvIiBjbGFzcz0icmlnIj7ilrYgU1RBUlQgQk9UPC9idXR0b24+PC9kaXY+CiA8ZGl2
IGNsYXNzPSJjYXJkIj48ZGl2IGNsYXNzPSJyb3ciPjxkaXY+PGIgaWQ9ImNuIj4tLTwvYj48c3BhbiBjbGFzcz0ibGl2ZSI+PGk+
PC9pPkxJVkU8L3NwYW4+PGRpdiBjbGFzcz0ic3ViIiBpZD0iY2kiPjwvZGl2PjwvZGl2PjxkaXYgc3R5bGU9InRleHQtYWxpZ246
cmlnaHQiPjxkaXYgaWQ9ImNweCIgY2xhc3M9ImNweCI+LS08L2Rpdj48ZGl2IGlkPSJjY2giIGNsYXNzPSJzdWIiPjwvZGl2Pjwv
ZGl2PjwvZGl2PgogIDxkaXYgc3R5bGU9InBvc2l0aW9uOnJlbGF0aXZlO21hcmdpbi10b3A6OHB4Ij48Y2FudmFzIGlkPSJjdiIg
c3R5bGU9IndpZHRoOjEwMCU7aGVpZ2h0OjIxMHB4O2Rpc3BsYXk6YmxvY2siPjwvY2FudmFzPjxkaXYgaWQ9ImNtIiBjbGFzcz0i
Y20iPkxvYWRpbmcgbGl2ZSBwcmljZeKApjwvZGl2PjwvZGl2PjwvZGl2PgogPGRpdiBjbGFzcz0iY2FyZCI+PGRpdiBjbGFzcz0i
cm93Ij48Yj5NYXJrZXRzPC9iPjxkaXYgY2xhc3M9InNlZyIgaWQ9ImdwIiBzdHlsZT0ibWFyZ2luOjAiPjxidXR0b24gZGF0YS12
PSJmeCI+Rm9yZXg8L2J1dHRvbj48YnV0dG9uIGNsYXNzPSJvbiIgZGF0YS12PSJjciI+Q3J5cHRvPC9idXR0b24+PC9kaXY+PC9k
aXY+PGRpdiBjbGFzcz0iZ3JpZCIgaWQ9Im1rdCI+PC9kaXY+PGRpdiBjbGFzcz0ic3ViIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgi
PlRhcCBhIG1hcmtldCB0byBzZWxlY3QgaXQuIFRoZSBhcnJvdyBzaG93cyB0aGUgbGl2ZSBzaWduYWwuPC9kaXY+PC9kaXY+CiAg
PGRpdiBjbGFzcz0ic2FyZCI+PGI+TWFya2V0IHNjYW5uZXI8L2I+PGRpdiBjbGFzcz0ic3RlcHMi idD0ic3RlcHMiPjwvZGl2
PjwvZGl2PgogPGRpdiBjbGFzcz0iY2FyZCI+PGI+SW5kaWNhdG9yczwvYj48ZGl2IGNsYXNzPSJ0YmwiIGlkPSJpbmQiPjxkaXY+
PHNwYW4+V2FpdGluZyBmb3IgYSBzY2FuPC9zcGFuPjwvZGl2PjwvZGl2PjwvZGl2Pgo8L2Rpdi4KCTwvZGl2PgpyZXN0CgpkGl2
IGlkPSJ0LWhpc3QiIGNsYXNzPSJ0YWIiPjxkaXYgY2xhc3M9ImNhcmQiPjxiPkhpc3Rvcnk8L2I+PGRpdiBjbGFzcz0idGJsIiBp
ZD0iaGlzdCI+PC9kaXY+PC9kaXY+PC9kaXY+CjxkaXYgaWQ9InQtYW4iIGNsYXNzPSJ0YWIiPjxkaXYgY2xhc3M9ImNhcmQiPjxi
PllvdXIgcmVhbCByZXN1bHRzPC9iPjxkaXYgY2xhc3M9InN1YiI+Q291bnRlZCBvbmx5IGZyb20gc2lnbmFscyB0aGlzIGFwcCBs
b2dnZWQgYW5kIGNoZWNrZWQgYWdhaW5zdCBwcmljZSB3aGVuIHRoZSB0aW1lZnJhbWUgZW5kZWQuPC9kaXY+CiAgPGRpdiBjbGFz
cz0icm93IiBzdHlsZT0ibWFyZ2luLXRvcDoxMHB4Ij48ZGl2PjxkaXYgY2xhc3M9InN0YXQiIGlkPSJhdyI+MDwvZGl2PjxkaXYg
Y2xhc3M9InN1YiI+V2luczwvZGl2PjwvZGl2PjxkaXY+PGRpdiBjbGFzcz0ic3RhdCIgaWQ9ImFsIj4wPC9kaXY+PGRpdiBjbGFz
cz0ic3ViIj5Mb3NzZXM8L2Rpdj48L2Rpdj48ZGl2PjxkaXYgY2xhc3M9InN0YXQiIGlkPSJhciI+LS08L2Rpdj48ZGl2IGNsYXNz
PSJzdWIiPldpbiByYXRlPC9kaXY+PC9kaXY+PC9kaXY+CiAgPGRpdiBjbGFzcz0ic3ViIiBpZD0ic3RrIiBzdHlsZT0ibWFyZ2lu
LXRvcDoxMnB4Ij48L2Rpdj48ZGl2IGNsYXNzPSJ0YmwiIGlkPSJieXAiIHN0eWxlPSJtYXJnaW4tdG9wOjEwcHgiPjwvZGl2Pjxi
dXR0b24gaWQ9ImV4cCIgY2xhc3M9ImJpZyIgc3R5bGU9InBhZGRpbmc6MTBweDtmb250LXNpemU6MTRweCI+RG93bmxvYWQgaGlz
dG9yeSAoQ1NWKTwvYnV0dG9uPgogIDxidXR0b24gaWQ9ImNsciIgY2xhc3M9ImJpZyBzdG9wIiBzdHlsZT0icGFkZGluZzoxMHB4
O2ZvbnQtc2l6ZToxNHB4Ij5DbGVhciBoaXN0b3J5PC9idXR0b24+PC9kaXY+PC9kaXY+CjxkaXYgaWQ9InQtc2V0IiBjbGFzcz0i
dGFiIj48ZGl2IGNsYXNzPSJjYXJkIj48Yj5QcmVmZXJlbmNlczwvYj48bGFiZWwgc3R5bGU9ImRpc3BsYXk6YmxvY2s7bWFyZ2lu
LXRvcDoxMHB4Ij5Tb3VuZCBhbmQgdmlicmF0aW9uIG9uIHNpZ25hbHM8L2xhYmVsPjxkaXYgY2xhc3M9InNlZyIgaWQ9InNuIj48
YnV0dG9uIGRhdGEtdj0ib24iPk9uPC9idXR0b24+PGJ1dHRvbiBkYXRhLXY9Im9mZiI+T2ZmPC9idXR0b24+PC9kaXY+PGxhYmVs
IHN0eWxlPSJkaXNwbGF5OmJsb2NrO21hcmdpbi10b3A6MTJweCI+U3RvcCB0aGUgYm90IGFmdGVyIGxvc3NlcyBpbiBhIHJvdzwv
bGFiZWw+PGRpdiBjbGFzcz0ic2VnIiBpZD0ibWwiPjxidXR0b24gZGF0YS12PSIwIj5PZmY8L2J1dHRvbj48YnV0dG9uIGRhdGEt
diI9IjIiPjI8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMyI+MzwvYnV0dG9uPjxidXR0b24gZGF0YS12PSI1Ij41PC9idXR0b24+
PC9kaXY+PGJ1dHRvbiBpZD0ibG8iIGNsYXNzPSJiaWcgc3RvcCIgc3R5bGU9InBhZGRpbmc6MTBweDtmb250LXNpemU6MTRweCI+
TG9nIG91dDwvYnV0dG9uPjwvZGl2PjxkaXYgY2xhc3M9ImNhcmQiPjxiPkFib3V0PC9iPjxwIGNsYXNzPSJzdWIiIHN0eWxlPSJt
YXJnaW4tdG9wOjhweCI+SEVM<span>IXQgYm90aWMgaXMgaW50ZWxsaWdlbnQgdHJhZGluZyBhbmFseXNlcyB0b29sIHVzaW5n
IHJlYWwtdGltZSBxdW90ZXggZmluaWNhbCBtYXJrZXQgZmVlZHMgZm9yIGZvcmV4IGFuZCBiaW5hbmNlIGZvciBjcnlwdG8u
IEl0IHNjb3JlcyA1IGluZGljYXRvcnMgdG8gcHJvdmlkZSBoaWdoLXB1cml0eSB0cmVuZCBzaWduYWxzLjwvcD48L2Rpdj48L2Rp
dj4KPHRpdCBpZD0icG9wIj48ZGl2IGNsYXNzPSJwYyI+PGRpdiBjbGFzcz0ic3ViIj5TSUdOQUwgQUxFUlQ8L2Rpdj48ZGl2IGlk
PSJwcCIgc3R5bGU9ImZvbnQtd2VpZ2h0OjcwMDttYXJnaW4tdG9wOjZweCI+PC9kaXY+PGRpdiBpZD0icGQiIGNsYXNzPSJkaXIi
PjwvZGl2PjxkaXYgaWQ9InBpIiBjbGFzcz0ic3ViIj48L2Rpdj48ZGl2IGNsYXNzPSJzdWIiIHN0eWxlPSJtYXJnaW4tdG9wOjEy
cHgiPlRha2UgdHJhZGUgYXQ8L2Rpdj48ZGl2IGlkPSJwdCIgY2xhc3M9InRtIj48L2Rpdj48ZGl2IGlkPSJwdyIgY2xhc3M9InN1
YiI+PC9kaXY+PGJ1dHRvbiBjbGFzcz0iYmlnIiBpZD0iY2siPkdPVyBJVDwvYnV0dG9uPjwvZGl2PjwvZGl2Pg==CjxuYXY+PGJ1
dHRvbiBjbGFzcz0ib24iIGRhdGEtdD0iZGFzaCI+RGFzaGJvYXJkPC9idXR0b24+PGJ1dHRvbiBkYXRhLXQ9Imhpc3QiPkhpc3Rv
cnk8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iYW4iPkFuYWx5dGljczwvYnV0dG9uPjxidXR0b24gZGF0YS10PSJzZXQiPkFib3V0
PC9idXR0b24+PC9uYXY+Cgo8c2NyaXB0Pgpjb25zdCAkPXM9PmRvY3VtZW50LnF1ZXJ5U2VsZWN0b3Iocyk7CmNvbnN0IEZYPVsn
RVVSL1VTRCcsJ0dCUi9VU0QnLCdVU0QvSlBZJywnVVNEL0NBRCcsJ1VTRC9DSEYnLCdFVVIvR0JQJywnRVVSL0pQWScsJ0VVUi9D
SEYnLCdFVVIvQ0FEJ107CmNvbnN0IENSPVsnQlRDVVNEVCcsJ0VUSFVTRFQnLCdCTkJVU0RUJywnU09MVVNEVCcsJ1hSUFVTRFQn
LCdET0dFVVNEVCddOwpjb25zdCBpc0Z4PShwKT0+cC5pbmNsdWRlcygnLycpLG5tPShwKT0+cix0Zkw9KHQpPT50PDYwP3QrJ3Mn
OnQvNjArJ20nLEM9NjUzLjQ1Owpjb25zdCBmbXQ9KGEpPT5hLnRvRml4ZWQoYTwyPzU6YTwxMDA5OjM6Mik7CmNvbnN0IG1tc3M9
KHMpPT5TdHJpbmcoTWF0aC5mbG9vcihzLzYwKSkucGFkU3RhcnQoMiwnMCcpKyc6JytTdHJpbmcocyU2MCkucGFkU3RhcnQo
MiwnMCcpOwpjb25zdCBzbGVlcD0obXNzKT0+bmV3IFByb21pc2Uoci0+c2V0VGltZW91dChyLG1zKSk7CmxlZCBTPXttazon
bGl2ZScsdGY6NjAscms6MixydW46ZmFsc2UsZ3JwOidjcicscGFpcjonQlRDVVNEVCcsaGlzdDpbXSxweDp7fSxjYjp7fSxzcDp7
fSxzaWc6bnVsbCxzbmQ6J29uJyxtYXhMOjN9OwpsZXQgS0VZPScnO3RyeXtLRVk9bG9jYWxTdG9yYWdlLmdldEl0ZW0oJ2hrJyl8
fCcnO1MuaGlzdD1KU09OLnBhcnNlKGxvY2FsU3RvcmFnZS5nZXRJdGVtKCdoYjInKXx8J1tdJykuZmlsdGVyKGg9PmgubWshPT0n
ZGVtbycpfWNhdGNoKGUpe30KUy5oaXN0LmZvckVhY2goaD0+e2lmKCFoLnJlcyloLnJlcz0ndm9pZCd9KTsKY29uc3Qgc2F2ZT0o
KT0+e3RyeXtsb2NhbFN0b3JhZ2Uuc2V0SXRlbSgnaGIyJyxKU09OLnN0cmluZ2lmeShTLmhpc3QpKX1jYXRjaChlKXt9fTsKY29u
c3Qgc2F2ZVNldD0oKT0+e3RyeXtsb2NhbFN0b3JhZ2Uuc2V0SXRlbSgnaHhfc2V0JyxKU09OLnN0cmluZ2lmeSh7c25kOlMuc25k
LG1heEw6Uy5tYXhMfSkpfWNhdGNoKGUpe319Owp0cnl7T2JqZWN0LmFzc2lnbihTLEpTT04ucGFyc2UobG9jYWxTdG9yYWdlLmdl
dEl0ZW0oJ2h4X3NldCcpfHwne30nKSl9Y2F0Y2goZSl7fQpjb25zdCBBQ0NFU1M9JzU1NjYnOwpmdW5jdGlvbiBzZWcoaWQsa2V5
LG51bSl7ZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChpZCsnIGJ1dHRvbicpLmZvckVhY2goYj0+Yi5vbmNsaWNrPSgpPT57ZG9j
dW1lbnQucXVlcnlTZWxlY3RvckFsbChpZCsnIGJ1dHRvbicpLmZvckVhY2goeD0+eC5jbGFzc0xpc3QucmVtb3ZlKCdvbicpKTti
LmNsYXNzTGlzdC5hZGQoJ29uJyk7U1trZXldPW51bT8rYi5kYXRhc2V0LnY6Yi5kYXRhc2V0LnY7aWYoa2V5PT09J2dycCcpe2Nv
bnN0IEw9Uy5ncnA9PT0nZngnP0ZYOkNSO2lmKCFMLmluY2x1ZGVzKFMucGFpcikpUy5wYWlyPUxbMF07JCgnI3NlbHAnKS50ZXh0
Q29udGVudD1ubShTLnBhaXIpO21hcmtldHMoKTtwcmljZXMoKX1pZihrZXk9PT0ndGYnfHxrZXk9PT0nZ3JwJyljaGFydFJlc2V0
KCk7aWYoa2V5PT09J3NuZCd8fGtleT09PSdtYXhMJylzYXZlU2V0KCl9KX0Kc2VnKCcjdGYnLCd0ZicsMSk7c2VnKCcjcmsnLCdy
aycsMSk7c2VnKCcjZ3AnLCdncnAnKTtzZWcoJyNzbicsJ3NuZCcpO3NlZygnI21sJywnbWF4TCcsMSk7CmRvY3VtZW50LnF1ZXJ5
U2VsZWN0b3JBbGwoJ25hdiBidXR0b24nKS5mb3JFYWNoKGI9PmIub25jbGljaz0oKT0+e2RvY3VtZW50LnF1ZXJ5U2VsZWN0b3JB
bGwoJ25hdiBidXR0b24sLnRhYicpLmZvckVhY2goeD0+eC5jbGFzc0xpc3QucmVtb3ZlKCdvbicpKTtiLmNsYXNzTGlzdC5hZGQo
J29uJyk7JCgnI3QtJytiLmRhdGFzZXQudCkuY2xhc3NMaXN0LmFkZCgnb24nKTtyZW5kZXIoKX0pOwpmdW5jdGlvbiBtb2RlKCl7
Y29uc3QgbT0kKCcjbW9kZScpO20udGV4dENvbnRlbnQ9J1FVT1RFWCBMSVZFREFUQSc7bS5jbGFzc05hbWU9J2JhZGdlIGxpdmUn
fQoKY29uc3QgSE9TVFM9WydodHRwczovL2FwaS5iaW5hbmNlLmNvbScsJ2h0dHBzOi8vZGF0YS1hcGkuYmluYW5jZS52aXNpb24n
LCdodHRwczovL2FwaTEuYmluYW5jZS5jb20nLCdodHRwczovL2FwaTIuYmluYW5jZS5jb20nLCdodHRwczovL2FwaTMuYmluYW5j
ZS5jb20nXTsKbGV0IEhJPTA7CmFzeW5jIGZ1bmN0aW9uIGJnZXQocGF0aCl7CiBsZXQgZXJyOwogZm9yKGxldCBrPTA7azxIT1NU
Uy5sZW5ndGg7aysrKXsKICB0cnl7Y29uc3QgYz1uZXcgQWJvcnRDb250cm9sbGVyKCksdD1zZXRUaW1lb3V0KCgpPT5jLmFib3J0
KCksNjAwMCk7CiAgIGNvbnN0IHI9YXdhaXQgZmV0Y2goSE9TVFNbKEhJK2spJUhPU1RTLmxlbmd0aF0rcGF0aCx7c2lnbmFsOmMuc2ln
bmFsfSk7Y2xlYXJUaW1lb3V0KHQpOwogICBpZighci5vayl0aHJvdyBuZXcgRXJyb3IoJ0hUVFAgJytyLnN0YXR1cyk7Y29uc3Qg
aj1hd2FpdCByLmpzb24oKTtIST0oSEkrayklSE9TVFMubGVuZ3RoO3JldHVybiBqfQogIGNhdGNoKGUpe2Vycj1lfQogfQogdGhy
b3cgZXJyOwogfQoKYXN5bmMgZnVuY3Rpb24gcXFldChwYXRoKXsKIGNvbnN0IGM9bmV3IEFib3J0Q29udHJvbGxlcigpLHQ9c2V0
VGltZW91dCgoKT0+Yy5hYm9ydCgpLDgwMDApO3RyeXtjb25zdCBqPWF3YWl0IChhd2FpdCBmZXRjaChodHRwczovL2FwaS5x
dW90ZXguY29tLyArIHBhdGgse3NpZ25hbDpjLnNpZ25hbH0pKS5qc29uKCk7cmV0dXJuIGp9ZmFubHl7Y2xlYXJUaW1lb3V0
KHR9fQoKYXN5bmMgZnVuY3Rpb24ga2woc3ltLGl2LGxpbSl7CiBpZihpc0Z4KHN5bSkpewogIGNvbnN0IHI9YXdhaXQgcXFldChgYXBp
L3YxL2NoYXJ0cy9oaXN0b3J5P3N5bWJvbD0ke2VuY29kZVVSSUNvbXBvbmVudChzeW0pfSZ0aW1lZnJhbWU9J3YxJmxpbWl0
PSR7bGltfWApOwogIGlmKGFycmF5LmlzQXJyYXkoaicpKSByZXR1cm4gai5tYXAoay0+KHtvOitrWzFdLGg6K2tbMl0sbDora1sz
XSxjOitrWzRdfSk7CiB9CiBjb25zdCBqPWF3YWl0IGJnZXQoYC9hcGkvdjMva2xpbmVzP3N5bWJvbD0ke3N5bX0maW50ZXJ2YWw9
JHtpdn0mbGltaXQ9JHtsaW19YCk7CiByZXR1cm4gai5tYXAoay0+KHtvOitrWzFdLGg6K2tbMl0sbDora1szXSxjOitrWzRdfSk7
fQoKYXN5bmMgZnVuY3Rpb24gcWFPaGxjKHBhaXIsdGYsbil7Ci const c=F502...; // Quotex feed mapping handled seamlessly
 return (await kl(pair, '1s', n));
}

const TK={};let NO1S=false;
async function pollTick(p){
 p=p||S.pair;
 try{
  let px;
  if(isFx(p)){
   const r=await qqet(`api/v1/ticker?pair=${encodeURIComponent(p)}`);
   px=+(r.price||r.last||r[0]);
  }else{
   const j=await bget('/api/v1/ticker/price?symbol='+p);
   px=+j.price;
  }
  if(!(px>0))return;
  const a=TK[p]=TK[p]||[],now=Date.now();
  if(a.length&&now-a[a.length-1].t>15000)a.length=0;
  a.push({t:now,p:px});if(a.length>1500)a.splice(0,a.length-1500);
 }catch(e){}
}
function tickCandles(p,b){
 const a=TK[p]||[],out=[];let cur=null;
 for(const x of a){
  const k=Math.floor(x.t/1000/b)*b;
  if(!cur||cur.t!==k){
   if(cur)for(let g=cur.t+b;g<k;g+=b)out.push({t:g,o:cur.c,h:cur.c,l:cur.c,c:cur.c});
   cur={t:k,o:x.p,h:x.p,l:x.p,c:x.p};out.push(cur);
  }else{cur.h=Math.max(cur.h,x.p);cur.l=Math.min(cur.l,x.p);cur.c=x.p;}
 }
 return out;
}
async function secCloses(pair,tf,n){
 const a=tf===5?1:tf===10?2:5,b=isFx(pair)?Math.max(a,2):a;
 await pollTick(pair);
 if(!(TK[pair]&&TK[pair].length))throw new Error(NOCONN);
 const c=tickCandles(pair,b).map(k=>k.c);
 if(c.length<60){const e=new Error('Collecting live prices… '+c.length+'/60 candles');e.wait=true;throw e;}
 return c.slice(-n);
}
async function spot(pair,tf){
 if(tf<60){await pollTick(pair);const a=TK[pair];return a&&a.length?a[a.length-1].p:null;}
 const c=await candles(pair,tf,60);return c[c.length-1];
}
async function candles(pair,tf,n=250){
 if(tf<60)return secCloses(pair,tf,n);
 try{return (await kl(pair,tf/60+'m',n)).map(k=>k.c);}catch(e){throw new Error(NOCONN);}
}
async function prices(){
 if(S.grp==='cr'){
  try{const j=await bget('/api/v1/ticker/24hr?symbols='+encodeURIComponent(JSON.stringify(CR)));
  j.forEach(x=>{S.px[x.symbol]=+x.lastPrice;S.ch[x.symbol]=+x.priceChangePercent});}catch(e){}
 }else{
  try{for(const p of FX){
   const r=await qqet(`api/v1/ticker?pair=${encodeURIComponent(p)}`);
   const px=+(r.price||r.last||0);if(px>0){S.px[p]=px;S.ch[p]=+(r.change||0);}
  }}catch(e){}
 }
 markets();
}
function ema(a,n){const k=2/(n+1);let e=a[0];return a.map(v=>e=v*k+e*(1-k))}
function rsi(a,n=14){let g=0,l=0;for(let i=1;i<=n;++i){const d=a[i]-a[i-1];d>0?g+=d:l-=d}g/=n;l/=n;for(let i=n+1;i<a.length;++i){const d=a[i]-a[i-1];g=(g*(n-1)+Math.max(d,0))/n;l=(l*(n-1)+Math.max(-d,0))/n}return l===0?100:100-100/(1+g/l)}
function recStat(p,t){const d=S.hist.filter(h=>h.pair===p&&h.tf===t&&(h.res==='win'||h.res==='loss'));return{n:d.length,w:d.filter(h=>h.res==='win').length}}
const sdv=a=>{const m=a.reduce((s,x)=>s+x,0)/a.length;return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/a.length)};
function analyze(c,pair,tf){
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
 else if(!ok)why=`Only ${mx}/5 agreed`;
 else if(S.rk<3&&dir!==htf)why='Higher timeframe trend disagrees';
 else if(S.rk<3&&(dir>0?px<=c[L-1]:px>=c[L-1]))why='Last candle is not confirming';
 else if(vr<.35)why='Market too quiet';
 else if(vr>2.5)why='Volatility spike';
 else if(S.rk<3&&st.n>=8&&wr<.45)why=`Your record on this pair is weak (${Math.round(wr*100)}%)`;
 const disp=v.concat([{n:'Higher timeframe',t:htf>0?'up':'down',s:htf},{n:'Volatility',t:vr.toFixed(2)+'x normal',s:0},{n:'Your record here',t:st.n?st.w+'W / '+(st.n-st.w)+'L':'no data yet',s:0}]);
 return{v:disp,dir:why?0:dir,agree:mx,px,why};
}
function spark(a){const x=a.slice(-40),lo=Math.min(...x),hi=Math.max(...x)||1,r=(hi-lo)||1;
 return `<svg viewBox="0 0 100 26" style="width:100%;height:26px;margin-top:4px"><polyline fill="none" style="stroke:var(--c)" stroke-width="1.6" points="${x.map((v,i)=>(i/(x.length-1)*100).toFixed(1)+','+(24-(v-lo)/r*22).toFixed(1)).join(' ')}"/></svg>`}
function markets(){
 const L=S.grp==='fx'?FX:CR;
 $('#mkt').innerHTML=L.map(p=>{const sg=S.sig&&S.sig.pair===p&&!S.sig.res?S.sig:null,px=S.px[p],ch=S.ch[p];
  return `<div class="pc2${p===S.pair?' sel':''}${sg?(sg.dir>0?' up':' dn'):''}" onclick="pick('${p}')"><div class="row"><b>${nm(p)}</b>${sg?`<span class="ar ${sg.dir>0?'up':'dn'}">${sg.dir>0?'▲':'▼'}</span>`:''}</div><div class="sub">${px?fmt(px):'—'}${ch!=null?` <span class="${ch>=0?'up':'dn'}">${ch>=0?'+':''}${ch.toFixed(2)}%</span>`:''}</div>${S.sp[p]?spark(S.sp[p]):''}</div>`}).join('');
 chartDraw();
}
function pick(p){S.pair=p;$('#selp').textContent=nm(p);markets();chartReset()}
function eng(state,ic,txt,sub,cls){
 const e=$('#eng');e.className='eng '+(state==='scan'?'scanning ':'')+(state==='up'?'gu ':state==='dn'?'gd':'')+(cls||'');
 void e.offsetWidth;if(state==='up'||state==='dn')e.classList.add(txt==='LOSS'?'shake':'burst');
 if(txt==='LOSS')e.classList.remove('burst');$('#ic').textContent=ic;$('#sig').textContent=txt;
 $('#sig').className='d '+(state==='up'?'up':state==='dn'?'dn':state==='nt'?'nt':'');$('#sub').textContent=sub;
}
const STEPS=['Reading candles','Calculating RSI (14)','Checking EMA 9/21/50 trend','Checking MACD (12,26,9)','Checking Bollinger bands','Checking higher-timeframe trend','Checking volatility and your record'];
async function scan(){
 const box=$('#steps');box.innerHTML=STEPS.map(s=>`<div>${s}</div>`).join('');
 const c=await candles(S.pair,S.tf);
 for(let i=0;i<STEPS.length;++i){await sleep(350);box.children[i].classList.add('ok')}
 S.sp[S.pair]=c.slice(-40);return analyze(c,S.pair,S.tf);
}
function popup(h){
 $('#pp').textContent=nm(h.pair)+' • '+tfL(h.tf);
 $('#pd').textContent=h.dir>0?'▲ UP (CALL)':'▼ DOWN (PUT)';$('#pd').className='dir '+(h.dir>0?'up':'dn');
 $('#pi').textContent=h.agree+'/5 indicators agree';
 $('#pt').textContent=new Date(h.at).toLocaleTimeString([],h.tf<60?{hour:'2-digit',minute:'2-digit',second:'2-digit'}:{hour:'2-digit',minute:'2-digit'});
 clearInterval(S.pw);const u=()=>{if(h.res&&h.res!=='void'){$('#pw').textContent='Result: '+h.res.toUpperCase();return}const s=Math.max(0,Math.round((h.at-Date.now())/1000));$('#pw').textContent=s>0?'Starts in '+s+'s':'Enter now'};u();S.pw=setInterval(u,1000);
 $('#pop').classList.add('on');
}
$('#ok').onclick=()=>{$('#pop').classList.remove('on');clearInterval(S.pw)};
$('#eng').onclick=()=>{if(!S.run)toggle();else if(S.sig&&!S.sig.res)popup(S.sig)};
async function cycle(){
 if(!S.run)return;
 eng('scan','⏳','SCANNING','Analyzing '+nm(S.pair)+'…');$('#pg').style.strokeDashoffset=C;$('#str').textContent='—';
 let a;try{a=await scan()}catch(e){if(!S.run)return;if(e.wait){eng('scan','🔄','COLLECTING DATA',e.message);S.timer=setTimeout(cycle,3000);return}eng('nt','!','NO DATA',e.message||'Data unavailable');S.timer=setTimeout(cycle,10000);return}
 if(!S.run)return;
 $('#px').textContent=fmt(a.px);S.px[S.pair]=a.px;
 $('#ind').innerHTML=a.v.map(x=>`<div><span>${x.n}</span><span class="${x.s>0?'up':x.s<0?'dn':'nt'}">${x.t}</span></div>`).join('');
 $('#str').textContent=a.agree+'/5';markets();
 if(a.dir===0){eng('nt','⟳','NO TRADE',a.why+'. Re-scanning…');S.timer=setTimeout(cycle,S.tf<60?3000:6000);return}
 const up=a.dir>0;
 eng(up?'up':'dn',up?'▲':'▼',up?'UP • CALL':'DOWN • PUT',a.agree+'/5 agreed • '+tfL(S.tf)+' • tap for details',up?'glowup':'glowdn');
 const now=Date.now(),at=S.tf<60?now+4000:Math.ceil((now+5000)/60000)*60000;
 const rec={t:now,at,pair:S.pair,tf:S.tf,dir:a.dir,entry:null,agree:a.agree,res:null,m:'live'};
 S.hist.unshift(rec);S.sig=rec;save();markets();popup(rec);beep(880,.18);
 const total=Math.round((at-now)/1000)+S.tf;let left=total,entered=false;
 clearInterval(S.tick);
 S.tick=setInterval(async()=>{left--;const l=Math.max(left,0);
  $('#left').textContent=mmss(l);$('#pg').style.strokeDashoffset=C*(1-l/total);
  if(!entered&&Date.now()>=at){entered=true;try{rec.entry=await spot(rec.pair,rec.tf);save()}catch(e){}}
  if(left<=0){clearInterval(S.tick);finish(rec)}
 },1000);
}
let AC;
function beep(f,d){if(S.snd!=='on')return;try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f;g.gain.value=.08;o.connect(g);g.connect(AC.destination);o.start();o.stop(AC.currentTime+d)}catch(e){}try{navigator.vibrate&&navigator.vibrate(Math.round(d*600))}catch(e){}}
function lossRun(){let n=0;for(const h of S.hist.filter(h=>h.res==='win'||h.res==='loss')){if(h.res==='loss')n++;else break}return n}
function confetti(){const c=$('#fx'),g=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;const cl=['#3ff2a0','#5eead4','#8b5cf6','#f5c46b'],P=Array.from({length:55},()=>({x:innerWidth/2,y:innerHeight*.4,vx:(Math.random()-.5)*13,vy:-Math.random()*13-2,s:4+Math.random()*5,col:cl[Math.random()*4|0],r:Math.random()*6}));let f=0;(function t(){g.clearRect(0,0,c.width,c.height);P.forEach(p=>{p.vy+=.35;p.x+=p.vx;p.y+=p.vy;p.r+=.2;g.fillStyle=p.col;g.save();g.translate(p.x,p.y);g.rotate(p.r);g.fillRect(-p.s/2,-p.s/2,p.s,p.r*.6);g.restore()});if(++f<75)requestAnimationFrame(t);else g.clearRect(0,0,c.width,c.height)})();}
async function finish(rec){
 let px=null;try{px=await spot(rec.pair,rec.tf)}catch(e){}
 if(px==null||rec.entry==null){rec.res='void'}
 else{rec.exit=px;rec.res=px===rec.entry?'tie':((px>rec.entry)===(rec.dir>0)?'win':'loss')}
 save();$('#left').textContent='—:—';markets();render();
 eng(rec.res==='win'?'up':rec.res==='loss'?'dn':'nt',rec.res==='win'?'✓':rec.res==='loss'?'✕':'=',rec.res.toUpperCase(),'Trade finished');
 if(rec.res==='win'){beep(1175,.25);confetti()}else if(rec.res==='loss')beep(220,.35);
 if(rec.res==='loss'&&S.maxL>0&&lossRun()>=S.maxL&&S.run){toggle();eng('nt','🚫','BOT STOPPED',S.maxL+' losses in a row. Take a break.');return}
 if(S.run)S.timer=setTimeout(cycle,4000);
}
function toggle(){
 S.run=!S.run;const b=$('#go');
 if(S.run){b.textContent='⏹ STOP BOT';b.className='big stop';cycle()}
 else{clearTimeout(S.timer);clearInterval(S.tick);if(S.sig&&!S.sig.res){S.sig.res='void';save()}b.textContent='▶ START BOT';b.className='big';eng('','🎧','STANDBY','Tap to start');$('#left').textContent='—:—';$('#pg').style.strokeDashoffset=C;markets()}
}
$('#go').onclick=toggle;
$('#clr').onclick=()=>{if(confirm('Delete all logged signals?')){S.hist=[];save();render()}};
function render(){
 const f=t=>new Date(t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});
 $('#hist').innerHTML=S.hist.length?S.hist.slice(0,50).map((h,i)=>`<div class="hrow" onclick="popup(S.hist[${i}])"><span>${nm(h.pair)} ${tfL(h.tf)} <b class="${h.dir>0?'up':'dn'}">${h.dir>0?'UP':'DOWN'}</b> • ${f(h.t)}</span><span class="${h.res==='win'?'up':h.res==='loss'?'dn':'nt'}">${h.res?h.res.toUpperCase():'pending'}</span></div>`).join(''):'<div><span>No signals yet</span></div>';
 const d=S.hist.filter(h=>h.res==='win'||h.res==='loss'),w=d.filter(h=>h.res==='win').length;
 $('#aw').textContent=w;$('#al').textContent=d.length-w;$('#ar').textContent=d.length?Math.round(w/d.length*100)+'%':'—';
 let k=d[0]&&d[0].res,st=0;for(const h of d){if(h.res===k)st++;else break}
 $('#stk').textContent=d.length?`Current streak: ${st} ${k}${st>1?(k==='win'?'s':'es'):''} • Stop-loss: ${S.maxL||'off'}`:'No finished trades yet';
 ['aw','al','ar'].forEach(i=>{const e=$('#'+i);if(e._v!==e.textContent){if(e._v!==undefined)e.animate([{transform:'scale(1.5)',opacity:.3},{transform:'scale(1)',opacity:1}],{duration:450});e._v=e.textContent}});
 const by={};d.forEach(h=>{const k=nm(h.pair)+' '+tfL(h.tf);(by[k]=by[k]||[0,0])[h.res==='win'?0:1]++});
 $('#byp').innerHTML=Object.entries(by).map(([k,v])=>`<div><span>${k}</span><span>${v[0]}W / ${v[1]}L</span></div>`).join('');
}
const CH={d:[],last:null,tm:null};
function chartMsg(t){$('#cm').textContent=t;$('#cm').style.display=t?'flex':'none'}
async function chartPull(){
 const p=S.pair,tf=S.tf;let d;
 try{
  if(tf<60){
   if(!isFx(p)&&!NO1S){try{d=await kl(p,'1s',60)}catch(e){NO1S=true}}
   if(!d){const t=tickCandles(p,isFx(p)?2:1).slice(-60);if(t.length<3)return chartMsg('Collecting live prices…');d=t}
  }else if(isFx(p))d=await kl(p,'v1',60);
  else d=await kl(p,tf/60+'m',60);
 }catch(e){return chartMsg(NOCONN)}
 if(isFx(p)&&tf>=60&&d.length&&Date.now()/1000-d[d.length-1].t>Math.max(900,tf*3))$('#ci').textContent=CH.ci+' • market may be closed';else $('#ci').textContent=CH.ci;
 if(p!==S.pair||tf!==S.tf||!d.length)return;
 chartMsg('');const sg=d.length+':'+d[d.length-1].c+':'+d[d.length-1].h+':'+d[d.length-1].l;if(sg===CH.sg)return;CH.sg=sg;
 const prev=CH.last;CH.d=d;CH.last=d[d.length-1].c;S.px[p]=CH.last;
 const e=$('#cpx');e.textContent=fmt(CH.last);$('#px').textContent=fmt(CH.last);
 if(prev!=null&&prev!==CH.last){e.className='cpx';void e.offsetWidth;e.className='cpx '+(CH.last>prev?'fu':'fd')}
 const ch=S.ch[p];$('#cch').textContent=ch!=null?(ch>=0?'+':'')+ch.toFixed(2)+'\% 24h':'';$('#cch').className='sub '+(ch>=0?'up':'dn');
 chartDraw();
}
function chartReset(){
 clearInterval(CH.tm);CH.d=[];CH.last=null;CH.sg=null;clearInterval(TK.tm);if(S.tf<60){pollTick();TK.tm=setInterval(pollTick,isFx(S.pair)?2000:1000)}
 $('#cn').textContent=nm(S.pair);$('#cpx').textContent='—';$('#cch').textContent='';
 CH.ci='Candles: '+(isFx(S.pair)?(S.tf<60?'live ticks • Quotex':''+tfL(S.tf)+' • Quotex'):(S.tf<60?'1s':'v1'+tfL(S.tf))+' • Binance');
 $('#ci').textContent=CH.ci;chartMsg('Loading live price…');chartDraw();chartPull();
 CH.tm=setInterval(chartPull,S.tf<60?1000:isFx(S.pair)?4000:3000);
}
function chartDraw(){
 const cv=$('#cv');if(!cv)return;const g=cv.getContext('2d'),dpr=window.devicePixelRatio||1,W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;if(cv.width!==Math.round(W*dpr)){cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr)}
 g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);const d=CH.d;if(!d.length)return;
 let lo=Math.min(...d.map(x=>x.l)),hi=Math.max(...d.map(x=>x.h));const pad=(hi-lo)*.1||hi*.0005;lo-=pad;hi+=pad;
 const pw=58,cw=(W-pw)/d.length,y=v=>H-8-(v-lo)/(hi-lo)*(H-16);
 g.font='10px sans-serif';g.lineWidth=1;
 for(let i=0;i<4;++i){const v=lo+(hi-lo)*i/3,yy=y(v);g.strokeStyle='#ffffff12';g.beginPath();g.moveTo(0,yy);g.lineTo(W-pw,yy);g.stroke();g.fillStyle='#8f93b8';g.fillText(fmt(v),W-pw+4,yy+3)}
 d.forEach((k,i)=>{const x=i*cw+cw/2,u=k.c>=k.o;g.strokeStyle=g.fillStyle=u?'#3ff2a0':'#ff5577';g.beginPath();g.moveTo(x,y(k.h));g.lineTo(x,y(k.l));g.stroke();g.fillRect(x-cw*.32,Math.min(y(k.o),y(k.c)),cw*.64,Math.max(1,Math.abs(y(k.o)-y(k.c))))});
 const last=d[d.length-1].c,ly=y(last);
 g.setLineDash([4,4]);g.strokeStyle='#8b5cf6';g.beginPath();g.moveTo(0,ly);g.lineTo(W-pw,ly);g.stroke();g.setLineDash([]);
 g.fillStyle='#8b5cf6';g.fillRect(W-pw,ly-9,pw,18);g.fillStyle='#fff';g.fillText(fmt(last),W-pw+4,ly+3);
 const s=S.sig;if(s&&!s.res&&s.pair===S.pair){const e=s.entry||last,ey=y(e),col=s.dir>0?'#3ff2a0':'#ff5577';
  g.setLineDash([2,3]);g.strokeStyle=col;g.beginPath();g.moveTo(0,ey);g.lineTo(W-pw,ey);g.stroke();g.setLineDash([]);
  g.font='bold 22px sans-serif';g.fillStyle=col;g.fillText(s.dir>0?'▲':'▼',W-pw-28,ey+(s.dir>0?-6:20))}
}
window.addEventListener('resize',chartDraw);
document.addEventListener('pointerdown',e=>{const b=e.target.closest('button');if(!b)return;const r=b.getBoundingClientRect(),d=Math.max(r.width,r.height)*2,p=document.createElement('span');p.className='rip';p.style.cssText=`width:${d}px;height:${d}px;left:${e.clientX-r.left-d/2}px;top:${e.clientY-r.top-d/2}px`;b.appendChild(p);setTimeout(()=>p.remove(),600)});
function boot(){
 document.querySelectorAll('#sn button').forEach(b=>b.classList.toggle('on',b.dataset.v===S.snd));
 document.querySelectorAll('#ml button').forEach(b=>b.classList.toggle('on',+b.dataset.v===S.maxL));
 mode();$('#selp').textContent=nm(S.pair);markets();render();prices();chartReset();setInterval(prices,15000);
}
$('#exp').onclick=()=>{const rows=[['time','pair','timeframe','direction','indicators_agree','entry','exit','result']].concat(S.hist.map(h=>[new Date(h.t).toISOString(),h.pair,tfL(h.tf),h.dir>0?'UP':'DOWN',h.agree,h.entry==null?'':h.entry,h.exit==null?'':h.exit,h.res||'']));const b=new Blob([rows.map(r=>r.join(',')).join('\n')],{type:'text/csv'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='helix-history.csv';a.click()};
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
</script></body></html>
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
