# RouterOS test file for lexer testing

# Comments
# This is a comment

# System identity
/system identity set name="Router1"

# Interface configuration
/interface ethernet set [find name=ether1] name=wan
/interface ethernet set [find name=ether2] name=lan

# IP address
/ip address add address=192.168.1.1/24 interface=lan

# Routes
/ip route add dst-address=0.0.0.0/0 gateway=192.168.1.254

# Firewall
/ip firewall filter add chain=forward action=accept in-interface=lan out-interface=wan

# NAT
/ip firewall nat add chain=srcnat action=masquerade out-interface=wan

# DHCP server
/ip dhcp-server add name=dhcp1 interface=lan address-pool=pool1
/ip dhcp-server network add address=192.168.1.0/24 gateway=192.168.1.1

# Variables
:local var1 "test"
:local var2 100
:set var1 "modified"

# Functions
:global myFunc do={
    :return ($1 + $2)
}

# Loops
:foreach i in=[/interface find] do={
    :put [/interface get $i name]
}

# If statements
:if ($var2 > 50) do={
    :put "Greater than 50"
} else={
    :put "Less or equal 50"
}

# Logging
:log info message="RouterOS script executed"

# Menu navigation
/ip firewall address-list
add list=blocklist address=1.2.3.4
add list=blocklist address=5.6.7.8
