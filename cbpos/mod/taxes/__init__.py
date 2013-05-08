from pydispatch import dispatcher

import cbpos
from cbpos.modules import BaseModuleLoader

logger = cbpos.get_logger(__name__)

class ModuleLoader(BaseModuleLoader):
    dependencies = ('base', 'currency', 'sales')
    config = [['mod.taxes', {}]]
    name = 'Taxes Support'

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
                tl.taxes = 0.1*tl.sell_price*tl.amount