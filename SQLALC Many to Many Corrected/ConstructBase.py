class ConstructBase:
    """This is a singleton design pattern that returns a class, rather than an object.
    Frankly, the distinction between classes and objects is really starting to get a
    little blurry for me."""

    # Static attribute of the class as a whole that points to the one and only instance
    # of this class that we're ever going to create.  The fact that we initialize it to
    # None will be used to tell whether we have entered the constructor
    _singleton = None

    """Override the __new__ method to first check to see whether we have an instance
    of this class on tap or not.  If not, then create it, otherwise, just return 
    the class that we've already constructed."""
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:  # We need to create the singleton
            """As near as I can determine, the class code block is all one piece, that is, we 
            cannot have conditions in the body of the class to conditionally determine how the 
            class gets constructed."""
            class ConstructedBase:
                """Create the constructor for the ConstructedBase class.  This is just here
                to give instances of ConstructedBase SOME property for demonstration purposes."""
                def __init__(self):
                    self.message = "Got into ConstructBase instance"

                """This method is something that I want to inherit in the subtypes of this 
                ConstructedBase class."""
                def hello(self):
                    return "my message is: " + self.message

            """We  out of the definition of the ConstructedBase class and back into the
            __new__ method.  Now we store a reference to the class that we just created.
            Notice that I don't reference ConstructedBase(), but the class itself."""
            cls._singleton = ConstructedBase
        # Return the factory-generated class.
        return cls._singleton
