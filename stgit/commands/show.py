# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from stgit import argparse, git
from stgit.argparse import opt
from stgit.commands.common import (DirectoryHasRepository,
                                   color_diff_flags,
                                   git_id,
                                   parse_patches)
from stgit.lib import git as gitlib
from stgit.pager import pager

__copyright__ = """
Copyright (C) 2006, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see http://www.gnu.org/licenses/.
"""

help = 'Show the commit corresponding to a patch'
kind = 'patch'
usage = ['[options] [--] [<patch1>] [<patch2>] [<patch3>..<patch4>]']
description = """
Show the commit log and the diff corresponding to the given patches.
The output is similar to that generated by 'git show'."""

args = [argparse.patch_range(argparse.applied_patches,
                             argparse.unapplied_patches,
                             argparse.hidden_patches)]
options = [
    opt('-b', '--branch', args = [argparse.stg_branches],
        short = 'Use BRANCH instead of the default branch'),
    opt('-a', '--applied', action = 'store_true',
        short = 'Show the applied patches'),
    opt('-u', '--unapplied', action = 'store_true',
        short = 'Show the unapplied patches'),
    opt('-s', '--stat', action = 'store_true',
        short = 'Show a diffstat summary of the specified patches'),
    ] + argparse.diff_opts_option()

directory = DirectoryHasRepository(log=False)
crt_series = None


def func(parser, options, args):
    """Show commit log and diff
    """
    if options.applied:
        patches = crt_series.get_applied()
    elif options.unapplied:
        patches = crt_series.get_unapplied()
    elif len(args) == 0:
        patches = ['HEAD']
    elif '..' in ' '.join(args):
        # patch ranges
        applied = crt_series.get_applied()
        unapplied = crt_series.get_unapplied()
        patches = parse_patches(args, applied + unapplied + \
                                crt_series.get_hidden(), len(applied))
    else:
        # individual patches or commit ids
        patches = args

    if not options.stat:
        options.diff_flags.extend(color_diff_flags())
    commit_ids = [git_id(crt_series, patch) for patch in patches]
    commit_str = '\n'.join([git.pretty_commit(commit_id,
                                              flags = options.diff_flags)
                            for commit_id in commit_ids])
    if options.stat:
        commit_str = gitlib.diffstat(commit_str)
    if commit_str:
        pager(commit_str.encode('utf-8'))
