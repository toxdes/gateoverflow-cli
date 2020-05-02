from gateoverflow import opengate, actions
import gateoverflow.state as s
if __name__ == "__main__":
    if s.DEBUG == True:
        opengate.main()
    else:
        try:
            opengate.main()
        except:
            print('I am the one who gets to say sorry here.')
            actions.exit_program()
