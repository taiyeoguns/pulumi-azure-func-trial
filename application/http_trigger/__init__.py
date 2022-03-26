import logging
from http import HTTPStatus

from azure import functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.exception("Unable to get data from request.")
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )

    return func.HttpResponse(
        "This HTTP triggered function executed successfully. "
        + "Pass a name in the query string "
        + "or in the request body for a personalized response.",
        status_code=HTTPStatus.OK,
    )
