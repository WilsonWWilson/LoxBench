from api.api_enums import Permission, Protocol


GET_DYNDNS_IP_URL = "http://dns.loxonecloud.com/?getip&snr={}"


TEST_COMMANDS = {
    "get_stats":            {"cmd": "dev/sps/getstats", "auth_req": True},
}


APP_COMMANDS = {
    # "get_structure": {"cmd": "/data/LoxAPP3.json", "descr": "Strukturdatei für die Visualisierung", "auth_req": True, "admin_only": False},       # can't decode JSON
    "enable_status_updates": {"cmd": "dev/sps/enablebinstatusupdate", "auth_req": True},
    "list_commands": {"cmd": "dec/sps/listcmds", "descr": "list commands recorded via the app", "auth_req": True}
}

BLOCK_COMMANDS = {
    "io":                   {"cmd": "dev/sps/io", "auth_req": True, "descr": "Issue commands to control blocks"},
    "io_secure":            {"cmd": "dev/sps/ios", "auth_req": True, "descr": "Issue secure commands to control blocks"},
}

BUS_COMMANDS = {
    "bus_frame_err":    {"cmd": "dev/bus/frameerrors", "descr": "Anzahl Frame-Fehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_overruns":     {"cmd": "dev/bus/overruns", "descr": "Anzahl Überlauffehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_pkts_rx":      {"cmd": "dev/bus/packetsreceived", "descr": "Anzahl empfangene Pakete am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_pkts_tx":      {"cmd": "dev/bus/packetssent", "descr": "Anzahl gesendete Pakete am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_parity_err":   {"cmd": "dev/bus/parityerrors", "descr": "Anzahl Paritätsfehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
    "bus_rx_err":       {"cmd": "dev/bus/receiveerrors", "descr": "Anzahl Empfangsfehler am Loxone-Link holen", "admin_only": True, "auth_req": True},
}


CALENDAR_COMMANDS = {
    "cal_create_entry":     {"cmd": "dev/sps/calendarcreateentry", "auth_req": True, "min_vers": "10.0.9.24"},
    "cal_delete_entry":     {"cmd": "dev/sps/calendardeleteentry", "auth_req": True, "min_vers": "10.0.9.24"},
    "cal_get_cool_period":  {"cmd": "dev/sps/calendargetcoolperiod", "auth_req": True, "min_vers": "10.0.9.24"},
    "cal_get_entries":      {"cmd": "dev/sps/calendargetentries", "auth_req": True, "min_vers": "10.0.9.24"},
    "cal_get_heat_period":  {"cmd": "dev/sps/calendargetheatperiod", "auth_req": True, "min_vers": "10.0.9.24"},
    "cal_update_entry":     {"cmd": "dev/sps/calendarupdateentry", "auth_req": True, "min_vers": "10.0.9.24"},
}

CONFIG_COMMANDS = {
    "get_api":              	{"cmd": "dev/cfg/api", "descr": ""},
    "get_apikey":           	{"cmd": "dev/cfg/apikey", "descr": ""},
    "get_mac":              	{"cmd": "dev/cfg/mac", "descr": "Retrieve mac (separated by ':')", "admin_only": False},
    "get_firmware_version_dot": {"cmd": "dev/cfg/version", "descr": "Get firmware version (dotted notation)", "admin_only": False, "auth_req": True},
    "get_firmware_version": 	{"cmd": "dev/sys/version", "descr": "Get firmware version (no separator)", "admin_only": False, "auth_req": True},
    "get_firmware_date":    	{"cmd": "dev/cfg/versiondate", "descr": "Erstellungsdatum der Firmware holen", "admin_only": False, "auth_req": True},
    "set_settings":         	{"cmd": "dev/cfg/settings", "auth_req": True},
    "get_dhcp":             	{"cmd": "dev/cfg/dhcp", "auth_req": True, "descr": "DHCP Konfiguration holen", "admin_only": True},
    "get_ip":               	{"cmd": "dev/cfg/ip", "auth_req": True, "descr": "IP-Adresse holen", "admin_only": True},
    "get_mask":             	{"cmd": "dev/cfg/mask", "auth_req": True, "descr": "IP-Maske holen", "admin_only": True},
    "get_gateway":          	{"cmd": "dev/cfg/gateway", "auth_req": True, "descr": "Gateway-Adresse holen", "admin_only": True},
    "get_device_name":      	{"cmd": "dev/cfg/device", "auth_req": True, "descr": "Miniserver Gerätenamen holen", "admin_only": True},
    "get_dns1":             	{"cmd": "dev/cfg/dns1", "auth_req": True, "descr": "DNS-Adresse 1 holen", "admin_only": True},
    "get_dns2":             	{"cmd": "dev/cfg/dns2", "auth_req": True, "descr": "DNS-Adresse 2 holen", "admin_only": True},
    "get_mtu":                  {"cmd": "dev/cfg/mtu", "auth_req": True},
    "get_ntp":              	{"cmd": "dev/cfg/ntp", "auth_req": True, "descr": "NTP-Adresse holen", "admin_only": True},
    "get_timezone_offset":  	{"cmd": "dev/cfg/timezoneoffset", "auth_req": True, "descr": "Zeitzonenoffset holen", "admin_only": False},
    "get_http_port":        	{"cmd": "dev/cfg/http", "auth_req": True, "descr": "HTTP-Port holen", "admin_only": True},
    "get_ftp_port":         	{"cmd": "dev/cfg/ftp", "auth_req": True, "descr": "FTP-Port holen", "admin_only": True},
    "get_town":                 {"cmd": "dev/cfg/town", "auth_req": True},
    "get_config_port":          {"cmd": "dev/cfg/LoxPLAN", "auth_req": True, "descr": "Konfigurationssoftware-Port holen", "admin_only": True},
    "get_only_local_config":    {"cmd": "dev/cfg/ftllocalonly", "auth_req": True, "descr": "‚FTP, Telnet, Softwarezugriff nur lokal erlauben‘ holen", "admin_only": True},
    "get_language":             {"cmd": "dev/cfg/getlanguage", "auth_req": True},
    "set_language":             {"cmd": "dev/cfg/setlanguage/{}", "auth_req": True},
    "loxone":                   {"cmd": "dev/cfg/loxone", "auth_req": True},                    # TODO determine purpose
    "logserver":                {"cmd": "dev/cfg/logserver", "auth_req": True},        # TODO determine purpose
    "get_log_level":            {"cmd": "dev/cfg/loglevel", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_update_level":         {"cmd": "dev/cfg/updatelevel", "min_vers": "9.0", "descr": "", "auth_req": True},         # interacts with updatecheck.xml?
    "cvt_time":                 {"cmd": "dev/cfg/cvttime/{}", "auth_req": True, "descr": "Converts the given number of seconds into date time. The base for the conversion is 2009-01-01", "admin_only": True},     # admin only?
}


DEBUG_COMMANDS = {
    "dbg_config": 			{"cmd": "dev/debug/config", "auth_req": True},
    "dbg_cycle": 			{"cmd": "dev/debug/cycle", "auth_req": True},
    "dbg_free": 			{"cmd": "dev/debug/free", "auth_req": True},
    "dbg_fs": 		    	{"cmd": "dev/debug/fs", "auth_req": True},
    "dbg_gateway": 			{"cmd": "dev/debug/gateway", "auth_req": True},
    "dbg_httpsockets":	    {"cmd": "dev/debug/httpsockets", "auth_req": True},
    "dbg_inmem": 			{"cmd": "dev/debug/inmem", "auth_req": True},
    "dbg_level": 			{"cmd": "dev/debug/level", "auth_req": True},
    "dbg_linkoff": 			{"cmd": "dev/debug/linkoff", "auth_req": True},
    "dbg_linkon": 			{"cmd": "dev/debug/linkon", "auth_req": True},
    "dbg_mem": 		    	{"cmd": "dev/debug/mem", "auth_req": True},
    "dbg_memtest_end": 		{"cmd": "dev/debug/memtestend", "auth_req": True},
    "dbg_memtest_start": 	{"cmd": "dev/debug/memteststart", "auth_req": True},
    "dbg_mutex": 	        {"cmd": "dev/debug/mutex", "auth_req": True},
    "dbg_rcv": 		        {"cmd": "dev/debug/rcv", "auth_req": True},
    "dbg_scheduler": 		{"cmd": "dev/debug/scheduler", "auth_req": True},
    "dbg_sockets": 		    {"cmd": "dev/debug/sockets", "auth_req": True},
    "dbg_plc": 		        {"cmd": "dev/debug/sps", "auth_req": True},
    "dbg_test": 		    {"cmd": "dev/debug/test", "auth_req": True}
}


EXTENSION_COMMANDS = {
    "air_get_learned":          {"cmd": "dev/sps/airgetlearned", "auth_req": True},
    "air_learn":                {"cmd": "dev/sps/airlearn", "auth_req": True},
    "air_set_ip":               {"cmd": "dev/sps/airsetip", "auth_req": True},
    "air_get_param":            {"cmd": "dev/sys/airgetparam", "auth_req": True},
    "air_mac_statistics":       {"cmd": "dev/sys/airmacstatistics", "auth_req": True},
    "air_set_param":            {"cmd": "dev/sys/airsetparam", "auth_req": True},
    "air_statistics":           {"cmd": "dev/sys/airstatistics", "auth_req": True},
    "air_trace":                {"cmd": "dev/sys/airtrace", "auth_req": True},
    "air_traceback":            {"cmd": "dev/sys/airtraceback", "auth_req": True},
    "air_unlock_otau":          {"cmd": "dev/sys/airunlockotau", "auth_req": True},
    "air_unpair":               {"cmd": "dev/sys/airunpair", "auth_req": True},
    "air_update_device":        {"cmd": "dev/sys/airupdatedevice", "auth_req": True},
    "get_air_statistics":       {"cmd": "dev/sys/AirStatistics/{sn}/deviceIndex", "descr": "Statistik der Air Geräte abrufen (0C000001 ersetzen durch Seriennummer der Extension)", "admin_only": True, "auth_req": True},
    "air_get_rssi":             {"cmd": "dev/sps/airrssi", "auth_req": True, "min_vers": "10.0.9.24"},
    "air_get_info":             {"cmd": "dev/sys/airinfo", "auth_req": True, "min_vers": "10.0.9.24"},
    "air_log_level":            {"cmd": "dev/sys/airloglevel", "auth_req": True, "min_vers": "10.0.9.24"},
    "air_need_ack":             {"cmd": "dev/sys/airneedack", "auth_req": True, "min_vers": "10.0.9.24"},
    "air_wake_up":              {"cmd": "dev/sys/airwakeup", "auth_req": True, "min_vers": "10.0.9.24"},
    "air_wake_up_all":          {"cmd": "dev/sys/airwakeupall", "auth_req": True, "min_vers": "10.0.9.24"},

    "dmx_get_searched":         {"cmd": "dev/sps/dmxgetsearched", "auth_req": True},
    "dmx_search":               {"cmd": "dev/sps/dmxsearch", "auth_req": True},
    "dmx_search_finished":      {"cmd": "dev/sps/dmxsearchfinished", "auth_req": True},

    "eib_program":              {"cmd": "dev/sps/eibprogram", "auth_req": True},
    "eib_state":                {"cmd": "dev/sps/eibstate", "auth_req": True},

    "ir_get_learned":           {"cmd": "dev/sps/irgetlearned", "auth_req": True},
    "ir_learn":                 {"cmd": "dev/sps/irlearn", "auth_req": True},

    "tree_set_serial": {"cmd": "dev/sps/treesetserial", "auth_req": True, "min_vers": "10.0.9.24"},
    "tree_shortcut":                {"cmd": "dev/sys/treeshortcut", "auth_req": True, "min_vers": "10.0.9.24"},

    "set_ext_serialno":         {"cmd": "dev/sys/extsetsn", "auth_req": True},
    "get_ext_statistics":       {"cmd": "dev/sys/extstatistics/{sn}", "descr": "Retrieve statistics of the extension with given serial number", "params": {"sn": "serial number of the extension"}, "admin_only": True, "auth_req": True},
    "get_ext_info":             {"cmd": "dev/sys/extinfo/{sn}", "auth_req": True, "descr": "Retrieve information of the extension with given serial number", "params": {"sn": "serial number of the extension"}, "min_vers": "10.0.9.24"},
    "update_extensions":        {"cmd": "dev/sys/updateext", "descr": "Update der Extensions starten", "admin_only": True, "auth_req": True},
    "update_ext_no_retries":    {"cmd": "dev/sys/updateextnoretries", "auth_req": True},
}


FIDELIO_COMMANDS = {
    "fidelio_get_io":               {"cmd": "dev/fidelio/io"},
    "fidelio_get_roommate":         {"cmd": "dev/fidelio/roommate"},
    "fidelio_test":                 {"cmd": "dev/fidelio/test"},
}


FS_COMMANDS = {
    "add_file": {"cmd": "dev/fsput/{}", "auth_req": True, "descr": "adds a file", "admin_only": True},
    "ls": {"cmd": "dev/fslist/{}", "auth_req": True, "descr": "lists the directory path on the SD card", "admin_only": True},
    "get_file": {"cmd": "dev/fsget/{path}", "auth_req": True, "descr": "retrieves a file", "admin_only": True},
    # "get_log": {"cmd": "dev/fsget/log/def.log", "descr": "Log abrufen", "admin_only": True, "auth_req": True},
    "rm_file": {"cmd": "dev/fsdel/{}", "auth_req": True, "descr": "deletes a file", "ad/min_only": True, "not_safe": True}
}


GATEWAY_COMMANDS = {
    "gw_estimate_stats":            {"cmd": "gw/estimatestats"},
    "gw_get_custom":                {"cmd": "gw/getcustom/{}", },
    "gw_get_device_state":          {"cmd": "gw/getdevicestate"},
    "gw_get_device_state_fast":     {"cmd": "gw/getdevicestatefast"},
    "gw_get_device_monitor_data":   {"cmd": "gw/getdevicemonitordata/{%d}/{%%d}"},
    "gw_get_file":                  {"cmd": "gw/getfile{%s}/{%d}"},
    "gw_get_file_parts":            {"cmd": "gw/getfilepart{%s}/{%%d}"},
    "gw_get_file_size":             {"cmd": "gw/getfilesize{%s}"},
    "gw_get_json_stats":            {"cmd": "gw/getjsonstats"},
    "gw_get_jstats_list":           {"cmd": "gw/getjstatslist/{%s}/{%%d}"},
    "gw_get_jstats_for_app":        {"cmd": "gw/getjstatslistforapp/{%s}/{%%d}"},
    "gw_get_stats":                 {"cmd": "gw/getstats/"},
    "gw_get_statslist":             {"cmd": "gw/getstatslist/{%s}/{%%d}"},
    "gw_get_statslist_for_app":     {"cmd": "gw/getstatslistforapp/{%s}/{%%d}"},
    "gw_get_tree":                  {"cmd": "gw/gettree"},
    "gw_get_jvirtual_in_out":       {"cmd": "gw/jvirtualinout/{%s}/{%%d}"},
    "gw_get_virtual_in_out":        {"cmd": "gw/virtualinout/{%s}/{%%d}"},
    "gw_get_structure_patch":       {"cmd": "gw/getstructurepatch/{%d}"},
    "gw_get_xml_stats":             {"cmd": "gw/getxmlstats"},
    "gw_get_sys_info":              {"cmd": "gw/getsysinfo/{}"},
    "update_gw":                    {"cmd": "dev/sys/updategw", "auth_req": True},
    "gw_get_io":                    {"cmd": "dev/gateway/io", "auth_req": True, "min_vers": "10.0.9.24"},
}


LAN_COMMANDS = {
    "get_num_sent_pkts":            {"cmd": "dev/lan/txp", "descr": "Anzahl LAN gesendete Pakete holen", "admin_only": True, "auth_req": True},
    "get_num_sent_pkts_error":      {"cmd": "dev/lan/txe", "descr": "Anzahl LAN gesendete Pakete mit Fehler holen", "admin_only": True, "auth_req": True},
"get_num_collisions":               {"cmd": "dev/lan/txc", "descr": "Anzahl LAN gesendete Pakete mit Kollision holen", "admin_only": True, "auth_req": True},
"get_num_buffer_error":             {"cmd": "dev/lan/exh", "descr": "Anzahl LAN Bufferfehler holen", "admin_only": True, "auth_req": True},
    "get_num_underrun_error":       {"cmd": "dev/lan/txu", "descr": "Anzahl LAN Underrunfehler holen", "admin_only": True, "auth_req": True},
    "get_num_received_pkts":        {"cmd": "dev/lan/rxp", "descr": "Anzahl LAN empfangene Pakete holen", "admin_only": True, "auth_req": True},
    "get_eof_error":                {"cmd": "dev/lan/eof", "descr": "Anzahl LAN EOF Fehler holen", "admin_only": True, "auth_req": True},
    "get_rx_overrun_error":         {"cmd": "dev/lan/rxo", "descr": "Anzahl LAN Empfangsüberlauffehler holen", "admin_only": True, "auth_req": True},
    "get_norecvbuffer_error":       {"cmd": "dev/lan/nob", "descr": "Retrieve number of LAN ‘No receive buffer’ errors", "admin_only": True, "auth_req": True},
    "get_num_lan_ints":             {"cmd": "dev/sys/lanints", "descr": "Anzahl LAN-Interrupts holen", "admin_only": True, "auth_req": True},
}


PLC_COMMANDS = {
    "auto_learn":           {"cmd": "dev/sps/autolearn", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_sps_clock":        {"cmd": "dev/sps/status", "auth_req": True, "descr": "aktuelle PLC Frequenz abfragen", "admin_only": False},
    "restart_sps":          {"cmd": "dev/sps/restart", "auth_req": True, "descr": "PLC neu starten", "admin_only": True, "not_safe": True},
    "stop_sps":             {"cmd": "dev/sps/stop", "auth_req": True, "descr": "PLC anhalten", "admin_only": True, "not_safe": True},
    "resume_sps":           {"cmd": "dev/sps/run", "auth_req": True, "descr": "PLC fortsetzen", "admin_only": True},
    "enable_logging":       {"cmd": "dev/sps/log", "auth_req": True, "descr": "PLC globales Logging erlauben", "admin_only": True},
    "list_devices":         {"cmd": "dev/sps/enumdev", "auth_req": True, "descr": "alle Geräte der PLC auflisten (Miniserver,Extensions,…)", "admin_only": True},
    "list_inputs":          {"cmd": "dev/sps/enumin", "auth_req": True, "descr": "alle Eingänge der PLC auflisten", "admin_only": True},
    "list_outputs":         {"cmd": "dev/sps/enumout", "auth_req": True, "descr": "alle Ausgänge der PLC auflisten", "admin_only": True},
    "identify_ms":          {"cmd": "dev/sps/identify", "auth_req": True, "descr": "Miniserver identifizieren für Erweiterungen muss die Seriennummer als Parameter mitgegeben werden.", "admin_only": True},
    "assign_user":          {"cmd": "dev/sps/assignuser", "auth_req": True},
    "change_mail":          {"cmd": "dev/sps/changemail", "auth_req": True},
    "get_changes":          {"cmd": "dev/sps/changes", "auth_req": True},              # 404 not found?
    "client":               {"cmd": "dev/sps/client", "auth_req": True},               # TODO determine purpose
    "commissioning":        {"cmd": "dev/sps/commissioning", "auth_req": True},        # TODO determine purpose
    "count":                {"cmd": "dev/sps/count", "auth_req": True},                # TODO determine purpose
    "create_stats":         {"cmd": "dev/sps/createstats", "auth_req": True},
    "create_user":          {"cmd": "dev/sps/createuser", "auth_req": True},
    "delete_user":          {"cmd": "dev/sps/deleteuser", "auth_req": True},
    "dis_stats":            {"cmd": "dev/sps/disstats", "auth_req": True},              # TODO determine purpose (disable stats?)
    "dump":                 {"cmd": "dev/sps/dump", "auth_req": True},
    "event":                {"cmd": "dev/sps/event", "auth_req": True},             # not working?
    "event_monitor":        {"cmd": "dev/sps/eventmonitor", "auth_req": True},
    "generate_stats":       {"cmd": "dev/sps/genstats", "auth_req": True, "descr": "Generate statistics for testing purposes"},
    "get_group_list":       {"cmd": "dev/sps/getgrouplist", "auth_req": True},
    "get_group_users":      {"cmd": "dev/sps/getgroupusers", "auth_req": True, "descr": "Retrieve list of groups with all its users"},
    "get_stats":            {"cmd": "dev/sps/getstats", "auth_req": True},
    "get_stats_date":       {"cmd": "dev/sps/getstatsdate", "auth_req": True},
    "get_mac_dash":         {"cmd": "dev/sys/mac", "auth_req": True, "descr": "Retrieve mac (separated by '-')"},
    "get_user_list":        {"cmd": "dev/sps/getuserlist", "auth_req": True, "descr": "Retrieve list of all users"},
    "list_commands":        {"cmd": "dev/sps/listcmds", "auth_req": True},
    "log":                  {"cmd": "dev/sps/log/{str}", "descr": "log given string in Loxone Monitor", "params": {"str": "the string, which will be extracted and displayed in Loxone Monitor"}, "auth_req": True},
    "log_irr":              {"cmd": "dev/sps/logirr", "auth_req": True},
    "log_blinds":           {"cmd": "dev/sps/logjal", "auth_req": True},
    "log_climate":          {"cmd": "dev/sps/logclimate", "auth_req": True, "min_vers": "10.0.9.24"},
    "log_expert":           {"cmd": "dev/sps/logexpert", "auth_req": True, "min_vers": "10.0.9.24"},
    "log_light":            {"cmd": "dev/sps/loglight", "auth_req": True, "min_vers": "10.0.9.24"},
    "log_weather_error":    {"cmd": "dev/sps/logweathererror", "auth_req": True, "min_vers": "10.0.9.24"},
    "add_cmd":              {"cmd": "dev/sps/addcmd", "auth_req": True, "min_vers": "10.0.9.24"},
    "add_secure_cmd":       {"cmd": "dev/sps/addscmd", "auth_req": True, "min_vers": "10.0.9.24"},

    "get_app_version":      {"cmd": "dev/sps/loxappversion", "auth_req": True},     # deprecated? TODO: determine max. version
    "get_app_version_2":    {"cmd": "dev/sps/loxappversion2", "auth_req": True},    # deprecated? TODO: determine max. version
    "get_program_version":  {"cmd": "dev/sps/LoxAPPversion3", "auth_req": True, "descr": "Get date and time of last modification of the smart home configuration"},

    "remove_cmd":           {"cmd": "dev/sps/removecmd", "auth_req": True},
    "remove_task":          {"cmd": "dev/sps/removetask", "auth_req": True},
    "remove_user":          {"cmd": "dev/sps/removeuser", "auth_req": True},

    "restart_clear":        {"cmd": "dev/sps/restartclear", "auth_req": True},
    "restart_clear_u":      {"cmd": "dev/sps/restartclearu", "auth_req": True},
    "restart_def_log":      {"cmd": "dev/sps/restartdeflog", "auth_req": True},
    "restart_no_rem":       {"cmd": "dev/sps/restartnorem", "auth_req": True},
    "search_devices":       {"cmd": "dev/sps/searchdev", "auth_req": True},
    "set_ip":               {"cmd": "dev/sps/setip", "auth_req": True},
    "set_pwd":              {"cmd": "dev/sps/setpwd", "auth_req": True},
    "start_weather":        {"cmd": "dev/sps/startweather", "auth_req": True},
    "get_sps_state":        {"cmd": "dev/sps/state", "admin_only": False, "descr": """PLC status query
0 – No status
1 – PLC booting
2 – PLC program is loaded
3 – PLC has started
4 – Loxone Link has started
5 – PLC running
6 – PLC change
7 – PLC error
8 – Update is occuring"""},
    "get_stats_type":       {"cmd": "dev/sps/statstype", "auth_req": True},
    "status_update":        {"cmd": "dev/sps/statusupdate", "auth_req": True},
    "update_secure_task":   {"cmd": "dev/sps/updatesecuretask", "auth_req": True},
    "update_task":          {"cmd": "dev/sps/updatetask", "auth_req": True},
    "update":               {"cmd": "dev/sys/update", "auth_req": True},    # TODO check what exactly is being updated
    "get_update_error":     {"cmd": "dev/sys/updateerror", "auth_req": True},
    "get_update_errortext": {"cmd": "dev/sys/updateerrortext", "auth_req": True},
    "update_files":         {"cmd": "dev/sys/updatefiles", "auth_req": True},   # TODO det. purpose
    "get_upload_error":     {"cmd": "dev/sys/uploaderror", "auth_req": True},
    "get_upload_errortext": {"cmd": "dev/sys/uploaderrortext", "auth_req": True},
    "get_ws_device":        {"cmd": "dev/sys/wsdevice", "auth_req": True},          # TODO det. purpose
    "get_ws_extension":     {"cmd": "dev/sys/wsextension", "auth_req": True},
    "is_secured":           {"cmd": "dev/sps/issecured/{}", "auth_req": True},     # TODO det purpose
    "update_user_access_code":      {"cmd": "dev/sps/updateuseraccesscode", "auth_req": True, "min_vers": "10.0.9.24"},
    "update_user_pwd":              {"cmd": "dev/sps/updateuserpwd", "auth_req": True, "min_vers": "10.0.9.24"},
    "update_user_pwd_hash":         {"cmd": "dev/sps/updateuserpwdh", "auth_req": True, "min_vers": "10.0.9.24"},
    "update_user_visu_pwd":         {"cmd": "dev/sps/updateuservisupwd", "auth_req": True, "min_vers": "10.0.9.24"},
    "update_user_visu_pwd_hash":    {"cmd": "dev/sps/updateuservisupwdh", "auth_req": True, "min_vers": "10.0.9.24"},
    "client_ip":                    {"cmd": "dev/sps/clientip", "auth_req": True, "min_vers": "10.0.9.24"},
    "edit_user":                    {"cmd": "dev/sps/edituser", "auth_req": True, "min_vers": "10.0.9.24"},
    "fix_stats":                    {"cmd": "dev/sps/fixstats", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_control_info":             {"cmd": "dev/sps/getcontrolinfo", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_program_info":             {"cmd": "dev/sps/programinfo", "auth_req": True, "min_vers": "10.0.9.24"},
    "reload_webinterface":          {"cmd": "dev/sps/reloadwebinterface", "auth_req": True, "min_vers": "10.0.9.24"},
    "save_weather_file":            {"cmd": "dev/sps/saveweatherfile", "auth_req": True, "min_vers": "10.0.9.24"},
    "set_external_resend_time":     {"cmd": "dev/sps/setexternalresendtime", "auth_req": True, "min_vers": "10.0.9.24"},
    "set_rating":                   {"cmd": "dev/sps/setrating", "auth_req": True, "min_vers": "10.0.9.24"},
    "updat_user_access_code":       {"cmd": "jdev/sps/updateuseraccesscode/%s/%s", "auth_req": True, "min_vers": "10.0.9.24"},
}


PROGRAM_COMMANDS = {
    "get_program_info":             {"cmd": "dev/sps/programinfo", "auth_req": True},
}

PUSH_NOTIFICATION_COMMANDS = {
    "pns_check_registration":       {"cmd": "dev/pns/checkregistration", "auth_req": True},
    "pns_get_history":              {"cmd": "dev/pns/gethistory", "auth_req": True},
    "pns_get_unread":               {"cmd": "dev/pns/getunread", "auth_req": True},
    "pns_mark_read":                {"cmd": "dev/pns/markread", "auth_req": True},
    "pns_read_msg":                 {"cmd": "dev/pns/readmessage", "auth_req": True, "min_vers": "10.0.9.24"},
    "pns_get_settings":             {"cmd": "dev/pns/settings", "auth_req": True, "min_vers": "10.0.9.24"},
    "pns_register":                 {"cmd": "dev/pns/register", "auth_req": True},
    "pns_unregister":               {"cmd": "dev/pns/unregister", "auth_req": True},
}


SESSION_COMMANDS = {
    "get_key":                      {"cmd": "dev/sys/getkey"},
    "authenticate":                 {"cmd": "authenticate/{}", "auth_req": True},     # hash   user:pwd          TODO: auth required?
    "get_usersalt":                 {"cmd": "dev/sys/getkey2/{}"},  # [user] --> requests both a one-time-salt (key) and a user-salt                !! 'code'  in response is lowercase, not uppercase as in all the other response
    "get_token":                    {"cmd": "dev/sys/gettoken/{}/{}/{}/{}/{}"},             # [hash, user, type:<int>, uuid, info] --> requests a token, type specifies the lifespan, uuid is used to identify who requested the token & info is a userfriendly info on the platformdevice used.
    "auth_with_token":              {"cmd": "authwithtoken/{}/{}", "auth_req": True},               # [hash, user]
    "refresh_token":                {"cmd": "dev/sys/refreshtoken/{}/{}", "auth_req": True},        # [tokenHash, user]
    "kill_token":                   {"cmd": "dev/sys/killtoken/{}/{}", "auth_req": True},              # [tokenHash, user]
    "kill_all_tokens": {"cmd": "dev/sys/killalltokens", "auth_req": True, "min_vers": "10.0.9.24"},
    "auth_arg":                     {"cmd": "autht={}&user={}", "socket_only": False, "http_only": True, "auth_req": True},  # [tokenhash, user]

    # encryption
    "get_public_key":               {"cmd": "dev/sys/getPublicKey"},
    "key_exchange":                 {"cmd": "dev/sys/keyexchange/{}"},      # RSA encrypted session key + iv in base64
    "authenticate_enc":             {"cmd": "authenticateEnc/{}", "auth_req": True},      # AES encrypted hash in base64        TODO: auth required?
    "aes_payload":                  {"cmd": "salt/{}/{}", "auth_req": True},                   # [salt, payload] --> this is the part that will be AES encrypted.
    "aes_next_salt":                {"cmd": "nextSalt/{}/{}/{}", "auth_req": True},          # [currSalt, nextSalt, payload] --> this is the part that will be AES encrypted.
    "enc_cmd":                      {"cmd": "dev/sys/enc/{}", "auth_req": True},                   # cipher
    "enc_cmd_and_response":         {"cmd": "dev/sys/fenc/{}", "auth_req": True}      # cipher, also the response will be encoded
}

SOCKET_COMMANDS = {

}

SYSTEM_COMMANDS = {
    "get_cc":                       {"cmd": "dev/sys/cc", "auth_req": True},        # TODO determine purpose (collisions?)
    "get_cpu":                      {"cmd": "dev/sys/cpu", "descr": "CPU-Last holen", "admin_only": True, "auth_req": True},
    "get_sys_ctx_switches": {"cmd": "dev/sys/contextswitches", "descr": "Anzahl Umschaltungen zwischen Tasks holen", "admin_only": True, "auth_req": True},
    "get_sys_ctx_switches_ints": {"cmd": "dev/sys/contextswitchesi", "descr": "Anzahl Umschaltungen zwischen Tasks holen, die von Interrupts ausgelöst wurden", "admin_only": True, "auth_req": True},
    "get_heap_size":                {"cmd": "dev/sys/heap", "descr": "Speichergröße holen", "admin_only": False, "auth_req": True},
    "get_help":                     {"cmd": "dev/sys/help", "auth_req": True, "descr": "Get list of commands supported by the MS"},
    "get_hw_id":                    {"cmd": "dev/sys/hwid", "auth_req": True},
    "get_num_ints":                 {"cmd": "dev/sys/ints", "descr": "Anzahl Systeminterrupts holen", "admin_only": True, "auth_req": True},
    "get_num_comm_ints":            {"cmd": "dev/sys/comints", "descr": "Anzahl Kommunikationsinterrupts holen", "admin_only": True, "auth_req": True},
    "get_data_flash":               {"cmd": "dev/sys/dataflash", "auth_req": True},             # TODO determine purpose
    "get_watchdog_bits":            {"cmd": "dev/sys/watchdog", "descr": "Watchdog-Bits holen", "admin_only": True, "auth_req": True},
    "get_date":                     {"cmd": "dev/sys/date", "descr": "Liefert das lokale Datum", "admin_only": True, "auth_req": True},
    "get_sys_info":                 {"cmd": "dev/sys/info", "auth_req": True, "descr": "Retrieve information about the system state in XML format", "min_vers": "10.0.9.24"},
    "get_time":                     {"cmd": "dev/sys/time", "descr": "Liefert die lokale Zeit", "admin_only": True, "auth_req": True},
    "get_arp_table":                {"cmd": "dev/sys/arp", "descr": "Retrieve all entries in arp table", "auth_req": True},
    "set_datetime":                 {"cmd": "dev/sys/setdatetime", "descr": "Sets or gets system date and time. Format: 2013-06-18 16:58:00 or 18/06/2013 16:58:00", "admin_only": False, "auth_req": True},
    "get_log_port":                 {"cmd": "dev/sys/logport", "auth_req": True},
    "get_log_seq":                  {"cmd": "dev/sys/logseq", "auth_req": True},
    "get_sps_cycles":               {"cmd": "dev/sys/spscycle", "descr": "Anzahl PLC-Zyklen holen", "admin_only": True, "auth_req": True},
    "get_bootloader_version":       {"cmd": "dev/sys/loaderversion", "auth_req": True, "min_vers": "10.0.9.24"},
    "query_ntp":                    {"cmd": "dev/sys/ntp", "descr": "NTP Anfrage forcieren", "admin_only": True, "auth_req": True},
    "reboot_ms":                    {"cmd": "dev/sys/reboot", "descr": "Reboot Miniserver", "admin_only": True, "auth_req": True, "not_safe": True},
    "reboot_ext":                   {"cmd": "dev/sys/rebootext", "auth_req": True},         # TODO check if only extensions are rebooted
    "show_config_conns":            {"cmd": "dev/sys/check", "descr": "Zeigt aktive Loxone Config Verbindungen", "admin_only": False, "auth_req": True},
    "log_config_off":               {"cmd": "dev/sys/logoff", "descr": "Trennt bestehende Loxone Config Verbindungen", "admin_only": True, "auth_req": True},
    "show_last_cpu":                {"cmd": "dev/sys/lastcpu", "descr": "zeigt letzen Wert der CPU Auslastung und Anzahl der PLC Zyklen", "admin_only": True, "auth_req": True},
    "start_dev_search":             {"cmd": "dev/sys/search", "auth_req": True},
    "get_dev_search_results":       {"cmd": "dev/sys/searchdata", "descr": "listet die Suchergebnisse", "admin_only": False},
    "get_status":                   {"cmd": "data/status", "descr": "zeigt Status von Miniserver und allen Extensions", "admin_only": False, "auth_req": True},
    "show_stats":                   {"cmd": "stats", "descr": "zeigt die Statistiken", "admin_only": True, "auth_req": True},
    "get_weather_file":             {"cmd": "data/weatheru.xml", "descr": "zeigt die Wetterdaten (nur bei aktivem Wetteservice)", "admin_only": False, "auth_req": True},
    "test_sdcard":                  {"cmd": "dev/sys/sdtest", "descr": "Testet die SD Karte", "admin_only": True, "auth_req": True, "not_safe": True},
    "test_sdcard_full":             {"cmd": "dev/sys/sdtestfull", "descr": "Testet die SD Karte", "admin_only": True, "auth_req": True, "not_safe": True},
    "test_sdcard_burn":             {"cmd": "dev/sys/sdtestburn", "descr": "Testet die SD Karte", "admin_only": True, "auth_req": True, "not_safe": True},
    "start_mem_stresstest":         {"cmd": "dev/sys/memstress", "auth_req": True},
    "repair_flash":                 {"cmd": "dev/sys/repairflash", "auth_req": True},
    "get_uptime":                   {"cmd": "dev/sys/secs", "auth_req": True, "descr": "Get uptime of Miniserver in seconds"},
    "check_udp":                    {"cmd": "dev/sys/udpcheck", "auth_req": True},      # TODO determine purpose - maybe check for update?
    "calculate_crc":                {"cmd": "dev/sys/crc", "auth_req": True},
    "set_webinterface":             {"cmd": "dev/sys/setwebif", "auth_req": True},
    "auto_update":                  {"cmd": "dev/sys/autoupdate", "auth_req": True, "min_vers": "10.0.9.24"},
    "begin_cycle_stats":            {"cmd": "dev/sys/begincyclestats", "auth_req": True, "min_vers": "10.0.9.24"},
    "check_rsa":                    {"cmd": "dev/sys/checkrsa", "auth_req": True, "min_vers": "10.0.9.24"},
    "check_tocken":                 {"cmd": "dev/sys/checktoken", "auth_req": True, "min_vers": "10.0.9.24"},
    "copy_boot_img":                {"cmd": "dev/sys/copybootimage", "auth_req": True, "min_vers": "10.0.9.24"},
    "crash":                        {"cmd": "dev/sys/crash", "auth_req": True, "min_vers": "10.0.9.24", "not_safe": True},
    "get_error_stats":              {"cmd": "dev/sys/errorstats", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_firwewall_info":           {"cmd": "dev/sys/fw", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_visu_salt":                {"cmd": "dev/sys/getvisusalt", "auth_req": True, "min_vers": "10.0.9.24"},
    "inet":                         {"cmd": "dev/sys/inet", "auth_req": True, "min_vers": "10.0.9.24"},                 # TODO det. purpose
    "get_link_stats":               {"cmd": "dev/sys/linkstats", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_mem_info":                 {"cmd": "dev/sys/meminfo", "auth_req": True, "min_vers": "10.0.9.24"},          # not formatting (neither XML nor JSON)
    "ping_device":                  {"cmd": "dev/sys/pingdevice", "auth_req": True, "min_vers": "10.0.9.24"},       # only extensions?
    "save_bna":                     {"cmd": "dev/sys/savebna", "auth_req": True, "min_vers": "10.0.9.24"},
    "set_branding_date":            {"cmd": "dev/sys/setbrandingdate", "auth_req": True, "min_vers": "10.0.9.24"},
    "check_wi":                     {"cmd": "dev/sys/wicheck", "auth_req": True, "min_vers": "10.0.9.24"},              # TODO det purpose
    "ws_device_timeout":            {"cmd": "dev/sys/wsdevicetimeout", "auth_req": True, "min_vers": "10.0.9.24"},      # TODO det purpose
}


TASK_COMMANDS = {
    "add_secure_task":              {"cmd": "dev/sps/addsecuretask", "auth_req": True, "min_vers": "10.0.9.24"},
    "add_task":                     {"cmd": "dev/sps/addtask", "auth_req": True, "min_vers": "10.0.9.24"},
    "get_num_tasks":                {"cmd": "dev/sys/numtasks", "descr": "Anzahl Tasks holen", "admin_only": True, "auth_req": True},
    "get_task_name":                {"cmd": "dev/task{}/name", "descr": "Retrieve task name (ID is 0-based)", "admin_only": True, "auth_req": True},
    "get_task_priority":            {"cmd": "dev/task{}/priority", "descr": "Task Priorität holen", "admin_only": True, "auth_req": True},
    "get_task_stack":               {"cmd": "dev/task{}/stack", "descr": "Task Stack holen", "admin_only": True, "auth_req": True},
    "get_task_num_ctxswitches":     {"cmd": "dev/task{}/contextswitches", "descr": "Task Anzahl Umschaltungen holen", "admin_only": True, "auth_req": True},
    "get_task_waittime":            {"cmd": "dev/task{}/waittimeout", "descr": "Task Wartezeit in ms holen", "admin_only": True, "auth_req": True},
    "get_task_state":               {"cmd": "dev/task{}/state", "descr": "Task Status holen", "admin_only": True, "auth_req": True},
}

UNKNOWN_COMMANDS = {
    "grw_mme":                      {"cmd": "dev/grw/mme", "auth_req": True},        # grw?
    "grw_test":                     {"cmd": "dev/grw/test", "auth_req": True},
    "get_room_no_io":               {"cmd": "dev/roomno/io"},
}


ALL_COMMANDS = [APP_COMMANDS, BLOCK_COMMANDS, BUS_COMMANDS, CALENDAR_COMMANDS, CONFIG_COMMANDS, DEBUG_COMMANDS, EXTENSION_COMMANDS, FIDELIO_COMMANDS, FS_COMMANDS, GATEWAY_COMMANDS, LAN_COMMANDS, PLC_COMMANDS, PROGRAM_COMMANDS, PUSH_NOTIFICATION_COMMANDS, SESSION_COMMANDS, SOCKET_COMMANDS, SYSTEM_COMMANDS, TASK_COMMANDS, UNKNOWN_COMMANDS]

