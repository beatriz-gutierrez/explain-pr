import markdown

# CSS styles from VS Code markdown preview feature
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<title>@@TITLE@@</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
html body {
    font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
    overflow: initial;
    box-sizing: border-box;
    word-wrap: break-word;
    margin-left: 10%;
    margin-right: 10%;
}
code {
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    background-color: #eee;
    padding: 0.25em;
    white-space: pre-wrap;
}
code.multi-line {
    display: block;
    margin-top: 1em;
}
</style>
<script>
document.addEventListener("DOMContentLoaded", function() {
    const codeBlocks = document.querySelectorAll("code");
    codeBlocks.forEach(code => {
        if (code.innerHTML.includes("\\n")) {
            code.classList.add("multi-line");
        }
    });
});
</script>
</head>
<body for="html-export">
<p>Pull Request: <a href="@@PR_URL@@">@@PR_URL@@</a></p>
@@CONTENT@@
</body>
</html>
"""


def markdown_to_html(markdown_text: str, pr_url: str, title: str) -> str:
    content = markdown.markdown(markdown_text)
    return HTML_TEMPLATE.replace("@@TITLE@@", title).replace("@@PR_URL@@", pr_url).replace("@@CONTENT@@", content)
