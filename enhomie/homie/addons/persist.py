"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from json import dumps
from json import loads
from threading import Lock
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.times import unitime
from encommon.times.common import UNITIME
from encommon.types import DictStrAny
from encommon.types import merge_dicts

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

HomiePersistLevel = Literal[
    'failure',
    'information',
    'success',
    'warning']



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
    value: HomiePersistValue
    value_unit: Optional[str]
    value_label: Optional[str]
    value_icon: Optional[str]
    about: Optional[str]
    about_label: Optional[str]
    about_icon: Optional[str]
    level: Optional[HomiePersistLevel]
    tags: Optional[list[str]]
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
        value = record.value
        value_unit = record.value_unit
        value_label = record.value_label
        value_icon = record.value_icon
        about = record.about
        about_label = record.about_label
        about_icon = record.about_icon
        level = record.level
        tags = record.tags
        expire = record.expire
        update = record.update


        self.unique = str(unique)


        self.about = (
            str(about)
            if about is not None
            else None)

        self.about_label = (
            str(about_label)
            if about_label is not None
            else None)

        self.about_icon = (
            str(about_icon)
            if about_icon is not None
            else None)


        assert value is not None

        self.value = loads(str(value))

        assert isinstance(
            self.value,
            _PERSIST_VALUE)

        self.value_label = (
            str(value_label)
            if value_label is not None
            else None)

        self.value_icon = (
            str(value_icon)
            if value_icon is not None
            else None)

        self.value_unit = (
            str(value_unit)
            if value_unit is not None
            else None)


        self.level = (
            str(level)  # type: ignore[assignment]
            if level is not None
            else None)


        self.tags = (
            loads(str(tags))
            if tags is not None
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

    value = Column(
        String,
        nullable=False)

    value_unit = Column(
        String,
        nullable=True)

    value_label = Column(
        String,
        nullable=True)

    value_icon = Column(
        String,
        nullable=True)

    about = Column(
        String,
        nullable=True)

    about_label = Column(
        String,
        nullable=True)

    about_icon = Column(
        String,
        nullable=True)

    level = Column(
        String,
        nullable=True)

    tags = Column(
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
        expire: Optional[UNITIME] = None,
        *,
        value_unit: Optional[str] = None,
        value_label: Optional[str] = None,
        value_icon: Optional[str] = None,
        about: Optional[str] = None,
        about_label: Optional[str] = None,
        about_icon: Optional[str] = None,
        level: Optional[HomiePersistLevel] = None,
        tags: Optional[list[str]] = None,
    ) -> None:
        """
        Insert the value within the persistent key value store.

        .. note::
           This will replace existing record with primary key.

        :param unique: Parameter value passed to the downstream.
        :param value: Parameter value passed to the downstream.
        :param value_unit: Parameter value passed to downstream.
        :param value_label: Parameter value passed to downstream.
        :param value_icon: Parameter value passed to downstream.
        :param expire: Parameter value passed to the downstream.
        :param about: Parameter value passed to the downstream.
        :param about_label: Parameter value passed to downstream.
        :param about_icon: Parameter value passed to downstream.
        :param level: Parameter value passed to the downstream.
        :param tags: Parameter value passed to the downstream.
        """

        homie = self.__homie

        params = homie.params

        persists = (
            params.persists
            or {})


        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable


        if value is None:

            self.delete(unique)

            return None

        assert isinstance(
            value, _PERSIST_VALUE)


        update = Time().spoch


        if expire is not None:

            expire = unitime(expire)

            assert isinstance(
                expire, int)

            expire = update + expire


        default: DictStrAny = {}

        if unique in persists:

            default = (
                persists[unique]
                .endumped)


        inputs: DictStrAny = {
            'unique': unique,
            'value': value,
            'value_unit': value_unit,
            'value_label': value_label,
            'value_icon': value_icon,
            'about': about,
            'about_label': about_label,
            'about_icon': about_icon,
            'level': level,
            'tags': tags,
            'expire': expire,
            'update': update}

        inputs = {
            k: v for k, v
            in inputs.items()
            if v is not None}


        insert: DictStrAny = (
            merge_dicts(
                default, inputs,
                force=True,
                merge_list=False,
                paranoid=True))

        insert['value'] = (
            dumps(insert['value']))

        if 'tags' in insert:
            insert['tags'] = (
                dumps(insert['tags']))


        with lock, sess as session:

            session.merge(
                table(**insert))

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


    def record(
        self,
        unique: str,
    ) -> HomiePersistRecord:
        """
        Return the record within the persistent key value store.

        :param unique: Unique identifier from within the table.
        :returns: Record within the persistent key value store.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        model = HomiePersistRecord
        field = table.unique

        self.expire()


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(field == unique))

            record = query.first()

            assert record is not None

            return model(record)


    def records(
        self,
    ) -> list[HomiePersistRecord]:
        """
        Return all records within the persistent key value store.

        :returns: Records within the persistent key value store.
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
