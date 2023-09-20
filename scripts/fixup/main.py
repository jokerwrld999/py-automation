#!/usr/bin/env python

import re
import sys

def commit_fixup(file_path):
    updated_commits = []
    duplicate_messages = set()

    file = open(file_path, 'r+')
    content = file.read()
    formated_content = re.sub(r'^.*?pick', '\npick', content)
    lines = formated_content.strip().split('\n')

    for line in lines:
        parts = line.strip().split(' ', 2)

        if parts[0] != 'pick':
            continue

        commit_action = parts[0]
        commit_hash = parts[1]
        commit_message = parts[2]

        if commit_message in duplicate_messages:
            updated_commits.append(f'fixup {commit_hash} {commit_message}')
        else:
            updated_commits.append(
                f'{commit_action} {commit_hash} {commit_message}')
            duplicate_messages.add(f'{commit_message}')

    file.seek(0)
    file.truncate()
    file.write('\n'.join(updated_commits))
    file.close()

    print('\nUpdated git-rebase-todo file.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("GIT_SEQUENCE_EDITOR='<commit_fixup_script_path>' git rebase -i --root")
        sys.exit(1)

    commit_fixup(sys.argv[1])
