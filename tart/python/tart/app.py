'''BlackBerry-Tart support code including Application class.'''

import sys
import pickle


class Application:
    '''Tart Application object for the Python backend.'''

    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            log('tart: app starting')

        super(Application, self).__init__()


    def start(self):
        '''entry point to main loop'''
        send('backendReady')

        self.loop()


    def loop(self):
        '''main loop'''
        while True:
            # block indefinitely, or until SystemExit is raised as the
            # Cascades Application is shutting down
            msg = wait()

            if self.debug:
                log('tart: msg', msg)

            # extract message type and build handler name based on convention
            # shared with and adopted from QML
            try:
                msg_type = msg[0]
                # apply Qt-style case normalization
                name = 'on' + msg_type[0].upper() + msg_type[1:]
            except IndexError:
                log('tart: ERROR, no type found in message')
                continue

            else:
                # find a matching handler routine, if there is one
                try:
                    handler = getattr(self, name)
                except AttributeError:
                    if msg_type.startswith('on'):
                        log('tart: WARNING, message starts with "on", maybe remove?')

                    self.missing_handler(msg)
                    continue

            try:
                # log('calling', handler)
                try:
                    kwargs = msg[1] or {}
                except KeyError:
                    kwargs = {}

                # actually process the message in the handler: note that
                # results are ignored for now
                result = handler(**kwargs)

            except SystemExit:  # never block this
                raise

            except:
                import traceback
                traceback.print_exception(*sys.exc_info())


    def missing_handler(self, msg):
        log('tart: ERROR, missing handler for', msg[0])


    def restore_data(self, data, path):
        '''Utility function to retrieve persisted data,
        if any, and restore only those items we currently support.
        This should probably be broken out to an optional and separate
        support package but, for now, here it is...
        '''
        try:
            saved = pickle.load(open(path, 'rb'))
        except:
            saved = {}

        # restore only recognized items, which means we'll ignore the
        # version key for now
        for key in data:
            try:
                data[key] = saved[key]
                # log('{}: restored {} = {!r}'.format(
                #     path,
                #     key,
                #     data[key],
                #     ))
            except KeyError:
                pass


    def save_data(self, data, path):
        '''See restore_data() or samples that use this.'''
        # we can get fancier later when we need
        data['version'] = 1

        # log('{}: persisting {!r}'.format(path, data))
        pickle.dump(data, open(path, 'wb'))


    def onUiReady(self):
        '''Sent when the QML has finished onCreationCompleted for the root
        component.  Override in subclasses as required.'''
        pass


    def onManualExit(self):
        '''Sent when the app is exiting, so we can save state etc.
        Override in subclasses as required.'''
        send('continueExit')


    #---------------------------------------------
    # Useful things with which to help JavaScript debugging.
    # These can be called from the command line interface via
    # telnet, or in some automated testing.  Not used but
    # left here for now, to inspire future ideas...

    def js(self, text):
        '''send to JavaScript for evaluation'''
        send('evalJavascript', text=text)


    def onEvalResult(self, value=None):
        '''result from JavaScript eval sent from js()'''
        print('result', value)


# EOF