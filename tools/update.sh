#!/usr/bin/env bash
python tools/mk_pyi.py
llms_txt2ctx nbs/llms.txt --optional true > nbs/llms-ctx-full.txt
llms_txt2ctx nbs/llms.txt > nbs/llms-ctx.txt
pysym2md --output_file nbs/apilist.txt fasthtml --include_no_docstring

