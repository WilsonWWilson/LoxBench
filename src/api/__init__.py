import re
import time
import secrets.credentials as credentials
from http_status_codes import HttpStatusCode
import posixpath
from api.commands import ALL_COMMANDS, CONFIG_COMMANDS


def _print_formatted_commands(cmds, ms_version=None, has_statuscode=False):
    print("#### {} new commands ####".format(len(cmds)))
    iter = ((c['cmd'], c['auth_req']) for c in cmds) if has_statuscode else zip(cmds, (True for _ in cmds))
    for nc, needs_auth in iter:
        min_vers = ', "min_vers": "{}"'.format(ms_version) if ms_version else ""
        print('\t"": {{"cmd": "{}", "auth_req": {}{}}},'.format(nc, needs_auth, min_vers))


def sync_api_list(source, ms_version=None):
    known_cmds = set({re.sub("/{.*}", "", props['cmd'].lower())      # merge all known commands to a set and remove placeholders
                      for grp in ALL_COMMANDS for props in grp.values()})
    help_cmds = set([c.replace(',', '').strip() for c in source])
    new_cmds = sorted(help_cmds - known_cmds)
    not_listed_cmds = sorted(known_cmds - help_cmds)

    _print_formatted_commands(new_cmds, ms_version)

    print("\n#### {} unlisted commands ####".format(len(not_listed_cmds)))
    for uc in not_listed_cmds:
        print("\t{}".format(uc))
    return new_cmds, not_listed_cmds


def _test_command(comm, cmd, creds=None, auth_req=False):
    used_creds = creds if auth_req else None
    res = comm.lox_get(comm.get_host(), cmd, used_creds, True)
    if auth_req and creds is None:
        print("'{}': claimed to need auth, but works without!".format(cmd))
    if type(res) is HttpStatusCode:
        print("'{}': got HttpStatusCode: {}".format(cmd, res))
        code, res = res, '-'
    else:
        code, res, res_cmd = res    # unpack full response
        if code == HttpStatusCode.UNAUTHORIZED and not auth_req:
            return _test_command(comm, cmd, creds, True)

        if code != HttpStatusCode.NOT_FOUND:
            print("{:<50}\t\t=> [{}] {}".format(cmd, code, res))
    return code, res, auth_req


def check_api_fns(cmds, comm):
    if len(cmds) == 0:
        return

    are_raw_cmds = type(cmds[0]) == str     # use commands as is; commands are not objects with additional informats
    creds = comm.get_credentials()

    if are_raw_cmds:
        for cmd in cmds:
            need_auth = []
            http_code, res = _test_command(comm, cmd, creds)

            if http_code == HttpStatusCode.UNAUTHORIZED:
                need_auth.append(cmd)
            elif http_code == HttpStatusCode.NOT_FOUND:
                pass

    else:
        for k, cmd_info in cmds:
            cmd = cmd_info["cmd"].replace('dev', 'jdev', True)
            admin_only = cmd_info.get("admin_only", False)
            socket_only = cmd_info.get("socket_only", False)
            not_safe = cmd_info.get("not_safe", False)
            auth_req = cmd_info.get("auth_req", False)
            user_creds = creds if auth_req else None

            if not_safe:    # skip requests, that might cause permanent changes
                continue

            # try:
            http_code, _ = _test_command(comm, cmd, user_creds, auth_req)
            # print("Checking {}   \t admin_only:{}    \t socket_only:{}".format(k, admin_only, socket_only))
            if not auth_req:
                print("'{}': Authentication is required!".format(k))
            _test_command(comm, cmd, (credentials.user, credentials.password), auth_req=True)
            # except:
            #     print("'{}': unhandled problem".format(k))

        time.sleep(0.2)


def discover_api_fns(suggestions, comm):
    """
    Hint: Suggested commands should be preprocessed. '/' at the beginning should be removed and no unnecessary symbols (or comments) should be at the end of the line
    :param suggestions:
    :param comm:
    :return:
    """
    def _eval_api_fn(cmd, creds):
        is_valid_cmd = False
        code, res, needs_auth = _test_command(comm, cmd, creds)   # test suggestion as is
        if code == HttpStatusCode.BLOCKED_TEMP:
            raise PermissionError("client was blocked temporarily")

        if code != HttpStatusCode.NOT_FOUND and code != HttpStatusCode.UNAUTHORIZED:
            c = cmd.replace('jdev', 'dev')
            if c in known_cmds:
                redundant_entries.append(c)
            elif c not in (c['cmd'] for c in found_cmds):
                found_cmds.append({"code": code, "cmd": cmd, "res": res, "auth_req": needs_auth})
                is_valid_cmd = True
        return code, is_valid_cmd

    found_cmds = []
    redundant_entries = []
    lvl1_pfxs = ['dev', 'jdev', 'gw', 'data']
    lvl2_pfxs = ['', 'cfg', 'sps', 'sys', 'pns', 'debug']
    known_cmds = set({re.sub("/{.*}", "", props['cmd'].lower())      # merge all known commands to a set and remove placeholders
                      for grp in ALL_COMMANDS for props in grp.values()})

    # TODO detect if response is a regular api (dev/jdev responses or a file like html, xml, etc.)
    # TODO test commands on socket connection as well
    suggestions = set(suggestions)      # deduplicate suggestions
    creds = credentials.user, credentials.password
    unauth_counter = 0

    try:
        for cmd in suggestions:
            cmd_found = False
            print("----- Testing '{}' -------".format(cmd))
            try:
                if cmd in known_cmds:
                    redundant_entries.append(cmd)
                    continue

                code, is_valid = _eval_api_fn(cmd, creds)
                cmd_found = cmd_found or is_valid
                for c in (posixpath.join(p1, p2, cmd) for p1 in lvl1_pfxs for p2 in lvl2_pfxs):
                    code, is_valid = _eval_api_fn(c, creds)
                    cmd_found = cmd_found or is_valid
                    if code == HttpStatusCode.UNAUTHORIZED:
                        unauth_counter += 1
                    elif code == HttpStatusCode.MS_OUT_OF_SERVICE:
                        # raise EnvironmentError("MS out of order")
                        time.sleep(30)
            except EnvironmentError as exc:
                print("skipped '{}' because '{}'".format(cmd, exc))
                break
    except PermissionError as exc:
        print("Stopped discovery process because '{}'".format(exc))

    # print("\n\n______________ found {} commands ______________".format(len(found_cmds)))
    # for cmd in found_cmds:
    #     print("'{:<20}' => [{}] {}".format(cmd['cmd'], cmd['code'], cmd['res']))

    if len(redundant_entries) > 0:
        print("\n____________ following {} commands are already known ______________".format(len(redundant_entries)))
        for cmd in redundant_entries:
            print("\t{}".format(cmd))

    print("\n")
    _print_formatted_commands(found_cmds, has_statuscode=True)
