import pathlib
import re
import os.path
import itertools
from api.commands import ALL_COMMANDS
from comm import HttpStatusCode


def sync_api_list(source, ms_version=None):
    path = pathlib.Path(source)
    if path.exists():
        with open(source, 'r') as f:
            source = f.readlines()

    cmds = {}
    test = [cmds.update(cs) for cs in ALL_COMMANDS]
    # known_cmds = set([c['cmd'].replace('/{}', '').lower() for c in cmds.values()])
    known_cmds = set([re.sub("/{.*}", "", c['cmd'].lower()) for c in cmds.values()])
    help_cmds = set([c.replace(',', '').strip() for c in source])

    new_cmds = sorted(help_cmds - known_cmds)
    not_listed_cmds = sorted(known_cmds - help_cmds)

    print("#### {} new commands ####".format(len(new_cmds)))
    for nc in new_cmds:
        min_vers = ', "min_vers": "{}"'.format(ms_version) if ms_version else ""
        print('\t"": {{"cmd": "{}", "auth_req": True{}}},'.format(nc, min_vers))

    print("\n#### {} unlisted commands ####".format(len(not_listed_cmds)))
    for uc in not_listed_cmds:
        print("\t{}".format(uc))


cnt = 0


def discover_api_fns(suggestions, comm):
    """
    Hint: Suggested commands should be preprocessed. '/' at the beginning should be removed and no unnecessary symbols (or comments) should be at the end of the line
    :param suggestions:
    :param comm:
    :return:
    """
    def _test_cmd(found_cmds, known_cmds, cmd):
        global cnt
        cnt += 1
        if cmd in known_cmds:
            code, res = HttpStatusCode.OK, "already known"
        else:
            code, res = comm.request(cmd, True)
        if code != HttpStatusCode.NOT_FOUND:
            found_cmds.append((cmd, res))
        return code != HttpStatusCode.OK, res

    found_cmds = []
    lvl1_pfxs = ['dev', 'gw', 'data']
    lvl2_pfxs = ['', 'cfg', 'sps', 'sys', 'pns', 'debug']
    cmds = {}
    test = [cmds.update(cs) for cs in ALL_COMMANDS]
    known_cmds = set([re.sub("/{.*}", "", c['cmd'].lower()) for c in cmds.values()])
    print("{} commands are already known prior to call!!".format(len(known_cmds)))

    # TODO split suggestions with path to it's fragments and don't query resulting duplicates  (cmd: dev/testcmd vs guessed /dev/dev/testcmd

    paths = [('',)] + list(itertools.product(lvl1_pfxs, lvl2_pfxs))

    for cmd in set(suggestions):     # deduplicate suggestions
        # clear '/' at beginning to be consistent
        for c in [os.path.join(*p, cmd) for p in paths]:
            if not cmd.startswith(pathlib.PurePath(c).anchor):
                continue   # lvl1 prefix can't be nested
            _test_cmd(found_cmds, known_cmds, c)
        #

    print(" --- {} requests ---".format(cnt))
    print("\n### Found {} commands\n".format(len(found_cmds)))
    # for c, res in found_cmds:
    #     print("'{}' => {}".format(c, res))
