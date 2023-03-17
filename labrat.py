from git.repo import Repo
import uuid

repo = Repo('.')
g = repo.git

start = g.status()
print(f'before all\n{start}')

g.add('.')
g.stash()

# flag2
branch_name = uuid.uuid4().hex
g.checkout('-b', branch_name)
g.stash('apply')

g.add('.')
g.commit('-m', f'message {branch_name}')
g.update_ref(f"refs/labrats/{branch_name}",branch_name)

g.checkout('master')
g.branch('-D',branch_name)

g.stash('pop')
g.reset()

after = g.status()
print(f'after all\n{after}')
assert start == after

print(branch_name)