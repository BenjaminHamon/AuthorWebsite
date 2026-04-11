import flask


class MainController:


    def home(self) -> str:
        return flask.render_template("home.html", title = "Home")


    def books(self) -> str:
        return flask.render_template("books.html", title = "Books")


    def about(self) -> str:
        return flask.render_template("about.html", title = "About")


    def contact(self) -> str:
        return flask.render_template("contact.html", title = "Contact")
