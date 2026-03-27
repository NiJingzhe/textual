# Textual Examples

This directory contains example Textual applications.

To run them, navigate to the examples directory and enter `python` followed by the name of the Python file.

`tailwind_arbitrary.py` demonstrates direct `classes="w-[42] bg-[#334155]"`
style usage with the arbitrary utility compiler wired into `DOMNode`, and
imports the bundled utility sheet via `from textual import tailwind_tcss`.
The bundled sheet now stays intentionally lean, so the example mixes core
utilities such as `border-round` and `px-4` with arbitrary values like
`bg-[#334155]` and `w-[42]`.

If you want the same bundled stylesheet as a file in your own project, run
`export-twcss ./styles` or `export-twcss --stdout > ./styles/tailwind.tcss`.

```
cd textual/examples
python pride.py
```
