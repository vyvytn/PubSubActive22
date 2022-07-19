from datetime import timedelta

from OpenCEP.CEP import CEP
from OpenCEP.base.Pattern import Pattern
from OpenCEP.stream.FileStream import FileInputStream, FileOutputStream
from PatternStructure import AndOperator, PrimitiveEventStructure, SeqOperator
from condition.BaseRelationCondition import SmallerThanEqCondition
from condition.CompositeCondition import AndCondition
from condition.Condition import Variable, SimpleCondition
from plugin.stocks.Stocks import MetastockDataFormatter

googleAscendPattern = Pattern(
        SeqOperator(PrimitiveEventStructure("GOOG", "a"),
                    PrimitiveEventStructure("GOOG", "b"),
                    PrimitiveEventStructure("GOOG", "c")),
        SimpleCondition(Variable("a", lambda x: x["Peak Price"]),
                        Variable("b", lambda x: x["Peak Price"]),
                        Variable("c", lambda x: x["Peak Price"]),
                        relation_op=lambda x,y,z: x < y < z),
        timedelta(minutes=3)
    )
cep = CEP([googleAscendPattern])
events = FileInputStream("OpenCEP/test/EventFiles/NASDAQ_TINY.txt")
cep.run(events, FileOutputStream('test/Matches', 'output.txt'), MetastockDataFormatter())
