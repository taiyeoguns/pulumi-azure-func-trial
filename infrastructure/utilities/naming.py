"""Naming utilities."""

import pulumi


def env_name(name, no_dash=False):
    """Generate environment name.

    Args:
        name (str): Original name
    """
    env_name = f"{name}-{pulumi.get_stack()[:9]}".lower()
    return env_name.replace("-", "") if no_dash else env_name
