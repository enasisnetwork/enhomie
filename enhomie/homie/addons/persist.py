"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from json import dumps
from json import loads
from threading import Lock
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

from encommon.times import Time
from encommon.times import unitime

from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from ..homie import Homie



HomiePersistValue = Optional[
    int | float | bool | str]

_PERSIST_VALUE = (
    int, float, bool, str)

HomiePersistExpire = Union[
    int, float, str]



class SQLBase(DeclarativeBase):
    """
    Some additional class that SQLAlchemy requires to work.
    """



@dataclass
class HomiePersistRecord:
    """
    Contain the information regarding the persistent value.
    """

    unique: str
    label: Optional[str]
    value: HomiePersistValue
    unit: Optional[str]
    icon: Optional[str]
    about: Optional[str]
    expire: Optional[Time]
    update: Time


    def __init__(
        self,
        record: 'HomiePersistTable',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        unique = record.unique
        label = record.label
        value = record.value
        unit = record.unit
        icon = record.icon
        about = record.about
        expire = record.expire
        update = record.update


        self.unique = str(unique)

        self.label = (
            str(label)
            if label is not None
            else None)


        assert value is not None

        self.value = loads(str(value))

        assert isinstance(
            self.value,
            _PERSIST_VALUE)


        self.unit = (
            str(unit)
            if unit is not None
            else None)

        self.icon = (
            str(icon)
            if icon is not None
            else None)

        self.about = (
            str(about)
            if about is not None
            else None)


        self.expire = (
            Time(float(expire))
            if expire is not None
            else None)

        self.update = (
            Time(float(update)))


        super().__init__()



class HomiePersistTable(SQLBase):
    """
    Schematic for the database operations using SQLAlchemy.

    .. note::
       Fields are not completely documented for this model.
    """

    unique = Column(
        String,
        primary_key=True,
        nullable=False)

    label = Column(
        String,
        nullable=True)

    value = Column(
        String,
        nullable=False)

    unit = Column(
        String,
        nullable=True)

    icon = Column(
        String,
        nullable=True)

    about = Column(
        String,
        nullable=True)

    expire = Column(
        Numeric,
        nullable=True)

    update = Column(
        Numeric,
        nullable=False)

    __tablename__ = 'persist'



class HomiePersist:
    """
    Store the persistent information in the key value store.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'

    __connect: str
    __locker: Lock

    __sengine: Engine
    __session: (
        # pylint: disable=unsubscriptable-object
        sessionmaker[Session])


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie

        params = homie.params

        self.__connect = (
            params.database)

        self.__locker = Lock()

        self.__build_engine()


    def __build_engine(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        path = self.__connect

        sengine = (
            create_engine(path))

        (SQLBase.metadata
         .create_all(sengine))

        session = (
            sessionmaker(sengine))

        self.__sengine = sengine
        self.__session = session


    def insert(  # noqa: CFQ002
        self,
        unique: str,
        value: HomiePersistValue,
        expire: HomiePersistExpire = '30d',
        *,
        label: Optional[str] = None,
        unit: Optional[str] = None,
        icon: Optional[str] = None,
        about: Optional[str] = None,
    ) -> None:
        """
        Insert the value within the persistent key value store.

        .. note::
           This will replace existing record with primary key.

        :param unique: Unique identifier from within the table.
        :param value: Value Which will be stored within record.
        :param expire: Optional time in seconds for expiration.
        :param label: Optional human friendly label for value.
        :param unit: Optional human friendly value unit label.
        :param icon: Optional human friendly icon in Material.
        :param about: Optional human friendly value description.
        """

        sess = self.__session()
        lock = self.__locker


        expire = unitime(expire)

        assert isinstance(expire, int)

        update = Time().spoch
        expire = update + expire


        if value is None:
            self.delete(unique)
            return None

        assert isinstance(
            value, _PERSIST_VALUE)


        with lock, sess as session:

            session.merge(
                HomiePersistTable(
                    unique=unique,
                    label=label,
                    value=dumps(value),
                    unit=unit,
                    icon=icon,
                    about=about,
                    expire=expire,
                    update=update))

            session.commit()


    def select(
        self,
        unique: str,
    ) -> HomiePersistValue:
        """
        Return the value from within persistent key value store.

        :param unique: Unique identifier from within the table.
        :returns: Value from within persistent key value store.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        field = table.unique


        self.expire()


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(field == unique))

            record = query.first()

            if record is None:
                return None

            value = str(record.value)

        value = loads(value)

        assert isinstance(
            value, _PERSIST_VALUE)

        return value


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the value within the persistent key value store.

        :param unique: Unique identifier from within the table.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        field = table.unique


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(field == unique))

            record = query.first()

            if record is None:
                return None

            session.delete(record)

            session.commit()


    def expire(
        self,
    ) -> None:
        """
        Remove the expired persistent key values from the table.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        expire = table.expire


        with lock, sess as session:

            now = Time().spoch

            (session.query(table)
             .filter(expire < now)
             .delete())

            session.commit()


    def records(
        self,
    ) -> list[HomiePersistRecord]:
        """
        Return all records from in persistent key value store.

        :returns: Records from in persistent key value store.
        """

        sess = self.__session()
        lock = self.__locker

        records: list[HomiePersistRecord]

        table = HomiePersistTable
        model = HomiePersistRecord


        with lock, sess as session:

            records = []

            query = (
                session.query(table))

            for record in query.all():

                object = model(record)

                records.append(object)

            return records
