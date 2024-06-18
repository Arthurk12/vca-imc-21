from common.platforms.elos import Elos
from common.platforms.bbb_local_server import BBBLocalServer
from common.platforms.meet import Meet
from common.platforms.ivca import Ivca
from common.platforms.constants import ELOS, BBB_LOCAL, MEET

from common.logger import logger

LOG_PREFIX = '[FACTORY_VCA]'

class Factory_vca:
  @staticmethod
  def create_vca(args, round) -> Ivca:
    logger.debug(f'{LOG_PREFIX} creating vca for url {args.url}')
    vca_type = infer_vca_from_url(args.url)
    logger.debug(f'{LOG_PREFIX} vca chosen is {vca_type}')
    if vca_type == ELOS or ELOS in args.url or 'live' in vca_type:
        return Elos(args, round)
    elif vca_type == MEET:
        return Meet(args, round)
    else:
        return BBBLocalServer(args, round)

def infer_vca_from_url(url) -> str:
    host = url.split("//")[-1].split("/")[0].split('?')[0].split('.')[0]
    if ELOS in host:
        return ELOS
    elif BBB_LOCAL in host:
        return BBB_LOCAL
    elif MEET in host:
        return MEET
    else:
        return host