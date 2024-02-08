from socket import *
serverPort = 12345  # Server will listen to this port
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP server creation
# Bind the socket to the server's address and port
serverSocket.bind(("", serverPort))
serverSocket.listen(1)  # Listen for incoming connections
print("The server is ready to receive")

# Keep the server running
while True:
    try:
        # Accept any incoming connection and retrieve the client's socket and address
        connectionSocket, addr = serverSocket.accept()
        # Receive data from the client and decode it
        sentence = connectionSocket.recv(2048).decode()
        print("addr:\n",)
        print("Sentence:", sentence)  # sentence == request

        request_parts = sentence.split()  # split creates a (tuple)
        # bo5d kol el request message o befselhom 3an ba3ad o b5znhom f tuple
        print(request_parts)
        if len(request_parts) < 2:
            # Construct an HTTP response with a "Malformed Request" message
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            response += "<html><head><title>Error 400</title></head><body>"
            response += "<h1>HTTP/1.1 400 Bad Request</h1>"
            response += "<p>Your request is malformed and could not be understood by the server.</p>"
            response += "</body></html>"
        # Send the response to the client (browser)
            connectionSocket.send(response.encode())
            connectionSocket.close()
            continue
        # requested_path : bo5d el matloob mn el request o bkon el tarteeb ta3o el tane fel tuple
        requested_path = request_parts[1]

        # Check the requested path and send appropriate responses back to the client
        if requested_path == '/' or requested_path == '/index.html' or requested_path == '/main_en.html' or requested_path == '/en':
            response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            with open("main_en.html", "rb") as f:
                data = f.read()
            connectionSocket.send(response_header.encode())
            connectionSocket.send(data)
            print("\nResponse Header: \n", response_header)
            # print("data: \n", data)

        elif requested_path == '/ar':
            response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            with open("main_ar.html", "rb") as f:
                data = f.read()
            connectionSocket.send(response_header.encode())
            connectionSocket.send(data)
            print("\nResponse Header: \n", response_header)

        elif requested_path == '/SortByPrice':
            # If the client wants laptops sorted by price
            try:
                laptops = []
                with open("Labtops.txt", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        parts = line.strip().split(":")
                        if len(parts) == 2:
                            laptop_name = parts[0]
                            laptop_price = int(parts[1])
                            laptops.append((laptop_name, laptop_price))

                sorted_laptops = sorted(laptops, key=lambda x: x[1])
                total_price = sum(price for _, price in sorted_laptops)

                # Construct the HTML response
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                response = response_header + "<html><head><title>Laptops</title>"
                response += "<link rel='stylesheet' href='BetterCSS.css'>"
                response += "</head><body>"
                response += "<div class='container'>"
                response += "<h1 class='heading'>Laptops Sorted by Price</h1>"
                response += "<h2 class='sub-heading'>Total Price of All Laptops: ${}</h2>".format(
                    total_price)
                response += "<ul class='laptop-list'>"
                for laptop_name, laptop_price in sorted_laptops:
                    response += f"<li class='laptop-item'>{laptop_name.upper()}: ${laptop_price}</li>"
                response += "</ul>"
                response += "</div>"
                response += "</body></html>"
                connectionSocket.send(response.encode())
                print("\nResponse Header: \n", response)

            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                response += "<html><head><title>Error 404</title></head><body>"
                response += "<h1>HTTP/1.1 404 Not Found</h1>"
                response += "<p>The file 'Labtops.txt' is not found</p>"
                response += "<p>Nafe Abubaker</p>"
                response += "<p>IP: {} Port: {}".format(
                    addr[0], addr[1]) + "</p>"
                response += "</body></html>"
                connectionSocket.send(response.encode())
                print("\nResponse Header: \n", response)

        elif requested_path == '/SortByName':
            # If the client wants laptops sorted by name
            try:
                laptops = []
                with open("Labtops.txt", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        parts = line.strip().split(":")
                        if len(parts) == 2:
                            laptop_name = parts[0]
                            laptop_price = int(parts[1])
                            laptops.append((laptop_name, laptop_price))

                sorted_laptops = sorted(laptops, key=lambda x: x[0].upper())

                # Construct the HTML response
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                response = response_header + "<html><head><title>Laptops</title>"
                response += "<link rel='stylesheet' href='BetterCSS.css'>"
                response += "</head><body>"
                response += "<div class='container'>"
                response += "<h1 class='heading'>Laptops Sorted by Name</h1>"
                response += "<ul class='laptop-list'>"
                for laptop_name, laptop_price in sorted_laptops:
                    response += f"<li class='laptop-item'>{laptop_name.upper()}: ${laptop_price}</li>"
                response += "</ul>"
                response += "</div>"
                response += "</body></html>"
                connectionSocket.send(response.encode())
                print("\nResponse Header: \n", response)

            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                response += "<html><head><title>Error 404</title></head><body>"
                response += "<h1>HTTP/1.1 404 Not Found</h1>"
                response += "<p>The file 'Labtops.txt' is not found</p>"
                response += "<p>Nafe Abubaker</p>"
                response += "<p>IP: {} Port: {}".format(
                    addr[0], addr[1]) + "</p>"
                response += "</body></html>"
                connectionSocket.send(response.encode())
                print("\nResponse Header: \n", response)

        # Redirect the client to external websites based on the path
        elif requested_path == '/azn':
            response_header = "HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.amazon.com\r\n\r\n"
            connectionSocket.send(response_header.encode())
            print("\nResponse Header: \n", response_header)
        elif requested_path == '/so':
            response_header = "HTTP/1.1 307 Temporary Redirect\r\nLocation: https://stackoverflow.com\r\n\r\n"
            connectionSocket.send(response_header.encode())
            print("\nResponse Header: \n", response_header)
        elif requested_path == '/bzu':
            response_header = "HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.birzeit.edu\r\n\r\n"
            connectionSocket.send(response_header.encode())
            print("\nResponse Header: \n", response_header)

        # If the client requests a CSS file
        elif requested_path.endswith('.css'):
            try:
                with open(requested_path[1:], 'rb') as f:
                    data = f.read()
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n"
                connectionSocket.send(response_header.encode())
                connectionSocket.send(data)
                print("\nResponse Header: \n", response_header)
            except FileNotFoundError:
                # Handle 404 for CSS file
                response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
                connectionSocket.send(response_header.encode())
                print("\nResponse Header: \n", response_header)
                print("\nCSS file not found")

        # If the client requests a PNG file
        elif requested_path.endswith('.png'):
            try:
                with open(requested_path[1:], 'rb') as f:
                    data = f.read()
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n"
                connectionSocket.send(response_header.encode())
                connectionSocket.send(data)
                print("\nResponse Header: \n", response_header)
            except FileNotFoundError:
                # Handle 404 for PNG file
                response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
                connectionSocket.send(response_header.encode())
                print("\nResponse Header: \n", response_header)
                print("\nPNG file not found")

        # If the client requests a JPG or JPEG file
        elif requested_path.endswith('.jpg') or requested_path.endswith('.jpeg'):
            try:
                with open(requested_path[1:], 'rb') as f:
                    data = f.read()
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n"
                connectionSocket.send(response_header.encode())
                connectionSocket.send(data)
                print("\nResponse Header: \n", response_header)
            except FileNotFoundError:
                # Handle 404 for JPG file
                response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
                connectionSocket.send(response_header.encode())
                print("\nResponse Header: \n", response_header)
                print("JPG file not found")

        elif requested_path == '/local_file.html':
            try:
                with open("local_file.html", "rb") as f:
                    data = f.read()
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                connectionSocket.send(response_header.encode())
                connectionSocket.send(data)
                print("\nResponse Header: \n", response_header)
            except FileNotFoundError:
                response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
                connectionSocket.send(response_header.encode())
                print("Local_file page not found\n")
                print("\nResponse Header: \n", response_header)

        else:
            # Handle 404 Not Found
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            response += "<html><head><title>Error 404</title>"
            response += "<style>"
            response += "body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }"
            response += ".container { text-align: center; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); }"
            response += ".header { color: #ff5252; font-size: 28px; margin-bottom: 10px; }"
            response += ".message { font-size: 18px; margin-bottom: 20px; }"
            response += ".link { color: #1976d2; text-decoration: none; font-weight: bold; }"
            response += ".link:hover { text-decoration: underline; }"
            response += "</style>"
            response += "</head><body>"
            response += "<div class='container'>"
            response += "<div class='header'>Oops, something went wrong!</div>"
            response += "<div class='message'>We couldn't find the page you're looking for.</div>"
            response += "<p style='font-weight: bold;'>Name: Nafe Abubaker | ID: 1200047</p>"
            response += "<p>Your IP: {} | Port: {}".format(
                addr[0], addr[1]) + "</p>"
            response += "<p>You can always go back to our <a class='link' href='/main_en.html'>Main Page</a>.</p>"
            response += "</div>"
            response += "</body></html>"
            connectionSocket.send(response.encode())
            print("\nResponse Header: \n", response)

        # Close the connection with the client because we are using TCP I guess
        connectionSocket.close()

    except OSError:
        print("IO error")
    else:
        print("OK for now")
        print("---------------------------------------------------")
