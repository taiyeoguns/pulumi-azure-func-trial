"""Tagging utilities."""

import pulumi


def register_auto_tags(auto_tags):
    """Register a global stack transformation that merges a set of tags.

    Merges with whatever was also explicitly added to the resource definition.

    Args:
        auto_tags ([type]): [description]
    """
    pulumi.runtime.register_stack_transformation(lambda args: auto_tag(args, auto_tags))


def auto_tag(args, auto_tags):
    """Apply the given tags to the resource properties if applicable.

    Args:
        args ([type]): [description]
        auto_tags ([type]): [description]

    Returns:
        [ResourceTransformationResult]: [ResourceTransformationResult]
    """
    args.props["tags"] = {**(args.props.get("tags") or {}), **auto_tags}
    return pulumi.ResourceTransformationResult(args.props, args.opts)
