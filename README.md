# vyos-dns-ipv6-generator
Generator for AAAA and PTR entries (for BIND zonefile) from VyOS config

This is quite a simple and unpolished script.
You must first collect some output from your VYOS router, in the following pattern, while in configuration mode:

`show | commands | grep YOUR_PREFIX | grep address | grep interfaces`

example usage if you owned 2001:db8:f00/44: `show | commands | grep 2001:db8:f00 | grep address | grep interfaces`

example output from your router: 
```
set interfaces dummy dum0 address '2001:db8:f000:ffff:a::12/128'
set interfaces ethernet eth1 address '2001:db8:f000:f00d::9:92/126'
set interfaces tunnel tun777 address '2001:db8:f000:feed:beef:4444:5555:6662/126'
set interfaces wireguard wg2 address '2001:db8:f000:dead::2:41/128'
```

Now, you must set the hardcoded `fqdn` variable within the script, to your fqdn, in this case `example.com.`

When you run the script, it will prompt you for your router name, I used DOCSRTR01 as an example.

```
python script.py
router name?

DOCSRTR01
paste show | commands | grep YOUR_PREFIX | grep address | grep interfaces

set interfaces dummy dum0 address '2001:db8:f000:ffff:a::12/128'
set interfaces ethernet eth1 address '2001:db8:f000:f00d::9:92/126'
set interfaces tunnel tun777 address '2001:db8:f000:feed:beef:4444:5555:6662/126'
set interfaces wireguard wg2 address '2001:db8:f000:dead::2:41/128'

----FORWARD ZONE----
dum0.DOCSRTR01    IN AAAA    2001:db8:f000:ffff:a::12
eth1.DOCSRTR01    IN AAAA    2001:db8:f000:f00d::9:92
tun777.DOCSRTR01    IN AAAA    2001:db8:f000:feed:beef:4444:5555:6662
wg2.DOCSRTR01    IN AAAA    2001:db8:f000:dead::2:41
----FORWARD ZONE----
----REVERSE ZONE----
2.1.0.0.0.0.0.0.0.0.0.0.a.0.0.0.f.f.f.f.0.0.0.f.8.b.d.0.1.0.0.2.ip6.arpa.    IN PTR dum0.DOCSRTR01.example.com.
2.9.0.0.9.0.0.0.0.0.0.0.0.0.0.0.d.0.0.f.0.0.0.f.8.b.d.0.1.0.0.2.ip6.arpa.    IN PTR eth1.DOCSRTR01.example.com.
2.6.6.6.5.5.5.5.4.4.4.4.f.e.e.b.d.e.e.f.0.0.0.f.8.b.d.0.1.0.0.2.ip6.arpa.    IN PTR tun777.DOCSRTR01.example.com.
1.4.0.0.2.0.0.0.0.0.0.0.0.0.0.0.d.a.e.d.0.0.0.f.8.b.d.0.1.0.0.2.ip6.arpa.    IN PTR wg2.DOCSRTR01.example.com.
----REVERSE ZONE----
````

Now you have easy copy-paste lines for your BIND Zonefile.
