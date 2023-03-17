from git.repo import Repo
import uuid
import functools
import re

repo = Repo('.')
g = repo.git


def get_current_branch():
    try:
        current_branch = repo.active_branch  # acquire current branch
    except:
        current_branch = re.findall(r'at (.*)\n', g.status())[0]  # resolve exception caused by detached HEAD
    return current_branch


def maintain_git_workspace(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        prev_branch = get_current_branch()
        g.add('.')
        g.stash()

        rv = func(*args, **kw)

        g.checkout(prev_branch)
        g.stash('pop')
        g.reset()

        return rv

    return wrapper


def take_snapshot():
    @maintain_git_workspace
    def save_new_branch():
        branch_name = f'labrat-tmp-branch-{uuid.uuid4().hex}'
        rat_id = uuid.uuid4().hex

        g.checkout('-b', branch_name)
        g.stash('apply')

        g.add('.')
        g.commit('-m', 'a snapshot commit created by labrat')

        g.update_ref(f"refs/labrats/{rat_id}", branch_name)

        return branch_name

    g.branch('-D', save_new_branch())

@maintain_git_workspace
def export_snapshot(rat_id):
    from shutil import copytree, ignore_patterns
    g.checkout(f"refs/labrats/{rat_id}")
    copytree('.', f'export-rats/{rat_id}', ignore=ignore_patterns('*.git'))
    

# take_snapshot()
