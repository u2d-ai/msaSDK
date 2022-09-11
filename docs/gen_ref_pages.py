"""Generate the code reference pages and navigation."""

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
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:  #
    nav_file.writelines(nav.build_literate_nav())  #
