def test_crio_sources_file(host):
    f = host.file("/etc/apt/sources.list.d/cri-o.sources")
    assert f.exists
    assert f.user == "root"
    assert "v1.32" in f.content_string

def test_crio_package_installed(host):
    pkg = host.package("cri-o")
    assert pkg.is_installed

def test_crio_service_running(host):
    svc = host.service("crio")
    assert svc.is_running
    assert svc.is_enabled