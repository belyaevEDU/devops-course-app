# belyaev.kube_init kube_apt_repo Role

The role adds the Kubernetes apt repository with the specified version

## Requirements

-

## Role Variables

`KUBERNETES_VERSION` - self-explanatory, default: `v1.32`

## Example Playbook

```yaml
- name: Add Kubernetes apt repository
  hosts: servers
  roles:
    - role: belyaev.kube_init.kube_apt_repo
      KUBERNETES_VERSION: v1.36
```