from pydispatch import dispatcher

import cbpos
from cbpos.modules import BaseModuleLoader

logger = cbpos.get_logger(__name__)

class ModuleLoader(BaseModuleLoader):
    def load_models(self):
        from cbpos.mod.taxes.models import Tax
        return [Tax]
    
    def test_models(self):
        from cbpos.mod.taxes.models import Tax
        from cbpos.mod.currency.models import Currency
        session = cbpos.database.session()
        
        usd = session.query(Currency).filter_by(symbol="USD").one()
        
        vat = Tax(name="Value Added Tax", code="VAT", rate=0.1, currency=usd)
        single = Tax(name="Single Rate Tax", code="SGL", rate=0.2, lower_limit=10, currency=usd)
        multiple = Tax(name="Range Tax", code="MUL", rate=0.3, lower_limit=100, upper_limit=200, currency=usd)
        
        session.add_all([vat, single, multiple])
        
        session.commit()

    def init(self):
        dispatcher.connect(self.onTaxesUpdate, signal='update-taxes')
        
        return True
    
    def onTaxesUpdate(self, signal, sender, manager):
        """
        Dummy implementation of taxes
        """
        logger.debug('Signal received is {} sent by {}'.format(signal, sender))
        
        logger.debug('Ticket is: {}'.format(manager.ticket))
        
        if manager.ticket is not None:
            for tl in manager.ticket.ticketlines:
                tl.taxes = tl.sell_price*tl.amount/10
