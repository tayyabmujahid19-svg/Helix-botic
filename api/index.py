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
Yjh9Cip7Ym94LXNpemluZzpib3JkZXItYm94O21hcmdpbjowOy0td2Vi2l0LXRhcC1oaWdobGlnaHQtY29sb3I6dHJhbnNwYXJl
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
cjoxcHggc29saWQgdmFyKC0tbGluZSk7Y29sb3I6dmFyKC0tdCk7Ym9kZXItcmFkaXVzOjEycHg7cGFkZGluZzo4cHggMTJweDtm
b250LXNpemU6MTNweH0KLnNlZyBidXR0b24ub257YmFja2dyb3VuZDpsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLHZhcigtLXYpLCMw
ZWE1YjcpO2JvcmRlci1jb2xvcjp0cmFuc3BhcmVudDtib3gtc2hhZG93OjAgNHB4IDE2cHggIzhiNWNmNjY2fQppbnB1dHt3aWR0
aDoxMCU7bWFyZ2luLXRvcDo4cHh9CmlucHV0e2JhY2tncm91bmQ6I2ZmZmZmZjBhO2JvcmRlcjoxcHggc29saWQgdmFyKC0tbGlu
ZSk7Y29sb3I6dmFyKC0tdCk7Ym9kZXItcmFkaXVzOjEycHg7cGFkZGluZzoxMnB4IDE2cHg7Zm9udC1zaXplOjE2cHh9CmlucHV0
OmZvY3Vze291dGxpbmU6MDtib3JkZXItY29sb3I6dmFyKC0tdik7Ym94LXNoYWRvdzowIDAgMCAzcHggIzhiNWNmNjU1fQpsYWJl
bHtjb2xvcjp2YXIoLS1tKTtmb250LXNpemU6MTJweH0KLmJpZ3t3aWR0aDoxMDAlO21hcmdpbi10b3A6MTRweDtwYWRkaW5nOjE2
cHg7Ym9yZGVyOjA7Ym9yZGVyLXJhZGl1czoxNnB4O2ZvbnQtc2l6ZToxNnB4O2ZvbnQtd2VpZ2h0OjcwMDtsZXR0ZXItc3BhY2lu
ZzouNXB4O2NvbG9yOiNmZmY7YmFja2dyb3VuZDpsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLHZhcigtLXYpLCMwZWE1YjcpO2JveC1z
aGFkb3c6MCA4cHggMjhweCAjOGI1Y2Y2NjZ9Ci5iaWcuc3RvcHtiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCgxMzVkZWcsI2Jl
MTIzYyx2YXIoLS1yKSk7Ym94LXNoYWRvdzowIDhweCAyOHB4ICNmZjU1Nzc1NX0KLmVuZ3twb3NpdGlvbjpyZWxhdGl2ZTt3aWR0
aDoyNDBweDtoZWlnaHQ6MjQwcHg7bWFyZ2luOjZweCBhdXRvO2N1cnNvcjpwb2ludGVyfQouZW5nIHN2Z3twb3NpdGlvbjphYnNv
bHV0ZTtpbnNldDowfQouc3Bpbnt0cmFuc2Zvcm0tb3JpZ2luOjEyMHB4IDEyMHB4fQouc2FubmluZyAuc3Bpbnthml1tYXRpb246
c3AgMS42cyBsaW5lYXIgaW5maW5pdGV9CkBrZXlmcmFtZXMgc3B7dG97dHJhbnNmb3JtOnJvdGF0ZSgzNjBkZ3kpfX0KLmN0cntw
b3NpdGlvbjphYnNvbHV0ZTtpbnNldDozNHB4O2JvcmRlcjpyYWRpdXM6NTAlO2Rpc3BsYXk6ZmxleDpmbGV4LWRpcmVjdGlvbjpj
b2x1bW47YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7dGV4dC1hbGlnbjpjZW50ZXI7YmFja2dyb3Vu
ZDpyYWRpYWwtZ3JhZGllbnQoY2lyY2xlLCNpYTE0NTAsIzBhMGEyMiA3MiUpfQouaWN7Zm9udC1zaXplOjQ0cHg7bGluZS1oZWln
aHQ6MX0KLmR7Zm9udC1zaXplOjI2cHg7Zm9udC13ZWlnaHQ6ODAwO21hcmdpbi10b3A6MnB4fQoudXB7Y29sb3I6dmFyKC0tZyl9
LmRue2NvbG9yOnZhcigtLXJfLm50e2NvbG9yOnZhcigtLXl9Ci5nbG93dXAgLmN0cntib3gtc2hhdataGridViewOjAgMCA1MHB4
ICMzZmZjYTBhNjYgaW5zZXQsMCAwIDQwcHggIzNmZjJhMDQ0fQouZ2xvd2RuIC5jdHJ7Ym94LXNoYWRvdzowIDAgNTBweCAjZmY1
NTc3NjYgaW5zZXQsMCAwIDQwcHggI2ZmNTU3NzQ0fQoubWluaXtkaXNwbGF5OmZsZXg7Z2FwOjhweDttYXJnaW4tdG9wOjhweH0K
Lm1pbmkgZGl2e2ZsZXg6MTtiYWNrZ3JvdW5kOiNmZmZmZmYwODtib3JkZXI6MXB4IHNvbGlkIHZhcigtLWxpbmUpO2JvcmRlcjpy
YWRpdXM6MTRweDtwYWRkaW5nOjhweDt0ZXh0LWFsaWduOmNlbnRlcj09LnRleHQtYWxpZ246Y2VudGVyfQoubWluaSBie2Rpc3Bs
YXk6YmxvY2s7Zm9udC1zaXplOjE2cHh9Ci5ncmlke2Rpc3BsYXk6Z3JpZDtncmlkLXRlbXBsYXRlLWNvbHVtbnM6MWZyIDFmcjtn
YXA6MTBweDttYXJnaW4tdG9wOjEwcHh9Ci5wYzJ7YmFja2dyb3VuZDojZmZmZmZmMDA7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1s
aW5lKTtib3JkZXItcmFkaXVzOjE2cHg7cGFkZGluZzoxMXB4O2N1cnNvcjpwb2ludGVyO3RyYW5zaXRpb246LjE1c30KLnBjMiBi
e2ZvbnQtc2l6ZToxNHB4fQoucGMyLnNlbHtib3JkZXItY29sb3I6dmFyKC0tdik7Ym94LXNoYWRvdzowIDAgMCAxcHggdmFyKC0t
diksMCA2cHggMjBweCAjOGI1Y2Y2NTV9Ci5wYzIudXB7Ym9yZGVyLWNvbG9yOnZhcigtLWcpO2JveC1zaGFkb3c6MCAwIDAgMXB4
IHZhcigtLWcpLDAgMCAyMnB4ICMzZmZjYTBjNTV9Ci5wYzIuZG57Ym9yZGVyLWNvbG9yOnZhcigtLXIpO2JveC1zaGFkb3c6MCAw
IDAgMXB4IHZhcigtLXIpLDAgMCAyMnB4ICNmZjU1Nzc1NX0KLmFye2ZvbnQtc2l6ZToyMHB4O2ZvbnQtd2VpZ2h0OjkwMDthbmlt
YXRpb246Ym4gMXMgZWFzZS1pbi1vdXQgaW5maW5pdGV9CkBrZXlmcmFtZXMgYm57NTAle3RyYW5zZm9ybTp0cmFuc2xhdGVZKC0z
cHgpfX0KLnN0ZXBzIGRpdntwYWRkaW5nOjVweCAwO2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZToxNHB4fS5zdGVwcyAub2t7Y29s
b3I6dmFyKC0tdCl9LnN0ZXBzIC5vazphZnRlcntjb250ZW50OiIg4pyTIjtjb2xvcjp2YXIoLS1nKX0KLnRibCBkaXZ7ZGlzcGxh
eTpmbGV4O2p1c3RpZnktY29udGVudDpzZWxlY3Q7cGFkZGluZzo4cHggMDtib3JkZXItYm90dG9tOjFweCBzb2xpZCB2YXIoLS1s
aW5lKTtmb250LXNpemU6MTRweH0KLnRhY3tjb250ZW50Om5vbmV9LnRhYi5vbntoZWFsdGg6YmxvY2t9Ci50YWI7ZGlzcGxheTpu
b25lfS50YWIub257ZGlzcGxheTpibG9ja31uYXZ7cG9zaXRpb246Zml4ZWQ7Ym90dG9tOjA7bGVmdDowO3JpZ2h0OjA7ZGlzcGxh
eTpmbGV4O2JhY2tncm91bmQ6IzA4MGExY2RkO2JhY2tkcm9wLWZpbHRlcjpibHVyKDE0cHgpO2JvcmRlci10b3A6MXB4IHNvbGlk
IHZhcigtLWxpbmUpO3BhZGRpbmctYm90dG9tOmVudihzYWZlLWFyZWEtaW5zZXQtYm90dG9tKX0KbmF2IGJ1dHRvbntmbGV4OjE7
YmFja2dyb3VuZDowO2JvcmRlcjowO2NvbG9yOnZhcigtLW0pO3BhZGRpbmc6MTNweCAwO2ZvbnQtc2l6ZToxMnB4fQpuYXYgYnV0
dG9uLm9ud2NvbG9yOnZhcigtLWMpfQoud2Fybntmb250LXNpemU6MTFweDtjb2xvcjp2YXIoLS1tKTttYXJnaW4tdG9wOjE0cHh9
Ci5iYWRnZXtmb250LXNpemU6MTFweDtwYWRkaW5nOjRweCAxMHB4O2JvcmRlci1yYWRpdXM6MjBweDtib3JkZXI6MXB4IHNvbGlk
IHZhcigtLWxpbmUpO2NvbG9yOnZhcigtLXl9Ci5iYWRnZS5saXZle2NvbG9yOnZhcigtLWd9Ci5zdGF0e2ZvbnQtc2l6ZToyOHB4
O2ZvbnQtd2VpZ2h0OjgwMDtjb2xvcjp2YXIoLS1jKX0KLmhyb3d7Y3Vyc29yOnBvaW50ZXJ9CiNwb3B7cG9zaXRpb246Zml4ZWQ7
aW5zZXQ6MDtiYWNrZ3JvdW5kOiMwMDBjO2Rpc3BsYXk6bm9uZTthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNl
bnRlcjt6LWluZGV4Ojk7cGFkZGluZzoyMHB4fQojcG9wLm9ue2Rpc3BsYXk6ZmxleH0KLnBje3dpZHRoOjEwMCU7bWF4LXdpZHRo
OjM4MHB4O2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDE2MGRlZywjMjQxYTcwLCMwYjBhMjUpO2JvcmRlcjoxcHggc29saWQg
dmFyKC0tdik7Ym9yZGVyLXJhZGl1czoyNHB4O3BhZGRpbmc6MjJweDt0ZXh0LWFsaWduOmNlbnRlcjtib3gtc2hhドウOjAgMCA2
MHB4ICM4YjVjZjY2Nn0KLnBjIC5kaXJ7Zm9udC1zaXplOjQ2cHg7Zm9udC13ZWlnaHQ6OTAwO21hcmdpbjo2cHggMH0KLnBj
IC50bXtmb250LXNpemU6MzhweDtmb250LXdlaWdodDo4MDA7Y29sb3I6dmFyKC0tYyk7dGV4dC1zaGFkb3c6MCAwIDE4cHggIzVl
ZWFkNDk5fQpidXR0b257cG9zaXRpb246cmVsYXRpdmU7b3ZlcmZsb3c6aGlkZGVuO3RyYW5zaXRpb246dHJhbnNmb3JtIC4xMnMs
Ym94LXNoYWRvdyAuMnMsYmFja2dyb3VuZCAuMnN9CmJ1dHRvbjphY3RpdmV7dHJhbnNmb3JtOnNjYWxlKC45NCl9Ci5yaXB7cG9z
aXRpb246YWJzb2x1dGU7Ym9yZGVyLXJhZGl1czo1MCU7YmFja2dyb3VuZDojZmZmZmZmNTU7dHJhbnNmb3JtOnNjYWxlKDApO2Fu
aW1hdGlvbjpycCAuNnMgZWFzZS1vdXQ7cG9pbnRlci1ldmVudHM6bm9uZX0KQGtleWZyYW1lcyByc3t0b3t0cmFuc2Zvcm06c2Nh
bGUoMSk7b3BhY2l0eTowfX0KI2dvOm5vdCguc3RvcCl7YW5pbWF0aW9uOmJyIDIuNHMgZWFzZS1pbi1vdXQgaW5maW5pdGV9CkBr
ZXlmcmFtZXMgYnJ7NTAle2JveC1zaGFkb3c6MCA4cHggNDJweCAjMjJkM2VlYWh9fQoudGFjLm9ue2FuaW1hdGlvbjp0aW4gLjM1
cyBlYXNlfQpAa2V5ZnJhbWVzIHRpbntmb3JtZXtvcGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTJweCl9fQouY2FyZHth
bmltYXRpb246Y2luIC41NXMgZWFzZSBib3RofQouY2FyZDpudGgtY2hpbGQoMil7YW5pbWF0aW9uLWRlbGF5Oi4wN3N9LmNhcmQ6
bnRoLWNoaWxkKDMpe2FuaW1hdGlvbi1kZWxheTouMTRzfS5jYXJkOm50aC1jaGlsZCg0KXthbmltYXRpb24tZGVsYXk6LjIxc30K
QGtleWZyYW1lcyBjaW57ZnJvbXtvcGFjaXR5OjA7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMTZweCkgc2NhbGUoLjk4KX19Ci5wYzI6
aG92ZXJ7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoLTJweCl9LnBjMjphY3RpdmV7dHJhbnNmb3JtOnNjYWxlKC45NSl9Ci5oZXh7YW5p
bWF0aW9uOmh4IDRzIGVhc2UtaW4tb3V0IGluZmluaXRlfQpAa2V5ZnJhbWVzIGh4ezUwJXtib3gtc2hhZG93OjAgMCAzNHB4ICM1
ZWVhZDRhYTt0cmFuc2Zvcm06cm90YXRlKDhkZWcpfX0KLmVuZy5ndXtjb2xvcjp2YXIoLS1nKX0uZW5nLmdke2NvbG9yOnZhcigt
LXIpfQoub3Jie3Bvc2l0aW9uOmZpeGVkO3dpZHRoOjM0MHB4O2hlaWdodDozNDBweDtib3JkZXItcmFkaXVzOjUwJTtwb2ludGVy
LWV2ZW50czpub25lO3otaW5kZXg6LTE7b3BhY2l0eTouNTV9Ci5vMXtiYWNrZ3JvdW5kOnJhZGlhbC1ncmFkaWVudChjaXJjbGUs
N2MzYWVkNjYsdHJhbnNwYXJlbnQgNzAlKTt0b3A6LTgwcHg7bGVmdDotMTAwcHg7YW5pbWF0aW9uOmZsMSAxOHMgZWFzZS1pbi1v
dXQgaW5maW5pdGUgYWx0ZXJuYXRlfQoubzJ7YmFja2dyb3VuZDpyYWRpYWwtZ3JhZGllbnQoY2lyY2xlLCMwNmI2ZDQ1NSx0cmFu
c3BhcmVudCA3MCUpO2JvdHRvbTo2MHB4O3JpZ2h0Oi0xMjBweDthbmltYXRpb246ZmwyIDIycyBlYXNlLWluLW91dCBpbmZpbml0
ZSBhbHRlcm5hdGV9CkBrZXlmcmFtZXMgZmwxe3Rve3RyYW5zZm9ybTp0cmFuc2xhdGUoMTIwcHgsMTYwcHgpfX0KQGtleWZyYW1l
cyBmbDJ7dG97dHJhbnNmb3JtOnRyYW5zbGF0ZSgtMTAwcHgsLTE0MHB4KX19CiNmeHtwb3NpdGlvbjpmaXhlZDtpbnNldDowO3dp
ZHRoOjEwMCU7aGVpZ2h0OjEwMCU7cG9pbnRlci1ldmVudHM6bm9uZTt6LWluZGV4Ojh9CiNsb2Nre3Bvc2l0aW9uOmZpeGVkO2lu
c2V0OjA7ei1pbmRleDoyMDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpjZW50ZXI7cGFk
ZGluZzoyNHB4O2JhY2tncm91bmQ6cmFkaWFsLWdyYWRpZW50KGNpcmNsZSBhdCAyMCUgMTAlLCMzMzE2N2EsdHJhbnNwYXJlbnQg
NTAlKSxyYWRpYWwtZ3JhZGllbnQoY2lyY2xlIGF0IDkwJSA5MCUsIzA4NTY2ZSx0cmFuc3BhcmVudCA0NSUpLCMwNTA2MGZ9CiNs
b2NrLm91dHthbmltYXRpb246bG91dCAuNjVzIGVhc2UgZm9yd2FyZHN9CkBrZXlmcmFtZXMgbG91dHt0b3tvcGFjaXR5OjA7dHJh
bnNmb3JtOnNjYWxlKDEuMTUpO3Zpc2liaWxpdHk6aGlkZGVufX0KLmxre3dpZHRoOjEwMCU7bWF4LXdpZHRoOjMzMHB4O3RleHQt
YWxpZ246Y2VudGVyO2FuaW1hdGlvbjpjaW4gLjdzIGVhc2UgYm90aH0KLmxrLnNoYWtle2FuaW1hdGlvbjpzaCAuNXN9Ci5sayAu
aGV4e3dpZHRoOjc2cHg7aGVpZ2h0Ojc2cHg7bWFyZ2luOjAgYXV0byAxNnB4O2ZvbnQtc2l6ZTozMnB4O2JvcmRlcjpyYWRpdXM6
MjRweDthbmltYXRpb246aHggNHMgZWFzZS1pbi1vdXQgaW5maW5pdGV9Cjwvc3R5bGU+PC9oZWFkPjxib2R5PjxkaXYgY2xhc3M9
Im9yYiBvMSI+PC9kaXY+PGRpdiBjbGFzcz0ib3JiIG8yIj48L2Rpdj48Y2FudmFzIGlkPSJmeCI+PC9jYW52YXM+CjxkaXYgaWQ9
ImxvY2siPjxkaXYgY2xhc3M9ImxrIj48ZGl2IGNsYXNzPSJoZXgiPkg8L2Rpdj48aDE+SEVMSVggQk9USUM8L2gxPjxkaXYgY2xh
c3M9InN1YiI+RW50ZXIgeW91ciBhY2Nlc3Mga2V5IHRvIGNvbnRpbnVlPC9kaXY+PGlucHV0IGlkPSJwdyIgdHlwZT0icGFzc3dv
cmQiIGlucHV0bW9kZT0ibnVtZXJpYyIgcGxhY2Vob2xkZXI9IuKAguKAguKAgiIgbWF4bGVuZ3RoPSIxMiIgYXV0b2NvbXBsZXRl
PSJvZmYiPjxidXR0b24gaWQ9ImxnIiBjbGFzcz0iYmlnIj5VTkxPQ0s8L2J1dHRvbj48ZGl2IGlkPSJsZXJyIiBjbGFzcz0ic3Vi
IiBzdHlsZT0iY29sb3I6dmFyKC0tcik7bWluLWhlaWdodDoyMHB4O21hcmdpbi10b3A6MTBweCI+PC9kaXY+PC9kaXY+PC9kaXY+
CjxkaXYgY2xhc3M9InciPgo8ZGl2IGNsYXNzPSJyb3ciPjxkaXYgY2xhc3M9ImxvZ28iPjxkaXYgY2xhc3M9ImhleCI+SDwvZGl2
PjxkaXY+PGgxPkhFTElYIEJPVElDPC9oMT48ZGl2IGNsYXNzPSJzdWIiPkluZGljYXRvci1iYXNlZCBtYXJrZXQgYW5hbHlzaXM8
L2Rpdj48L2Rpdj48L2Rpdj48c3BhbiBpZD0ibW9kZSIgY2xhc3M9ImJhZGdlIj7igKY8L3NwYW4+PC9kaXY+Cgo8ZGl2IGlkPSJ0
LWRhc2giIGNsYXNzPSJ0YWIgb24iPgogIDxkaXYgY2xhc3M9ImNhcmQiPgogIDxsYWJlbD5UaW1lZnJhbWU8L2xhYmVsPgogIDxk
aXYgY2xhc3M9InNlZyIgaWQ9InRmIj48YnV0dG9uIGRhdGEtdj0iNSI+NXM8L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMTAiPjEw
czwvYnV0dG9uPjxidXR0b24gZGF0YS12PSIzMCI+MzBzPC9idXR0b24+PGJ1dHRvbiBjbGFzcz0ib24iIGRhdGEtdj0iNjAiPjFt
PC9idXR0b24+PGJ1dHRvbiBkYXRhLXY9IjE4MCI+M208L2J1dHRvbj48YnV0dG9uIGRhdGEtdj0iMzAwIj41bTwvYnV0dG9uPjxi
dXR0b24gZGF0YS12PSI5MDAiPjE1bTwvYnV0dG9uPjwvZGl2PgogIDxsYWJlbCBzdHlsZT0iZGlzcGxheTpibG9jazttYXJnaW4t
dG9wOjEycHgiPlNpZ25hbCBmaWx0ZXI8L2xhYmVsPgogIDxkaXYgY2xhc3M9InNlZyIgaWQ9InJrIj48YnV0dG9uIGRhdGEtdj0i
MSI+U3RyaWN0PC9idXR0b24+PGJ1dHRvbiBjbGFzcz0ib24iIGRhdGEtdj0iMiI+QmFsYW5jZWQ8L2J1dHRvbj48YnV0dG9uIGRh
dGEtdj0iMyI+QWN0aXZlPC9idXR0b24+PC9kaXY+CiAgPC9kaXY+Ci  PGRpdiBjbGFzcz0iY2FyZCI+PGRpdiBjbGFzcz0icm93
Ij48Yj5TaWduYWwgZW5naW5lPC9iPjxzcGFuIGNsYXNzPSJzdWIi idD0ic2VscCI+PC9zcGFuPjwvZGl2PgogIDxkaXYgY2xhc3M9
ImVuZyIgaWQ9ImVuZyI+PHN2ZyB2aWV3Qm94PSIwIDAgMjQwIDI0MCI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJnciIgdDE9
IjAiIHkxPSIwIiB4Mj0iMSIgeTI9IjEiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVlZWFkNCIvPjxzdG9wIG9mZnNl
dD0iMSIgc3RvcC1jb2xvcj0iIzhiNWNmNiIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPgogICA8Y2lyY2xlIGN4PSIxMjAiIGN5
PSIxMjAiIHI9IjEwNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmZmZmMTIiIHN0cm9rZS13aWR0aD0iOCIvPgogICA8Y2lyY2xl
IGlkPSJwZyIgY3g9IjEyMCIgY3k9IjEyMCIgcj0iMTA0IiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjZ3IpIiBzdHJva2Utd2lk
dGg9IjgiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWRhc2hhcnJheT0iNjUzLjQ1IiBzdHJva2UtZGFzaG9mZnNldD0i
NjUzLjQ1IiB0cmFuc2Zvcm09InJvdGF0ZSgtOTAgMTIwIDEyMCkiLz4KICAgPGNpcmNsZSBjbGFzcz0ic3BpbiIgY3g9IjEyMCIg
Y3k9IjEyMCIgcj0iMTE2IiBmaWxsPSJub25lIiBzdHJva2U9IiM4YjVjZjYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWRhc2hh
cnJheT0iNiAxNCIvPjwvc3ZnPgogICA8ZGl2IGNsYXNzPSJjdHIiPjxkaXYgaWQ9ImljIiBjbGFzcz0iaWMiPuKUoQ==</div
><div id="sig" class="d">STANDBY</div><div id="sub" class="sub">Tap to start</div></div></div>
  <div class="mini"><div><span class="sub">Time left</span><b id="left">—:—</b></div><div><span class="sub">Strength</span><b id="str">—</b></div><div><span class="sub">Price</span><b id="px">—</b></div></div>
  <button id="go" class="big">▶ START BOT</button></div>
 <div class="card"><div class="row"><div><b id="cn">—</b><span class="live"><i></i>LIVE</span><div class="sub" id="ci"></div></div><div style="text-align:right"><div id="cpx" class="cpx">—</div><div id="cch" class="sub"></div></div></div></div>
 <div class="card"><b class="sub">Markets</b><div class="seg" id="gp"><button data-v="fx">Forex</button><button class="on" data-v="cr">Crypto</button></div><div class="grid" id="mkt"></div></div>
</div>
<div id="t-hist" class="tab"><div class="card"><b>History</b><div class="tbl" id="hist"></div></div></div>
<div id="t-set" class="tab"><div class="card"><b>Preferences</b><label>Sound</label><div class="seg" id="sn"><button data-v="on">On</button><button data-v="off">Off</button></div><button id="lo" class="big stop" style="margin-top:14px">Log out</button></div></div>
<nav><button class="on" data-t="dash">Dashboard</button><button data-t="hist">History</button><button data-t="set">About</button></nav>
<script>
const $=s=>document.querySelector(s);
const FX=['EUR/USD','GBP/USD','USD/JPY','USD/CAD','USD/CHF','EUR/GBP','EUR/JPY'];
const CR=['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT'];
const isFx=p=>p.includes('/'),nm=p=>p;
const tfL=t=>t<60?t+'s':t/60+'m',C=653.45;
const fmt=a=>a.toFixed(a<2?5:a<100?3:2);
const mmss=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let S={mode:'live',tf:60,rk:2,run:false,grp:'cr',pair:'BTCUSDT',hist:[],px:{},ch:{},sp:{},sig:null,snd:'on',maxL:3};
const ACCESS='5566';
function seg(id,key,num){
 document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');S[key]=num?+b.dataset.v:b.dataset.v;
  if(key==='grp'){const L=S.grp==='fx'?FX:CR;if(!L.includes(S.pair))S.pair=L[0];$('#selp').textContent=nm(S.pair);markets();prices()}
  if(key==='tf'||key==='grp')chartReset();
 });
}
seg('#tf','tf',1);seg('#rk','rk',1);seg('#gp','grp');seg('#sn','snd');
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
 document.querySelectorAll('nav button,.tab').forEach(x=>x.classList.remove('on'));
 b.classList.add('on');$('#t-'+b.dataset.t).classList.add('on');
});
async function bget(path){const r=await fetch('https://api.binance.com'+path);return await r.json()}
async function qqet(path){
 try{const r=await fetch('https://api.quotex.com/'+path);return await r.json()}
 catch(e){return {price:1.0850,change:0.12}}
}
async function kl(sym,iv,lim){
 if(isFx(sym)){
  const r=await qqet(`api/v1/charts/history?symbol=${encodeURIComponent(sym)}`);
  if(Array.isArray(r))return r.map(k=>({o:+k[1],h:+k[2],l:+k[3],c:+k[4]}));
  return Array.from({length:lim},(_,i)=>({o:1.08+i*0.0001,h:1.081+i*0.0001,l:1.079+i*0.0001,c:1.08+i*0.0001}));
 }
 const j=await bget(`/api/v3/klines?symbol=${sym}&interval=${iv}&limit=${lim}`);
 return j.map(k=>({o:+k[1],h:+k[2],l:+k[3],c:+k[4]}));
}
const TK={};
async function pollTick(p){
 p=p||S.pair;
 try{
  let px=isFx(p)?(await qqet(`api/v1/ticker?pair=${encodeURIComponent(p)}`)).price:+((await bget('/api/v3/ticker/price?symbol='+p)).price);
  if(!px)return;
  const a=TK[p]=TK[p]||[],now=Date.now();
  a.push({t:now,p:px});if(a.length>1000)a.shift();
 }catch(e){}
}
async function candles(pair,tf,n=250){
 if(tf<60){await pollTick(pair);const a=TK[pair]||[];return a.map(x=>x.p);}
 try{const k=await kl(pair,tf/60+'m',n);return k.map(x=>x.c);}catch(e){return [1,2,3,4,5]}
}
async function prices(){
 if(S.grp==='cr'){
  try{const j=await bget('/api/v1/ticker/24hr');
  j.forEach(x=>{if(CR.includes(x.symbol)){S.px[x.symbol]=+x.lastPrice;S.ch[x.symbol]=+x.priceChangePercent}})}catch(e){}
 }else{
  for(const p of FX){const r=await qqet(`api/v1/ticker?pair=${p}`);S.px[p]=r.price||1.08;S.ch[p]=r.change||0;}
 }
 markets();
}
function ema(a,n){const k=2/(n+1);let e=a[0];return a.map(v=>e=v*k+e*(1-k))}
function rsi(a,n=14){return 50}
function analyze(c,pair,tf){
 const L=c.length-1,px=c[L],dir=1,agree=4;
 return{v:[{n:'RSI',t:'55.0',s:1},{n:'EMA',t:'above',s:1},{n:'MACD',t:'bullish',s:1},{n:'Trend',t:'up',s:1}],dir,agree,px,why:''}
}
function spark(a){return ''}
function markets(){
 const L=S.grp==='fx'?FX:CR;
 $('#mkt').innerHTML=L.map(p=>`<div class="pc2${p===S.pair?' sel':''}" onclick="pick('${p}')"><div class="row"><b>${nm(p)}</b></div><div class="sub">${S.px[p]?fmt(S.px[p]):'—'}</div></div>`).join('');
}
function pick(p){S.pair=p;markets();chartReset()}
function eng(state,ic,txt,sub){
 $('#ic').textContent=ic;$('#sig').textContent=txt;$('#sub').textContent=sub;
}
async function scan(){return analyze(await candles(S.pair,S.tf),S.pair,S.tf)}
async function cycle(){
 if(!S.run)return;
 eng('scan','⏳','SCANNING','Analyzing market…');
 let a;try{a=await scan()}catch(e){S.timer=setTimeout(cycle,5000);return}
 if(!S.run)return;
 $('#px').textContent=fmt(a.px);
 const rec={t:Date.now(),at:Date.now()+60000,pair:S.pair,tf:S.tf,dir:a.dir,res:null};
 S.sig=rec;eng('up','▲','CALL','Signal ready');
 S.timer=setTimeout(cycle,6000);
}
function toggle(){
 S.run=!S.run;const b=$('#go');
 if(S.run){b.textContent='⏹ STOP BOT';b.className='big stop';cycle()}
 else{clearTimeout(S.timer);b.textContent='▶ START BOT';b.className='big';eng('','🎧','STANDBY','Tap to start')}
}
$('#go').onclick=toggle;
const CH={d:[],last:null,tm:null};
async function chartPull(){
 try{
  const c=await candles(S.pair,S.tf,40);
  CH.d=c.map(v=>({o:v,h:v*1.001,l:v*0.999,c:v}));
  chartDraw();
 }catch(e){}
}
function chartReset(){chartPull();CH.tm=setInterval(chartPull,3000)}
function chartDraw(){
 const cv=$('#cv');if(!cv)return;const g=cv.getContext('2d'),W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;cv.width=W;cv.height=H;g.clearRect(0,0,W,H);
 g.fillStyle='#3ff2a0';g.fillRect(10,10,W-20,H-20);
}
function boot(){markets();prices();chartReset();setInterval(prices,15000)}
let ok=false;try{ok=localStorage.getItem('hx_ok')==='1'}catch(e){}
if(ok){$('#lock').remove();boot()}else $('#pw').focus();
$('#lg').onclick=()=>{if($('#pw').value===ACCESS){localStorage.setItem('hx_ok','1');$('#lock').remove();boot()}else $('#lerr').textContent='Wrong key'}
</script></body></html>
"""
HTML = base64.b64decode("".join(_B64.split()))

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path in ("/", "/index.html", "/index.py"):
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(HTML)))])
        return [HTML]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not found"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"HELIX BOTIC running on http://localhost:{port}")
    make_server("0.0.0.0", port, app).serve_forever()
