from functools import wraps


def position_argument_at(index):
    """
    This decorator ensures that the decorated function recieves a valid position
    as the ´index´-th argument. It will look at the arument in question
    and try to convert it into a Point object.

    !!! None is treated as a valid position !!!

    Currently this accepts 3 kinds of arguments as valid positions:
        - already a Point object
        - a tuple of length two
        - two integers (looking at the following given argument)

    Example:
    > @position_argument_at(0):
    > def example(positon):
    >    return position
    >
    > example(Point(0, 0)) # valid
    > example((0, 0))      # valid
    > example(0, 0)        # valid
    """
    def decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            # If the argument in question is not given, it is probably optional and SHOULD already be a point.
            # If the argument is already a Point, no action is needed
            if len(args) <= index \
                    or isinstance(args[index], Point) or args[index] is None:
                return func(*args, **kwargs)

            # Convert to list for easier manipulation
            args = list(args)

            # If got 2-tuple
            if isinstance(args[index], tuple) \
                    and len(args[index]) == 2:
                args[index] = Point(args[index][0], args[index][1])

            # If got two integers
            elif isinstance(args[index], int) \
                    and isinstance(args[index+1], int):
                args[index] = Point(args[index], args[index+1])
                del args[index+1]

            # Raise TypeError
            else:
                raise TypeError("unsupported type for a position argument: "
                                f"'{type(args[index])}'")

            return func(*args, **kwargs)
        return decorated_func
    return decorator


class Point:
    """
    An implementation of 2 dimensional coordiantes.

    The values for x and y are integers and count the games' base unit.
    For DnD this would be 5 feet.

    Coordinates support the abs() function. It will give the point's
    distance from the origin. Like in DnD every second diagonal
    step adds 2 and every other one just 1 to the distance.
    """

    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        if isinstance(x, int) and isinstance(y, int):
            self.x = x
            self.y = y
        else:
            raise TypeError("Arguments 'x' and 'y' must be of type 'int'")

    @position_argument_at(1)
    def __add__(self, obj):
        return Point(self.x + obj.x, self.y + obj.y)

    @position_argument_at(1)
    def __radd__(self, obj):
        return obj + self

    @position_argument_at(1)
    def __sub__(self, obj):
        return Point(self.x - obj.x, self.y - obj.y)

    @position_argument_at(1)
    def __rsub__(self, obj):
        return obj - self

    def __mul__(self, obj):
        return Point(round(self.x * obj), round(self.y * obj))

    def __rmul__(self, obj):
        return self * obj

    def __abs__(self):
        x = abs(self.x)
        y = abs(self.y)
        if x < y:
            return y + x // 2
        else:
            return x + y // 2

    @position_argument_at(1)
    def __equal_point(self, obj):
        if obj is not None:
            return self.x == obj.x and self.y == obj.y
        else:
            return False

    def __eq__(self, obj):
        try:
            return self.__equal_point(obj)
        except TypeError:
            return False

    def __hash__(self):
        return hash((self.x, self.y, ))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"
