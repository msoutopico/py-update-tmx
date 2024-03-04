## Data required in the request

The data required in the translation change request must include, for each change, at least: 

- an identification of the translation unit where the change is required
- the new requested translation

That identificiation should be precise and accurate. It may include at least one of the following:

- source text
- target text
- omegat identifier (key)
- file path

If the three items above are provided, the change will be implemented only when the three match. If one or two of those three details is not provided, then it won't be considered. 

> Example 1: if a repeated segment appears twice with different identifiers and one of the identifiers is provided, the change will be applied where the identifier matches but will not where the identifier does not match.

> Example 2: if a repeated segment appears twice with different identifiers and both the source text and one of the identifiers are provided, the change will be applied where the source text and the identifier match but will not where the identifier does not match even if the source text matches.

> Example 3: if a repeated segment appears twice with different identifiers and the source text is provided in the data but no identifier is provided, no identifier will be considered and the changes will be applied where the source text match.

## Accepted formats

The translation change requests form must be ODS of XLSX.