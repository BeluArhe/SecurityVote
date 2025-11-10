import logging

logger = logging.getLogger(__name__)


def get_db_config():
  """Devuelve la configuración de conexión a la base de datos.

  Edita estos valores según tu entorno (usuario, contraseña y dsn).
  """
  return {
    'user': 'Netrunners',
    'password': '123',
    'dsn': 'localhost:1521/orcl',
    'encoding': 'UTF-8'
  }


def crear_pool(min=1, max=5, increment=1):
  """Crea y devuelve un SessionPool de cx_Oracle.

  Si falla la creación devuelve None y registra el error.
  """
  cfg = get_db_config()
  # Intentamos usar cx_Oracle si está disponible, si no usamos oracledb
  try:
    import cx_Oracle as dbapi
    pool = dbapi.SessionPool(user=cfg['user'],
                 password=cfg['password'],
                 dsn=cfg['dsn'],
                 min=min, max=max, increment=increment,
                 encoding=cfg.get('encoding', 'UTF-8'))
    logger.info('Oracle SessionPool creado con cx_Oracle')
    return pool
  except ImportError:
    try:
      import oracledb as dbapi
      # oracledb.create_pool devuelve un pool con acquire()
      pool = dbapi.create_pool(user=cfg['user'],
                   password=cfg['password'],
                   dsn=cfg['dsn'],
                   min=min, max=max, increment=increment,
                   encoding=cfg.get('encoding', 'UTF-8'))
      logger.info('Oracle pool creado con oracledb')
      return pool
    except Exception as e:
      logger.exception('No se pudo crear el pool de Oracle con oracledb: %s', e)
      return None
  except Exception as e:
    logger.exception('No se pudo crear el pool de Oracle con cx_Oracle: %s', e)
    return None


def conectar_directo():
  """Conexión directa (sin pool) — útil para pruebas puntuales."""
  cfg = get_db_config()
  try:
    import cx_Oracle as dbapi
    return dbapi.connect(user=cfg['user'], password=cfg['password'], dsn=cfg['dsn'], encoding=cfg.get('encoding', 'UTF-8'))
  except ImportError:
    import oracledb as dbapi
    return dbapi.connect(user=cfg['user'], password=cfg['password'], dsn=cfg['dsn'], encoding=cfg.get('encoding', 'UTF-8'))