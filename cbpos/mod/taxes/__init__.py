import cbpos
from cbpos.modules import BaseModuleLoader

class ModuleLoader(BaseModuleLoader):
    dependencies = ('base', 'currency', 'sales')
    config = [['mod.taxes', {}]]
    name = 'Taxes Support'
