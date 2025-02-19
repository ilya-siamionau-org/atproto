from sphinx.addnodes import pending_xref
from sphinx.ext.intersphinx import missing_reference

from docs.source.aliases_db import ALIASES_DB

# FIXME(MarshalX): I didn't find a fast way to fix aliases resolving after migration to Pydantic.
#  I hope this is temporary and resolving will be on the Sphinx side.


def get_alias_from_db(alias: str):
    # FIXME(MarshalX): Resolving of models.AppBskyGraphDefs ListPurpose is not working.
    alias_split = alias.rsplit('.', maxsplit=1)
    if len(alias_split) < 2:
        return None

    alias_prefix, alias_suffix = alias_split
    if alias_prefix not in ALIASES_DB:
        return None

    return f'{ALIASES_DB[alias_prefix]}.{alias_suffix}'


def resolve_intersphinx_aliases(app, env, node, contnode):
    alias = node.get('reftarget', None)
    if alias is None:
        return None

    resolved_alias = get_alias_from_db(alias)
    if resolved_alias:
        node['reftarget'] = resolved_alias
        return missing_reference(app, env, node, contnode)

    return None


def resolve_internal_aliases(_, doctree):
    for node in doctree.traverse(condition=pending_xref):
        alias = node.get('reftarget', None)
        if alias is None:
            continue

        resolved_alias = get_alias_from_db(alias)
        if resolved_alias:
            node['reftarget'] = resolved_alias
