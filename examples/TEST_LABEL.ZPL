^XA

^FX Setup printer
~JSN   ^FX Set Backfeed Sequence
^LT0   ^FX Set Label Top
^MD2   ^FX Set Media Darkness, +2
^MNW   ^FX Set Media Tracking, web sensing
^MTT   ^FX Set Media Type, thermal transfer
^PR4,4 ^FX Set Print Rate, 4 ips
^CI31  ^FX Set Character Encoding, ZCP 1250
^PW304 ^FX Set Print Width, 304 (1.5 in)
^LL203 ^FX Set Label Length, 203 (1 in)

^FX Data Matrix Barcode
^FX PN=15, Year=2, Julian=3, SN=4, Vendor=6
^FT25,110
^BXN,3,200,26,26,,,1
^FD0000000123456781736500001000421^FS

^FX Text Fields
^FT25,160^A0N,32,34^FD12345678^FS
^FT25,190^A0N,32,34^FD173650001^FS

^FX Print 1 Label
^PQ1

^XZ
