from sys import argv


def main():
    # Get params from user input in console
    if len(argv) < 3:
        print("Usage: python3.11 main.py <host_type> <url1> <url2> ...")
        return

    print(argv[1])
    print(argv[2:])


if __name__ == "__main__":
    main()
