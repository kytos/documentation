import os
import shutil
import json
from pathlib import Path


BASE = Path(__file__).parent

docs_dir = BASE / 'docs'
tmp_dir = BASE / 'tmp'

if docs_dir.exists():
    shutil.rmtree(docs_dir, ignore_errors=True)

if tmp_dir.exists():
    shutil.rmtree(tmp_dir, ignore_errors=True)

docs_dir.mkdir()
tmp_dir.mkdir()

data = open("data.json", 'r')
data = json.loads(data.read())
versions = data.get('versions',[])
repositories = data.get('repositories', [])

download_command = "wget {} -O {}"
unpack_tar_command = "tar -xf {} -C {}"
sphinx_command = "make -C {} SPHINXOPTS=\"{}\""

for version_name, tag_name in versions.items():
    for repository_name, repository in repositories.items():
        tarball_label = "{}-{}".format(repository_name, tag_name)

        # download tarball
        tarball_url = "{}/archive/{}.tar.gz".format(repository, tag_name)
        dst_tarball = tmp_dir / "{}.tar.gz".format(tarball_label)
        os.system(download_command.format(tarball_url, dst_tarball))
        # unpack tarball
        os.system(unpack_tar_command.format(dst_tarball, tmp_dir))

        # build sphinx docs
        doc_dir = tmp_dir / tarball_label / "docs"
        versions_flags = "-A versions={} -A show_version=True -A version={}"
        versions_flags = versions_flags.format(",".join(versions.keys()),
                                               version_name)
        os.system(sphinx_command.format(doc_dir, versions_flags))

        # move from tmp to docs
        src = doc_dir /  "_build/dirhtml"
        dst = docs_dir / version_name / repository_name

        os.makedirs(dst)
        src.rename(dst)
