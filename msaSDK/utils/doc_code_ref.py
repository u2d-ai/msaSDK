"""Generate the code reference pages and navigation."""

import os.path
import pickle
from os.path import exists
from pathlib import Path
from typing import List

import mkdocs_gen_files


def format_pip_result(pip_result, version):
    req_line_text: str = ""
    check_version: str = ""
    check_required: List[str] = []
    for req_line in pip_result.splitlines():
        if not req_line.__contains__("Location:"):
            if req_line.__contains__("Version:") and not req_line.__contains__(version) and len(
                    version) > 0:
                check_version = req_line
            if req_line.__contains__("Requires:"):
                temp_req_line = req_line.replace("Requires:", "").strip()
                if len(temp_req_line) > 0:
                    tl: List[str] = temp_req_line.split(", ")
                    if len(tl) > 0:
                        check_required = tl.copy()

            req_line_text += f"    {req_line}\n"  # keep the spaces !important

    return req_line_text, check_version, check_required


def generate_sub_process_result(requirement_file) -> dict:
    sub_process_result: dict = {}
    with open(requirement_file, "r") as req_file:
        req_txt = req_file.read()
        if req_txt and len(req_txt) > 0:
            from subprocess import PIPE, run
            for line in req_txt.splitlines():
                line = line.strip()

                if line == '':
                    continue
                elif not line or line.startswith('#'):
                    continue
                else:
                    parts: list = line.split("#")
                    parts_front = str(parts[0]).strip()
                    parts_front = parts_front.replace("==", "=")
                    package: str = \
                        str(parts_front).split("=")[0].replace(">", "").replace("<", "").replace("~", "").split("[")[0]
                    version: str = ""
                    package = package.lower()
                    comment: str = ""
                    if len(str(parts_front).split("=")) > 1:
                        version: str = str(parts_front).split("=")[1].replace(">", "") \
                            .replace("<", "").replace("~", "").strip()
                        version_link: str = f"[![PyPI version fury.io](https://badge.fury.io/py/{package}.svg)](https://pypi.org/project/{package}/{version}/)"
                        condition: str = parts_front.replace(package, "")  # .replace(version, "")
                        if condition.__contains__("]"):
                            condition = condition.split("]")[1]

                    if len(parts) > 1:
                        comment = str(parts[1]).strip().capitalize()

                    pip_result: str = ""
                    command = ['pip', 'show', package]
                    print("Collect PIP Infos for package:", package)
                    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

                    pip_result = result.stdout
                    if result.returncode != 0:
                        print("ERROR Pip result:", result.returncode, result.stderr, len(pip_result), pip_result)
                    else:
                        req_line_text: str
                        check_version: str
                        check_required: List[str]
                        req_line_text, check_version, check_required = format_pip_result(pip_result=pip_result,
                                                                                         version=version)
                        sub_process_result[package] = {"pip_result": pip_result,
                                                       "version": version,
                                                       "version_link": version_link,
                                                       "condition": condition,
                                                       "req_line_text": req_line_text,
                                                       "check_version": check_version,
                                                       "check_required": check_required,
                                                       "comment": comment,
                                                       }
                        for entry in check_required:
                            entry = entry.lower()
                            if entry not in sub_process_result:

                                command = ['pip', 'show', entry]
                                print("Collect Req. PIP Infos for package:", entry)
                                result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

                                r_pip_result = result.stdout
                                if result.returncode != 0:
                                    print("ERROR: Req. Pip result:", result.returncode, result.stderr,
                                          len(r_pip_result),
                                          r_pip_result)
                                else:
                                    r_req_line_text, r_check_version, r_check_required = format_pip_result(
                                        pip_result=r_pip_result,
                                        version=version)
                                    sub_process_result[entry] = {"pip_result": r_pip_result,
                                                                 "req_line_text": r_req_line_text,
                                                                 "check_required": r_check_required,
                                                                 }

    return sub_process_result


def generate_code_reference_documentation(virtual_ref_nav_path: str = "reference",
                                          ref_md_file: str = "SUMMARY.md",
                                          virtual_requirements_nav_path: str = "requirements",
                                          req_md_file: str = "requirements.md",
                                          source_path: str = "msaSDK",
                                          source_file_type_filter: str = "*.py",
                                          requirement_file: str = "requirements.txt",
                                          md_file_type: str = ".md",
                                          recreate_pip_info: bool = False,
                                          exclude_functions: List[str] = ["__init__", "__main__", "main", "run", ],
                                          pkl_info_file: str = "docs/saved_req_package_pip_info.pkl"):
    """Generates the virtual mkdocs md files and adds them to the navigation.

    Scans the requirement file and gets pip show info for each package and stores it to a pickle file.
    """
    nav = mkdocs_gen_files.Nav()

    for path in sorted(Path(source_path).rglob(source_file_type_filter)):

        module_path = path.relative_to(source_path).with_suffix("")
        doc_path = path.relative_to(source_path).with_suffix(md_file_type)
        full_doc_path = Path(virtual_ref_nav_path, doc_path)

        parts = tuple(module_path.parts)

        if parts[-1] in exclude_functions:
            continue

        nav[parts] = doc_path.as_posix()  #

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(parts)
            print("Create Virtual MD Doc for:", full_doc_path, "Set the ident to:", ident, )
            fd.write(f"# {source_path} Module\n")
            fd.write(f"## **``.{ident}``**\n***\n\n")
            fd.write(f"::: {ident}")

        mkdocs_gen_files.set_edit_path(full_doc_path, path)

    genfile: str = os.path.join(virtual_ref_nav_path, ref_md_file)
    with mkdocs_gen_files.open(genfile, "w") as nav_file:  #
        nav_file.writelines(nav.build_literate_nav())  #

    req_txt: str = ""
    sub_process_result: dict = {}
    sub_process_result_file_needs_update: bool = False
    sub_process_result_file_exists: bool = exists(pkl_info_file)

    if sub_process_result_file_exists and not recreate_pip_info:
        with open(pkl_info_file, 'rb') as f:
            print("Load existing", pkl_info_file, "file")
            sub_process_result = pickle.load(f)
    else:
        sub_process_result = generate_sub_process_result(requirement_file=requirement_file)

    with open(requirement_file, "r") as req_file:
        req_txt = req_file.read()
        if req_txt and len(req_txt) > 0:
            from subprocess import PIPE, run

            with mkdocs_gen_files.open(req_md_file, "w") as fd:
                fd.write(f"# {source_path.replace('_', ' ')} - Included Libraries\n***\n\n")
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
                        package: str = \
                            str(parts_front).split("=")[0].replace(">", "").replace("<", "").replace("~", "").split(
                                "[")[0]
                        version: str = ""
                        version_link: str = ""
                        package = package.lower()
                        if package in sub_process_result:
                            sub_entry: dict = sub_process_result[package]

                            if "condition" in sub_entry:
                                condition: str = sub_entry["condition"]
                                fd.write(f"### **{package}** ``{condition}``\n\n")
                            else:
                                fd.write(f"### **{package}**\n")

                            if "version" in sub_entry:
                                version = sub_entry["version"]
                                version_link = sub_entry["version_link"]
                                fd.write(f"{version_link}\n\n")

                            if "comment" in sub_entry:
                                comment: str = sub_entry["comment"]
                                fd.write(f"{comment.capitalize()}\n\n")
                            else:
                                fd.write(f"\n\n")

                            pip_result: str = sub_entry["pip_result"]

                            if "req_line_text" in sub_entry:
                                req_line_text: str = sub_entry["req_line_text"]
                                check_version: str = ""
                                if "check_version" in sub_entry:
                                    check_version = sub_entry["check_version"]
                                check_required: List[str] = sub_entry["check_required"]

                                if len(check_version) > 0:
                                    fd.write(f"<span style='color:red'> Check {check_version} vs {version}</span>\n")

                                fd.write(f"=== \"{package}\"\n")
                                fd.write(
                                    f"    ```console\n\n{req_line_text}\n\n    ```\n")  # keep the spaces !important

                                for entry in check_required:
                                    entry = entry.lower()
                                    if entry in sub_process_result:
                                        sub_entry_req: dict = sub_process_result[entry]
                                        pip_result: str = sub_entry_req["pip_result"]
                                        req_line_text = sub_entry_req["req_line_text"]

                                        fd.write(f"=== \"rqr: {entry}\"\n")
                                        fd.write(
                                            f"    ```console\n\n{req_line_text}\n\n    ```\n")  # keep the spaces !important
                                    else:
                                        print("ERROR: entry not in results:", package, entry, req_line_text, check_required)

        nav[virtual_requirements_nav_path] = req_md_file
        print("Nav:", nav)
    if not sub_process_result_file_exists or sub_process_result_file_needs_update or recreate_pip_info:
        with open(pkl_info_file, 'wb') as f:
            pickle.dump(sub_process_result, f)

