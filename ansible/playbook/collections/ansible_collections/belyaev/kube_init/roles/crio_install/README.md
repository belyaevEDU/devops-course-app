# belyaev.kube_init crio_install Role

The role adds the CRI-O apt repository & installs it.

Minimal version is set by `CRIO_MINIMAL_VERSION` and by default is `v1.32`, the role checks for the set version to be >= the minimal one.

## Requirements

-

## Role Variables

`CRIO_VERSION` - self-explanatory, default: `v1.32`
`CRIO_MINIMAL_VERSION` - self-explanatory, default: `v1.32`

## Example Playbook

```yaml
- name: Install cri-o
  hosts: servers
  roles:
    - role: belyaev.kube_init.crio_install
      CRIO_VERSION: v1.36
```