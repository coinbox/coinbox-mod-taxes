import cbpos
from cbpos.modules import BaseModuleMetadata

class ModuleMetadata(BaseModuleMetadata):
    base_name = 'taxes'
    version = '0.1.0'
    display_name = 'Taxes Module'
    dependencies = (
        ('base', '0.1'),
        ('currency', '0.1'),
        ('stock', '0.1'),
        ('sales', '0.1'),
    )
    config_defaults = tuple()
