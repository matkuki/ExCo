
# -*- coding: utf-8 -*-

"""
Copyright (c) 2018 Matic Kukovec. 
"""

import keyword
import builtins
import re
import functions
import data
import time
import lexers


class RouterOS(data.QsciLexerCustom):
    """
    Custom lexer for the RouterOS syntax for MikroTik routers (WinBox)
    """
    styles = {
        "Default" : 0,
        "Operator" : 1,
        "Comment" : 2,
        "Keyword1" : 3,
        "Keyword2" :  4,
        "Keyword3" : 5,
    }
    #Class variables
    default_color       = data.QColor(data.theme.Font.RouterOS.Default[1])
    default_paper       = data.QColor(data.theme.Paper.RouterOS.Default)
    default_font        = data.QFont(data.current_font_name, data.current_font_size)
    #All keywords, operators, ...
    operator_list = [
        '!', '$', '(', ')', ',', ':', '[', ']', '{', '|', '}', "="
    ]
    comment_list = [
        '#'
    ]
    keyword1_list = [
        'ac-name', 'accept', 'accessible-via-web', 'account-local-traffic', 'accounting', 'action', 'active-flow-timeout', 'active-mode', 'add-default-route', 'address-list', 'address-pool', 'address', 'addresses-per-mac', 'admin-mac', 'advertise-dns', 'advertise-mac-address', 'ageing-time', 'allocate-udp-ports-from', 'allow-disable-external-interface', 'allow-guests', 'allow-remote-requests', 'allow', 'allowed-number', 'always-from-cache', 'area-id', 'area', 'arp', 'as', 'audio-max', 'audio-min', 'audio-monitor', 'auth-algorithms', 'auth-method', 'auth', 'authenticate', 'authentication-password', 'authentication-protocol', 'authentication-types', 'authentication', 'authoritative', 'auto-mac', 'auto-negotiation', 'auto-send-supout', 'automatic-supout', 'autonomous', 'backup-allowed', 'baud-rate', 'bidirectional-timeout', 'blank-interval', 'bootp-support', 'bridge-mode', 'bridge', 'broadcast-addresses', 'broadcast', 'bsd-syslog', 'cable-settings', 'cache-administrator', 'cache-entries', 'cache-hit-dscp', 'cache-max-ttl', 'cache-on-disk', 'cache-size', 'certificate', 'chain', 'change-tcp-mss', 'channel-time', 'channel', 'check-interval', 'cipher', 'client-to-client-reflection', 'comment', 'connection-bytes', 'connection-idle-timeout', 'connection-mark', 'connection-state', 'contact', 'contrast', 'cpu', 'data-bits', 'default-ap-tx-limit', 'default-authentication', 'default-client-tx-limit', 'default-forwarding', 'default-group', 'default-profile', 'default-route-distance', 'default', 'dh-group', 'dhcp-option', 'dial-on-demand', 'directory', 'disable-running-check', 'disabled', 'disk-file-count', 'disk-file-name', 'disk-lines-per-file', 'disk-stop-on-full', 'display-time', 'distance', 'distribute-default', 'distribute-for-default-route', 'dns-name', 'dns-server', 'domain', 'dpd-interval', 'dpd-maximum-failures', 'dst-address-list', 'dst-address', 'dst-delta', 'dst-end', 'dst-port', 'dst-start', 'dynamic-label-range', 'e', 'eap-methods', 'enabled', 'enc-algorithm', 'enc-algorithms', 'encryption-password', 'encryption-protocol', 'engine-id', 'exchange-mode', 'exclude-groups', 'file-limit', 'file-name', 'filter-ip-address', 'filter-ip-protocol', 'filter-mac-address', 'filter-mac-protocol', 'filter-mac', 'filter-port', 'filter-stream', 'flow-control', 'forward-delay', 'frame-size', 'frames-per-second', 'from', 'full-duplex', 'garbage-timer', 'gateway-class', 'gateway-keepalive', 'gateway-selection', 'gateway', 'generate-policy', 'generic-timeout', 'group-ciphers', 'group-key-update', 'hash-algorithm', 'hide-ssid', 'hop-limit', 'hotspot-address', 'html-directory', 'http-cookie-lifetime', 'http-proxy', 'i', 'icmp-timeout', 'idle-timeout', 'ignore-as-path-len', 'in-filter', 'in-interface', 'inactive-flow-timeout', 'instance', 'interface', 'interfaces', 'interim-update', 'interval', 'ipsec-protocols', 'jump-target', 'keep-max-sms', 'keepalive-timeout', 'kind', 'l2mtu', 'latency-distribution-scale', 'lease-time', 'level', 'lifebytes', 'lifetime', 'line-count', 'list', 'local-address', 'location', 'log-prefix', 'login-by', 'login', 'loop-detect', 'lsr-id', 'mac-address', 'managed-address-configuration', 'management-protection-key', 'management-protection', 'manycast', 'max-cache-size', 'max-client-connections', 'max-connections', 'max-fresh-time', 'max-message-age', 'max-mru', 'max-mtu', 'max-server-connections', 'max-sessions', 'max-station-count', 'max-udp-packet-size', 'memory-limit', 'memory-lines', 'memory-scroll', 'memory-stop-on-full', 'metric-bgp', 'metric-connected', 'metric-default', 'metric-ospf', 'metric-other-ospf', 'metric-rip', 'metric-static', 'min-rx', 'mode', 'mpls-mtu', 'mq-pfifo-limit', 'mrru', 'mtu', 'multi-cpu', 'multicast', 'multiple-channels', 'multiplier', 'my-id-user-fqdn', 'name', 'nat-traversal', 'netmask', 'network', 'new-connection-mark', 'new-packet-mark', 'new-routing-mark', 'no-ping-delay', 'note', 'ntp-server', 'on-backup', 'on-master', 'only-headers', 'only-one', 'origination-interval', 'other-configuration', 'out-filter', 'out-interface', 'page-refresh', 'parent-proxy-port', 'parent-proxy', 'parent', 'parity', 'passthrough', 'password', 'path-vector-limit', 'paypal-accept-pending', 'paypal-allowed', 'paypal-secure-response', 'permissions', 'pfifo-limit', 'pfs-group', 'policy', 'port', 'ports', 'preemption-mode', 'preferred-gateway', 'preferred-lifetime', 'prefix', 'primary-ntp', 'primary-server', 'priority', 'profile', 'propagate-ttl', 'proposal-check', 'proposal', 'proprietary-extensions', 'protocol-mode', 'protocol', 'query-interval', 'query-response-interval', 'queue', 'quick-leave', 'ra-delay', 'ra-interval', 'ra-lifetime', 'radius-eap-accounting', 'radius-mac-accounting', 'radius-mac-authentication', 'radius-mac-caching', 'radius-mac-format', 'radius-mac-mode', 'ranges', 'rate-limit', 'reachable-time', 'read-access', 'read-only', 'receive-all', 'receive-enabled', 'receive-errors', 'red-avg-packet', 'red-burst', 'red-limit', 'red-max-threshold', 'red-min-threshold', 'redistribute-bgp', 'redistribute-connected', 'redistribute-ospf', 'redistribute-other-bgp', 'redistribute-other-ospf', 'redistribute-rip', 'redistribute-static', 'remember', 'remote-address', 'remote-ipv6-prefix-pool', 'remote-port', 'remote', 'require-client-certificate', 'retransmit-interval', 'router-id', 'routing-mark', 'routing-table', 'sa-dst-address', 'sa-src-address', 'scope', 'secondary-ntp', 'secondary-server', 'secret', 'security-profile', 'security', 'send-initial-contact', 'serialize-connections', 'servers', 'service-name', 'set-system-time', 'sfq-allot', 'sfq-perturb', 'shared-users', 'show-at-login', 'show-dummy-rule', 'signup-allowed', 'sip-direct-media', 'skin', 'smtp-server', 'source', 'speed', 'split-user-domain', 'src-address-list', 'src-address', 'src-port', 'ssid-all', 'ssid', 'state-after-reboot', 'static-algo-0', 'static-algo-1', 'static-algo-2', 'static-algo-3', 'static-key-0', 'static-key-1', 'static-key-2', 'static-key-3', 'static-sta-private-algo', 'static-sta-private-key', 'static-transmit-key', 'status-autorefresh', 'stop-bits', 'store-every', 'store-leases-disk', 'streaming-enabled', 'streaming-max-rate', 'streaming-server', 'supplicant-identity', 'switch-to-spt-bytes', 'switch-to-spt-interval', 'switch-to-spt', 'syslog-facility', 'syslog-severity', 'target-scope', 'target', 'tcp-close-timeout', 'tcp-close-wait-timeout', 'tcp-established-timeout', 'tcp-fin-wait-timeout', 'tcp-last-ack-timeout', 'tcp-syn-received-timeout', 'tcp-syn-sent-timeout', 'tcp-syncookie', 'tcp-time-wait-timeout', 'term', 'test-id', 'threshold', 'time-zone-name', 'time-zone', 'timeout-timer', 'timeout', 'tls-certificate', 'tls-mode', 'to-addresses', 'topics', 'transmit-hold-count', 'transparent-proxy', 'transport-address', 'trap-generators', 'trap-target', 'trap-version', 'ttl', 'tunnel', 'type', 'udp-stream-timeout', 'udp-timeout', 'unicast-ciphers', 'update-stats-interval', 'update-timer', 'use-compression', 'use-encryption', 'use-explicit-null', 'use-ip-firewall-for-pppoe', 'use-ip-firewall-for-vlan', 'use-ip-firewall', 'use-ipv6', 'use-mpls', 'use-peer-dns', 'use-peer-ntp', 'use-radius', 'use-service-tag', 'use-vj-compression', 'user', 'v3-protocol', 'valid-lifetime', 'vcno', 'verify-client-certificate', 'version', 'vlan-id', 'vrid', 'watch-address', 'watchdog-timer', 'wds-cost-range', 'wds-default-bridge', 'wds-default-cost', 'wds-ignore-ssid', 'wds-mode', 'wins-server', 'wmm-support', 'wpa-pre-shared-key', 'wpa2-pre-shared-key', 'write-access', 'burst-limit', 'burst-threshold', 'burst-time', 'limit-at', 'priority', 'max-limit', 'tree', 'packet-mark', 'value', 'option', 'target-addresses', 'queue', 'encryption-password', 'always-broadcast', 'connect-to', 'adaptive-noise-immunity', 'compression', 'band', 'country', 'frequency', 'hw-retries', 'rate-selection', 'scan-list'
    ]
    keyword2_list = [
        'set', 'add', 'delay', 'do', 'error', 'execute', 'find', 'for', 'foreach', 'global', 'if', 'len', 'local', 'nothing', 'parse', 'pick', 'put', 'resolve', 'set', 'time', 'toarray', 'tobool', 'toid', 'toip', 'toip6', 'tonum', 'tostr', 'totime', 'typeof', 'while', 'beep', 'export', 'import', 'led', 'password', 'ping', 'quit', 'redo', 'setup', 'undo', 'print', 'detail', 'file', 'log', 'info', 'get', 'warning', 'critical'
    ]
    keyword3_list = [
        '/', 'aaa', 'accounting', 'address', 'address-list', 'align', 'area', 'bandwidth-server', 'bfd', 'bgp', 'bridge', 'client', 'clock', 'community', 'config', 'connection', 'console', 'customer', 'default', 'dhcp-client', 'dhcp-server', 'discovery', 'dns', 'e-mail', 'ethernet', 'filter', 'firewall', 'firmware', 'gps', 'graphing', 'group', 'hardware', 'health', 'hotspot', 'identity', 'igmp-proxy', 'incoming', 'instance', 'interface0', 'ip', 'ipsec', 'ipv6', 'irq', 'l2tp-server', 'lcd', 'ldp', 'logging', 'mac-server', 'mac-winbox', 'mangle', 'manual', 'mirror', 'mme', 'mpls', 'nat', 'nd', 'neighbor', 'network', 'note', 'ntp', 'ospf', 'ospf-v3', 'ovpn-server', 'page', 'peer', 'pim', 'ping', 'policy', 'pool', 'port', 'ppp', 'pppoe-client', 'pptp-server', 'prefix', 'profile', 'proposal', 'proxy', 'queue', 'radius', 'resource', 'rip', 'ripng', 'route', 'routing', 'screen', 'script', 'security-profiles', 'server', 'service', 'service-port', 'settings', 'shares', 'smb', 'sms', 'sniffer', 'snmp', 'snooper', 'socks', 'sstp-server', 'system', 'tool', 'tracking', 'traffic-flow', 'traffic-generator', 'type', 'upgrade', 'upnp', 'user', 'user-manager', 'users', 'vlan', 'vrrp', 'watchdog', 'web-access', 'wireless', 'pptp', 'pppoe', 'lan', 'wan', 'layer7-protocol', 'eth-', 'wlan-', 'bridge-'
    ]
    
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    #Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = [":", "="]

    def __init__(self, parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the default style values
        self.setDefaultColor(self.default_color)
        self.setDefaultPaper(self.default_paper)
        self.setDefaultFont(self.default_font)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "RouterOS"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the RouterOS syntax by MikroTik"
        else:
            description = ""
        return description
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return data.QFont(data.current_font_name, data.current_font_size)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.QColor(theme.Paper.RouterOS.Default), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, getattr(theme.Font.RouterOS, style))
    
    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        NOTE:
            Very slow if done in Python!
            Using the Cython version is better.
            The fastest would probably be adding the lexer directly into
            the QScintilla source. Maybe never :-)
        """
        #Style in pure Python, VERY SLOW!
        editor = self.editor()
        if editor is None:
            return
        #Initialize the styling
        self.startStyling(start)
        #Scintilla works with bytes, so we have to adjust the start and end boundaries
        text = bytearray(editor.text().lower(), "utf-8")[start:end].decode("utf-8")
        #Loop optimizations
        setStyling      = self.setStyling
        operator_list   = self.operator_list
        comment_list    = self.comment_list
        keyword1_list   = self.keyword1_list
        keyword2_list   = self.keyword2_list
        keyword3_list   = self.keyword3_list
        DEFAULT     = self.styles["Default"]
        OPERATOR    = self.styles["Operator"]
        COMMENT     = self.styles["Comment"]
        KEYWORD1    = self.styles["Keyword1"]
        KEYWORD2    = self.styles["Keyword2"]
        KEYWORD3    = self.styles["Keyword3"]
        #Initialize various states and split the text into tokens
        commenting          = False
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in self.splitter.findall(text)]
        #Style the tokens accordingly
        for i, token in enumerate(tokens):
            if commenting == True:
                #Continuation of comment
                setStyling(token[1], COMMENT)
                #Check if comment ends
                if "\n" in token[0]:
                    commenting = False
            elif token[0] in operator_list:
                setStyling(token[1], OPERATOR)
            elif token[0] in comment_list:
                setStyling(token[1], COMMENT)
                commenting = True
            elif token[0] in keyword1_list:
                setStyling(token[1], KEYWORD1)
            elif token[0] in keyword2_list:
                setStyling(token[1], KEYWORD2)
            elif token[0] in keyword3_list:
                setStyling(token[1], KEYWORD3)
            else:
                setStyling(token[1], DEFAULT)