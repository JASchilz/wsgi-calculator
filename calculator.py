"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback


def instruct(*args):
    """Returns a STRING with instructions for the system"""
    body = ['<h1>How to use the Calculator<h1>',
            '<h3>Start with the URL <a href="localhost:8080">localhost:8080</a>.</h3>',
            '<p>Append "/" and the operation you want!</p>',
            'Choose From:', '<ul>']

    for operation in ['add', 'subtract', 'multiply', 'divide']:
        body.append('<li>{}</li>'.format(operation))

    body.append('</ul>')
    body.append('<p>Finally, add "/x/y where x and y are the numbers to use.</p>')
    body.append('<p>For example, multiplying 2 and 29 would look like this: '
                '<a href="localhost:8080/multiply/2/29">localhost:8080/multiply/2/29</a></p>')
    body.append('<p>Note that the system subtracts the second number from '
                'the first and divides the first number by the second</p>')

    return '\n'.join(body)


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    total = 0
    for arg in args:
        total += int(arg)

    return str(total)


def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    total = 1
    for arg in args:
        total *= int(arg)

    return str(total)


def subtract(*args):
    """ Returns a STRING, subtracting the second arg from the first """

    return str(int(args[0]) - int(args[1]))


def divide(*args):
    """ Returns a STRING, dividing the second arg by the first"""

    try:
        return str(int(args[0]) / int(args[1]))
    except ZeroDivisionError:
        return 'The system cannot divide by zero. The answer is undefined.'


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {'': instruct,
             'add': add,
             'multiply': multiply,
             'divide': divide,
             'subtract': subtract}

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero. - I did this in the division app

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
