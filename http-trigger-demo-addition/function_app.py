import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger_demo_addition")
def http_trigger_demo_addition(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed an addition request.')

    # 1. Try to get values from query string parameters
    num1_raw = req.params.get('num1')
    num2_raw = req.params.get('num2')

    # 2. If missing from query parameters, look in the JSON request body
    if not num1_raw or not num2_raw:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = None
            
        if req_body:
            if not num1_raw:
                num1_raw = req_body.get('num1')
            if not num2_raw:
                num2_raw = req_body.get('num2')

    # 3. If both parameters are found, try to convert them to integers and sum them up
    if num1_raw is not None and num2_raw is not None:
        try:
            num1 = int(num1_raw)
            num2 = int(num2_raw)
            result = num1 + num2
            return func.HttpResponse(
                f"The sum of {num1} and {num2} is: {result}", 
                status_code=200
            )
        except ValueError:
            return func.HttpResponse(
                "Invalid input. Please make sure both 'num1' and 'num2' are valid integers.",
                status_code=400
            )
            
    # 4. Fallback message if parameters are completely missing
    return func.HttpResponse(
         "Please pass 'num1' and 'num2' as integers in the query string or in the request body.",
         status_code=200
    )


@app.route(route="http_trigger3", auth_level=func.AuthLevel.FUNCTION)
def http_trigger3(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )