import ipaddress
fqdn = "example.com."

print("router name?")

router_name = input()
fzone = []
rzone = []
lines = []
input_finished = False
print("paste show | commands | grep YOUR_PREFIX | grep address | grep interfaces")
while not input_finished:
    current_line = input()
    if current_line == "":
        input_finished = True
    else:
        if current_line.find("set interfaces") != -1:
            lines.append(current_line)
        else:
            print("Line NOT valid")

for line in lines:
    nline = ""
    interface = ""
    address = ""
    valid = True
    if line[:15] == "set interfaces ":
        nline = line[15:]
        apos = nline.find("address")
        nline2 = nline[:apos]
        address = nline.split("'")[1]
        if nline2[:8] == "ethernet":
            interface = nline2[9:-1]
        elif nline2[:9] == "wireguard":
            interface = nline2[10:-1]
        elif nline2[:6] == "bridge":
            interface = nline2[7:-1]
        elif nline2[:5] == "dummy":
            interface = nline2[6:-1]
        elif nline2[:6] == "tunnel":
            interface = nline2[7:-1]
        else:
            valid = False
    else:
        valid = False
    if valid == True:
        address = address.split("/")[0]
        fzone.append(interface+"."+router_name+"    IN AAAA    "+address)
        rzone.append(str(ipaddress.ip_address(address).reverse_pointer)+".    IN PTR "+interface+"."+router_name+"."+fqdn)

print("----FORWARD ZONE----")
for line in fzone:
    print(line)
print("----FORWARD ZONE----")

print("----REVERSE ZONE----")
for line in rzone:
    print(line)
print("----REVERSE ZONE----")


