"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation=None, name=None, diameter=float('nan'), hazardous=None):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = designation
        if self.designation == '':
            self.designation = None
        self.name = name
        if self.name == '':
            self.name = None
        try:
            self.diameter = float(diameter)
        except ValueError:
            self.diameter = float('nan')
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        name = self.name or "EmptyName"
        return f'{self.designation} {name}'

    def __str__(self):
        """Return `str(self)`."""
        support_string = 'not' if not self.hazardous else ''
        return f"A NearEarthObject designated as {self.designation}, named {self.name}, which has a diameter of {self.diameter:.3f} and is {support_string} hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        return {
            'designation': self.designation or '',
            'name': self.name or '',
            'diameter_km': self.diameter or float('nan'),
            'potentially_hazardous': self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info.get('designation', '')
        self.time = info.get('time', None)
        if self.time:
            self.time = cd_to_datetime(self.time)
        self.distance = float(info.get('distance', 0.0))
        self.velocity = float(info.get('velocity', 0.0))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        if not self.time:
            return ''

        return_value = f'Time {datetime_to_str(self.time)}'
        if self.neo:
            return_value += f'Name {self.neo.name} Designation {self.neo.designation}'
        return return_value

    def __str__(self):
        """Return `str(self)`."""
        return f"A CloseApproach in {self.time_str!r} with distance {self.distance:.2f}, velocity {self.velocity:.2f} and NEO {self.neo!r}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        return {
            'datetime_utc': self.time.strftime("%Y-%m-%d %H:%M"),
            'distance_au': self.distance or float('nan'),
            'velocity_km_s': self.velocity or float('nan'),
        }
