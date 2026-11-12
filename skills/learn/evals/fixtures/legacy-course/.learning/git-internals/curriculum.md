# Git internals (synthetic fixture)

Goal: explain what Git stores and predict what everyday commands change.

## Course mode

Style: `tutorial`. About 30 minutes per session.

## Unit 1: Objects

- `git.blob`: file contents as blobs
- `git.tree`: a tree lists names and blobs
- `git.commit-snapshot`: a commit points at one tree and its parents
- `git.hash`: object names are hashes of content

## Unit 2: Branches and HEAD

- `git.branch-pointer`: a branch is a name that points at one commit
- `git.head`: HEAD names the current branch or commit
- `git.fast-forward`: when a merge only moves a pointer
- `git.merge-commit`: a commit with two parents
- `git.detached-head`: HEAD pointing at a commit directly

## Unit 3: Remotes

- `git.remote-tracking`: remote-tracking branches
- `git.fetch-vs-pull`: what each command changes
