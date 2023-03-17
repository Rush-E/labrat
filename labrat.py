from git.repo import Repo
import uuid
import re

repo = Repo('.')
g = repo.git

try:
    prev_branch = repo.active_branch  # acquire current branch
except:
    prev_branch = re.findall(r'at (.*)\n', g.status())[0]  # resolve exception caused by detached HEAD

start = g.status()

g.add('.')
g.stash()

branch_name = f'labrat-tmp-branch-{uuid.uuid4().hex}'
ref_id = uuid.uuid4().hex

g.checkout('-b', branch_name)
g.stash('apply')

g.add('.')
g.commit('-m', 'a snapshot commit created by labrat')

g.update_ref(f"refs/labrats/{ref_id}", branch_name)

g.checkout(prev_branch)

g.branch('-D', branch_name)

g.stash('pop')
g.reset()

assert start == g.status()