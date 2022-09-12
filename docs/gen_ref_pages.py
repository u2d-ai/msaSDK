"""Generate the code reference pages and navigation."""
import pickle
from os.path import exists
from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("u2d_msa_sdk").rglob("*.py")):

    module_path = path.relative_to("u2d_msa_sdk").with_suffix("")
    doc_path = path.relative_to("u2d_msa_sdk").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
        continue
    elif parts[-1] == "__main__":
        continue
    elif parts[-1] == "main":
        continue
    elif parts[-1] == "run":
        continue

    nav[parts] = doc_path.as_posix()  #

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        print("Create Virtual MD Doc for:", full_doc_path, "Set the ident to:", ident, )
        fd.write(f"# u2d_msa_sdk Module\n")
        fd.write(f"## **``.{ident}``**\n***\n\n")
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:  #
    nav_file.writelines(nav.build_literate_nav())  #

req_txt: str = ""
pkl_info_file: str = "docs/saved_req_package_pip_info.pkl"
sub_process_result: dict ={}
sub_process_result_file_needs_update: bool = False
sub_process_result_file_exists: bool = exists(pkl_info_file)
if sub_process_result_file_exists:
    with open(pkl_info_file, 'rb') as f:
        print("Load existing", pkl_info_file, "file")
        sub_process_result = pickle.load(f)

with open("requirements.txt", "r") as req_file:
    req_txt = req_file.read()
    if req_txt and len(req_txt) > 0:
        from subprocess import PIPE, run

        with mkdocs_gen_files.open("requirements.md", "w") as fd:
            fd.write(f"# u2d_msa_sdk - Included Libraries\n***\n\n")
            # Python 3.x only
            for line in req_txt.splitlines():
                line = line.strip()

                if line == '':
                    continue
                elif not line or line.startswith('#'):
                    # comments are lines that start with # only
                    fd.write(f"\n\n## **{line.replace('# ', '')}**\n***\n\n")
                    continue
                else:
                    parts: list = line.split("#")

                    parts_front = str(parts[0]).strip()
                    parts_front = parts_front.replace("==", "=")
                    package: str = str(parts_front).split("=")[0].replace(">", "").replace("<", "").replace("~", "").split("[")[0]
                    version: str = ""
                    if len(str(parts_front).split("=")) > 1:
                        version: str = str(parts_front).split("=")[1].replace(">", "").replace("<", "").replace("~", "").strip()
                        version_link: str = f"[![PyPI version fury.io](https://badge.fury.io/py/{package}.svg)](https://pypi.org/project/{package}/{version}/)"
                        condition: str = parts_front.replace(package, "") # .replace(version, "")
                        if condition.__contains__("]"):
                            condition = condition.split("]")[1]
                        fd.write(f"### **{package}** ``{condition}`` {version_link}\n")
                    else:
                        fd.write(f"### **{package}**\n")

                    if len(parts) > 1:
                        comment: str = str(parts[1]).strip().capitalize()
                        fd.write(f"{comment.capitalize()}\n\n")
                    else:
                        fd.write(f"\n\n")
                    pip_result: str = ""
                    if not sub_process_result_file_exists or package not in sub_process_result.keys():
                        sub_process_result_file_needs_update = True
                        command = ['pip', 'show', package]
                        print("Collect PIP Infos for package:", package)
                        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                        pip_result = result.stdout
                        sub_process_result[package] = pip_result
                    else:
                        pip_result = sub_process_result[package]

                    if len(pip_result) > 0:
                        req_line_text: str = ""
                        check_version: str = ""
                        for req_line in pip_result.splitlines():
                            if not req_line.__contains__("Location"):
                                if req_line.__contains__("Version") and not req_line.__contains__(version) and len(version)>0:
                                    check_version = req_line

                                req_line_text += f"{req_line}\n"

                        if len(check_version) > 0:
                            fd.write(f"<span style='color:red'> Check {check_version} vs {version}</span>\n")

                        fd.write(f"\n```console\n\n{req_line_text}```\n\n")

    nav["requirements"] = "requirements.md"

if not sub_process_result_file_exists or sub_process_result_file_needs_update:
    with open(pkl_info_file, 'wb') as f:
        pickle.dump(sub_process_result, f)
