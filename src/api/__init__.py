import pathlib
import re
from api.commands import ALL_COMMANDS


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

