
APP_COMMANDS = {
    # "get_structure": {"cmd": "/data/LoxAPP3.json", "descr": "Strukturdatei für die Visualisierung", "auth_req": True, "admin_only": False},       # can't decode JSON
    "get_appversion": {"cmd": "dev/sps/LoxAPPversion3", "auth_req": True},        # diff with data/LoxAPP3.json?
    "enable_status_updates": {"cmd": "dev/sps/enablebinstatusupdate", "auth_req": True},
    "list_commands": {"cmd": "dec/sps/listcmds", "descr": "list commands recorded via the app", "auth_req": True}
}


BUS_COMMANDS = {
    "bus_pkts_tx":      {"cmd": "dev/bus/packetssent", "descr": "Anzahl gesendete Pakete am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_pkts_rx":      {"cmd": "dev/bus/packetsreceived", "descr": "Anzahl empfangene Pakete am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_rx_err":       {"cmd": "dev/bus/receiveerrors", "descr": "Anzahl Empfangsfehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_frame_err":    {"cmd": "dev/bus/frameerrors", "descr": "Anzahl Frame-Fehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_overruns":     {"cmd": "dev/bus/overruns", "descr": "Anzahl Überlauffehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_parity_err":   {"cmd": "dev/bus/parityerrors", "descr": "Anzahl Paritätsfehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
}


CONFIG_COMMANDS = {
    "get_update_level":         {"cmd": "dev/cfg/updatelevel", "min_vers": "9.0", "descr": "", "auth_req": True},         # interacts with updatecheck.xml?
    "get_api":              	{"cmd": "dev/cfg/api", "descr": ""},
    "get_apikey":           	{"cmd": "dev/cfg/apikey", "descr": ""},
    "get_mac":              	{"cmd": "dev/cfg/mac", "descr": "MAC-Adresse holen", "admin_only": False},
    "get_firmware_version": 	{"cmd": "dev/cfg/version", "descr": "Firmware Version holen", "admin_only": False, "auth_req": True},
    "get_firmware_date":    	{"cmd": "dev/cfg/versiondate", "descr": "Erstellungsdatum der Firmware holen", "admin_only": False, "auth_req": True},
    "set_settings":         	{"cmd": "dev/cfg/settings", "auth_req": True},
    "get_dhcp":             	{"cmd": "dev/cfg/dhcp", "auth_req": True, "descr": "DHCP Konfiguration holen", "admin_only": True},
    "get_ip":               	{"cmd": "dev/cfg/ip", "auth_req": True, "descr": "IP-Adresse holen", "admin_only": True},
    "get_mask":             	{"cmd": "dev/cfg/mask", "auth_req": True, "descr": "IP-Maske holen", "admin_only": True},
    "get_gateway":          	{"cmd": "dev/cfg/gateway", "auth_req": True, "descr": "Gateway-Adresse holen", "admin_only": True},
    "get_device_name":      	{"cmd": "dev/cfg/device", "auth_req": True, "descr": "Miniserver Gerätenamen holen", "admin_only": True},
    "get_dns1":             	{"cmd": "dev/cfg/dns1", "auth_req": True, "descr": "DNS-Adresse 1 holen", "admin_only": True},
    "get_dns2":             	{"cmd": "dev/cfg/dns2", "auth_req": True, "descr": "DNS-Adresse 2 holen", "admin_only": True},
    "get_ntp":              	{"cmd": "dev/cfg/ntp", "auth_req": True, "descr": "NTP-Adresse holen", "admin_only": True},
    "get_timezone_offset":  	{"cmd": "dev/cfg/timezoneoffset", "auth_req": True, "descr": "Zeitzonenoffset holen", "admin_only": False},
    "get_http_port":        	{"cmd": "dev/cfg/http", "auth_req": True, "descr": "HTTP-Port holen", "admin_only": True},
    "get_ftp_port":         	{"cmd": "dev/cfg/ftp", "auth_req": True, "descr": "FTP-Port holen", "admin_only": True},
    "get_town":                 {"cmd": "dev/cfg/town", "auth_req": True},
    "get_config_port":          {"cmd": "dev/cfg/LoxPLAN", "auth_req": True, "descr": "Konfigurationssoftware-Port holen", "admin_only": True},
    "get_only_local_config":    {"cmd": "dev/cfg/ftllocalonly", "auth_req": True, "descr": "‚FTP, Telnet, Softwarezugriff nur lokal erlauben‘ holen", "admin_only": True},
}


DEBUG_COMMANDS = {
    "dbg_config": 			{"cmd": "debug/config", "auth_req": True},
    "dbg_cycle": 			{"cmd": "debug/cycle", "auth_req": True},
    "dbg_free": 			{"cmd": "debug/free", "auth_req": True},
    "dbg_fs": 		    	{"cmd": "debug/fs", "auth_req": True},
    "dbg_inmem": 			{"cmd": "debug/inmem", "auth_req": True},
    "dbg_level": 			{"cmd": "debug/level", "auth_req": True},
    "dbg_linkoff": 			{"cmd": "debug/linkoff", "auth_req": True},
    "dbg_linkon": 			{"cmd": "debug/linkon", "auth_req": True},
    "dbg_mem": 		    	{"cmd": "debug/mem", "auth_req": True},
    "dbg_memtest_end": 		{"cmd": "debug/memtestend", "auth_req": True},
    "dbg_memtest_start": 	{"cmd": "debug/memteststart", "auth_req": True},
    "dbg_rcv": 		        {"cmd": "debug/rcv", "auth_req": True},
    "dbg_scheduler": 		{"cmd": "debug/scheduler", "auth_req": True},
    "dbg_sockets": 		    {"cmd": "debug/sockets", "auth_req": True},
    "dbg_plc": 		        {"cmd": "debug/sps", "auth_req": True},
    "dbg_test": 		    {"cmd": "debug/test", "auth_req": True}
}

FS_COMMANDS = {
    "add_file": {"cmd": "dev/fsput/{}", "auth_req": True, "descr": "adds a file", "admin_only": True},
    "ls": {"cmd": "dev/fslist/{}", "auth_req": True, "descr": "lists the directory path on the SD card", "admin_only": True},
    "get_file": {"cmd": "dev/fsget/{}", "auth_req": True, "descr": "retrieves a file", "admin_only": True},
    "get_log": {"cmd": "dev/fsget/log/def.log", "descr": "Log abrufen", "admin_only": True, "auth_req": True},
    "rm_file": {"cmd": "dev/fsdel/{}", "auth_req": True, "descr": "deletes a file", "ad/min_only": True, "not_safe": True}
}

LAN_COMMANDS = {
    "get_num_sent_pkts": {"cmd": "dev/lan/txp", "descr": "Anzahl LAN gesendete Pakete holen", "admin_only": True, "auth_req": True},
    "get_num_sent_pkts_error": {"cmd": "dev/lan/txe", "descr": "Anzahl LAN gesendete Pakete mit Fehler holen", "admin_only": True, "auth_req": True},
    "get_num_collisions": {"cmd": "dev/lan/txc", "descr": "Anzahl LAN gesendete Pakete mit Kollision holen", "admin_only": True, "auth_req": True},
    "get_num_buffer_error": {"cmd": "dev/lan/exh", "descr": "Anzahl LAN Bufferfehler holen", "admin_only": True, "auth_req": True},
    "get_num_underrun_error": {"cmd": "dev/lan/txu", "descr": "Anzahl LAN Underrunfehler holen", "admin_only": True, "auth_req": True},
    "get_num_received_pkts": {"cmd": "dev/lan/rxp", "descr": "Anzahl LAN empfangene Pakete holen", "admin_only": True, "auth_req": True},
    "get_eof_error": {"cmd": "dev/lan/eof", "descr": "Anzahl LAN EOF Fehler holen", "admin_only": True, "auth_req": True},
    "get_rx_overrun_error": {"cmd": "dev/lan/rxo", "descr": "Anzahl LAN Empfangsüberlauffehler holen", "admin_only": True, "auth_req": True},
    "get_norecvbuffer_error": {"cmd": "dev/lan/nob", "descr": "Retrieve number of LAN ‘No receive buffer’ errors", "admin_only": True, "auth_req": True},
}


PLC_COMMANDS = {
    "get_sps_state": {"cmd": "dev/sps/state", "admin_only": False, "descr": """PLC status query
0 – No status
1 – PLC booting
2 – PLC program is loaded
3 – PLC has started
4 – Loxone Link has started
5 – PLC running
6 – PLC change
7 – PLC error
8 – Update is occuring"""},
    "get_sps_clock": {"cmd": "dev/sps/status", "auth_req": True, "descr": "aktuelle PLC Frequenz abfragen", "admin_only": False},
    "restart_sps": {"cmd": "dev/sps/restart", "auth_req": True, "descr": "PLC neu starten", "admin_only": True, "not_safe": True},
    "stop_sps": {"cmd": "dev/sps/stop", "auth_req": True, "descr": "PLC anhalten", "admin_only": True, "not_safe": True},
    "resume_sps": {"cmd": "dev/sps/run", "auth_req": True, "descr": "PLC fortsetzen", "admin_only": True},
    "enable_logging": {"cmd": "dev/sps/log", "auth_req": True, "descr": "PLC globales Logging erlauben", "admin_only": True},
    "list_devices": {"cmd": "dev/sps/enumdev", "auth_req": True, "descr": "alle Geräte der PLC auflisten (Miniserver,Extensions,…)", "admin_only": True},
    "list_inputs": {"cmd": "dev/sps/enumin", "auth_req": True, "descr": "alle Eingänge der PLC auflisten", "admin_only": True},
    "list_outputs": {"cmd": "dev/sps/enumout", "auth_req": True, "descr": "alle Ausgänge der PLC auflisten", "admin_only": True},
    "identify_ms": {"cmd": "dev/sps/identify", "auth_req": True, "descr": "Miniserver identifizieren für Erweiterungen muss die Seriennummer als Parameter mitgegeben werden.", "admin_only": True}
}


SESSION_COMMANDS = {
    "get_key": {"cmd": "dev/sys/getkey"},
    "authenticate": {"cmd": "authenticate/{}", "auth_req": True},     # hash   user:pwd          TODO: auth required?
    "get_usersalt": {"cmd": "dev/sys/getkey2/{}"},  # [user] --> requests both a one-time-salt (key) and a user-salt                !! 'code'  in response is lowercase, not uppercase as in all the other response
    "get_token": {"cmd": "dev/sys/gettoken/{}/{}/{}/{}/{}"},             # [hash, user, type:<int>, uuid, info] --> requests a token, type specifies the lifespan, uuid is used to identify who requested the token & info is a userfriendly info on the platformdevice used.
    "auth_with_token": {"cmd": "authwithtoken/{}/{}", "auth_req": True},               # [hash, user]
    "refresh_token": {"cmd": "dev/sys/refreshtoken/{}/{}", "auth_req": True},        # [tokenHash, user]
    "kill_token": {"cmd": "dev/sys/killtoken/{}/{}", "auth_req": True},              # [tokenHash, user]
    "auth_arg": {"cmd": "autht={}&user={}", "socket_only": False, "auth_req": True},  # [tokenhash, user]

    # encryption
    "get_public_key": {"cmd": "dev/sys/getPublicKey"},
    "key_exchange": {"cmd": "dev/sys/keyexchange/{}"},      # RSA encrypted session key + iv in base64
    "authenticate_enc": {"cmd": "authenticateEnc/{}", "auth_req": True},      # AES encrypted hash in base64        TODO: auth required?
    "aes_payload": {"cmd": "salt/{}/{}", "auth_req": True},                   # [salt, payload] --> this is the part that will be AES encrypted.
    "aes_next_salt": {"cmd": "nextSalt/{}/{}/{}", "auth_req": True},          # [currSalt, nextSalt, payload] --> this is the part that will be AES encrypted.
    "enc_cmd": {"cmd": "dev/sys/enc/{}", "auth_req": True},                   # cipher
    "enc_cmd_and_response": {"cmd": "dev/sys/fenc/{}", "auth_req": True}      # cipher, also the response will be encoded
}

SYSTEM_COMMANDS = {
    "get_cpu": {"cmd": "dev/sys/cpu", "descr": "CPU-Last holen", "admin_only": True, "auth_req": True},
    "get_sys_ctx_switches": {"cmd": "dev/sys/contextswitches", "descr": "Anzahl Umschaltungen zwischen Tasks holen", "admin_only": True, "auth_req": True},
    "get_sys_ctx_switches_ints": {"cmd": "dev/sys/contextswitchesi", "descr": "Anzahl Umschaltungen zwischen Tasks holen, die von Interrupts ausgelöst wurden", "admin_only": True, "auth_req": True},
    "get_heap_size": {"cmd": "dev/sys/heap", "descr": "Speichergröße holen", "admin_only": False, "auth_req": True},
    "get_num_ints": {"cmd": "dev/sys/ints", "descr": "Anzahl Systeminterrupts holen", "admin_only": True, "auth_req": True},
    "get_num_comm_ints": {"cmd": "dev/sys/comints", "descr": "Anzahl Kommunikationsinterrupts holen", "admin_only": True, "auth_req": True},
    "get_num_lan_ints": {"cmd": "dev/sys/lanints", "descr": "Anzahl LAN-Interrupts holen", "admin_only": True, "auth_req": True},
    "get_watchdog_bits": {"cmd": "dev/sys/watchdog", "descr": "Watchdog-Bits holen", "admin_only": True, "auth_req": True},
    "get_date": {"cmd": "dev/sys/date", "descr": "Liefert das lokale Datum", "admin_only": True, "auth_req": True},
    "get_time": {"cmd": "dev/sys/time", "descr": "Liefert die lokale Zeit", "admin_only": True, "auth_req": True},
    "get_arp_table": {"cmd": "dev/sys/arp", "descr": "Retrieve all entries in arp table", "auth_req": True},
    "set_datetime": {"cmd": "dev/sys/setdatetime", "descr": "Sets or gets system date and time. Format: 2013-06-18 16:58:00 or 18/06/2013 16:58:00", "admin_only": False, "auth_req": True},
    "get_sps_cycles": {"cmd": "dev/sys/spscycle", "descr": "Anzahl PLC-Zyklen holen", "admin_only": True, "auth_req": True},
    "query_ntp": {"cmd": "dev/sys/ntp", "descr": "NTP Anfrage forcieren", "admin_only": True, "auth_req": True},
    "reboot_ms": {"cmd": "dev/sys/reboot", "descr": "Miniserver booten", "admin_only": True, "auth_req": True, "not_safe": True},
    "show_config_conns": {"cmd": "dev/sys/check", "descr": "Zeigt aktive Loxone Config Verbindungen", "admin_only": False, "auth_req": True},
    "log_config_off": {"cmd": "dev/sys/logoff", "descr": "Trennt bestehende Loxone Config Verbindungen", "admin_only": True, "auth_req": True},
    "show_last_cpu": {"cmd": "dev/sys/lastcpu", "descr": "zeigt letzen Wert der CPU Auslastung und Anzahl der PLC Zyklen", "admin_only": True, "auth_req": True},
    "get_searchdata": {"cmd": "dev/sys/searchdata", "descr": "listet die Suchergebnisse", "admin_only": False},
    "get_status": {"cmd": "/data/status", "descr": "zeigt Status von Miniserver und allen Extensions", "admin_only": False, "auth_req": True},
    "get_stats": {"cmd": "/stats", "descr": "zeigt die Statistiken", "admin_only": True, "auth_req": True},
    "get_weather_file": {"cmd": "/data/weatheru.xml", "descr": "zeigt die Wetterdaten (nur bei aktivem Wetteservice)", "admin_only": False, "auth_req": True},
    "get_1wire_stat": {"cmd": "dev/sys/ExtStatistics/05000001", "descr": "Statistik der 1-Wire Extension abrufen (05000001 ersetzen durch Seriennummer der Extension)", "admin_only": True, "auth_req": True},
    "get_air_stat": {"cmd": "dev/sys/AirStatistics/0C000001deviceIndex", "descr": "Statistik der Air Geräte abrufen (0C000001 ersetzen durch Seriennummer der Extension)", "admin_only": True, "auth_req": True},
    "update_extensions": {"cmd": "dev/sys/updateext", "descr": "Update der Extensions starten", "admin_only": True, "auth_req": True},
    "test_sdcard": {"cmd": "dev/sys/sdtest", "descr": "Testet die SD Karte", "admin_only": True, "auth_req": True, "not_safe": True},
    "test_sdcard_full": {"cmd": "dev/sys/sdtestfull", "descr": "Testet die SD Karte", "admin_only": True, "auth_req": True, "not_safe": True},
    "test_sdcard_burn": {"cmd": "dev/sys/sdtestburn", "descr": "Testet die SD Karte", "admin_only": True, "auth_req": True, "not_safe": True},
}


TASK_COMMANDS = {
    "get_num_tasks":            {"cmd": "dev/sys/numtasks", "descr": "Anzahl Tasks holen", "admin_only": True, "auth_req": True},
    "get_task_name":            {"cmd": "dev/task{}/name", "descr": "Retrieve task name (ID is 0-based)", "admin_only": True, "auth_req": True},
    "get_task_priority":        {"cmd": "dev/task{}/priority", "descr": "Task Priorität holen", "admin_only": True, "auth_req": True},
    "get_task_stack":           {"cmd": "dev/task{}/stack", "descr": "Task Stack holen", "admin_only": True, "auth_req": True},
    "get_task_num_ctxswitches": {"cmd": "dev/task{}/contextswitches", "descr": "Task Anzahl Umschaltungen holen", "admin_only": True, "auth_req": True},
    "get_task_waittime":        {"cmd": "dev/task{}/waittimeout", "descr": "Task Wartezeit in ms holen", "admin_only": True, "auth_req": True},
    "get_task_state":           {"cmd": "dev/task{}/state", "descr": "Task Status holen", "admin_only": True, "auth_req": True},
}


ALL_COMMANDS = [APP_COMMANDS, BUS_COMMANDS, CONFIG_COMMANDS, DEBUG_COMMANDS, FS_COMMANDS, LAN_COMMANDS, PLC_COMMANDS, SESSION_COMMANDS, SYSTEM_COMMANDS, TASK_COMMANDS]

