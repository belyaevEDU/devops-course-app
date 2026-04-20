# belyaev.kube_init kubelet_install Role

The role adds the Kubernetes apt repository & installs Kubelet

## Requirements

-

Uses internal `kube_apt_repo` role

## Role Variables

`KUBERNETES_VERSION` - self-explanatory, default: `v1.32`

## Example Playbook

```yaml
- name: Install kubelet
  hosts: servers
  roles:
    - role: belyaev.kube_init.kubelet_install
      KUBERNETES_VERSION: v1.36
```