# belyaev.kube_init kubeadm_install Role

The role adds the Kubernetes apt repository & installs Kubeadm

## Requirements

-

Uses internal `kube_apt_repo` role

## Role Variables

`KUBERNETES_VERSION` - self-explanatory, default: `v1.32`

## Example Playbook

```yaml
- name: Install kubeadm
  hosts: servers
  roles:
    - role: belyaev.kube_init.kubeadm_install
      KUBERNETES_VERSION: v1.36
```