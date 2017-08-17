#!/usr/bin/env python

import subprocess
from subprocess import Popen, PIPE
import re
import os
import sys
import traceback

STATUS_CMD = ['git', 'status', '--porcelain']
ADDED_FILE_FLAGS = ['A ', 'M ', '?? ']
GIT_RESET_CMD = ['git', 'reset']
GIT_ADD_CMD = ['git', 'add']
STAGE_GITATTRS_CMD = ['git', 'add', '.gitattributes']
GITATTRS_CHANGED = False
DIVIDER = 80*'-'

# don't do anything, just print log:
DRY_RUN = False


def _get_non_lfs_extensions():
    """
    """
    exts = []

    non_lfs_files = os.path.join(os.getcwd(), 'git_hooks/non_lfs_files.txt')
    
    with open(non_lfs_files) as f:
        exts = f.readlines()
        exts = [x.strip() for x in exts]

    return exts


def track():
    """
    Main entry point for hook, figure out what needs to be tracked as lfs and do it.
    """
    git_status = Popen(STATUS_CMD, stdout=PIPE, stderr=PIPE)
    git_status_result = git_status.stdout.readlines()

    non_lfs_extensions = _get_non_lfs_extensions()
    print '\nnon-lfs files: %s' % non_lfs_extensions
    
    for line in git_status_result:
        line = line[:-1]
        file_name = ''

        for file_flag in ADDED_FILE_FLAGS:
            if line.startswith(file_flag):
                file_name = line.replace(file_flag, '')

        if file_name == '':
            continue

        if file_name.startswith(' '):
            file_name = file_name[1::]

        # remove any leading and trailing double quotes
        if file_name.startswith('"') and file_name.endswith('"'):
            file_name = file_name[1:-1:]
        
        file_is_lfs = True
        for ext in non_lfs_extensions:
            rgx = r'.*\.%s$' % ext
            if re.match(rgx, file_name, re.IGNORECASE):
                file_is_lfs = False

        if file_is_lfs:

            print '\n' + DIVIDER
            print 'staged file: "%s"' % file_name
            print 'file is lfs: %s' % file_is_lfs
            
            try:
                _track_as_lfs(file_name)
                print "done"
                print DIVIDER                
            except Exception as e:
                print "LFS tracking failed: "
                print e
    
    if GITATTRS_CHANGED and not DRY_RUN:
        print '\n.gitattributes were changed, staging:'
        subprocess.check_call('git add .gitattributes', shell=True)


def _track_as_lfs(file_name):
    """
    Track a given file or file type (if extension is presnet) as lfs
    """
    # ensure file_name is wrapped in double quotes, for file paths with spaces
    if not file_name.startswith('"') and not file_name.endswith('"'):
        file_name = '"%s"' % file_name    

    file_split = file_name.split('.')

    # track files with extensions as a wildcard:
    if len(file_split) > 1:
        lfs_pattern = '"*.%s' % file_split[-1]

    # track files without extensions as unique paths:
    else:
        lfs_pattern = file_name

    reset_cmd = 'git reset ' + file_name
    lfs_cmd = 'git --work-tree "' + os.getcwd() + '" lfs track ' + lfs_pattern
    add_cmd = 'git add ' + file_name

    print reset_cmd
    print lfs_cmd
    print add_cmd
    
    global GITATTRS_CHANGED
    GITATTRS_CHANGED = True

    if not DRY_RUN:
        subprocess.check_call(reset_cmd, shell=True)
        subprocess.check_call(lfs_cmd, shell=True)
        subprocess.check_call(add_cmd, shell=True)


if __name__ == "__main__":
    print "LFS tracking hook started"
    try:
        track()
    except Exception as e:
        print "\nLFS tracking hook failed: "
        exc_type, exc_value, exc_traceback = sys.exc_info()                
        print traceback.format_exc()
        exit(1)
    
    print "\nLFS tracking hook ended"
    exit(0)
