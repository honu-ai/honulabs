def prompt_with_default(prompt: str, default_to_yes: bool = True) -> bool:
    """
    Prompts the user with a [Y/n] or [y/N] question and returns a boolean.

    Args:
        prompt: The question to ask the user.
        default_to_yes: If True, the default is Yes [Y/n]. If False, the default is No [y/N].

    Returns:
        True if the user chose 'yes', False if 'no'.
    """
    if default_to_yes:
        prompt_suffix = " [Y/n] "
    else:
        prompt_suffix = " [y/N] "

    while True:
        response = input(prompt + prompt_suffix).lower().strip()
        if response == "":
            return default_to_yes
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please answer 'y' or 'n'.") 