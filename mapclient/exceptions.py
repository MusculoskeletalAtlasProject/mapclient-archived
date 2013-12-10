class ClientRuntimeError(RuntimeError):
    """
    Generic error for indicating errors that should be notified to the
    user running the client.
    """

    def __init__(self, title='Error', description=''):
        super(ClientRuntimeError, self).__init__(description)
        self.title = title
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.title, self.description)
