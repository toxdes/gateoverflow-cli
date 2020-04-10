from gateoverflow import opengate, actions

if __name__ == "__main__":
    try:
        opengate.main()
    except:
        print('I am the one who gets to say sorry here.')
        actions.exit_program()
