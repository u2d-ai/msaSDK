import typing

from ..jpcore.justpy_app import JustpyApp


class SetRoute:
    """
    Justpy specific route annotation

    """

    def __init__(self, route: str, **kwargs):
        """
        Constructor

        Args:
            route: the FastAPI route to set
            kwargs: Arbitrary keyword arguments.
        """
        self.route = route
        self.kwargs = kwargs

    def __call__(self, wpfunc: typing.Callable, **_instance_kwargs):
        """
        Args:
            wpfunc: a WebPage returning function (Callable)
            _instance_kwargs: Arbitrary keyword arguments (ignored).

        """
        # Create a new route
        app = JustpyApp.app
        app.add_jproute(
            path=self.route, wpfunc=wpfunc, name=self.kwargs.get("name", None)
        )
        return wpfunc
