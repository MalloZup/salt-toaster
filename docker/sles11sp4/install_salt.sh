zypper --non-interactive in salt-master salt-minion
zypper --non-interactive source-install -D salt
zypper --non-interactive in --oldpackage test-package=42:0.0
zypper --non-interactive up zypper libzypp