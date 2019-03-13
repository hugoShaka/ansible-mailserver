# Firewall

This role is used to configure port blocking on hosts via iptables.

## Requirements

None.

## Role Variables

- `ports`

  This parameter is a list of the ports to be opened on each host. A number of ports are opened by default but the user can specify other ports if they desire, or remove some from the list.


## Example Playbook

```yml
---
- name: Provision the firewall configuration
  hosts: all
  vars:
    ports:
      - 22
      - 25
  roles:
    - firewall
...
```
