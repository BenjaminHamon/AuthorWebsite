__product__ = None
__copyright__ = None
__version__ = None
__date__ = None


try:
    import benjaminhamon_author_website.__metadata__ # pyright: ignore[reportMissingImports]

    # pylint: disable = no-member
    __product__ = benjaminhamon_author_website.__metadata__.__product__
    __copyright__ = benjaminhamon_author_website.__metadata__.__copyright__
    __version__ = benjaminhamon_author_website.__metadata__.__version__
    __date__ = benjaminhamon_author_website.__metadata__.__date__
    # pylint: enable = no-member

except ImportError:
    pass
