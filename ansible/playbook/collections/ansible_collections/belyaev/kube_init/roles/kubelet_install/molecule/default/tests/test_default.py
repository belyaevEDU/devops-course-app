def test_kubernetes_sources_file(host):
    f = host.file("/etc/apt/sources.list.d/kubernetes.sources")
    assert f.exists
    assert f.user == "root"
    assert "v1.32" in f.content_string

def test_kubelet_package_installed(host):
    pkg = host.package("kubelet")
    assert pkg.is_installed

def test_kubelet_binary_exists(host):
    f = host.file("/usr/bin/kubelet")
    assert f.exists
    assert f.mode == 0o755