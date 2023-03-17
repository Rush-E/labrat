import git
import uuid

repo = git.Repo('.')


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

g.checkout('master')

g.stash('pop')
g.reset()

after = g.status()
print(f'after all\n{after}')
assert start == after

print(branch_name)

#
# 123123123
# 1231231231231
# new change
###
