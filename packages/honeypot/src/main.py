from servers import simple_http

if __name__ == "__main__":
    print("Hello, world!")

    c = simple_http.createServerAdapter()
    c.start()
