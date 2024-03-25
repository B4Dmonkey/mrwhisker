# Algorithm to render [mustache spec](https://mustache.github.io/mustache.5.html)

## Inputs
1. **Template:** string or TextIOWrapper to be rendered
2. **Data:** data to be rendered in the template

## Output
1. Rendered template as a string

## Algorithm
1. Tokenize template into list of tokens
2. For each token in the list of tokens render the value of the token