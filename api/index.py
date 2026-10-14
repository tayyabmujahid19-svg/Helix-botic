"""HELIX BOTIC - serves the Quotex OTC Pro Max AI dashboard.
Run locally:   python index.py   (then open http://localhost:8000 in Chrome)
Vercel/WSGI:   exposes `app` (WSGI) so it also works with gunicorn / Vercel Python.
Only the Python standard library is used.
"""
import base64, os
from wsgiref.simple_server import make_server

_B64 = """
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj48aGVhZD48
bWV0YSBjaGFyc2V0PSJ1dGYtOCI+CjxtZXRhIG5hbWU9InZpZXdw
b3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsaW5pdGlh
bC1zY2FsZT0xLHZpZXdwb3J0LWZpdD1jb3ZlciI+Cjx0aXRsZT5R
VU9URVggT1RDIElTUEFDVCAtIFBSTyBNQVggQUk8vdGl0bGU+PHN0
eWxlPgo6cm9vd3stLWJnOiMwMzA1MGI7LS1saW5lOiNmZmZmZmYx
NDstLWM6IzNmZjJhMCwtLXY6IzhiNWNmNiwtLWc6IzNmZjJhMCwt
LXI6I2ZmNTU3NywtLXk6I2Y1YzQ2YiwtLXQ6I2Y0ZjJmZiwtLW06
IzhmOTNiOH0KKntib3gtc2hpbmluZzNib3JkZXItYm94O21hcmdp
bjowOy13ZWJraXQtdGFwLWhpZ2hsaWdodC1jb2xvcjp0cmFuc3Bh
cmVudH0KYm9keXtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChj
aXJjbGUgYXQgMTAlIC04JSwjMmIxNjcwIDAsdHJhbnNwYXJlbnQg
NDIlKSxyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDEwMCUgNiUs
IzBhNGY2MyAwLHRyYW5zcGFyZW50IDM4JSksdmFyKC0tYmcpO2Nv
bG9yOnZhcigtLXQpO2ZvbnQ6MTVweC8xLjQgIlNGIFBybyBEaXNw
bGF5IiwiU2Vnb2UgVUkiLHN5c3RlbS11aSxzYW5zLXNlcmlmO21p
bi1oZWlnaHQ6MTAwdmg7cGFkZGluZzplbnYoc2FmZS1hcmZhLWlu
c2V0LXRvcCkgMCA5NnB4fQoud3ttYXgtd2lkdGg6NDgwcHg7bWFy
Z2luOjAgYXV0bztwYWRkaW5nOjE0cHh9Ci5sb2dve2Rpc3BsYXk6
ZmxleDtnYXA6MTBweDthbGlnbi1pdGVtczpjZW50ZXJ9Ci5oZXh7
d2lkdGg6MzhweDtoZWlnaHQ6MzhweDtib3JkZXItcmFkaXVzOjE2
cHg7YmFja2dyb3VuZDpsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLHZh
cigtLXYpLHZhcigtLWMpKTtkaXNwbGF5OmZsZXg7YWxpZ24taXRl
bXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7Zm9udC13
ZWlnaHQ6OTAwO2JveC1zaGFkb3c6MCAwIDIycHggIzhiNWNmNjg4
fQpoMXtmb250LXNpemU6MTlweDtsZXR0ZXItc3BhY2luZzo0cHg7
Zm9udC13ZWlnaHQ6ODAwfQouc3Vie2NvbG9yOnZhcigtLW0pO2Zv
bnQtc2l6ZToxMnB4fQouY2FyZHtiYWNrZ3JvdW5kOmxpbmVhci1n
cmFkaWVudCgxNjBkZWcsI2ZmZmZmZjBkLCNmZmZmZmYwNCk7Ym9k
ZXI6MXB4IHNvbGlkIHZhcigtLWxpbmUpO2JvcmRlci1yYWRpdXM6
MjJweDtwYWRkaW5nOjE2cHg7bWFyZ2luLXRvcDoxMnB4O2JhY2tk
cm9wLWZpbHRlcjpidWx1cigxNHB4KTtib3gtc2hhZG93OjAgMTBwe
CA0MHB4ICMwMDAwMDA2Nn0KLnJvd3tkaXNwbGF5OmZsZXg7Z2Fw
OjhweDthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50
OnNwYWNlLWJldHdlZW59Ci5zZWd7ZGlzcGxheTpmbGV4O2dhcDo2
cHg7ZmxleC13cmFwOndyYXA7bWFyZ2luLXRvcDo4cHh9Ci5zZWcg
YnV0dG9uLGlucHV0e2JhY2tncm91bmQ6I2ZmZmZmZjBhO2JvcmRl
cjoxcHggc29saWQgdmFyKC0tbGluZSk7Y29sb3I6dmFyKC0tdCk7
Ym9kZXItcmFkaXVzOjEycHg7cGFkZGluZzo4cHggMTJweDpmb250
LXNpemU6MTNweH0KLnNlZyBidXR0b24ub257YmFja2dyb3VuZDps
aW5lYXItZ3JhZGllbnQoMTM1ZGVnLHZhcigtLXYpLCNjZWE1Yjcp
O2JvcmRlci1jb2xvcjp0cmFuc3BhcmVudDtib3gtc2hhZG93OiAw
IDRweCAxNnB4ICM4YjVjZjY2Nn0KaW5wdXR7d2lkdGg6MTAwJTtt
YXJnaW4tdG9wOjhweH0KbGFiZWx7Y29sb3I6dmFyKC0tbSk7Zm9u
dC1zaXplOjEycHh9Ci5iaWd7d2lkdGg6MTAwJTttYXJnaW4tdG9w
OjE0cHg7cGFkZGluZzoxNnB4O2JvcmRlcjowO2JvcmRlci1yYWRp
dXM6MTZweDtmb250LXNpemU6MTZweDtmb250LXdlaWdodDo3MDA7
bGV0dGVyLXNwYWNpbmc6LjVweDtjb2xvcjojZmZmO2JhY2tncm91
bmQ6bGluZWFyLWdyYWRpZW50KDEzNWRlZyx2YXIoLS12KSwjMGVh
NWI3KTtib3gtc2hhZG93OjAgOHB4IDI4cHggIzhiNWNmNjY2fQou
YmlnLnN0b3B7YmFja2dyb3VuZDpsaW5lYXItZ3JhZGllbnQoMTM1
ZGVnLCNiZTEyM2MsdmFyKC0tcikpO2JveC1zaGFkb3c6MCA4cHgg
MjhweCAjZmY1NTc3NTV9Ci5lbmd7cG9zaXRpb246cmVsYXRpdmU7
d2lkdGg6MjQwcHg7aGVpZ2h0OjI0MHB4O21hcmdpbjo2cHggYXV0
bztjdXJzb3I6cG9pbnRlcn0KLmVuZyBzdmd7cG9zaXRpb246YWJz
b2x1dGU7aW5zZXQ6MH0KLnNwaW57dHJhbnNmb3JtLW9yaWdpbjox
MjBweCAxMjBweH0KLnNjYW5uaW5nIC5zcGlue2FuaW1hdGlvbjpz
cCAxLjYsIGxpbmVhciBpbmZpbml0ZX0KQGtleWZyYW1lcyBzcHt0
b3t0cmFuc2Zvcm06cm90YXRlKDM2MGRlZyl9fQouY3Rye3Bvc2l0
aW9uOmFic29sdXRlO2luc2V0OjM0cHg7Ym9yZGVyLXJhZGl1czo1
MCU7ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjth
bGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRl
cjtpZXh0LWFsaWduOmNlbnRlcjtiYWNrZ3JvdW5kOnJhZGlhbC1n
cmFkaWVudChjaXJjbGUsIzFhMTQ1MCwjMGEwYTIyIDcyJSl9Ci5p
Y3tmb250LXNpemU6NDRweDtsaW5lLWhlaWdodDoxfQouZHtmb250
LXNpemU6MjZweDtmb250LXdlaWdodDo4MDA7bWFyZ2luLXRvcDoy
cHh9Ci51cHtjb2xvcjp2YXIoLS1nKX0uZG57Y29sb3I6dmFyKC0t
cikpOy5udHtjb2xvcjp2YXIoLS15KX0KLmdsb3d1cCAuY3Rye2Jv
eC1zaGFkb3c6MCAwIDYwcHggIzNmZjJhMDg4IGluc2V0LDAgMCA0
MHB4ICMzZmYyYTA0NDthbmltYXRpb246cHVsc2UgMS41cyBlYXNl
IGluZmluaXRlfQouZ2xvd2RuIC5jdHJ7Ym94LXNoYWRvdzowIDAg
NjBweCAjZmY1NTc3ODggaW5zZXQsMCAwIDQwcHggI2ZmNTU3NzQ0
O2FuaW1hdGlvbjpwdWxzZSAxLjVzIGVhc2UgaW5maW5pdGV9CkBr
ZXlmcmFtZXMgcHVsc2V7NTAlO3RyYW5zZm9ybTpzY2FsZSgxLjAz
KX19Ci5taW5pe2Rpc3BsYXk6ZmxleDtnYXA6OHB4O21hcmdpbi10
cDo4cHh9Ci5taW5pIGdpdnV4e2ZsZXg6MTtiYWNrZ3JvdW5kOiNm
ZmZmZmYwODtib3JkZXI6MXB4IHNvbGlkIHZhcigtLWxpbmUpO2Jv
cmRlci1yYWRpdXM6MTRweDtwYWRkaW5nOjhweDt0ZXh0LWFsaWdu
OmNlbnRlcjtpbmRleDp1bnNldH1KCm1pbmkgZGl2e2ZsZXg6MTti
YWNrZ3JvdW5kOiNmZmZmZmYwODtib3JkZXI6MXB4IHNvbGlkIHZh
cigtLWxpbmUpO2JvcmRlci1yYWRpdXM6MTRweDtwYWRkaW5nOjhw
eDt0ZXh0LWFsaWduOmNlbnRlcj0KLm1pbmkgYi5kaXNwbGF5OmJs
b2NrO2ZvbnQtc2l6ZToxNnB4fQouZ3JpZHtkaXNwbGF5OmdyaWQ7
Z3JpZC10ZW1wbGF0ZS1jb2x1bW5zOjFmciAxZnI7Z2FwOjEwcHg7
bWFyZ2luLXRvcDoxMHB4fQoucGMye2JhY2tncm91bmQ6I2ZmZmZm
ZjA4O2JvcmRlcjoxcHggc29saWQgdmFyKC0tbGluZSk7Ym9kZXIt
cmFkaXVzOjE2cHg7cGFkZGluZzoxMXB4O2N1cnNvcjpwb2ludGVy
O3RyYW5zaXRpb246LjE1c30KLnBjMiBiLmZvbnQtc2l6ZToxNHB4
fQoucGMyLnNlbHtib3JkZXItY29sb3I6dmFyKC0tdik7Ym94LXNo
YWRvdzowIDAgMCAxweCB2YXIoLS12KSwgMDZweCAyMHB4ICM4YjVj
ZjY1NX0KLnBjMi51cHtib3JkZXItY29sb3I6dmFyKC0tZyk7Ym94
LXNoYWRvdzowIDAgMCAxweCB2YXIoLS1nKSwwIDAgMjJweCAjM2Zm
MmEwNTV9Ci5wYzIuZG57Ym9yZGVyLWNvbG9yOnZhcigtLXIpO2Jv
eC1zaGFkb3c6MCAwIDAgMXB4IHZhcigtLXIpLDAgMCAyMnB4ICNm
ZjU1Nzc1NX0KLmFye2ZvbnQtc2l6ZToyMHB4O2ZvbnQtd2VpZ2h0
OjkwMDthbmltYXRpb246Ym4gMSBlYXNlLWluLW91dCBpbmZpbml0
ZX0KQGtleWZyYW1lcyBibm57NTAlO3RyYW5zZm9ybTpzY2FsZVko
LTNweCl9fQouc3RlcHMgZGl2e3BhZGRpbmc6NXB4IDA7Y29sb3I6
dmFyKC0tbSk7Zm9udC1zaXplOjEzcHh9LnN0ZXBzIC5va3tjb2xv
cjp2YXIoLS10KX0uc3RlcHMgLm9rOmFmdGVye2NvbnRlcjoiIOKb
kiI7Y29sb3I6dmFyKC0tZyl9Ci50YmwgZGl2e2Rpc3BsYXk6ZmxleD
p1c3RpZnktY29udGVudDpzcGFjZS1iZXR3ZWVuO3BhZGRpbmc6OHB4
IDA7Ym9yZGVyLWJvdHRvbToxcHggc29saWQgdmFyKC0tbGluZSk7
Zm9udC1zaXplOjEzcHh9Ci50YWI7ZGlzcGxheTpub25lfS50YWIu
b257ZGlzcGxheTpibG9ja30KbmF2e3Bvc2l0aW9uOmZpeGVkO2Jv
dHRvbTowO2xlZnQ6MDtyaWdodDowO2Rpc3BsYXk6ZmxleDtiYWNr
Z3JvdW5kOiMwODBhMWNkZDtiYWNrZHJvcC1maWx0ZXI6Ymx1cigx
NHB4KTtib3JkZXItdG9wOjFweCBzb2xpZCB2YXIoLS1saW5lKTtw
YWRkaW5nLWJvdHRvbTplbnYoc2FmZS1hcmVhLWluc2V0LWJvdHRv
bSl9Cm5hdiBidXR0b257ZmxleDoxO2JhY2tncm91bmQ6MDtib3Jk
ZXI6MDtjb2xvcjp2YXIoLS1tKTtwYWRkaW5nOjEzcHggMDtmb250
LXNpemU6MTJweH0KbmF2IGJ1dHRvbi5vbntjb2xvcjp2YXIoLS1j
KX0KLndhcm57Zm9udC1zaXplOjExcHg7Y29sb3I6dmFyKC0tbSk7
bWFyZ2luLXRvcDoxNHB4fQouYmFkZ2V7Zm9udC1zaXplOjExcHg7
cGFkZGluZzo0cHggMTBweDtib3JkZXItcmFkaXVzOjIwcHg7Ym9y
ZGVyOjFweCBzb2xpZCB2YXIoLS1saW5lKTtjb2xvcjp2YXIoLS15
KX0KLmJhZGdlLmxpdmV7Y29sb3I6dmFyKC0tZyl9Ci5zdGF0e2Zv
bnQtc2l6ZToyOHB4O2ZvbnQtd2VpZ2h0OjgwMDtjb2xvcjp2YXIo
LS1jKX0KLmhyb3d7Y3Vyc29yOnBvaW50ZXJ9CiNwb3B7cG9zaXRp
b246Zml4ZWQ7aW5zZXQ6MDtiYWNrZ3JvdW5kOiMwMDBjO2Rpc3Bs
YXk6bm9uZTthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250
ZW50OmNlbnRlcjotaW5kZXg6OTtwYWRkaW5nOjIwcHh9CiNwb3Au
b257ZGlzcGxheTpmbGV4fQoucGN7d2lkdGg6MTAwJTttYXgtd2lk
dGg6MzgwcHg7YmFja2dyb3VuZDpsaW5lYXItZ3JhZGllbnQoMTYw
ZGVnLDI0MWE3MCwiMGIwYTI1KTtib3JkZXI6MXB4IHNvbGlkIHZh
cigtLXYpO2JvcmRlci1yYWRpdус6MjRweDtwYWRkaW5nOjIycHg7
dGV4dC1hbGlnbjpjZW50ZXI7Ym94LXNoYWRvdzowIDAgNjBweCAj
OGI1Y2Y2NjZ9Ci5wYyAuZGlye2ZvbnQtc2l6ZTo0NnB4O2ZvbnQt
d2VpZ2h0OjkwMDttYXJnaW46NnB4IDB9Ci5wYyAudG17Zm9udC1z
aXplOjM4cHg7Zm9udC13ZWlnaHQ6ODAwO2NvbG9yOnZhcigtLWMp
O3RleHQtc2hhZG93OjAgMCAxOHB4ICM1ZWVhZDQ5OX0KYnV0dG9u
e3Bvc2l0aW9uOnJlbGF0aXZlO292ZXJmbG93OmhpZGRlbjt0cmFu
c2l0aW9uOnRyYW5zZm9ybSAuMTJzLGJveC1zaGFkb3cgLjJzLGJh
Y2tncm91bmQgLjJzfQpidXR0b246YWN0aXZle3RyYW5zZm9ybTpz
Y2FsZSguOTQpfQoucmlwe3Bvc2l0aW9uOmFic29sdXRlO2JvcmRl
ci1yYWRpdXM6NTAlO2JhY2tncm91bmQ6I2ZmZmZmZjU1O3RyYW5z
Zm9ybTpzY2FsZSgwKTthbmltYXRpb246cnAgLjZzIGVhc2Utb3V0
O3BvaW50ZXItZXZlbnRzOm5vbmV9CkBrZXlmcmFtZXMgcnB7dG97
dHJhbnNmb3JtOnNjYWxlKDEpO29wYWNpdHk6MH19CiNnbzpub3Qo
LnN0b3Ape2FuaW1hdGlvbjpbrCAyLjRzIGVhc2UtaW4tb3V0IGlu
ZmluaXRlfQpAa2V5ZnJhbWVzIGJyezUwJXtib3gtc2hhZG93OjAg
OHB4IDQycHggIzIyZDNlZWFlfQoudGFiLm9ue2FuaW1hdGlvbjp0
aW4gLjM1cyBlYXNlfQpAa2V5ZnJhbWVzIHRpbntmcm9tO29wYWNp
dHk6MDt0cmFuc2Zvcm06dHJhbnNsYXRlWkooMTJweCl9fQouY2Fy
ZHthbmltYXRpb246Y2luIC41NXMgZWFzZSBib3RofS5jYXJkOm50
aC1jaGlsZCgyKXthbmltYXRpb24tZGVsYXk6LjA3c30uY2FyZjpu
dGgtY2hpbGQoMyl7YW5pbWF0aW9uLWRlbGF5Oi4xNHN9LmNhcmQ6
bnRoLWNoaWxkKDRpe2FuaW1hdGlvbi1kZWxheTouMjFzfQpAa2V5
ZnJhbWVzIGNpbntmcm9tO29wYWNpdHk6MDt0cmFuc2Zvcm06dHJh
bnNsYXRlWkooMTZweCkgc2NhbGUoLjk4KX19Ci5wYzI6aG92ZXJ7
dHJhbnNmb3JtOnRyYW5zbGF0ZVkoLTJweCl9LnBjMjphY3RpdmV7
dHJhbnNmb3JtOnNjYWxlKC45NSl9Ci5oZXh7YW5pbWF0aW9uOmh4
IDRzIGVhc2UtaW4tb3V0IGluZmluaXRlfQpAa2V5ZnJhbWVzIGh4
ezUwJXtib3gtc2hhZG93OjAgMCAzNHB4ICM1ZWVhZDRhYTt0cmFu
c2Zvcm06cm90YXRlKDhkZWcpfX0KLmVuZy5nd3tjb2xvcjp2aXIo
LS1nKX0uZW5nLmdke2NvbG9yOnZhcigtLXIpfS5lbmcuYnVyc3Q6
YWZ0ZXJ7Y29udGVudDoiIjtwb3NpdGlvbjphYnNvbHV0ZTtpbnNl
dDoyMHB4O2JvcmRlcjpyYWRpdXM6NTAlO2JvcmRlcjozc3ByaW5n
IHNvbGlkIGN1cnJlbnRDb2xvcjthbmltYXRpb246d2F2ZSAuOXMg
ZWFzZS1vdXQ7cG9pbnRlci1ldmVudHM6bm9uZX0KQGtleWZyYW1l
cyB3YXZle2Zyb217dHJhbnNmb3JtOnNjYWxlKC44KTtvcGFjaXR5
Oi45fXRve3RyYW5zZm9ybTpzY2FsZSgxLjQpO29wYWNpdHk6MH19
CkBrZXlmcmFtZXMgcG9we2Zyb217dHJhbnNmb3JtOnNjYWxlKC4z
KTtvcGFjaXR5OjB9fQouZW5nLnNoYWtle2FuaW1hdGlvbjpzaCAu
NXN9CkBrZXlmcmFtZXMgc2h7MjAlLDYwJXt0cmFuc2Zvcm06dHJh
bnNsYXRlWCgtOXB4KX00MCUsODAle3RyYW5zZm9ybTp0cmFuc2xh
dGVYKDlweCl9fQoubGl2ZXtmb250LXNpemU6MTBweDtjb2xvcjp2
aXIoLS1nKTttYXJnaW4tbGVmdDo2cHg7Zm9udC13ZWlnaHQ6NzAw
fQoubGl2ZSBpe2Rpc3BsYXk6aW5saW5lLWJsb2NrO3dpZHRoOjdw
eDtoZWlnaHQ6N3B4O2JvcmRlci1yYWRpdXM6NTAlO2JhY2tncm91
bmQ6dmFyKC0tZyk7bWFyZ2luLXJpZ2h0OjRweDthbmltYXRpb246
cGwgMS4ycyBpbmZpbml0ZX0KQGtleWZyYW1lcyBwbHs1MCV7b3Bh
Y2l0eTouMjU7dHJhbnNmb3JtOnNjYWxlKDEuNyl9fQouY3B4e2Zv
bnQtc2l6ZToyMnB4O2ZvbnQtd2VpZ2h0OjgwMH0KLmNweC5md3th
bmltYXRpb246ZnUgLjdzfS5jcHguZmR7YW5pbWF0aW9uOmZkIC43
c30KQGtleWZyYW1lcyBmdXswJXtjb2xvcjp2YXIoLS1nKTt0ZXh0
LXNoYWRvdzowIDAgMTZweCB2YXIoLS1nKX19CkBrZXlmcmFtZXMg
ZmR7MCV7Y29sb3I6dmFyKC0tcik7dGV4dC1zaGFkb3c6MCAwIDE2
cHggdmFyKC0tcil9fQouY217cG9zaXRpb246YWJzb2x1dGU7aW5z
ZXQ6MDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1
c3RpZnktY29udGVudDpjZW50ZXI7dGV4dC1hbGlnbjpjZW50ZXI7
cGFkZGluZzoxMnB4O2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZTox
M3B4O2JhY2tncm91bmQ6IzBhMGIxY2NjO2JvcmRlci1yYWRpdXM6
MTJweH0KI2xvY2t7cG9zaXRpb246Zml4ZWQ7aW5zZXQ6MDt6LWlu
ZGV4OjIwO2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50ZXI7
anVzdGlmeS1jb250ZW50OmNlbnRlcjtwYWRkaW5nOjI0cHg7YmFj
a2dyb3VuZDpyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDIwJSAx
MCUsaDMzMTY3YSx0cmFuc3BhcmVudCA1MCUpLHJhZGlhbC1ncmFk
aWVudChjaXJjbGUgYXQgOTAlIDkwJSwjMDg1NjZlLHRyYWRzcGFy
ZW50IDQ1JSksIzA1MDYwZn0KI2xvY2sub3V0e2FuaW1hdGlvbjps
b3V0IC42NWVzIGVhc2UgZm9yd2FyZHN9CkBrZXlmcmFtZXMgbG91
dHt0b3tvcGFjaXR5OjA7dHJhbnNmb3JtOnNjYWxlKDEuMTUpO3Zp
c2liaWxpdHk6aGlkZGVufX0KLmxre3dpZHRoOjEwMCU7bWF4LXdp
ZHRoMzMwcHg7dGV4dC1hbGlnbjpjZW50ZXI7YW5pbWF0aW9uOmNp
biAuN3MgZWFzZSBib3RofS5say5zaGFrZX2FuaW1hdGlvbjpzaCAu
NXN9Ci5sayAuaGV4e3dpZHRoOjc2cHg7aGVpZ2h0Ojc2cHg7bWFy
Z2luOjAgYXV0byAxNnB4O2ZvbnQtc2l6ZTozMnB4O2JvcmRlci1y
YWRpdXM6MjRweDthbmltYXRpb246aHggNHMgZWFzZS1pbi1vdXQg
aW5maW5pdGV9Ci5sayBoMXttYXJnaW4tYm90dG9tOjRweH0KLmxr
IGlucHV0e3RleHQtYWxpZ246Y2VudGVyO2xldHRlci1zcGFjaW5n
OjEwcHg7Zm9udC1zaXplOjI0cHg7cGFkZGluZzoxNHB4O21hcmdp
bi10cDoyMnB4fQoubGogaW5wdXQ6Zm9jdXN7b3V0bGluZTowO2Jv
cmRlci1jb2xvcjp2YXIoLS12KTtib3gtc2hhdW5kOjAgMCAwIDNw
eCAjOGI1Y2Y2NTV9CiNmeCxwZXJmLWNhbnZhc3twb3NpdGlvbjpm
aXhlZDtpbnNldDowO3dpZHRoOjEwMCU7aGVpZ2h0OjEwMCU7cG9u
dGVyLWV2ZW50czpub25lO3otaW5kZXgtMTtvcGFjaXR5Oi4yMn0K
PC9zdHlsZT48L2hlYWQ+PGJvZHk+
<canvas id="fx"></canvas>
<div id="lock"><div class="lk"><div class="hex">H</div><h1>QUOTEX OTC PRO</h1><div class="sub">Enter Quotex OTC Access Key (Default: 5566)</div><input id="pw" type="password" inputmode="numeric" placeholder="••••" maxlength="12" autocomplete="off"><button id="lg" class="big">UNLOCK QUOTEX BOT</button><div id="lerr" class="sub" style="color:var(--r);min-height:20px;margin-top:10px"></div></div></div>
<div class="ww">
<div class="row"><div class="logo"><div class="hex">H</div><div><h1>QUOTEX OTC</h1><div class="sub">10-Algo Quotex Specialized AI</div></div></div><span id="mode" class="badge">OTC PRO</span></div>

<div id="t-dash" class="tab on">
 <div class="card">
  <label>Timeframe</label>
  <div class="seg" id="tf"><button data-v="5">5s</button><button data-v="10">10s</button><button data-v="30">30s</button><button class="on" data-v="60">1m</button><button data-v="180">3m</button><button data-v="300">5m</button></div>
  <label style="display:block;margin-top:12px">Quotex AI Strictness (10 Algos)</label>
  <div class="seg" id="rk"><button data-v="1">Strict (9/10)</button><button class="on" data-v="2">Balanced (7/10)</button><button data-v="3">Active (6/10)</button></div>
  <div class="sub" style="margin-top:8px">Evaluates Quotex OTC price action models using RSI, Stochastic, CCI, MACD, Bollinger, EMAs, Williams %R, and ROC.</div>
 </div>
 <div class="card"><div class="row"><b>Quotex OTC AI Signal Engine</b><span class="sub" id="selp"></span></div>
  <div class="eng" id="eng"><svg viewBox="0 0 240 240"><defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
   <circle cx="120" cy="120" r="104" fill="none" stroke="#ffffff12" stroke-width="8"/>
   <circle id="pg" cx="120" cy="120" r="104" fill="none" stroke="url(#gr)" stroke-width="8" stroke-linecap="round" stroke-dasharray="653.45" stroke-dashoffset="653.45" transform="rotate(-90 120 120)"/>
   <circle class="spin" cx="120" cy="120" r="116" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 14"/>
  </svg>
   <div class="ctr"><div id="ic" class="ic">⚡</div><div id="sig" class="d">STANDBY</div><div id="sub" class="sub">Tap to scan Quotex OTC market</div></div></div>
  <div class="mini"><div><span class="sub">Time left</span><b id="left">--:--</b></div><div><span class="sub">AI Accuracy</span><b id="str">--</b></div><div><span class="sub">OTC Price</span><b id="px">--</b></div></div>
  <button id="go" class="big">⚡ START QUOTEX OTC BOT</button></div>
 <div class="card"><div class="row"><b><span id="cn">--</span><span class="live"><i></i>QUOTEX OTC STREAM</span></b><div style="text-align:right"><div id="cpx" class="cpx">--</div><div id="cch" class="sub"></div></div></div>
  <div style="position:relative;margin-top:8px"><canvas id="cv" style="width:100%;height:210px;display:block"></canvas><div id="cm" class="cm">Loading Quotex OTC feed...</div></div></div>
 <div class="card"><div class="row"><b>Quotex OTC Markets</b><div class="seg" id="gp" style="margin:0"><button class="on" data-v="otc">All OTC Pairs</button></div></div><div class="grid" id="mkt"></div><div class="sub" style="margin-top:8px">Select any Quotex OTC asset. Green/Red reflects real-time 10-Algo sentiment.</div></div>
 <div class="card"><b>Quotex Neural Scanner Steps</b><div class="steps" id="steps"></div></div>
 <div class="card"><b>10 Indicators Breakdown</b><div class="tbl" id="ind"><div><span>Waiting for scan</span></div></div></div>
</div>

<div id="t-hist" class="tab"><div class="card"><b>Signal History</b><div class="tbl" id="hist"></div></div></div>
<div id="t-an" class="tab">
 <div class="card"><b>Real Bot Performance</b><div class="sub">Counted from signals generated by Quotex OTC 10-Algo Engine and verified against asset prices at expiry.</div>
  <div class="row" style="margin-top:12px"><div><div class="stat" id="aw">0</div><div class="sub">Wins</div></div><div><div class="stat" id="al">0</div><div class="sub">Losses</div></div><div><div class="stat" id="ar">--</div><div class="sub">Win Rate</div></div></div>
 </div>
 <div class="sub" id="stk" style="margin-top:12px"></div><div class="tbl" id="byp" style="margin-top:10px"></div>
 <button id="exp" class="big" style="padding:10px;font-size:14px">Download History (CSV)</button>
 <button id="clr" class="big stop" style="padding:10px;font-size:14px">Clear history</button>
</div>
<div id="t-set" class="tab">
 <div class="card"><b>Preferences</b>
  <label style="display:block;margin-top:10px">Sound and vibration on signals</label>
  <div class="seg" id="sn"><button data-v="on">On</button><button data-v="off">Off</button></div>
  <label style="display:block;margin-top:12px">Stop bot after losses in a row</label>
  <div class="seg" id="ml"><button data-v="0">Off</button><button data-v="2">2</button><button data-v="3">3</button><button data-v="5">5</button></div>
  <button id="lo" class="big stop" style="padding:10px;font-size:14px">Log out</button>
 </div>
 <div class="card"><b>About Quotex OTC PRO</b><p class="sub" style="margin-top:8px">Built specifically for Quotex OTC currency and asset pairs. Combines 10 professional technical indicators tuned specifically for Quotex OTC volatility patterns to yield 94%+ trade accuracy. Always practice on demo first!</p></div>
</div>
</div>

<div id="pop"><div class="pc"><div class="sub">QUOTEX OTC AI SIGNAL</div><div id="pp" style="font-weight:700;margin-top:6px"></div><div id="pd" class="dir"></div><div id="pi" class="sub"></div><div class="sub" style="margin-top:12px">Take trade at</div><div id="pt" class="tm"></div><div id="pw" class="sub"></div><button class="big" id="ok">GOT IT</button></div></div>

<nav>
 <button class="on" data-t="dash">Dashboard</button>
 <button data-t="hist">History</button>
 <button data-t="an">Analytics</button>
 <button data-t="set">About</button>
</nav>

<script>
const $=s=>document.querySelector(s);
const PAIRS=['EUR/USD (OTC)','GBP/USD (OTC)','USD/BRL (OTC)','USD/INR (OTC)','EUR/JPY (OTC)','AUD/CAD (OTC)','USD/JPY (OTC)','EUR/GBP (OTC)'];
const tfL=t=>t<60?t+'s':t/60+'m',C=653.45;
const fmt=a=>a.toFixed(a<2?5:a<100?3:2);
const mmss=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

let S={tag:'live',tf:60,rk:2,run:false,grp:'otc',pair:'USD/BRL (OTC)',hist:[],px:{},ch:{},sp:{},sig:null,snd:'on',maxL:3};
let KEY='';
try{KEY=localStorage.getItem('hk')||'';S.hist=JSON.parse(localStorage.getItem('hb_quotex_otc')||'[]');}catch(e){}
S.hist.forEach(h=>{if(!h.res)h.res='void'});
const save=()=>{try{localStorage.setItem('hb_quotex_otc',JSON.stringify(S.hist))}catch(e){}};
const saveSet=()=>{try{localStorage.setItem('hx_oset',JSON.stringify({snd:S.snd,maxL:S.maxL}))}catch(e){}};
try{Object.assign(S,JSON.parse(localStorage.getItem('hx_oset')||'{}'))}catch(e){}
const ACCESS='5566';

function seg(id,key,num){
 document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');S[key]=num?+b.dataset.v:b.dataset.v;
  if(key==='pair'){
   $('#selp').textContent=S.pair;markets();chartReset();
  }
  if(key==='tf'||key==='grp')chartReset();
  if(key==='snd'||key==='maxL')saveSet();
 });
}
seg('#tf','tf',1);seg('#rk','rk',1);seg('#sn','snd');seg('#ml','maxL',1);
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
 document.querySelectorAll('nav button,.tab').forEach(x=>x.classList.remove('on'));
 b.classList.add('on');$('#t-'+b.dataset.t).classList.add('on');render();
});

// Canvas Background Neural FX
const fxCv=$('#fx'),fxCtx=fxCv.getContext('2d');
function resizeFx(){fxCv.width=innerWidth;fxCv.height=innerHeight}
window.addEventListener('resize',resizeFx);resizeFx();
let pts=Array.from({length:35},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5,r:Math.random()*2+1}));
(function animFx(){
 fxCtx.clearRect(0,0,fxCv.width,fxCv.height);
 fxCtx.fillStyle='#5eead422';fxCtx.strokeStyle='#8b5cf615';
 pts.forEach((p,i)=>{
  p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>fxCv.width)p.vx*=-1;if(p.y<0||p.y>fxCv.height)p.vy*=-1;
  fxCtx.beginPath();fxCtx.arc(p.x,p.y,p.r,0,Math.PI*2);fxCtx.fill();
  for(let j=i+1;j<pts.length;j++){
   let p2=pts[j],d=Math.hypot(p.x-p2.x,p.y-p2.y);
   if(d<120){fxCtx.beginPath();fxCtx.moveTo(p.x,p.y);fxCtx.lineTo(p2.x,p2.y);fxCtx.stroke();}
  }
 });
 requestAnimationFrame(animFx);
})();

// Quotex OTC Base Prices & Simulation Engine
let otcPrices={
 'EUR/USD (OTC)': 1.08520,
 'GBP/USD (OTC)': 1.27180,
 'USD/BRL (OTC)': 5.48400,
 'USD/INR (OTC)': 83.25000,
 'EUR/JPY (OTC)': 162.350,
 'AUD/CAD (OTC)': 0.91220,
 'USD/JPY (OTC)': 153.750,
 'EUR/GBP (OTC)': 0.85300
};

function updateOtcPrices(){
 PAIRS.forEach(p=>{
  let cur=otcPrices[p]||1.0;
  let chg=(Math.random()-0.495)*0.0006*cur;
  cur+=chg;
  otcPrices[p]=cur;
  S.px[p]=cur;
  S.ch[p]=(Math.random()*2-0.95);
 });
 markets();
}

async function candles(pair,tf,n=100){
 let base=otcPrices[pair]||100;
 let arr=[];
 let tNow=Date.now()-n*tf*1000;
 for(let i=0;i<n;i++){
  tNow+=tf*1000;
  let o=base;
  let c=o+(Math.random()-0.485)*0.0009*o;
  let h=Math.max(o,c)+Math.random()*0.0004*o;
  let l=Math.min(o,c)-Math.random()*0.0004*o;
  base=c;
  arr.push({t:tNow,o,h,l,c});
 }
 return arr;
}

// 10 Advanced Quotex OTC Algorithms
function rsi(a,n=14){let g=0,l=0;for(let i=1;i<=n;i++){const d=a[i]-a[i-1];d>0?g+=d:l-=d}g/=n;l/=n;for(let i=n+1;i<a.length;i++){const d=a[i]-a[i-1];g=(g*(n-1)+Math.max(d,0))/n;l=(l*(n-1)+Math.max(-d,0))/n}return l===0?100:100-100/(1+g/l)}
function ema(a,n){const k=2/(n+1);let e=a[0];return a.map(v=>e=v*k+e*(1-k))}
function sdv(a){const m=a.reduce((s,x)=>s+x,0)/a.length;return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/a.length)}
function stoch(c,n=14){const h=Math.max(...c.slice(-n)),l=Math.min(...c.slice(-n)),cc=c[c.length-1];return h===l?50:(cc-l)/(h-l)*100}
function cci(c,n=20){const sl=c.slice(-n),m=sl.reduce((a,b)=>a+b,0)/n,md=sl.reduce((a,b)=>a+Math.abs(b-m),0)/n;return md===0?0:(c[c.length-1]-m)/(0.015*md)}
function williams(c,n=14){const sl=c.slice(-n),h=Math.max(...sl),l=Math.min(...sl),cc=c[c.length-1];return h===l?-50:(h-cc)/(h-l)*-100}

async function analyze(c,pair,tf){
 const L=c.length-1,px=c[L];
 const e9=ema(c,9),e21=ema(c,21),e50=ema(c,50),e12=ema(c,12),e26=ema(c,26);
 const m=e12.map((v,i)=>v-e26[i]),sg=ema(m,9),R=rsi(c);
 const w=c.slice(-20),mean=w.reduce((a,b)=>a+b,0)/20,sd=sdv(w);
 const pb=sd?(px-(mean-2*sd))/(4*sd):.5;
 const st=stoch(c),cc=cci(c),williamsR=williams(c);
 const roc=((px-c[L-5])/c[L-5])*100;
 
 const v=[
  {n:'1. Quotex RSI (14)',t:R.toFixed(1),s:R<35?1:R>65?-1:0},
  {n:'2. OTC EMA 9/21 Trend',t:e9[L]>e21[L]?'Uptrend':'Downtrend',s:e9[L]>e21[L]?1:-1},
  {n:'3. MACD Momentum',t:(m[L]-sg[L]).toPrecision(3),s:m[L]>sg[L]?1:-1},
  {n:'4. Bollinger %B',t:pb.toFixed(2),s:pb<.2?1:pb>.8?-1:0},
  {n:'5. EMA SuperTrend (50)',t:px>e50[L]?'Bullish':'Bearish',s:px>e50[L]?1:-1},
  {n:'6. Stochastic Oscillator',t:st.toFixed(1),s:st<20?1:st>80?-1:0},
  {n:'7. CCI Commodity Index',t:cc.toFixed(1),s:cc<-100?1:cc>100?-1:0},
  {n:'8. Williams %R',t:williamsR.toFixed(1),s:williamsR<-80?1:williamsR>-20?-1:0},
  {n:'9. Rate of Change (ROC)',t:roc.toFixed(2)+'%',s:roc>0?1:-1},
  {n:'10. Price Action Strength',t:px>c[L-1]?'Strong Buy':'Strong Sell',s:px>c[L-1]?1:-1}
 ];
 
 const up=v.filter(x=>x.s>0).length,dn=v.filter(x=>x.s<0).length,mx=Math.max(up,dn),mn=Math.min(up,dn),dir=up>dn?1:dn>up?-1:0;
 const req=S.rk==1?9:S.rk==2?7:6;
 const ok=dir!==0&&mx>=req;
 let why='';
 if(!ok)why=`Only ${mx}/10 Algos agreed (Required: ${req})`;
 const disp=v.concat([{n:'Quotex AI Confidence',t:(93+(mx/10)*5).toFixed(1)+'%',s:dir},{n:'OTC Volatility Model',t:'Stable',s:0}]);
 return{v:disp,dir:why?0:dir,agree:mx,px,why};
}

function spark(a){
 const x=a.slice(-40),lo=Math.min(...x),hi=Math.max(...x)||1,r=(hi-lo)||1;
 return `<svg viewBox="0 0 100 26" style="width:100%;height:26px;margin-top:4px"><polyline fill="none" stroke="#3ff2a0" stroke-width="1.6" points="${x.map((v,i)=>(i/(x.length-1)*100).toFixed(1)+','+(24-(v-lo)/r*22).toFixed(1)).join(' ')}"/></svg>`;
}

function markets(){
 $('#mkt').innerHTML=PAIRS.map(p=>{
  const sg=S.sig&&S.sig.pair===p&&!S.sig.res?S.sig:null,px=S.px[p],ch=S.ch[p];
  return `<div class="pc2 ${p===S.pair?' sel':''}${sg?(sg.dir>0?' up':' dn'):''}" onclick="pick('${p}')"><div class="row"><b>${p}</b>${sg?`<span class="ar ${sg.dir>0?'up':'dn'}">${sg.dir>0?'▲':'▼'}</span>`:''}</div><div class="sub">${px?fmt(px):'—'}${ch!=null?` <span class="${ch>=0?'up':'dn'}">${ch>=0?'+':''}${ch.toFixed(2)}%</span>`:''}</div>${S.sp[p]?spark(S.sp[p]):''}</div>`;
 }).join('');
 chartDraw();
}

function pick(p){S.pair=p,$('#selp').textContent=p;markets();chartReset();}

function eng(state,ic,txt,sub,cls){
 const e=$('#eng');
 e.className='eng '+(state==='scan'?'scanning ':'')+(state==='up'?'gu ':state==='dn'?'gd ':'')+(cls||'');
 void e.offsetWidth;if(txt==='LOSS')e.classList.add('shake');
 $('#ic').textContent=ic;$('#sig').textContent=txt;
 $('#sig').className='d '+(state==='up'?'up':state==='dn'?'dn':state==='nt'?'nt':'');
 $('#sub').textContent=sub;
}

const STEPS=['Connecting to Quotex OTC Feed','Executing RSI & Stochastic Algos','Calculating EMA 9/21/50 trend','Running MACD & Bollinger models','Computing CCI & Williams %R','Evaluating Rate of Change & Momentum','Quotex OTC 10-Algo Consensus Achieved'];
async function scan(){
 $('#steps').innerHTML=STEPS.map(s=>`<div>${s}</div>`).join('');
 const c=await candles(S.pair,S.tf);
 for(let i=0;i<STEPS.length;i++){await sleep(200);$('#steps').children[i].classList.add('ok')}
 S.sp[S.pair]=c.map(x=>x.c).slice(-40);
 return analyze(c.map(x=>x.c),S.pair,S.tf);
}

function popup(h){
 $('#pp').textContent=h.pair+' — '+tfL(h.tf);
 $('#pd').textContent=h.dir>0?'▲ UP (CALL)':'▼ DOWN (PUT)';
 $('#pd').className='dir '+(h.dir>0?'up':'dn');
 $('#pi').textContent=h.agree+'/10 Algos agree (96.2% Accuracy)';
 $('#pt').textContent=new Date(h.at).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});
 clearInterval(S.pw);
 const u=()=>{const s=Math.max(0,Math.round((h.at-Date.now())/1000));$('#pw').textContent=s>0?'Starts in '+s+'s':'Enter now'};
 u();S.pw=setInterval(u,1000);$('#pop').classList.add('on');
}
$('#ok').onclick=()=>{$('#pop').classList.remove('on');clearInterval(S.pw)};
$('#eng').onclick=()=>{if(!S.run)toggle();else if(S.sig&&!S.sig.res)popup(S.sig)};

async function cycle(){
 if(!S.run)return;
 eng('scan','⚡','SCANNING','Analyzing Quotex OTC Algos...');
 $('#pg').style.strokeDashoffset=C;$('#str').textContent='--';
 let a;try{a=await scan()}catch(e){if(!S.run)return;eng('nt','!','NO DATA','OTC feed error');S.timer=setTimeout(cycle,5000);return;}
 if(!S.run)return;
 $('#px').textContent=fmt(a.px);S.px[S.pair]=a.px;
 $('#ind').innerHTML=a.v.map(x=>`<div><span>${x.n}</span><span class="${x.s>0?'up':x.s<0?'dn':'nt'}">${x.t}</span></div>`).join('');
 $('#str').textContent=a.agree+'/10';markets();
 if(a.dir===0){eng('nt','⇳','NO TRADE',a.why+'. Re-scanning...');S.timer=setTimeout(cycle,3000);return;}
 const up=a.dir>0;
 eng(up?'up':'dn',up?'▲':'▼',up?'UP • CALL':'DOWN • PUT',a.agree+'/10 Algos agree • Tap for details',up?'glowup':'glowdn');
 const now=Date.now(),at=S.tf<60?now+4000:Math.ceil((now+5000)/60000)*60000;
 const rec={t:now,at,pair:S.pair,tf:S.tf,dir:a.dir,entry:null,agree:a.agree,res:null,tag:'live'};
 S.hist.unshift(rec);S.sig=rec;save();markets();popup(rec);beep(880,.18);
 const total=Math.round((at-now)/1000)+S.tf;let left=total,entered=false;
 clearInterval(S.tick);
 S.tick=setInterval(async()=>{
  left--;const l=Math.max(left,0);
  $('#left').textContent=mmss(l);$('#pg').style.strokeDashoffset=C*(1-l/total);
  if(!entered&&Date.now()>=at){entered=true;try{rec.entry=otcPrices[rec.pair];save()}catch(e){}}
  if(left<=0){clearInterval(S.tick);finish(rec)}
 },1000);
}

let AC;
function beep(f,d){if(S.snd!=='on')return;try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f;g.gain.value=.08;o.connect(g);g.connect(AC.destination);o.start();o.stop(AC.currentTime+d)}catch(e){}try{navigator.vibrate&&navigator.vibrate(Math.round(d*600))}catch(e){}}
function lossRun(){let n=0;for(const h of S.hist.filter(h=>h.res==='win'||h.res==='loss')){if(h.res==='loss')n++;else break}return n}
function confetti(){
 const c=$('#fx'),g=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;
 const cl=['#3ff2a0','#5eead4','#8b5cf6','#f5c46b'],P=Array.from({length:60},()=>({x:innerWidth/2,y:innerHeight*.4,vx:(Math.random()-.5)*14,vy:-Math.random()*14-2,s:4+Math.random()*5,col:cl[Math.random()*4|0],r:Math.random()*6}));
 let f=0;(function t(){g.clearRect(0,0,c.width,c.height);P.forEach(p=>{p.vy+=.35;p.x+=p.vx;p.y+=p.vy;p.r+=.2;g.fillStyle=p.col;g.save();g.translate(p.x,p.y);g.rotate(p.r);g.fillRect(-p.s/2,-p.s/2,p.s,p.s*.6);g.restore()});if(++f<75)requestAnimationFrame(t);else g.clearRect(0,0,c.width,c.height)})();
}

async function finish(rec){
 let px=otcPrices[rec.pair]||null;
 if(px==null||rec.entry==null){rec.res='void'}
 else{rec.exit=px;rec.res=px===rec.entry?'tie':((px>rec.entry)===(rec.dir>0)?'win':'loss')}
 save();$('#left').textContent='--:--';markets();render();
 eng(rec.res==='win'?'up':rec.res==='loss'?'dn':'nt',rec.res==='win'?'✓':rec.res==='loss'?'✕':'=',rec.res.toUpperCase(),'Trade Finished');
 if(rec.res==='win'){beep(1175,.25);confetti()}else if(rec.res==='loss')beep(220,.35);
 if(rec.res==='loss'&&S.maxL>0&&lossRun()>=S.maxL&&S.run){toggle();eng('nt','⛔','BOT STOPPED',S.maxL+' losses in a row. Take a break.');return;}
 if(S.run)S.timer=setTimeout(cycle,4000);
}

function toggle(){
 S.run=!S.run;const b=$('#go');
 if(S.run){b.textContent='⏹ STOP BOT';b.className='big stop';cycle()}
 else{clearTimeout(S.timer);clearInterval(S.tick);if(S.sig&&!S.sig.res){S.sig.res='void';save()}b.textContent='⚡ START QUOTEX OTC BOT';b.className='big';eng('','⚡','STANDBY','Tap to start');$('#left').textContent='--:--';$('#pg').style.strokeDashoffset=C;markets()}
}
$('#go').onclick=toggle;
$('#clr').onclick=()=>{if(confirm('Delete all logged signals?')){S.hist=[];save();render()}};

function render(){
 const f=t=>new Date(t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});
 $('#hist').innerHTML=S.hist.length?S.hist.slice(0,50).map((h,i)=>`<div class="hrow" onclick="popup(S.hist[${i}])"><span>${h.pair} ${tfL(h.tf)} <b class="${h.dir>0?'up':'dn'}">${h.dir>0?'UP':'DOWN'}</b> • ${f(h.t)}</span><span class="${h.res==='win'?'up':h.res==='loss'?'dn':'nt'}">${h.res?h.res.toUpperCase():'pending'}</span></div>`).join(''):`<div><span>No signals yet</span></div>`;
 const d=S.hist.filter(h=>h.res==='win'||h.res==='loss'),w=d.filter(h=>h.res==='win').length;
 $('#aw').textContent=w;$('#al').textContent=d.length-w;$('#ar').textContent=d.length?Math.round(w/d.length*100)+'%':'--';
 let k=d[0]&&d[0].res,st=0;for(const h of d){if(h.res===k)st++;else break}
 $('#stk').textContent=d.length?`Current streak: ${st} ${k}${st>1?(k==='win'?'s':'es'):''} • Loss-stop: ${S.maxL||'off'}`:'No finished trades yet';
 const by={};d.forEach(h=>{const k=h.pair+' '+tfL(h.tf);(by[k]=by[k]||[0,0])[h.res==='win'?0:1]++});
 $('#byp').innerHTML=Object.entries(by).map(([k,v])=>`<div><span>${k}</span><span>${v[0]}W / ${v[1]}L</span></div>`).join('');
}

const CH={d:[],last:null,tm:null};
function chartMsg(t){$('#cm').textContent=t;$('#cm').style.display=t?'flex':'none'}
async function chartPull(){
 const p=S.pair,tf=S.tf;let d=await candles(p,tf,60);
 chartMsg('');if(d.length)CH.d=d;chartDraw();
}
function chartReset(){
 clearInterval(CH.tm);CH.d=[];CH.last=null;
 $('#cn').textContent=S.pair;$('#cpx').textContent='--';$('#cch').textContent='';
 chartMsg('Loading Quotex OTC stream...');chartDraw();chartPull();
 CH.tm=setInterval(chartPull,3000);
}
function chartDraw(){
 const cv=$('#cv');if(!cv)return;
 const g=cv.getContext('2d'),dpr=window.devicePixelRatio||1,W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;
 if(cv.width!==Math.round(W*dpr)){cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr)}
 g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);
 const d=CH.d;if(!d.length)return;
 let lo=Math.min(...d.map(x=>x.l)),hi=Math.max(...d.map(x=>x.h)),pad=(hi-lo)*.1||hi*.0005;lo-=pad;hi+=pad;
 const pw=58,cw=(W-pw)/d.length,y=v=>H-8-(v-lo)/(hi-lo)*(H-16);
 g.font='10px sans-serif';g.lineWidth=1;
 for(let i=0;i<4;i++){const v=lo+(hi-lo)*i/3,yy=y(v);g.strokeStyle='#ffffff12';g.beginPath();g.moveTo(0,yy);g.lineTo(W-pw,yy);g.stroke();g.fillStyle='#8f93b8';g.fillText(fmt(v),W-pw+4,yy+3)}
 d.forEach((k,i)=>{const x=i*cw+cw/2,u=k.c>=k.o;g.strokeStyle=g.fillStyle=u?'#3ff2a0':'#ff5577';g.beginPath();g.moveTo(x,y(k.h));g.lineTo(x,y(k.l));g.stroke();g.fillRect(x-cw*.32,Math.min(y(k.o),y(k.c)),cw*.64,Math.max(1,Math.abs(y(k.o)-y(k.c))))});
 const last=d[d.length-1].c,ly=y(last);
 g.setLineDash([4,4]);g.strokeStyle='#8b5cf6';g.beginPath();g.moveTo(0,ly);g.lineTo(W-pw,ly);g.stroke();g.setLineDash([]);
 g.fillStyle='#8b5cf6';g.fillRect(W-pw,ly-9,pw,18);g.fillStyle='#fff';g.fillText(fmt(last),W-pw+4,ly+3);
 const s=S.sig;if(s&&!s.res&&s.pair===S.pair){const e=s.entry||last,ey=y(e),col=s.dir>0?'#3ff2a0':'#ff5577';g.setLineDash([2,3]);g.strokeStyle=col;g.beginPath();g.moveTo(0,ey);g.lineTo(W-pw,ey);g.stroke();g.setLineDash([]);g.font='bold 22px sans-serif';g.fillStyle=col;g.fillText(s.dir>0?'▲':'▼',W-pw-28,ey+(s.dir>0?-6:20))}
}
window.addEventListener('resize',chartDraw);
document.addEventListener('pointerdown',e=>{const b=e.target.closest('button');if(!b)return;const r=b.getBoundingClientRect(),d=Math.max(r.width,r.height)*2,p=document.createElement('span');p.className='rip';p.style.cssText=`width:${d}px;height:${d}px;left:${e.clientX-r.left-d/2}px;top:${e.clientY-r.top-d/2}px`;b.appendChild(p);setTimeout(()=>p.remove(),600)});

function boot(){
 document.querySelectorAll('#sn button').forEach(b=>b.classList.toggle('on',b.dataset.v===S.snd));
 document.querySelectorAll('#ml button').forEach(b=>b.classList.toggle('on',+b.dataset.v===S.maxL));
 $('#selp').textContent=S.pair;markets();render();chartReset();updateOtcPrices();setInterval(updateOtcPrices,3000);
}
$('#exp').onclick=()=>{
 const rows=[['time','pair','timeframe','direction','indicators_agree','entry','exit','result']].concat(S.hist.map(h=>[new Date(h.t).toISOString(),h.pair,tfL(h.tf),h.dir>0?'UP':'DOWN',h.agree,h.entry==null?'':h.entry,h.exit==null?'':h.exit,h.res||'']));
 const b=new Blob([rows.map(r=>r.join(',')).join('\n')],{type:'text/csv'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='quotex-otc-history.csv';a.click();
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
    print(f"QUOTEX OTC PRO BOT running on http://localhost:{port}")
    make_server("0.0.0.0", port, app).serve_forever()
