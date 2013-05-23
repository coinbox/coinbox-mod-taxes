import cbpos

import cbpos.mod.base.models.common as common

import cbpos.mod.currency.controllers as currency

from sqlalchemy import func, cast, Table, Column, Integer, String, Float, Boolean, Enum, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class Tax(cbpos.database.Base, common.Item):
    __tablename__ = 'taxes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(5), nullable=True, unique=True)
    rate = Column(Integer, nullable=False, default=0)
    lower_limit = Column(Float, nullable=True)
    upper_limit = Column(Float, nullable=True)
    currency_id = Column(String(3), ForeignKey('currencies.id'))

    currency = relationship("Currency", backref="taxes")

    HAS_LOWER = 1
    HAS_UPPER = 2

    SINGLE = 0
    DEPENDENT_SINGLE = HAS_LOWER
    DEPENDENT_RANGE = HAS_LOWER | HAS_UPPER

    @hybrid_property
    def type(self):
        has_lower = Tax.HAS_LOWER if self.lower_limit is not None else 0
        has_upper = Tax.HAS_UPPER if self.upper_limit is not None else 0
        return has_lower | has_upper

    @type.setter
    def type(self, value):
        has_lower = value & Tax.HAS_LOWER
        has_upper = value & Tax.HAS_UPPER
        
        if not has_lower:
            self.lower_limit = None
        
        if not has_upper:
            self.upper_limit = None

    @type.expression
    def type(cls):
        return  (cast(cls.lower_limit != None, Integer) * Tax.HAS_LOWER) + \
                (cast(cls.upper_limit != None, Integer) * Tax.HAS_UPPER)
    
    __type_names = ('SINGLE', 'DEPENDENT_SINGLE', 'DEPENDENT_RANGE') 
    @hybrid_property
    def type_name(self):
        type = self.type
        for i in self.__type_names:
            if getattr(self, i) == type:
                return i
    
    def __repr__(self):
        return "<Tax %s>" % (self.id,)
