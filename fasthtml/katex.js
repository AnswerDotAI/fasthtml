import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import katex from "https://cdn.jsdelivr.net/npm/katex/dist/katex.mjs";

const renderMath = (tex, displayMode) => { return katex.renderToString(tex, {
    throwOnError: false, displayMode: displayMode, output: 'html', trust: true
}) };

const processLatexEnvironments = (content) => {
    return content.replace(/\\begin{(\w+)}([\s\S]*?)\\end{\1}/g, (match, env, innerContent) => {
        if ([{env_list}].includes(env)) { return `{display_delim}${match}{display_delim}`; }
        return match;
}) };

proc_htmx('{sel}', e => {
    let content = processLatexEnvironments(e.textContent);
    // Display math (including environments)
    content = content.replace(/{display_delim}([\s\S]+?){display_delim}/gm, (_, tex) => renderMath(tex.trim(), true));
    // Inline math
    content = content.replace(/(?<!\w){inline_delim}([^{inline_delim}\s](?:[^{inline_delim}]*[^{inline_delim}\s])?){inline_delim}(?!\w)/g, (_, tex) => renderMath(tex.trim(), false));
    e.innerHTML = marked.parse(content);
});

