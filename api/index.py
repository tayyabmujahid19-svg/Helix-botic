"""HELIX BOTIC - serves the dashboard using Flask.
Vercel compatible.
"""
from flask import Flask, Response
import base64, os

app = Flask(__name__)

_B64 = """
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj48aGVhZD48bWV0YSBjaGFyc2V0PSJ1dGYtOCI+CjxtZXRhIG5hbWU9InZp
ZXdwb3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsaW5pdGlhbC1zY2FsZT0xLHZpZXdwb3J0LWZpdD1jb3ZlciI+Cjx0
aXRsZT5IRUxJWCBCT1RJQzwvdGl0bGU+CjxzdHlsZT4KOnJvb3R7LS1iZzojMDUwNjBmOy0tbGluZTojZmZmZmZmMTQ7LS1jOiM1
ZWVhZDQ7LS12OiM4YjVjZjY7LS1nOiMzZmYyYTA7LS1yOiNmZjU1Nzc7LS15OiNmNWM0NmI7LS10OiNmNGYyZmY7LS1tOiM4Zjkz
Yjh9Cip7Ym94LXNpemluZzpib3JkZXItYm94O21hcmdpbjowOy13ZWJraXQtdGFwLWhpZ2hsaWdodC1jb2xvcjp0cmFuc3BhcmVu
dH0KYm9keXtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChjaXJjbGUgYXQgMTAlIC04JSwjMmIxNjcwIDAsdHJhbnNwYXJlbnQg
NDIlKSxyYWRpYWwtZ3JhciA=
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
ZmxleC13cmFwOndyYXA7bWFyZ2luLXRvcDogOHB4fQouc2VnIGJ1dHRvbixpbnB1dHtiYWNrZ3JvdW5kOiNmZmZmZmYwYjtib3Jk
ZXI6MXB4IHNvbGlkIHZhcigtLWxpbmUpO2NvbG9yOnZhcigtLXQpO2JvcmRlci1yYWRpdXM6MTJweDtwYWRkaW5nOjhweCAxMnB4
O2ZvbnQtc2l6ZToxM3B4fQouc2VnIGJ1dHRvbi5vbntiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCgxMzVkZWcsdmFyKC0tdiksIzBl
YTViNyk7Ym9yZGVyLWNvbG9yOnRyYW5zcGFyZW50O2JveC1zaGFkb3c6MCA0cHggMTZweCAjOGI1Y2Y2NjZ9CmlucHV0e3dpZHRo
OjEwMCU7bWFyZ2luLXRvcDo4cHh9CmxhYmVse2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxMnB4fQouYmlnewlkc3BsYXk6Ymxv
Y2s7d2lkdGg6MTAwJTttYXJnaW4tdG9wOjE0cHg7cGFkZGluZzoxNnB4O2JvcmRlcjowO2JvcmRlci1yYWRpdXM6MTZweDtmb250
LXNpemU6MTZweDtmb250LXdlaWdodDo3MDA7bGV0dGVyLXNwYWNpbmc6LjVweDtjb2xvcjojZmZmO2JhY2tncm91bmQ6bGluZWFy
LWdyYWRpZW50KDEzNWRlZyx2YXIoLS12KSwjMGVhNWI3KTtib3gtc2hhZG93OjAgOHB4IDI4cHggIzhiNWNmNjY2fQouYmlnLnN0
b3B7YmFja2dyb3VuZDpsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLCNiZTEyM2MsdmFyKC0tcikpO2JveC1zaGFkb3c6MCA4cHggMjhw
eCAjZmY1NTc3NTV9Ci5lbmd7cG9zaXRpb246cmVsYXRpdmU7d2lkdGg6MjQwcHg7aGVpZ2h0OjM0MHB4O21hcmdpbjo2cHggYXV0
bztjdXJzb3I6cG9pbnRlcn0KLmVuZyBzdmd7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MH0KLnNwaW57dHJhbnNmb3JtLW9yaWdp
bjoxMjBweCAxMjBweH0KLnNjYW5uaW5nIC5zcGlue2FuaW1hdGlvbjpzcCAxLjZzIGxpbmVhciBpbmZpbml0ZX0KQGtleWZyYW1l
cyBzcHt0b3t0cmFuc2Zvcm06cm90YXRlKDM2MGRlZyl9fQouY3Rye3Bvc2l0aW9uOmFic29sdXRlO2luc2V0OjM0cHg7Ym9yZGVy
LXJhZGl1czo1MCU7ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1j
b250ZW50OmNlbnRlcjt0ZXh0LWFsaWduOmNlbnRlcjtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChjaXJjbGUsIzFhMTQ1MCwj
MGEwYTIyIDcyJSl9Ci5pY3tmb250LXNpemU6NDRweDtsaW5lLWhlaWdodDoxfQouZHtmb250LXNpemU6MjZweDtmb250LXdlaWdo
dDo4MDA7bWFyZ2luLXRvcDoycHh9Ci51cHtjb2xvcjp2YXIoLS1nKX0uZG57Y29sb3I6dmFyKC0tcil9Lm50e2NvbG9yOnZhcigt
LXlpfQouZ2xvd3VwIC5jdHJ7Ym94LXNoYWRvdzowIDAgNTBweCAjM2ZmMmEwNjYgaW5zZXQsMCAwIDQwcHggIzNmZjJhMDQ0fQou
Z2xvd2RuIC5jdHJ7Ym94LXNoYWRvdzowIDAgNTBweCAjZmY1NTc3NjYgaW5zZXQsMCAwIDQwcHggI2ZmNTU3NzQ0fQoubWluaXt
kaXNwbGF5OmZsZXg7Z2FwOjhweDttYXJnaW4tdG9wOjhweH0KLm1pbmkgZGl2e2ZsZXg6MTtiYWNrZ3JvdW5kOiNmZmZmZmYwODti
b3JkZXI6MXB4IHNvbGlkIHZhcigtLWxpbmUpO2JvcmRlci1yYWRpdXM6MTRweDtwYWRkaW5nOjhweDt0ZXh0LWFsaWduOmNlbnRl
cn0KLm1pbmkgYntkaXNwbGF5OmJsb2NrO2ZvbnQtc2l6ZToxNnB4fQouZ3JpZHtkaXNwbGF5OmdyaWQ7Z3JpZC10ZW1wbGF0ZS1j
b2x1bW5zOjFmciAxZnI7Z2FwOjEwcHg7bWFyZ2luLXRvcDoxMHB4fQoucGMye2JhY2tncm91bmQ6I2ZmZmZmZjA4O2JvcmRlcjox
cHggc29saWQgdmFyKC0tbGluZSk7Ym9yZGVyLXJhZGl1czoxNnB4O3BhZGRpbmc6MTFweDtjdXJzb3I6cG9pbnRlcjt0cmFuc2l0
aW9uOi4xNXN9Ci5wYzIgYntmb250LXNpemU6MTRweH0KLnBjMi5zZWx7Ym9yZGVyLWNvbG9yOnZhcigtLXYpO2JveC1zaGFkb3c6
MCAwIDAgMXB4IHZhcigtLXYpLDAgNnB4IDIwcHggIzhiNWNmNjU1fQoucGMyLnVwe2JvcmRlc-mNvbG9yOnZhcigtLWcpOy1ib3gt
c2hhZG93OjAgMCAwIDFweCB2YXIoLS1nKSwwIDAgMjJweCAjM2ZmMmEwNTV9Ci5wYzIuZG57Ym9yZGVyLWNvbG9yOnZhcigtLXIp
O2JveC1zaGFkb3c6MCAwIDAgMXB4IHZhcigtLXIpLDAgMCAyMnB4ICNmZjU1Nzc1NX0KLmFye2ZvbnQtc2l6ZToyMHB4O2ZvbnQt
d2VpZ2h0OjkwMDthbmltYXRpb246Ym4gMXMgZWFzZS1pbi1vdXQgaW5maW5pdGV9CkBrZXlmcmFtZXMgYm57NTAle3RyYW5zZm9y
bTp0cmFuc2xhdGVZKC0zcHgpfX0KLnN0ZXBzIGRpdntwYWRkaW5nOjVweCAwO2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxNHB4
fS5zdGVwcyAub2t7Y29sb3I6dmFyKC0tdCl9LnN0ZXBzIC5vazphZnRlcntjb250ZW50OiIg4pyTIjtjb2xvcjp2YXIoLS1nKX0K
LnRibCBkaXZ7ZGlzcGxheTpmbGV4O2p1c3RpZnktY29udGVudDpzcGFjZS1iZXR3ZWVuO3BhZGRpbmc6OHB4IDA7Ym9yZGVyLWJv
dHRvbToxcHggc29saWQgdmFyKC0tbGluZSk7Zm9udC1zaXplOjE0cHh9Ci50YWJ7ZGlzcGxheTpub25lfS50YWIub257ZGlzcGxh
eTibG9ja30KbmF2e3Bvc2l0aW9uOmZpeGVkO2JvdHRvbTowO2xlZnQ6MDtyaWdodDowO2Rpc3BsYXk6ZmxleDtiYWNrZ3JvdW5k
OiMwODBhMWNkZDtiYWNrZHJvcC1maWx0ZXI6Ymx1cigxNHB4KTtib3JkZXItdG9wOjFweCBzb2xpZCB2YXIoLS1saW5lKTtwYWRk
aW5nLWJvdHRvbTplbnYoc2FmZS1hcmVhLWluc2V0LWJvdHRvbSl9Cm5hdiBidXR0b257ZmxleDoxO2JhY2tncm91bmQ6MDtib3Jk
ZXI6MDtjb2xvcjp2YXIoLS1tKTtwYWRkaW5nOjEzcHggMDtmb250LXNpemU6MTJweH0KbmF2IGJ1dHRvbi5vbntjb2xvcjp2aXIo
LS1jKX0KLndhcm57Zm9udC1zaXplOjExcHg7Y29sb3I6dmFyKC0tbSk7bWFyZ2luLXRvcDoxNHB4fQouYmFkZ2V7Zm9udC1zaXpl
OjExcHg7cGFkZGluZzo0cHggMTBweDtib3JkZXItcmFkaXVzOjIwcHg7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1saW5lKTtjb2xv
cjp2YXIoLS15KX0KLmJhZGdlLmxpdmV7Y29sb3I6dmFyKC0tZyl9Ci5zdGF0e2ZvbnQtc2l6ZToyOHB4O2ZvbnQtd2VpZ2h0Ojgw
MDtjb2xvcjp2YXIoLS1jKX0KLmhyb3d7Y3Vyc29yOnBvaW50ZXJ9CiNwb3B7cG9zaXRpb246Zml4ZWQ7aW5zZXQ6MDtiYWNrZ3Jv
dW5kOiMwMDBjO2Rpc3BsYXk6bm9uZTthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRlcjt6LWluZGV4Ojk7
cGFkZGluZzoyMHB4fQojcG9wLm9ue2Rpc3BsYXk6ZmxleH0KLnBje3dpZHRoOjEwMCU7bWF4LXdpZHRoOjM4MHB4O2JhY2tncm91
bmQ6bGluZWFyLWdyYWRpZW50KDE2MGRlZywjMjQxYTcwLCMwYjBhMjUpO2JvcmRlcjoxcHggc29saWQgdmFyKC0tdik7Ym9yZGVy
LXJhZGl1czoyNHB4O3BhZGRpbmc6MjJweDt0ZXh0LWFsaWduOmNlbnRlcjtib3gtc2hhZG93OjAgMCA2MHB4ICM4YjVjZjY2Nn0K
LnBjIC5kaXJ7Zm9udC1zaXplOjQ2cHg7Zm9udC13ZWlnaHQ6OTAwO21hcmdpjo2cHggMH0KLnBjIC50bXtmb250LXNpemU6MzhweDtm
b250LXdlaWdodDo4MDA7Y29sb3I6dmFyKC0tYyk7dGV4dC1zaGFkb3c6MCAwIDE4cHggIzVlZWFkNDk5fQoKYnV0dG9ue3Bvc2l0
aW9uOnJlbGF0aXZlO292ZXJmbG93OmhpZGRlbjt0cmFuc2l0aW9uOnRyYW5zZm9ybSAuMTJzLGJveC1zaGFkb3cgLjJzLGJhY2tn
cm91bmQgLjJzfQpidXR0b246YWN0aXZle3RyYW5zZm9ybTpzY2FsZSguOTQpfQoucmlwe3Bvc2l0aW9uOmFic29sdXRlO2JvcmRl
ci1yYWRpdXc6NTAlO2JhY2tncm91bmQ6I2ZmZmZmZjU1O3RyYW5zZm9ybTpzY2FsZSgwKTthbmltYXRpb246cnAgLjZzIGVhc2Ut
b3V0O3BvaW50ZXItZXZlbnRzOm5vbmV9CkBrZXlmcmFtZXMgcnB7dG97dHJhbnNmb3JtOnNjYWxlKDEpO29wYWNpdHk6MH19CiNn
bzpub3QoLnN0b3Ape2FuaW1hdGlvbjpiciAyLjRzIGVhc2UtaW4tb3V0IGluZmluaXRlfQpAa2V5ZnJhbWVzIGJyezUwJXtib3gt
c2hhZG93OjAgOHB4IDQycHggIzIyZDNlZWFhfX0KLnRhYi5vbnthbmltYXRpb246dGluIC4zNXMgZWFzZX0KQGtleWZyYW1lcyB0
aW57ZnJvbXtvcGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTJweCl9fQouY2FyZHthbmltYXRpb246Y2luIC41NXMgZWFz
ZSBib3RofQouY2FyZDpudGgtY2hpbGQoMil7YW5pbWF0aW9uLWRlbGF5Oi4wN3N9LmNhcmQ6bnRoLWNoaWxkKDMpe2FuaW1hdGlv
bi1kZWxheTouMTRzfS5jYXJkOm50aC1jaGlsZCg0KXthbmltYXRpb24tZGVsYXk6LjIxc30KQGtleWZyYW1lcyBjaW57ZnJvbXtv
cGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTZweCkgc2NhbGUoLjk4KX19Ci5wYzI6aG92ZXJ7dHJhbnNmb3JtOnRyYW5z
bGF0ZVkoLTJweCl9LnBjMjphY3RpdmV7dHJhbnNmb3JtOnNjYWxlKC45NSl9Ci5oZXh7YW5pbWF0aW9uOmh4IDRzIGVhc2UtaW4t
b3V0IGluZmluaXRlfQpAa2V5ZnJhbWVz h4ezUwJXtib3gtc2hhZG93OjAgMCAzNHB4ICM1ZWVhZDRhYTt0cmFuc2Zvcm06
cm90YXRlKDhkZWcpfX0KLmVuZy5ndXtjb2xvcjp2YXIoLS1nKX0uZW5nLmdke2NvbG9yOnZhcigtLXIpfQouZW5nLmJ1cnN0OmFm
dGVye2NvbnRlbnQ6IiI7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MjBweDtib3JkZXItcmFkaXVzOjUwJTtib3JkZXI6M3B4IHNv
bGlkIGN1cnJlbnRDb2xvcjthbmltYXRpb246d2F2ZSAuOXMgZWFzZS1vdXQ7cG9pbnRlci1ldmVudHM6bm9uZX0KLmVuZy5idXJz
dCAjaWMsLmVuZy5idXJzdCAuZHthbmltYXRpb246cG9wIC41NXMgY3ViaWMtYmV6aWVyKC4yLDEuNiwuNCwxKX0KQGtleWZyYW1l
cyB3YXZle2Zyb217dHJhbnNmb3JtOnNjYWxlKC44KTtvcGFjaXR5Oi45fXRve3RyYW5zZm9ybTpzY2FsZSgxLjQpO29wYWNpdHk6
MH19CkBrZXlmcmFtZXMgcG9we2Zyb217dHJhbnNmb3JtOnNjYWxlKC4zKTtvcGFjaXR5OjB9fQouZW5nLnNoYWtle2FuaW1hdGlv
bnNoIC41Nn0KQGtleWZyYW1lcyBzaHsyMCUsNjAldHJhbnNmb3JtOnRyYW5zbGF0ZVgoLTlweCl9NDAlLDgwJXt0cmFuc2Zvcm06
dHJhbnNsYXRlWCg5cHgoKX09fQoubGl2ZXtmb250LXNpemU6MTBweDtjb2xvcjp2YXIoLS1nKTttYXJnaW4tbGVmdDo2cHg7Zm9u
dC13ZWlnaHQ6NzAwfQoubGl2ZSBpe2Rpc3BsYXk6aW5saW5lLWJsb2NrO3dpZHRoOjdweDtoZWlnaHQ6N3B4O2JvcmRlcj-yYWRp
dXM6NTAlO2JhY2tncm91bmQ6dmFyKC0tZyk7bWFyZ2luLXJpZ2h0OjRweDthbmltYXRpb246cGwgMS4ycyBpbmZpbml0ZX0KQGtl
eWZyYW1lcyBwbHs1MCV7b3BhY2l0eTouMjU7dHJhbnNmb3JtOnNjYWxlKDEuNyl9fQouY3B4e2ZvbnQtc2l6ZToyMnB4O2ZvbnQt
d2VpZ2h0OjgwMH0KLmNweC5mdXthbmltYXRpb246ZnUgLjdzfS5jcHguZmR7YW5pbWF0aW9uOmZkIC43c30KQGtleWZyYW1lcyBm
d3swJXtjb2xvcjp2YXIoLS1nKTt0ZXh0LXNoYWRvdzowIDAgMTZweCB2YXIoLS1nKX19CkBrZXlmcmFtZXMgZmR7MCV7Y29sb3I6
dmFyKC0tcik7dGV4dC1zaGFkb3c6MCAwIDE2cHggdmFyKC0tcil9fQouY217cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MDtkaXNw
bGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7dGV4dC1hbGlnbjpjZW50ZXI7cGFkZGlu
ZzoxMnB4O2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxM3B4O2JhY2tncm91bmQ6IzBhMGIxY2NjO2JvcmRlcjByYWRpdXM6MTJw
eH0KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOnJlZHVjZSl7KnthbmltYXRpb246bm9uZSFpbXBvcnRhbnQ7dHJhbnNp
dGlvbjpub25lIWltcG9ydGFudH19CgouY2FyZCxuYXZ7YmFja2Ryb3AtZmlsdGVyOm5vbmUhaW1wb3J0YW50Oy13ZWJraXQtYmFj
a2Ryb3AtZmlsdGVyOm5vbmUhaW1wb3J0YW50fQpuYXZ7YmFja2dyb3VuZDojMDgwYTFjIWltcG9ydGFudH0KLmNhcmR7Ym94LXNo
YWRvdzpub25lIWltcG9ydGFudDthbmltYXRpb246Y2luIC4zNXMgZWFzZSBib3RofQojZ286bm90KC5zdG9wKSwuaGV4e2FuaW1h
dGlvbjpub25lIWltcG9ydGFudH0KCi5vcmJ7cG9zaXRpb246Zml4ZWQ7d2lkdGg6MzQwcHg7aGVpZ2h0OjM0MHB4O2JvcmRlci1y
YWRpdXM6NTAlO3BvaW50ZXItZXZlbnRzOm5vbmU7ei1pbmRleDotMTtvcGFjaXR5Oi41NX0KLm8xe2JhY2tncm91bmQ6cmFkaWFs
LWdyYWRpZW50KGNpcmNsZSwjN2MzYWVkNjYsdHJhbnNwYXJlbnQgNzAlKTt0b3A6LTgwcHg7bGVmdDotMTAwcHg7YW5pbWF0aW9u
OmZsMSAxOHMgZWFzZS1pbi1vdXQgaW5maW5pdGUgYWx0ZXJuYXRlfQoubzJ7YmFja2dyb3VuZDpyYWRpYWwtZ3JhZGllbnRPY2ly
Y2xlLCMwNmI2ZDQ1NSx0cmFuc3BhcmVudCA3MCUpO2JvdHRvbTo2MHB4O3JpZ2h0Oi0xMjBweDthbmltYXRpb246ZmwyIDIycyBl
YXNlLWluLW91dCBpbmZpbml0ZSBhbHRlcm5hdGV9CkBrZXlmcmFtZXMgZmwxe3Rve3RyYW5zZm9ybTp0cmFuc2xhdGUoMTIwcHgs
MTYwcHgpfX0KQGtleWZyYW1lcyBmbDJ7dG97dHJhbnNmb3JtOnRyYW5zbGF0ZSgtMTAwcHgsLTE0MHB4KX19CiNmeHtwb3NpdGlv
bjpmaXhlZDtpbnNldDowO3dpZHRoOjEwMCU7aGVpZ2h0OjEwMCU7cG9pbnRlci1ldmVudHM6bm9uZTt6LWluZGV4Ojh9Ci5zd2Vl
cHtwb3NpdGlvbjphYnNvbHV0ZTtpbnNldDoxMHB4O2JvcmRlci1yYWRpdXc6NTAlO2JhY2tncm91bmQ6Y29uaWMtZ3JhZGllbnQo
ZnJvbSAwZGVnLHRyYW5zcGFyZW50IDAgMjkwZGVnLCM1ZWVhZDQ2NiAzNjBkZWcpO29wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNp
dHkgLjNzfQouc2Nhbm5pbmcgLnN3ZWVwe29wYWNpdHk6MTthbmltYXRpb246c3AgMS42cyBsaW5lYXIgaW5maW5pdGV9CiNsb2Nr
e3Bvc2l0aW9uOmZpeGVkO2luc2V0OjA7ei1pbmRleDoyMDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnkt
Y29udGVudDpjZW50ZXI7cGFkZGluZzoyNHB4O2JhY2tncm91bmQ6cmFkaWFsLWdyYWRpZW50KGNpcmNsZSBhdCAyMCUgMTAlLCMz
MzE2N2EsdHJhbnNwYXJlbnQgNTAlKSxyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDkwJSA5MCUsIzA4NTY2ZSx0cmFuc3BhcmVu
dCA0NSUpLCMwNTA2MGZ9CiNsb2NrLm91dHthbmltYXRpb246bG91dCAuNjVzIGVhc2UgZm9yd2FyZHN9CkBrZXlmcmFtZXMgbG91
dHt0b3tvcGFjaXR5OjA7dHJhbnNmb3JtOnNjYWxlKDEuMTUpO3Zpc2liaWxpdHk6aGlkZGVufX0KLmxre3dpZHRoOjEwMCU7bWF4
LXdpZHRoOjMzMHB4O3RleHQtYWxpZ246Y2VudGVyO2FuaW1hdGlvbjpjaW4gLjdzIGVhc2UgYm90aH0KLmxrLnNoYWtle2FuaW1h
dGlvbjpzaCAuNXN9Ci5sayAuaGV4e3dpZHRoOjc2cHg7aGVpZ2h0Ojc2cHg7bWFyZ2luOjAgYXV0byAxNnB4O2ZvbnQtc2l6ZToz
MnB4O2JvcmRlcj1yYWRpdXM6MjRweDthbmltYXRpb246aHggNHMgZWFzZS1pbi1vdXQgaW5maW5pdGV9Ci5sayBoMXttYXJnaW4t
Ym90dG9tOjRweH0KLmxrIGlucHV0e3RleHQtYWxpZ246Y2VudGVyO2xldHRlci1zcGFjaW5nOjEwcHg7Zm9udC1zaXplOjI0cHg7
cGFkZGluZzoxNHB4O21hcmdpbi10b3A6MjJweH0KLmxrIGlucHV0OmZvY3Vze291dGxpbmU6MDtib3JkZXItY29sb3I6dmFyKC0t
dik7Ym94LXNoYWRvdzowIDAgMCAzcHggIzhiNWNmNjU1fQo8L3N0eWxlPjwvaGVhZD48Ym9keT48ZGl2IGNsYXNzPSJvcmIgbzEi
PjwvZGl2PjxkaXYgY2xhc3M9Im9yYiBvMiI+PC9kaXY+PGNhbnZhcyBpZD0iZngiPjwvY2FudmFzPgo8ZGl2IGlkPSJsb2NrIj48
ZGl2IGNsYXNzPSJsayI+PGRpdiBjbGFzcz0iaGV4Ij5IPC9kaXY+PGgxPkhFTElYIEJPVElDPC9oMT48ZGl2IGNsYXNzPSJzdWIi
PkVudGVyIHlvdXIgYWNjZXNzIGtleSB0byBjb250aW51ZTwvZGl2PjxpbnB1dCBpZD0icHciIHR5cGU9InBhc3N3b3JkIiBpbnB1
dG1vZGU9Im51bWVyaWMiIHBsYWNlaG9sZGVyPSLigKLigKLigKLigKIiIG1heGxlbmd0aD0iMTIiIGF1dG9jb21wbGV0ZT0ib2Zm
Ij48YnV0dG9uIGlkPSJsZyIgY2xhc3M9ImJpZyI+VU5MT0NLPC9idXR0b24+PGRpdiBpZD0ibGVyciIgY2xhc3M9InN1YiIg
c3R5bGU9ImNvbG9yOnZhcigtLXIpO21pbi1oZWlnaHQ6MjBweDttYXJnaW4tdG9wOjEwcHgiPjwvZGl2PjwvZGl2PjwvZGl2Pgo8
ZGl2IGNsYXNzPSJ3Ij4KCjxkaXYgY2xhc3M9InJvdyI+PGRpdiBjbGFzcz0ibG9nbyI+PGRpdiBjbGFzcz0iaGV4Ij5IPC9kaXY+
PGRpdj48aDE+SEVMSVggQk9USUM8L2gxPjxkaXYgY2xhc3M9InN1YiI+SW5kaWNhdG9yLWJhc2VkIG1hcmtldCBhbmFseXNpczwv
ZGl2PjwvZGl2PjwvZGl2PjxzcGFuIGlkPSJtb2RlIiBjbGFzcz0iYmFkZ2UiPuKAmDwvc3Bhbj48L2Rpdj4KCjxkaXYgaWQ9InQt
ZGFzaCIgY2xhc3M9InRhYiBvbiI+Ci <div class="card">
  <label>Timeframe</label>
  <div class="seg" id="tf"><button data-v="5">5s</button><button data-v="10">10s</button><button data-v="30">30s</button><button class="on" data-v="60">1m</button><button data-v="180">3m</button><button data-v="300">5m</button><button data-v="900">15m</button></div>
  <label style="display:block;margin-top:10px">Signal filter</label>
  <div class="seg" id="rk"><button data-v="1">Strict</button><button class="on" data-v="2">Balanced</button><button data-v="3">Active</button></div>
  <div class="sub" style="margin-top:8px">Strict: 4 of 5 indicators agree, none oppose. Balanced: 3 of 5. Both also need the higher-timeframe trend, a confirming candle and normal volatility. Active: majority of 5 only.</div>
 </div>
 <div class="card"><div class="row"><b>Signal engine</b><span class="sub" id="selp"></span></div>
  <div class="eng" id="eng"><svg viewBox="0 0 240 240"><defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
   <circle cx="120" cy="120" r="104" fill="none" stroke="#ffffff12" stroke-width="8"/>
   <circle id="pg" cx="120" cy="120" r="104" fill="none" stroke="url(#gr)" stroke-width="8" stroke-linecap="round" stroke-dasharray="653.45" stroke-dashoffset="653.45" transform="rotate(-90 120 120)"/>
   <circle class="spin" cx="120" cy="120" r="116" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 14"/></svg>
   <div class="sweep"></div><div class="ctr"><div id="ic" class="ic">⚡</div><div id="sig" class="d">STANDBY</div><div id="sub" class="sub">Tap to start</div></div></div>
  <div class="mini"><div><span class="sub">Time left</span><b id="left">--:--</b></div><div><span class="sub">Strength</span><b id="str">--</b></div><div><span class="sub">Price</span><b id="px">--</b></div></div>
  <button id="go" class="big">⚡ START BOT</button></div>
 <div class="card"><div class="row"><div><b id="cn">--</b><span class="live"><i></i>LIVE</span><div class="sub" id="ci"></div></div><div style="text-align:right"><div id="cpx" class="cpx">--</div><div id="cch" class="sub"></div></div></div></div>
  <div style="position:relative;margin-top:8px"><canvas id="cv" style="width:100%;height:210px;display:block"></canvas><div id="cm" class="cm">Loading live price…⌛</div></div></div>
 <div class="card"><div class="row"><b>Markets</b><div class="seg" id="gp" style="margin:0"><button data-v="fx">Forex</button><button class="on" data-v="cr">Crypto</button></div></div><div class="grid" id="mkt"></div><div class="sub" style="margin-top:8px">Tap a market to select it. The arrow shows the live signal.</div></div>
 <div class="card"><b>Market scanner</b><div class="steps" id="steps"></div></div>
 <div class="card"><b>Indicators</b><div class="tbl" id="ind"><div><span>Waiting for a scan</span></div></div></div>
</div>

<div id="t-hist" class="tab"><div class="card"><b>History</b><div class="tbl" id="hist"></div></div></div>
<div id="t-an" class="tab"><div class="card"><b>Your real results</b><div class="sub">Counted only from signals this app logged and checked against price when the timeframe ended.</div>
 <div class="row" style="margin-top:12px"><div><div class="stat" id="aw">0</div><div class="sub">Wins</div></div><div><div class="stat" id="al">0</div><div class="sub">Losses</div></div><div><div class="stat" id="ar">--</div><div class="sub">Win rate</div></div></div></div>
 <div class="sub" id="stk" style="margin-top:12px"></div><div class="tbl" id="byp" style="margin-top:10px"></div><button id="exp" class="big" style="padding:10px;font-size:14px">Download history (CSV)</button>
 <button id="clr" class="big stop" style="padding:10px;font-size:14px">Clear history</button></div></div>
<div id="t-set" class="tab"><div class="card"><b>Preferences</b><label style="display:block;margin-top:10px">Sound and vibration on signals</label><div class="seg" id="sn"><button data-v="on">On</button><button data-v="off">Off</button></div><label style="display:block;margin-top:12px">Stop the bot after losses in a row</label><div class="seg" id="ml"><button data-v="0">Off</button><button data-v="2">2</button><button data-v="3">3</button><button data-v="5">5</button></div><button id="lo" class="big stop" style="padding:10px;font-size:14px">Log out</button></div><div class="card"><b>About</b><p class="sub" style="margin-top:8px">HELIX BOTIC uses live data only (Including Live Quotex Forex & OTC feeds, and Crypto from Binance). It scores 5 indicators (RSI 14, EMA 9/21, MACD, Bollinger bands, EMA 50 trend), then also checks the higher-timeframe trend, the last candle, volatility and your own win record on that pair before it signals. Strength shows how many agree, not the chance of winning. Seconds timeframes are close to a coin flip even with filters. Binary options can lose your whole stake: use a demo account first and never trade money you cannot lose.<br><b>AI BOT BY HELIX BOTICS</b></p></div></div></div>
<div class="warn">Not financial advice. Signals can be wrong. Win rate is only from your own logged results.<br><b>AI BOT BY HELIX BOTICS</b></div>
</div>
<div id="pop"><div class="pc"><div class="sub">SIGNAL ALERT</div><div id="pp" style="font-weight:700;margin-top:6px"></div><div id="pd" class="dir"></div><div id="pi" class="sub"></div><div class="sub" style="margin-top:12px">Take trade at</div><div id="pt" class="tm"></div><div id="pw" class="sub"></div><button class="big" id="ok">GOT IT</button></div></div>
<nav><button class="on" data-t="dash">Dashboard</button><button data-t="hist">History</button><button data-t="an">Analytics</button><button data-t="set">About</button></nav>

<script>
const $=s=>document.querySelector(s);
const FX=['EUR/USD (OTC)','GBP/USD (OTC)','USD/JPY (OTC)','USD/CAD (OTC)','USD/CHF (OTC)','EUR/GBP (OTC)','EUR/JPY (OTC)','EUR/CHF (OTC)','EUR/CAD (OTC)'];
const CR=['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT','DOGEUSDT'];
const isFx=p=>p.includes('/'),nm=p=>isFx(p)?p:p.replace('USDT','/USDT');
const tfL=t=>t<60?t+'s':t/60+'m',C=653.45;
const fmt=a=>a.toFixed(a<2?5:a<100?3:2);
const mmss=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let S={mode:'live',tf:60,rk:2,run:false,grp:'cr',pair:'BTCUSDT',hist:[],px:{},ch:{},sp:{},sig:null,snd:'on',maxL:3};
let KEY='';try{KEY=localStorage.getItem('hk')||'';S.hist=JSON.parse(localStorage.getItem('hb2')||'[]').filter(h=>h.mk!=='demo')}catch(e){}
S.hist.forEach(h=>{if(!h.res)h.res='void'});
const save=()=>{try{localStorage.setItem('hb2',JSON.stringify(S.hist))}catch(e){}};
const saveSet=()=>{try{localStorage.setItem('hx_set',JSON.stringify({snd:S.snd,maxL:S.maxL}))}catch(e){}};
try{Object.assign(S,JSON.parse(localStorage.getItem('hx_set')||'{}'))}catch(e){}
const ACCESS='5566';
function seg(id,key,num){document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));b.classList.add('on');S[key]=num?+b.dataset.v:b.dataset.v;if(key==='grp'){const L=S.grp==='fx'?FX:CR;if(!L.includes(S.pair))S.pair=L[0];$('#selp').textContent=nm(S.pair);markets();prices()}if(key==='tf'||key==='grp')chartReset();if(key==='snd'||key==='maxL')saveSet()})}
seg('#tf','tf',1);seg('#rk','rk',1);seg('#gp','grp');seg('#sn','snd');seg('#ml','maxL',1);
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{document.querySelectorAll('nav button,.tab').forEach(x=>x.classList.remove('on'));b.classList.add('on');$('#t-'+b.dataset.t).classList.add('on');render()});
function mode(){const m=$('#mode');m.textContent='LIVE DATA';m.className='badge live'}

const HOSTS=['https://api.binance.com','https://data-api.binance.vision','https://api1.binance.com','https://api2.binance.com','https://api3.binance.com'];
let Hi=0;
async function bget(path){
 let err;
 for(let k=0;k<HOSTS.length;k++){const c=new AbortController(),t=setTimeout(()=>c.abort(),6000);try{const r=await fetch(HOSTS[(Hi+k)%HOSTS.length]+path,{signal:c.signal});clearTimeout(t);if(!r.ok)throw new Error('HTTP '+r.status);const j=await r.json();Hi=(Hi+k)%HOSTS.length;return j}catch(e){err=e}}throw err;
}
const NOCONN='Cannot reach market data. Open this file in Chrome (not inside Claude), check internet, or try a VPN';
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
function eng(state,ic,txt,sub,cls){const e=$('#eng');e.className='eng '+(state==='scan'?'scanning ':''+)(state==='up'?'gu ':state==='dn'?'gd ':'')+(cls||'');void e.offsetWidth;if(state==='up'||state==='dn')e.classList.add(txt==='LOSS'?'shake':'burst');if(txt==='LOSS')e.classList.remove('burst');$('#ic').textContent=ic;$('#sig').textContent=txt;$('#sig').className='d '+(state==='up'?'up':state==='dn'?'dn':state==='nt'?'nt':'');$('#sub').textContent=sub}
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
 eng(rec.res==='win'?'up':rec.res==='loss'?'dn':-nt,rec.res==='win'?'✓':rec.res==='loss'?'✕':'=',rec.res.toUpperCase(),'Trade finished');
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
 $('#hist').innerHTML=S.hist.length?S.hist.slice(0,50).map((h,i)=>`<div class="hrwo" onclick="popup(S.hist[${i}])"><span>${nm(h.pair)} ${tfL(h.tf)} <b class="${h.dir>0?'up':'dn'}">${h.dir>0?'UP':'DOWN'}</b> • ${f(h.t)}</span><span class="${h.res==='win'?'up':h.res==='loss'?'dn':'nt'}">${h.res?h.res.toUpperCase():'pending'}</span></div>`).join(''):'<div><span>No signals yet</span></div>';
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
 CH.ci=isFx(S.pair)?(S.tf<60?'forex needs 1m or longer':tfL(S.tf)+' • Quotex OTCLive'):(S.tf>60?'1s':tfL(S.tf)+' • Binance');
 $('#ci').textContent=CH.ci;
 chartMsg('Loading live price…⌛');chartDraw();chartPull();
 CH.tm=setInterval(chartPull,isFx(S.pair)?4000:S.tf<60?1500:3000);
}
function chartDraw(){
 const cv=$('#cv');if(!cv)return;const g=cv.getContext('2d'),dpr=window.devicePixelRatio||1,W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;if(cv.width!==Math.round(W*dpr)){cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr)}
 g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);const d=CH.d;if(!d.length)return;
 let lo=Math.min(...d.map(x=>x.l)),hi=Math.max(...d.map(x=>x.h));const pad=(hi-lo)*.1||hi*.0005;lo-=pad;hi+=pad;
 const pw=48,cw=(W-pw)/d.length,y=v=>H-8-(v-lo)/(hi-lo)*(H-16);
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

boot();
</script>
</body>
</html>
"""

@app.route('/')
@app.route('/index.html')
@app.route('/index.py')
def home():
    return Response(base64.b64decode("".join(_B64.split())), mimetype='text/html; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
